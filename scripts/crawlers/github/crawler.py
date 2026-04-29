"""Crawls GitHub for repos implementing AI agent skills (Class B evidence)."""

import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from common.taxonomy_mapper import GITHUB_TOPIC_TO_SKILL, map_github_topics, map_to_skills
from common.evidence_scorer import compute_github_score
from common.candidate_builder import build_candidate, normalize_id
from common.dedup import deduplicate
from common.proposer import open_proposal_pr

SCORE_THRESHOLD = 30
MIN_STARS = 50
MAX_AGE_DAYS = 365
BATCH_SIZE = 30


def gh_api(endpoint: str) -> dict | None:
    """Call GitHub API via gh CLI and return parsed JSON."""
    try:
        result = subprocess.run(
            ["gh", "api", endpoint, "--paginate"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        if result.returncode != 0:
            print(f"  gh api error: {result.stderr.strip()}")
            return None
        return json.loads(result.stdout)
    except (subprocess.TimeoutExpired, json.JSONDecodeError, FileNotFoundError) as e:
        print(f"  gh api exception: {e}")
        return None


def search_repos_by_topic(topic: str, min_stars: int = MIN_STARS, limit: int = 20) -> list[dict]:
    """Search GitHub repos by topic, sorted by stars."""
    query = f"topic:{topic}+stars:>={min_stars}"
    endpoint = f"/search/repositories?q={query}&sort=stars&order=desc&per_page={limit}"
    data = gh_api(endpoint)
    if not data:
        return []
    return data.get("items", [])


def assess_repo(repo: dict) -> dict | None:
    """Assess a repo and compute its evidence score."""
    stars = repo.get("stargazers_count", 0)
    forks = repo.get("forks_count", 0)
    open_issues = repo.get("open_issues_count", 0)
    has_license = repo.get("license") is not None
    description = repo.get("description") or ""
    topics = repo.get("topics", [])
    last_push = repo.get("pushed_at", "")

    # Estimate total issues from open issues (GitHub doesn't return total directly)
    total_issues = max(open_issues, 1)

    score = compute_github_score(
        stars=stars,
        forks=forks,
        open_issues=open_issues,
        total_issues=total_issues,
        last_push=last_push,
        has_ci=True,  # Assume CI for repos with high stars
        has_license=has_license,
        has_readme=True,  # GitHub repos virtually always have READMEs
    )

    if score < SCORE_THRESHOLD:
        return None

    skill_ids = map_github_topics(topics)
    if not skill_ids:
        skill_ids = map_to_skills(
            repo.get("name", ""),
            description,
            keywords=topics,
        )

    if not skill_ids:
        return None

    return {
        "repo": repo,
        "score": score,
        "skill_ids": skill_ids,
        "description": description,
        "url": repo.get("html_url", ""),
    }


def main():
    """Main crawler entry point."""
    print("GitHub Crawler — searching for AI agent skill implementations")
    print(f"  Topics to search: {len(GITHUB_TOPIC_TO_SKILL)}")
    print(f"  Min stars: {MIN_STARS}, Score threshold: {SCORE_THRESHOLD}")
    print()

    all_candidates = []
    seen_repo_ids = set()

    topics_searched = 0
    for topic, default_skill_id in GITHUB_TOPIC_TO_SKILL.items():
        if topics_searched >= BATCH_SIZE:
            break

        print(f"  Searching topic: {topic}")
        repos = search_repos_by_topic(topic, min_stars=MIN_STARS)

        for repo in repos:
            repo_id = repo.get("id")
            if repo_id in seen_repo_ids:
                continue
            seen_repo_ids.add(repo_id)

            assessment = assess_repo(repo)
            if not assessment:
                continue

            candidate = build_candidate(
                id=normalize_id(f"{default_skill_id}-gh-{repo.get('name', '')[:20]}"),
                name=repo.get("name", ""),
                description=assessment["description"][:200] or f"GitHub repo implementing {default_skill_id}",
                skill_type="atomic",
                source_url=assessment["url"],
                source_type="github",
                evidence_class="B",
                score=assessment["score"],
            )
            all_candidates.append(candidate)

        topics_searched += 1
        time.sleep(2)

    print(f"\n  Raw candidates: {len(all_candidates)}")

    # Deduplicate by candidate ID within this batch
    seen_ids = set()
    unique_candidates = []
    for c in all_candidates:
        if c["id"] not in seen_ids:
            seen_ids.add(c["id"])
            unique_candidates.append(c)

    # Deduplicate against existing graph
    final = deduplicate(unique_candidates)
    print(f"  After dedup: {len(final)}")

    if final:
        output = open_proposal_pr(final, "github")
        print(f"\n  Output: {output}")
    else:
        print("\n  No new candidates to propose.")


if __name__ == "__main__":
    main()
