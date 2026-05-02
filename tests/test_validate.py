import subprocess
import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# Define paths
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VALIDATE_SCRIPT = os.path.join(REPO_ROOT, "scripts", "validate.py")
FIXTURES_DIR = os.path.join(REPO_ROOT, "tests", "fixtures")
REAL_GRAPH_PATH = os.path.join(REPO_ROOT, "registry", "gaia.json")

def run_validate(graph_path):
    """Helper to run validate.py and return (exit_code, stdout)."""
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    result = subprocess.run(
        ["python3", VALIDATE_SCRIPT, "--graph", graph_path],
        capture_output=True,
        text=True,
        encoding="utf-8",
        env=env
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
        """Ensure extras with < 2 prerequisites are caught."""
        code, out = run_validate(os.path.join(FIXTURES_DIR, "orphaned_extra.json"))
        self.assertEqual(code, 1, "Expected orphaned extra to fail validation.")
        self.assertIn("needs ≥2 prerequisites", out)

    def test_legendary_no_approval(self):
        """Ensure validated ultimate with < 3 Class A/B evidence is caught."""
        code, out = run_validate(os.path.join(FIXTURES_DIR, "ultimate_no_approval.json"))
        self.assertEqual(code, 1, "Expected ultimate with no approval to fail validation.")
        self.assertIn("Validated ultimate", out)
        self.assertIn("needs ≥3 Class A/B evidence", out)

    def test_atomic_with_prerequisites(self):
        """Ensure a basic skill that declares prerequisites is rejected."""
        code, out = run_validate(os.path.join(FIXTURES_DIR, "basic_with_prereqs.json"))
        self.assertEqual(code, 1, "Expected basic-with-prereqs to fail validation.")
        self.assertIn("must have 0 prerequisites", out)

class TestNamedSkillValidation(unittest.TestCase):
    """Tests that verify named skill files pass validate_and_group rules."""

    def test_seed_skills_have_valid_levels(self):
        """All seed named skills have a level in the valid set (II–VI)."""
        from scripts.generateNamedIndex import load_named_skills, validate_and_group, load_gaia_skill_ids

        named_dir = os.path.join(REPO_ROOT, "registry", "named")
        if not os.path.isdir(named_dir):
            self.skipTest("Named skills directory not present.")

        named_skills = load_named_skills(named_dir)
        named_skills = [(fp, fm) for fp, fm in named_skills if not fp.endswith("index.json")]

        valid_ids = load_gaia_skill_ids(REAL_GRAPH_PATH)
        errors, buckets, *_ = validate_and_group(named_skills, valid_ids)

        self.assertEqual(
            errors,
            [],
            f"Seed named skills failed validation:\n" + "\n".join(errors),
        )

    def test_seed_skills_have_no_level_i(self):
        """No seed named skill uses level I (which is forbidden for named skills)."""
        from scripts.generateNamedIndex import load_named_skills, parse_frontmatter

        named_dir = os.path.join(REPO_ROOT, "registry", "named")
        if not os.path.isdir(named_dir):
            self.skipTest("Named skills directory not present.")

        named_skills = load_named_skills(named_dir)
        named_skills = [(fp, fm) for fp, fm in named_skills if not fp.endswith("index.json")]

        for fp, fm in named_skills:
            level = fm.get("level", "")
            self.assertNotEqual(
                level,
                "I",
                f"Seed skill {fp} has forbidden level 'I'.",
            )

    def test_bad_level_fails_validation(self):
        """validate_and_group reports an error when level is 'I'."""
        from scripts.generateNamedIndex import validate_and_group

        named_skills = [
            (
                "registry/named/fake/skill.md",
                {
                    "id": "fake/skill",
                    "name": "Fake",
                    "contributor": "fake",
                    "origin": True,
                    "genericSkillRef": "web-search",
                    "status": "named",
                    "level": "I",
                    "description": "A fake skill at level I.",
                },
            )
        ]
        errors, *_ = validate_and_group(named_skills, {"web-search"})
        self.assertTrue(
            any("level" in e.lower() or "'I'" in e or "level I" in e or "II or above" in e
                for e in errors),
            f"Expected a level error, got: {errors}",
        )

    def test_missing_required_field_fails_validation(self):
        """validate_and_group reports an error for missing required fields."""
        from scripts.generateNamedIndex import validate_and_group

        named_skills = [
            (
                "registry/named/fake/incomplete.md",
                {
                    "id": "fake/incomplete",
                    # Missing: name, contributor, origin, genericSkillRef, status, level, description
                },
            )
        ]
        errors, *_ = validate_and_group(named_skills, set())
        self.assertGreater(len(errors), 0, "Expected errors for missing required fields.")

    def test_unresolved_generic_ref_fails_validation(self):
        """validate_and_group reports an error when genericSkillRef is not in gaia.json."""
        from scripts.generateNamedIndex import validate_and_group

        named_skills = [
            (
                "registry/named/fake/skill.md",
                {
                    "id": "fake/skill",
                    "name": "Fake Skill",
                    "contributor": "fake",
                    "origin": True,
                    "genericSkillRef": "definitely-not-a-real-skill-id",
                    "status": "named",
                    "level": "II",
                    "description": "A skill that references a nonexistent generic skill.",
                },
            )
        ]
        errors, *_ = validate_and_group(named_skills, {"web-search"})
        self.assertTrue(
            any("definitely-not-a-real-skill-id" in e for e in errors),
            f"Expected unresolved-ref error, got: {errors}",
        )


if __name__ == "__main__":
    unittest.main()
