"""Computes an evidence score (0-100) from marketplace signals."""

import math
from datetime import datetime, timezone


def compute_score(
    downloads: int = 0,
    stars: int = 0,
    last_updated: str = None,
    has_readme: bool = False,
    has_examples: bool = False,
) -> int:
    """Compute evidence quality score from marketplace signals.

    Scoring:
      - Downloads/installs (log-scaled): max 40 points
      - Stars/likes (log-scaled): max 20 points
      - Recency (linear decay from last update): max 20 points
      - Documentation quality: max 20 points
    """
    score = 0

    # Downloads: log10 scale, 1=0, 10=10, 100=20, 1000=30, 10000=40
    if downloads > 0:
        score += min(40, int(math.log10(downloads) * 10))

    # Stars: log2 scale, 1=0, 4=4, 16=8, 64=12, 256=16, 1024=20
    if stars > 0:
        score += min(20, int(math.log2(stars) * 2))

    # Recency: full points if updated within 30 days, linear decay to 0 at 365 days
    if last_updated:
        try:
            updated = datetime.fromisoformat(last_updated.replace("Z", "+00:00"))
            days_ago = (datetime.now(timezone.utc) - updated).days
            if days_ago <= 30:
                score += 20
            elif days_ago < 365:
                score += max(0, int(20 * (1 - (days_ago - 30) / 335)))
        except (ValueError, TypeError):
            pass

    # Documentation
    if has_readme:
        score += 10
    if has_examples:
        score += 10

    return min(100, score)


def compute_github_score(
    stars: int = 0,
    forks: int = 0,
    open_issues: int = 0,
    total_issues: int = 0,
    last_push: str = None,
    has_ci: bool = False,
    has_license: bool = False,
    has_readme: bool = False,
) -> int:
    """Compute evidence quality score for a GitHub repository.

    Scoring:
      - Stars (log-scaled): max 25 points
      - Forks (log-scaled): max 15 points
      - Issue health (closed/total ratio): max 10 points
      - Recency of last push: max 20 points
      - CI present: 10 points
      - License present: 10 points
      - README present: 10 points
    """
    score = 0

    if stars > 0:
        score += min(25, int(math.log10(stars) * 8))

    if forks > 0:
        score += min(15, int(math.log10(forks) * 6))

    if total_issues > 0:
        closed_ratio = (total_issues - open_issues) / total_issues
        score += int(10 * closed_ratio)

    if last_push:
        try:
            pushed = datetime.fromisoformat(last_push.replace("Z", "+00:00"))
            days_ago = (datetime.now(timezone.utc) - pushed).days
            if days_ago <= 30:
                score += 20
            elif days_ago < 365:
                score += max(0, int(20 * (1 - (days_ago - 30) / 335)))
        except (ValueError, TypeError):
            pass

    if has_ci:
        score += 10
    if has_license:
        score += 10
    if has_readme:
        score += 10

    return min(100, score)


def compute_skillsmp_score(
    stars: int = 0,
    category_count: int = 0,
    has_content: bool = False,
) -> int:
    """Compute evidence quality score for a SkillsMP entry.

    Scoring:
      - Stars (log-scaled): max 30 points
      - Category/occupation coverage: max 30 points
      - Has SKILL.md content: 40 points
    """
    score = 0

    if stars > 0:
        score += min(30, int(math.log2(max(1, stars)) * 6))

    score += min(30, category_count * 5)

    if has_content:
        score += 40

    return min(100, score)
