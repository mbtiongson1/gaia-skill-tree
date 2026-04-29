import json
import os
import re

DEFAULT_EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".next",
    ".nuxt",
    ".turbo",
    ".cache",
    ".pytest_cache",
    ".mypy_cache",
    ".venv",
    "venv",
    "env",
    "node_modules",
    "dist",
    "build",
    "coverage",
    "vendor",
    "__pycache__",
}

DEFAULT_EXCLUDED_EXTENSIONS = (
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".ico",
    ".pdf",
    ".pyc",
    ".o",
    ".gexf",
)


def load_config():
    config_path = '.gaia/config.json'
    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r') as f:
        return json.load(f)


def scan_file_for_skills(filepath):
    skill_pattern = re.compile(r'\b[a-z][a-z0-9]*(-[a-z0-9]+)*\b')
    found_skills = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for match in skill_pattern.finditer(content):
                found_skills.add(match.group(0))
    except Exception:
        pass
    return found_skills


def _should_scan_file(filename):
    return not filename.startswith('.') and not filename.endswith(DEFAULT_EXCLUDED_EXTENSIONS)


def scan_repo_detailed():
    config = load_config()
    empty = {
        "tokens": set(),
        "files_scanned": 0,
        "candidate_count": 0,
        "paths_found": [],
        "paths_missing": [],
    }
    if not config:
        return empty

    scan_paths = config.get('scanPaths', [])
    all_found = set()
    files_scanned = 0
    paths_found = []
    paths_missing = []

    for path in scan_paths:
        if os.path.isfile(path):
            paths_found.append(path)
            all_found.update(scan_file_for_skills(path))
            files_scanned += 1
        elif os.path.isdir(path):
            paths_found.append(path)
            for root, dirs, files in os.walk(path):
                dirs[:] = [d for d in dirs if d not in DEFAULT_EXCLUDED_DIRS and not d.startswith('.')]
                for file in files:
                    if _should_scan_file(file):
                        all_found.update(scan_file_for_skills(os.path.join(root, file)))
                        files_scanned += 1
        else:
            paths_missing.append(path)

    return {
        "tokens": all_found,
        "files_scanned": files_scanned,
        "candidate_count": len(all_found),
        "paths_found": paths_found,
        "paths_missing": paths_missing,
    }


def scan_repo():
    return scan_repo_detailed()["tokens"]
