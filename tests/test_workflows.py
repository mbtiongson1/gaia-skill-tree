import os
import unittest


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTO_TRIAGE_PATH = os.path.join(REPO_ROOT, ".github", "workflows", "auto-triage.yml")


class TestWorkflowConfig(unittest.TestCase):
    def test_auto_triage_watches_intake_paths(self):
        with open(AUTO_TRIAGE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('- "intake/**"', content)


if __name__ == "__main__":
    unittest.main()
