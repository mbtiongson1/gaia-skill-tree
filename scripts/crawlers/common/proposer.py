"""Writes Gaia crawler proposal batches for branch-based review."""

import json
import os
from datetime import datetime


def _proposal_output_path(source_name: str, date: str) -> str:
    output_dir = os.path.join(os.path.dirname(__file__), "..", "..", "..", "proposals")
    os.makedirs(output_dir, exist_ok=True)
    return os.path.join(output_dir, f"{source_name}-{date}.json")


def write_proposals(candidates: list[dict], source_name: str) -> str:
    """Write proposed skills to proposals/ for the crawler workflow branch."""
    if not candidates:
        print("No candidates to propose.")
        return ""

    date = datetime.now().strftime("%Y-%m-%d")
    branch = f"bot/{source_name}/{date}"
    output_file = _proposal_output_path(source_name, date)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(candidates, f, indent=2)

    print(f"Wrote {len(candidates)} candidates to {output_file}")
    print(f"Proposal branch: {branch}")
    print("Crawler workflows push proposals to this branch for review only.")

    return output_file


def write_evidence_upgrades(upgrades: list[dict], source_name: str) -> str:
    """Write evidence upgrade proposals to proposals/ for the crawler workflow branch."""
    if not upgrades:
        print("No evidence upgrades to propose.")
        return ""

    date = datetime.now().strftime("%Y-%m-%d")
    branch = f"bot/{source_name}/{date}"
    output_file = _proposal_output_path(source_name, date)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(upgrades, f, indent=2)

    print(f"Wrote {len(upgrades)} evidence upgrades to {output_file}")
    print(f"Proposal branch: {branch}")
    print("Crawler workflows push proposals to this branch for review only.")

    return output_file
