import json
import os
import tempfile
import unittest

from scripts.generateRealSkills import generate_catalog_pages


REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATALOG_PATH = os.path.join(REPO_ROOT, "graph", "real_skill_catalog.json")


class TestRealSkillCatalog(unittest.TestCase):
    def load_catalog(self):
        with open(CATALOG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    def test_catalog_includes_requested_real_sources(self):
        catalog = self.load_catalog()
        source_ids = {source["id"] for source in catalog["sources"]}

        self.assertIn("awesome-agent-skills", source_ids)
        self.assertIn("agentskills-me", source_ids)
        self.assertIn("superpowers", source_ids)
        self.assertIn("openai-skills", source_ids)

    def test_catalog_buckets_real_named_skills(self):
        catalog = self.load_catalog()
        items = [
            item
            for bucket in catalog["buckets"]
            for item in bucket["items"]
        ]
        names = {item["name"] for item in items}

        self.assertIn("superpowers/brainstorming", names)
        self.assertIn("superpowers/systematic-debugging", names)
        self.assertIn("codex", names)
        self.assertIn("vercel-react-best-practices", names)
        self.assertIn("openai/openai-docs", names)
        self.assertIn("openai/security-threat-model", names)

    def test_generate_catalog_pages_outputs_linked_html(self):
        catalog = self.load_catalog()
        with tempfile.TemporaryDirectory() as tmp:
            html_path, md_path = generate_catalog_pages(catalog, tmp)

            with open(html_path, "r", encoding="utf-8") as f:
                html = f.read()
            with open(md_path, "r", encoding="utf-8") as f:
                markdown = f.read()

        self.assertIn("<title>Gaia Real Skill Catalog</title>", html)
        self.assertIn("https://github.com/VoltAgent/awesome-agent-skills", html)
        self.assertIn("https://agentskills.me/skill/codex", html)
        self.assertIn("https://officialskills.sh/openai/skills", html)
        self.assertIn("superpowers/brainstorming", html)
        self.assertIn("openai/security-threat-model", html)
        self.assertIn("## Agent Workflow and Superpowers", markdown)
        self.assertIn("## Security and Governance", markdown)


if __name__ == "__main__":
    unittest.main()
