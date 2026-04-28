"""Deduplicates crawler candidates against the existing graph."""

import json
import os


def load_existing_skills(graph_path: str = None) -> set:
    """Load all existing skill IDs from gaia.json."""
    if graph_path is None:
        graph_path = os.path.join(
            os.path.dirname(__file__), "..", "..", "..", "graph", "gaia.json"
        )

    graph_path = os.path.abspath(graph_path)
    if not os.path.exists(graph_path):
        return set()

    with open(graph_path, "r") as f:
        graph = json.load(f)

    return {skill["id"] for skill in graph.get("skills", [])}


def deduplicate(candidates: list[dict], graph_path: str = None) -> list[dict]:
    """Remove candidates that already exist in the registry."""
    existing = load_existing_skills(graph_path)
    return [c for c in candidates if c["id"] not in existing]
