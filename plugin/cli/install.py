"""Named skill install, sync, and uninstall logic.

Manages a dual-layer cache:
- Global: ~/.gaia/skills/{contributor}/{skill-name}.md
- Repo:   .gaia/named-skills/{contributor}/{skill-name}.md (symlink on Unix, copy on Windows)
"""

import hashlib
import json
import os
import shutil
import sys
from datetime import datetime, timezone


def get_global_cache_dir():
    return os.path.join(os.path.expanduser("~"), ".gaia", "skills")


def get_repo_skills_dir():
    return os.path.join(".gaia", "named-skills")


def get_manifest_path():
    return os.path.join(".gaia", "install-manifest.json")


def load_manifest():
    path = get_manifest_path()
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return {"installed": []}


def save_manifest(manifest):
    path = get_manifest_path()
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(manifest, f, indent=2)


def compute_sha256(filepath):
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            h.update(chunk)
    return h.hexdigest()


def find_named_skill_source(skill_id, registry_path):
    parts = skill_id.split("/", 1)
    if len(parts) != 2:
        return None
    contributor, skill_name = parts
    source = os.path.join(registry_path, "graph", "named", contributor, f"{skill_name}.md")
    if os.path.exists(source):
        return source
    return None


def install_skill(skill_id, registry_path):
    source = find_named_skill_source(skill_id, registry_path)
    if not source:
        print(f"Error: Named skill '{skill_id}' not found in registry.", file=sys.stderr)
        return False

    parts = skill_id.split("/", 1)
    contributor, skill_name = parts

    global_dir = os.path.join(get_global_cache_dir(), contributor)
    os.makedirs(global_dir, exist_ok=True)
    global_path = os.path.join(global_dir, f"{skill_name}.md")
    shutil.copy2(source, global_path)

    repo_dir = os.path.join(get_repo_skills_dir(), contributor)
    os.makedirs(repo_dir, exist_ok=True)
    repo_path = os.path.join(repo_dir, f"{skill_name}.md")

    if sys.platform != "win32":
        if os.path.exists(repo_path) or os.path.islink(repo_path):
            os.remove(repo_path)
        os.symlink(os.path.abspath(global_path), repo_path)
    else:
        shutil.copy2(global_path, repo_path)

    manifest = load_manifest()
    sha = compute_sha256(global_path)
    existing = next((s for s in manifest["installed"] if s["id"] == skill_id), None)
    if existing:
        existing["sha256"] = sha
        existing["installedAt"] = datetime.now(timezone.utc).isoformat()
    else:
        manifest["installed"].append({
            "id": skill_id,
            "installedAt": datetime.now(timezone.utc).isoformat(),
            "sourceRef": f"graph/named/{contributor}/{skill_name}.md",
            "sha256": sha,
        })
    save_manifest(manifest)
    print(f"Installed: {skill_id}")
    return True


def sync_skills(registry_path):
    manifest = load_manifest()
    if not manifest["installed"]:
        print("No named skills installed.")
        return

    updated = 0
    for entry in manifest["installed"]:
        skill_id = entry["id"]
        source = find_named_skill_source(skill_id, registry_path)
        if not source:
            print(f"  Warning: Source not found for {skill_id}")
            continue

        new_sha = compute_sha256(source)
        if new_sha != entry.get("sha256"):
            install_skill(skill_id, registry_path)
            updated += 1
        else:
            print(f"  Up to date: {skill_id}")

    print(f"\nSync complete. {updated} skill(s) updated.")


def uninstall_skill(skill_id):
    parts = skill_id.split("/", 1)
    if len(parts) != 2:
        print("Error: Invalid skill ID format. Expected 'contributor/skill-name'.", file=sys.stderr)
        return False
    contributor, skill_name = parts

    repo_path = os.path.join(get_repo_skills_dir(), contributor, f"{skill_name}.md")
    if os.path.exists(repo_path) or os.path.islink(repo_path):
        os.remove(repo_path)

    manifest = load_manifest()
    manifest["installed"] = [s for s in manifest["installed"] if s["id"] != skill_id]
    save_manifest(manifest)
    print(f"Uninstalled: {skill_id}")
    return True


def list_installed():
    manifest = load_manifest()
    if not manifest["installed"]:
        print("No named skills installed.")
        return

    print(f"{'ID':<35} {'Installed':<25} {'SHA-256 (short)'}")
    print("-" * 75)
    for entry in manifest["installed"]:
        sha_short = entry.get("sha256", "unknown")[:12]
        print(f"{entry['id']:<35} {entry['installedAt'][:19]:<25} {sha_short}")
