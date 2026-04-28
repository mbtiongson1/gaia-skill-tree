import json
import os
import subprocess
import tempfile
import unittest


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_PATH = os.path.join(REPO_ROOT, "plugin", "cli", "main.py")


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
                f.write("tokenize semantic-search")
            
            # Initialize dummy git repo to ensure predictable repo detection
            subprocess.run(["git", "init"], cwd=tmp, check=True, capture_output=True)
            subprocess.run(
                ["git", "remote", "add", "origin", "https://github.com/tester/local-repo.git"],
                cwd=tmp, check=True, capture_output=True
            )

            env = os.environ.copy()
            env.pop("GITHUB_REPOSITORY", None)
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
            self.assertEqual([s["skillId"] for s in batch["knownSkills"]], ["tokenize"])
            self.assertEqual([s["id"] for s in batch["proposedSkills"]], ["semantic-search"])
            self.assertEqual(batch["userId"], "tester")
            self.assertEqual(batch["sourceRepo"], "tester/local-repo")


if __name__ == "__main__":
    unittest.main()
