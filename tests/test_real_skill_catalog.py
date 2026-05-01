import json
import os
import tempfile
import unittest

from scripts.generateRealSkills import generate_catalog_pages


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(REPO_ROOT, "registry", "real-skills.json")


class TestRealSkillCatalog(unittest.TestCase):
    def load_catalog(self):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_catalog_includes_requested_real_sources(self):
        catalog = self.load_catalog()
        source_repos = {source["repo"] for source in catalog["sources"]}

        self.assertIn("karpathy/autoresearch", source_repos)
        self.assertIn("cognition-labs/devin", source_repos)
        self.assertIn("mattpocock/skills", source_repos)
        self.assertIn("openai/skills", source_repos)

    def test_catalog_buckets_real_named_skills(self):
        catalog = self.load_catalog()
        items = catalog.get("items", [])
        names = {item["name"] for item in items}

        self.assertIn("karpathy/autoresearch", names)
        self.assertIn("mattpocock/write-a-skill", names)
        self.assertIn("openai/openai-docs", names)
        self.assertIn("openai/security-best-practices", names)
        self.assertTrue(len(names) >= 2, f"Expected at least 2 items, got: {names}")

    def test_generate_catalog_pages_outputs_linked_html(self):
        catalog = self.load_catalog()
        with tempfile.TemporaryDirectory() as tmp:
            html_path, md_path = generate_catalog_pages(catalog, tmp)

            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
            with open(md_path, "r", encoding="utf-8") as f:
                markdown = f.read()

        self.assertIn("<title>Gaia Real Skill Catalog</title>", html)
        self.assertIn("karpathy/autoresearch", html)
        self.assertIn("openai/openai-docs", html)
        self.assertIn("openai/security-best-practices", markdown)


if __name__ == "__main__":
    unittest.main()
