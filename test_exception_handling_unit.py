import unittest
from datetime import date, timedelta
from unittest.mock import patch

from generators.contrib_card import _latest_contribution_date
from utils.api_validators import safe_get_nested_value
from utils.github_api import fetch_sparkline_data


class ExplodingDict(dict):
    def __getitem__(self, key):
        raise RuntimeError("boom")


class FakeResponse:
    def __init__(self, status_code, payload):
        self.status_code = status_code
        self._payload = payload

    def json(self):
        return self._payload


class ExceptionHandlingTests(unittest.TestCase):
    def test_latest_contribution_date_skips_invalid_dates(self):
        valid_date = date.today() - timedelta(days=2)
        newer_valid_date = date.today() - timedelta(days=1)
        contributions = [
            {"date": "not-a-date", "count": 1},
            {"date": valid_date.isoformat(), "count": 2},
            {"date": None, "count": 3},
            {"date": newer_valid_date.isoformat(), "count": 4},
        ]

        self.assertEqual(_latest_contribution_date(contributions), newer_valid_date)

    def test_safe_get_nested_value_does_not_swallow_runtime_errors(self):
        with self.assertRaises(RuntimeError):
            safe_get_nested_value(ExplodingDict({"data": {}}), ["data", "user"], default=None)

    @patch("utils.github_api.requests.get")
    def test_fetch_sparkline_data_skips_malformed_events(self, mock_get):
        today = date.today().strftime("%Y-%m-%d")
        mock_get.return_value = FakeResponse(
            200,
            [
                {"type": "PushEvent", "created_at": f"{today}T12:00:00Z", "payload": {"distinct_size": 3}},
                {"type": "PushEvent", "created_at": f"{today}T13:00:00Z", "payload": None},
                {"type": "PushEvent"},
                "not-a-dict",
            ],
        )

        counts = fetch_sparkline_data("octocat")

        self.assertEqual(len(counts), 30)
        self.assertGreaterEqual(counts[-1], 3)


if __name__ == "__main__":
    unittest.main()