"""Tests for crawler common modules."""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts", "crawlers"))

from common.taxonomy_mapper import map_to_skills
from common.evidence_scorer import compute_score
from common.candidate_builder import build_candidate, normalize_id
from common.dedup import load_existing_skills, deduplicate


class TestTaxonomyMapper:
    def test_maps_web_scraping_keywords(self):
        assert "web-scrape" in map_to_skills("scraper", "a web scraping tool")

    def test_maps_rag_keywords(self):
        assert "rag-pipeline" in map_to_skills("my-rag", "retrieval augmented generation")

    def test_maps_code_generation(self):
        assert "code-generation" in map_to_skills("codegen", "code generation tool")

    def test_maps_from_keywords_list(self):
        result = map_to_skills("tool", "generic tool", ["embedding", "vector"])
        assert "embed-text" in result

    def test_returns_empty_for_unrelated(self):
        assert map_to_skills("database", "postgres connection pool manager") == []


class TestEvidenceScorer:
    def test_high_score_for_popular_recent_package(self):
        score = compute_score(
            downloads=10000, stars=500, last_updated="2026-04-20",
            has_readme=True, has_examples=True
        )
        assert score >= 60

    def test_low_score_for_unpopular_stale_package(self):
        score = compute_score(
            downloads=5, stars=0, last_updated="2024-01-01",
            has_readme=False, has_examples=False
        )
        assert score < 30

    def test_score_capped_at_100(self):
        score = compute_score(
            downloads=10000000, stars=100000, last_updated="2026-04-28",
            has_readme=True, has_examples=True
        )
        assert score <= 100

    def test_zero_inputs_give_zero(self):
        assert compute_score() == 0


class TestCandidateBuilder:
    def test_builds_valid_candidate(self):
        c = build_candidate("test-skill", "Test", "A test skill", source_url="https://x.com", source_type="npm", score=75)
        assert c["id"] == "test-skill"
        assert c["type"] == "atomic"
        assert c["status"] == "provisional"
        assert c["evidence"][0]["class"] == "C"
        assert "75" in c["evidence"][0]["notes"]

    def test_normalize_id(self):
        assert normalize_id("Web Scraper Tool") == "web-scraper-tool"
        assert normalize_id("Hello!! World??") == "hello-world"
        assert normalize_id("  spaces  ") == "spaces"


class TestDedup:
    def test_loads_existing_skills(self):
        skills = load_existing_skills()
        assert len(skills) > 0
        assert "web-scrape" in skills

    def test_removes_existing_skills(self):
        candidates = [
            {"id": "web-scrape", "name": "Web Scrape"},
            {"id": "brand-new-skill-xyz", "name": "New"},
        ]
        result = deduplicate(candidates)
        assert len(result) == 1
        assert result[0]["id"] == "brand-new-skill-xyz"
