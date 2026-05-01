import os
import sys
import unittest


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, REPO_ROOT)

from gaia_cli.prWriter import build_intake_pr_body


class TestPrWriter(unittest.TestCase):
    def test_build_intake_pr_body_contains_summary_table_and_checklists(self):
        batch = {
            "batchId": "20260429000000-tester-repo",
            "userId": "tester",
            "sourceRepo": "tester/repo",
            "generatedAt": "2026-04-29T00:00:00Z",
            "knownSkills": [{"skillId": "web-search"}],
            "proposedSkills": [
                {
                    "id": "semantic-search",
                    "name": "Semantic Search",
                    "type": "atomic",
                }
            ],
            "similarity": [
                {
                    "sourceSkillId": "semantic-search",
                    "targetSkillId": "web-search",
                    "score": 0.73,
                    "reason": "Lexical similarity from Gaia push scan.",
                }
            ],
        }
        body = build_intake_pr_body(batch)
        self.assertIn("Known skills: `1`", body)
        self.assertIn("Proposed skills: `1`", body)
        self.assertIn("`semantic-search`", body)
        self.assertIn("`web-search` (0.730)", body)
        self.assertIn("### Reviewer Checklist", body)
        self.assertIn("### Maintainer Promotion Checklist", body)


if __name__ == "__main__":
    unittest.main()
