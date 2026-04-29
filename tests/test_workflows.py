import os
import unittest


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUTO_TRIAGE_PATH = os.path.join(REPO_ROOT, ".github", "workflows", "auto-triage.yml")


class TestWorkflowConfig(unittest.TestCase):
    def test_auto_triage_watches_intake_paths(self):
        with open(AUTO_TRIAGE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn('- "intake/**"', content)

    def test_auto_triage_uses_pull_request_target(self):
        """Regression: pull_request gives read-only token on fork PRs, breaking label writes."""
        with open(AUTO_TRIAGE_PATH, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("pull_request_target", content)
        self.assertNotIn("on:\n  pull_request:\n", content)


if __name__ == "__main__":
    unittest.main()
