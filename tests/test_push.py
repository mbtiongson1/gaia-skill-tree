import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_PATH = os.path.join(REPO_ROOT, "plugin", "cli", "main.py")
sys.path.insert(0, REPO_ROOT)

from plugin.cli.push import build_skill_batch


class TestGaiaPush(unittest.TestCase):
    def test_push_dry_run_separates_known_and_proposed_skills(self):
        with tempfile.TemporaryDirectory() as tmp:
            os.makedirs(os.path.join(tmp, ".gaia"))
            os.makedirs(os.path.join(tmp, "src"))
            with open(os.path.join(tmp, ".gaia", "config.json"), "w") as f:
                json.dump(
                    {
                        "gaiaUser": "tester",
                        "gaiaRegistryRef": "main",
                        "scanPaths": ["src"],
                    },
                    f,
                )
            with open(os.path.join(tmp, "src", "agent.txt"), "w") as f:
                f.write("web-search semantic-search")

            env = os.environ.copy()
            env["PYTHONPATH"] = REPO_ROOT
            result = subprocess.run(
                [
                    "python3",
                    CLI_PATH,
                    "--registry",
                    REPO_ROOT,
                    "push",
                    "--dry-run",
                ],
                cwd=tmp,
                env=env,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            batch = json.loads(result.stdout)
            self.assertEqual([s["skillId"] for s in batch["knownSkills"]], ["web-search"])
            self.assertEqual([s["id"] for s in batch["proposedSkills"]], ["semantic-search"])
            self.assertEqual(batch["userId"], "tester")
            self.assertEqual(batch["sourceRepo"], "tester/local-repo")

    def test_push_no_pr_writes_batch_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = os.path.join(tmp, "registry")
            os.makedirs(os.path.join(registry, "graph"), exist_ok=True)
            os.makedirs(os.path.join(registry, "intake", "skill-batches"), exist_ok=True)
            shutil.copyfile(os.path.join(REPO_ROOT, "graph", "gaia.json"), os.path.join(registry, "graph", "gaia.json"))
            os.makedirs(os.path.join(tmp, ".gaia"))
            os.makedirs(os.path.join(tmp, "src"))
            with open(os.path.join(tmp, ".gaia", "config.json"), "w") as f:
                json.dump(
                    {
                        "gaiaUser": "tester",
                        "gaiaRegistryRef": "main",
                        "scanPaths": ["src"],
                    },
                    f,
                )
            with open(os.path.join(tmp, "src", "agent.txt"), "w") as f:
                f.write("web-search semantic-search")

            env = os.environ.copy()
            env["PYTHONPATH"] = REPO_ROOT
            result = subprocess.run(
                [
                    "python3",
                    CLI_PATH,
                    "--registry",
                    registry,
                    "push",
                    "--no-pr",
                ],
                cwd=tmp,
                env=env,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("Skipped PR creation (--no-pr).", result.stdout)
            self.assertIn("Wrote skill batch intake record:", result.stdout)
            self.assertTrue(os.listdir(os.path.join(registry, "intake", "skill-batches")))

    def test_proposed_filtering_keeps_known_and_removes_noise(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = os.path.join(tmp, "registry")
            os.makedirs(os.path.join(registry, "graph"), exist_ok=True)
            shutil.copyfile(os.path.join(REPO_ROOT, "graph", "gaia.json"), os.path.join(registry, "graph", "gaia.json"))
            batch = build_skill_batch(
                {"web-search", "a", "and", "semantic-search"},
                {"gaiaUser": "tester"},
                registry,
            )
            self.assertEqual([s["skillId"] for s in batch["knownSkills"]], ["web-search"])
            self.assertEqual([s["id"] for s in batch["proposedSkills"]], ["semantic-search"])


if __name__ == "__main__":
    unittest.main()
