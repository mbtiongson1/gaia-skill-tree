import subprocess
import os
import unittest

# Define paths
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATE_SCRIPT = os.path.join(REPO_ROOT, "scripts", "validate.py")
FIXTURES_DIR = os.path.join(REPO_ROOT, "tests", "fixtures")
REAL_GRAPH_PATH = os.path.join(REPO_ROOT, "graph", "gaia.json")

def run_validate(graph_path):
    """Helper to run validate.py and return (exit_code, stdout)."""
    result = subprocess.run(
        ["python3", VALIDATE_SCRIPT, "--graph", graph_path],
        capture_output=True,
        text=True
    )
    return result.returncode, result.stdout

class TestValidate(unittest.TestCase):
    def test_clean_graph(self):
        """Ensure the real gaia.json passes validation."""
        code, out = run_validate(REAL_GRAPH_PATH)
        self.assertEqual(code, 0, f"Expected clean graph to pass, but it failed with output:\n{out}")
        self.assertIn("All validation checks passed.", out)

    def test_cycle(self):
        """Ensure a cycle is detected."""
        code, out = run_validate(os.path.join(FIXTURES_DIR, "cycle.json"))
        self.assertEqual(code, 1, "Expected cycle graph to fail validation.")
        self.assertIn("Cycle detected:", out)

    def test_missing_ref(self):
        """Ensure a missing reference is detected."""
        code, out = run_validate(os.path.join(FIXTURES_DIR, "missing_ref.json"))
        self.assertEqual(code, 1, "Expected missing ref graph to fail validation.")
        self.assertIn("references missing prerequisite", out)

    def test_bad_evidence(self):
        """Ensure insufficient evidence is caught."""
        code, out = run_validate(os.path.join(FIXTURES_DIR, "bad_evidence.json"))
        self.assertEqual(code, 1, "Expected bad evidence graph to fail validation.")
        self.assertIn("needs evidence class", out)

    def test_orphaned_composite(self):
        """Ensure composites with < 2 prerequisites are caught."""
        code, out = run_validate(os.path.join(FIXTURES_DIR, "orphaned_composite.json"))
        self.assertEqual(code, 1, "Expected orphaned composite to fail validation.")
        self.assertIn("needs ≥2 prerequisites", out)

    def test_legendary_no_approval(self):
        """Ensure validated legendary with < 3 Class A/B evidence is caught."""
        code, out = run_validate(os.path.join(FIXTURES_DIR, "legendary_no_approval.json"))
        self.assertEqual(code, 1, "Expected legendary with no approval to fail validation.")
        self.assertIn("Validated legendary", out)
        self.assertIn("needs ≥3 Class A/B evidence", out)

if __name__ == "__main__":
    unittest.main()
