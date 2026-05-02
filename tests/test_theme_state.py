import unittest

from utils.theme_state import reset_theme_filter_state, theme_filter_widget_keys


class ThemeStateTests(unittest.TestCase):
    def test_theme_filter_widget_keys_are_namespaced(self):
        keys = theme_filter_widget_keys("Space")

        self.assertEqual(
            keys,
            {
                "bg_color": "customize_bg_Space",
                "title_color": "customize_title_Space",
                "text_color": "customize_text_Space",
                "border_color": "customize_border_Space",
            },
        )

    def test_reset_theme_filter_state_restores_defaults(self):
        session_state = {
            "customize_bg_Space": "#111111",
            "customize_title_Space": "#222222",
            "customize_text_Space": "#333333",
            "customize_border_Space": "#444444",
        }
        theme_defaults = {
            "bg_color": "#0b0c1f",
            "title_color": "#a371f7",
            "text_color": "#d0dfff",
            "border_color": "#6e5cdb",
        }

        reset_theme_filter_state(session_state, "Space", theme_defaults)

        self.assertEqual(session_state["customize_bg_Space"], "#0b0c1f")
        self.assertEqual(session_state["customize_title_Space"], "#a371f7")
        self.assertEqual(session_state["customize_text_Space"], "#d0dfff")
        self.assertEqual(session_state["customize_border_Space"], "#6e5cdb")


if __name__ == "__main__":
    unittest.main()