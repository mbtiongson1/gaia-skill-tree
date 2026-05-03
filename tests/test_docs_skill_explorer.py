from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_skill_explorer_uses_open_source_skills_npx_install():
    js = (ROOT / "docs" / "js" / "skill-explorer.js").read_text(encoding="utf-8")

    assert "npx skills add " in js
    assert "skills package" in js
    assert "npx @gaia-registry/cli install " not in js
    assert "@gaia-registry/cli" not in js


def test_skill_explorer_normalizes_github_skill_file_urls_for_skills_add():
    js = (ROOT / "docs" / "js" / "skill-explorer.js").read_text(encoding="utf-8")

    assert ".replace('/blob/', '/tree/')" in js
    assert ".replace(/\\/SKILL\\.md$/i, '')" in js
