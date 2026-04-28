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
