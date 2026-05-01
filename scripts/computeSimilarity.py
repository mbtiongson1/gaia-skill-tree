"""Compute pairwise cosine similarity for all skills in registry/embeddings.json.

Reads registry/embeddings.json, computes pairwise cosine similarity for all skill
pairs above a configurable threshold, and writes registry/similarity.json.
"""

import argparse
import json
import math
import os
import sys
from datetime import date


def cosine_similarity(a, b):
    """Compute cosine similarity between two vectors.

    Uses numpy when available; falls back to pure Python otherwise.
    """
    try:
        import numpy as np
        a_arr = np.array(a, dtype=float)
        b_arr = np.array(b, dtype=float)
        norm_a = float(np.linalg.norm(a_arr))
        norm_b = float(np.linalg.norm(b_arr))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return float(np.dot(a_arr, b_arr) / (norm_a * norm_b))
    except ImportError:
        dot = sum(x * y for x, y in zip(a, b))
        norm_a = math.sqrt(sum(x * x for x in a))
        norm_b = math.sqrt(sum(x * x for x in b))
        if norm_a == 0.0 or norm_b == 0.0:
            return 0.0
        return dot / (norm_a * norm_b)


def compute_similarity(embeddings_path, output_path, threshold=0.3):
    """Read embeddings, compute pairwise similarity, and write similarity.json.

    Args:
        embeddings_path: path to registry/embeddings.json
        output_path:     path to write registry/similarity.json
        threshold:       minimum cosine similarity score to include a pair
    """
    if not os.path.exists(embeddings_path):
        print(
            f"Error: embeddings file not found at {embeddings_path}\n"
            "Run the embeddings generator before computing similarity."
        )
        sys.exit(1)

    with open(embeddings_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    entries = data.get("entries", [])
    n = len(entries)
    print(f"Computing pairwise similarity for {n} skills (threshold={threshold})...")

    pairs = []
    for i in range(n):
        for j in range(i + 1, n):
            score = cosine_similarity(entries[i]["vector"], entries[j]["vector"])
            if score >= threshold:
                pairs.append({
                    "a": entries[i]["id"],
                    "b": entries[j]["id"],
                    "score": round(score, 6),
                })

    # Sort by score descending for readability
    pairs.sort(key=lambda p: p["score"], reverse=True)

    output = {
        "generatedAt": str(date.today()),
        "threshold": threshold,
        "pairs": pairs,
    }

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2)

    print(f"Wrote {len(pairs)} pairs to {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Compute pairwise cosine similarity for Gaia skill embeddings"
    )
    parser.add_argument(
        "--embeddings",
        default="registry/embeddings.json",
        help="Path to embeddings JSON file (default: registry/embeddings.json)",
    )
    parser.add_argument(
        "--output",
        default="registry/similarity.json",
        help="Path to write similarity JSON file (default: registry/similarity.json)",
    )
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.3,
        help="Minimum cosine similarity score to include a pair (default: 0.3)",
    )
    args = parser.parse_args()
    compute_similarity(args.embeddings, args.output, threshold=args.threshold)


if __name__ == "__main__":
    main()
