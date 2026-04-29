import json
import os
import re
import subprocess
from datetime import datetime, timezone
from difflib import SequenceMatcher

try:
    from plugin.cli.resolver import load_canonical_skills
except ModuleNotFoundError:
    from cli.resolver import load_canonical_skills


SKILL_ID_RE = re.compile(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$")
MIN_PROPOSED_TOKEN_LENGTH = 3
PROPOSED_STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "to",
    "was",
    "were",
    "with",
    "already",
}


def load_canonical_skill_map(registry_path):
    if not os.path.exists(registry_path):
        return {}
    try:
        with open(registry_path, "r") as f:
            data = json.load(f)
    except Exception:
        return {}
    return {skill["id"]: skill for skill in data.get("skills", [])}


def skill_name_from_id(skill_id):
    words = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", skill_id).replace("_", " ")
    return words[:1].upper() + words[1:]


def detect_source_repo(config):
    env_repo = os.environ.get("GITHUB_REPOSITORY")
    if env_repo:
        return env_repo

    try:
        remote = subprocess.run(
            ["git", "config", "--get", "remote.origin.url"],
            capture_output=True,
            text=True,
            check=False,
            cwd=".",
        ).stdout.strip()
    except Exception:
        remote = ""

    if remote:
        cleaned = remote.removesuffix(".git")
        if cleaned.startswith("git@") and ":" in cleaned:
            return cleaned.split(":", 1)[1]
        if "github.com/" in cleaned:
            return cleaned.split("github.com/", 1)[1]

    return f"{config.get('gaiaUser', 'unknown')}/local-repo"


def build_proposed_skill(skill_id, source_repo):
    name = skill_name_from_id(skill_id)
    return {
        "id": skill_id,
        "name": name,
        "type": "atomic",
        "description": f"Candidate skill detected from {source_repo} usage: {name}.",
        "sourceRepo": source_repo,
        "lifecycle": "pending",
    }


def find_named_skill_suggestions(proposed_id, named_dir, limit=3):
    """Return named skills from graph/named/ that are lexically similar to proposed_id."""
    if not os.path.isdir(named_dir):
        return []
    suggestions = []
    for root, _dirs, files in os.walk(named_dir):
        for fname in files:
            if not fname.endswith(".md"):
                continue
            rel = os.path.relpath(os.path.join(root, fname), named_dir)
            # Normalise to forward slashes and strip .md extension.
            rel_fwd = rel.replace("\\", "/")
            named_id = rel_fwd[:-3]  # strip ".md"
            parts = named_id.split("/")
            slug = parts[-1] if parts else named_id
            score = max(
                SequenceMatcher(None, proposed_id.lower(), slug.lower()).ratio(),
                SequenceMatcher(None, proposed_id.lower(), named_id.lower()).ratio(),
            )
            if score >= 0.45:
                suggestions.append((score, named_id))
    suggestions.sort(key=lambda x: x[0], reverse=True)
    return [
        {"namedSkillId": named_id, "score": round(score, 3)}
        for score, named_id in suggestions[:limit]
    ]


def similarity_score(candidate_id, canonical_skill):
    candidate_name = skill_name_from_id(candidate_id).lower()
    canonical_id = canonical_skill["id"].lower()
    canonical_name = canonical_skill.get("name", canonical_skill["id"]).lower()
    return max(
        SequenceMatcher(None, candidate_id.lower(), canonical_id).ratio(),
        SequenceMatcher(None, candidate_name, canonical_name).ratio(),
    )


def build_similarity(proposed_ids, canonical_skill_map, limit_per_skill=3):
    links = []
    for proposed_id in proposed_ids:
        scored = []
        for skill in canonical_skill_map.values():
            score = similarity_score(proposed_id, skill)
            if score >= 0.45:
                scored.append((score, skill["id"]))
        for score, target_id in sorted(scored, reverse=True)[:limit_per_skill]:
            links.append(
                {
                    "sourceSkillId": proposed_id,
                    "targetSkillId": target_id,
                    "score": round(score, 3),
                    "reason": "Lexical similarity from Gaia push scan.",
                }
            )
    return links


def filter_proposed_ids(valid_tokens, canonical_ids):
    filtered = []
    for token in valid_tokens:
        if token in canonical_ids:
            continue
        if len(token) < MIN_PROPOSED_TOKEN_LENGTH:
            continue
        if token in PROPOSED_STOPWORDS:
            continue
        filtered.append(token)
    return filtered


def build_skill_batch(raw_tokens, config, registry_root, now=None):
    graph_path = os.path.join(registry_root, "graph", "gaia.json")
    canonical_ids = load_canonical_skills(graph_path)
    canonical_map = load_canonical_skill_map(graph_path)
    source_repo = detect_source_repo(config)
    timestamp = now or datetime.now(timezone.utc)
    generated_at = timestamp.replace(microsecond=0).isoformat().replace("+00:00", "Z")

    valid_tokens = sorted(token for token in raw_tokens if SKILL_ID_RE.match(token))
    known_ids = [token for token in valid_tokens if token in canonical_ids]
    proposed_ids = filter_proposed_ids(valid_tokens, canonical_ids)
    batch_id = (
        f"{timestamp.strftime('%Y%m%d%H%M%S')}-"
        f"{config.get('gaiaUser', 'unknown')}-{source_repo.split('/')[-1]}"
    )

    named_dir = os.path.join(registry_root, "graph", "named")
    proposed_skills = []
    for skill_id in proposed_ids:
        skill = build_proposed_skill(skill_id, source_repo)
        skill["namedSuggestions"] = find_named_skill_suggestions(skill_id, named_dir)
        proposed_skills.append(skill)

    return {
        "batchId": batch_id,
        "userId": config.get("gaiaUser", "unknown"),
        "sourceRepo": source_repo,
        "generatedAt": generated_at,
        "knownSkills": [{"skillId": skill_id} for skill_id in known_ids],
        "proposedSkills": proposed_skills,
        "similarity": build_similarity(proposed_ids, canonical_map),
    }


def write_skill_batch(batch, registry_root):
    intake_dir = os.path.join(registry_root, "intake", "skill-batches")
    os.makedirs(intake_dir, exist_ok=True)
    batch_path = os.path.join(intake_dir, f"{batch['batchId']}.json")
    with open(batch_path, "w") as f:
        json.dump(batch, f, indent=2)
        f.write("\n")
    return batch_path
