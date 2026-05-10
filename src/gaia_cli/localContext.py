"""Local-first skill context.

Merges user tree, detected tokens, named skill map, and canonical registry
into a unified data source that commands consume by default.
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from gaia_cli.registry import registry_graph_path, named_skills_dir, user_tree_path
from gaia_cli.treeManager import load_tree
from gaia_cli.pathEngine import load_paths


@dataclass
class LocalContext:
    """Unified local-first view of skill state."""

    username: str
    owned_ids: set[str] = field(default_factory=set)
    detected_ids: set[str] = field(default_factory=set)
    novel_ids: set[str] = field(default_factory=set)
    named_map: dict[str, str] = field(default_factory=dict)  # generic_skill_id -> "contributor/name"
    tree_data: Optional[dict] = None
    graph_data: Optional[dict] = None
    _skill_map: dict[str, dict] = field(default_factory=dict, repr=False)

    @classmethod
    def load(cls, registry_path: str, username: str, *, include_scan: bool = True) -> "LocalContext":
        """Build context from local state.

        Args:
            registry_path: Path to the registry root
            username: Gaia username
            include_scan: Whether to load last scan results (paths.json)
        """
        # Load user tree
        tree_data = load_tree(username, registry_path=registry_path)
        owned_ids = set()
        if tree_data:
            owned_ids = {s.get('skillId') for s in tree_data.get('unlockedSkills', []) if s.get('skillId')}

        # Load canon graph
        graph_path = registry_graph_path(registry_path)
        graph_data = None
        skill_map = {}
        canon_ids = set()
        if os.path.isfile(graph_path):
            with open(graph_path, 'r', encoding='utf-8') as f:
                graph_data = json.load(f)
            for skill in graph_data.get('skills', []):
                sid = skill.get('id')
                if sid:
                    skill_map[sid] = skill
                    canon_ids.add(sid)

        # Load detected skills from last scan
        detected_ids = set()
        novel_ids = set()
        if include_scan:
            paths = load_paths()
            if paths:
                # nearUnlocks and oneAway contain detected skill IDs
                for path_entry in paths.get("availablePaths", []):
                    for prereq in path_entry.get("ownedPrereqs", []):
                        detected_ids.add(prereq)
                # Also consider owned as detected
                detected_ids |= owned_ids
                # Novel = detected but not in canon
                novel_ids = detected_ids - canon_ids

        # Build named_map from registry/named/
        named_map = _build_named_map(registry_path)

        ctx = cls(
            username=username,
            owned_ids=owned_ids,
            detected_ids=detected_ids,
            novel_ids=novel_ids,
            named_map=named_map,
            tree_data=tree_data,
            graph_data=graph_data,
        )
        ctx._skill_map = skill_map
        return ctx

    def is_named(self, skill_id: str) -> bool:
        """Check if a canonical skill has a named implementation."""
        return skill_id in self.named_map

    def named_ref(self, skill_id: str) -> Optional[str]:
        """Return 'contributor/name' for a named skill, or None."""
        return self.named_map.get(skill_id)

    def named_contributor(self, skill_id: str) -> Optional[str]:
        """Return just the contributor name for a named skill."""
        ref = self.named_map.get(skill_id)
        if ref and "/" in ref:
            return ref.split("/", 1)[0]
        return None

    def is_local(self, skill_id: str) -> bool:
        """Check if skill is local-only (not in canon)."""
        return skill_id in self.novel_ids

    def is_owned(self, skill_id: str) -> bool:
        """Check if user owns (has unlocked) this skill."""
        return skill_id in self.owned_ids

    def skill_level(self, skill_id: str) -> str:
        """Get the user's level for a skill, or canon level, or '0⭐'."""
        if self.tree_data:
            for s in self.tree_data.get('unlockedSkills', []):
                if s.get('skillId') == skill_id:
                    return s.get('level', '0⭐')
        skill = self._skill_map.get(skill_id)
        if skill:
            return skill.get('level', '0⭐')
        return "0⭐"

    def skill_type(self, skill_id: str) -> str:
        """Get skill type (basic/extra/ultimate)."""
        skill = self._skill_map.get(skill_id)
        if skill:
            return skill.get('type', 'basic')
        return 'basic'

    def all_skills(self) -> list[dict]:
        """Return merged skill list: canon + novel local skills."""
        skills = list(self._skill_map.values())
        for novel_id in self.novel_ids:
            if novel_id not in self._skill_map:
                skills.append({
                    "id": novel_id,
                    "name": novel_id,
                    "type": "basic",
                    "level": "0⭐",
                    "rarity": "common",
                    "prerequisites": [],
                    "derivatives": [],
                    "local": True,
                })
        return skills

    def display_name(self, skill_id: str) -> str:
        """Return the best display name for a skill (plain text, no ANSI).

        Priority: named ref > local user/id > /id
        """
        if skill_id in self.named_map:
            return self.named_map[skill_id]
        if skill_id in self.novel_ids:
            return f"{self.username}/{skill_id}"
        return f"/{skill_id}"


def _build_named_map(registry_path: str) -> dict[str, str]:
    """Scan registry/named/ to build generic_skill_id -> 'contributor/name' map."""
    named_dir = Path(named_skills_dir(registry_path))
    named_map: dict[str, str] = {}
    if not named_dir.is_dir():
        return named_map
    for md_path in sorted(named_dir.glob("*/*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
        except OSError:
            continue
        if not text.startswith("---\n"):
            continue
        # Parse frontmatter for genericSkillRef and id
        frontmatter_end = text.find("\n---", 4)
        if frontmatter_end == -1:
            continue
        frontmatter = text[4:frontmatter_end]
        skill_id = None
        generic_ref = None
        for line in frontmatter.splitlines():
            if ":" not in line:
                continue
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key == "id":
                skill_id = value
            elif key == "genericSkillRef":
                generic_ref = value
        if generic_ref and skill_id:
            named_map[generic_ref] = skill_id
    return named_map
