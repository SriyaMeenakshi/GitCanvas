import os
import json
import subprocess
import unittest
from pathlib import Path
import tempfile


class ThemeLoaderTests(unittest.TestCase):
    def test_import_and_load_custom_themes_are_cwd_independent(self):
        repo_root = Path(__file__).resolve().parent

        with tempfile.TemporaryDirectory() as temp_dir:
            env = os.environ.copy()
            env["PYTHONPATH"] = str(repo_root) + os.pathsep + env.get("PYTHONPATH", "")

            result = subprocess.run(
                [
                    os.sys.executable,
                    "-c",
                    "from themes.styles import *; import json; print(json.dumps(load_custom_themes()))",
                ],
                cwd=temp_dir,
                env=env,
                capture_output=True,
                text=True,
                check=True,
            )

        custom_themes = json.loads(result.stdout)
        self.assertIsInstance(custom_themes, dict)


if __name__ == "__main__":
    unittest.main()