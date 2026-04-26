import json
import os
import re

def load_config():
    config_path = '.gaia/config.json'
    if not os.path.exists(config_path):
        return None
    with open(config_path, 'r') as f:
        return json.load(f)

def scan_file_for_skills(filepath):
    skill_pattern = re.compile(r'\b[a-z][a-zA-Z0-9]*\b')
    found_skills = set()
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            for match in skill_pattern.finditer(content):
                found_skills.add(match.group(0))
    except Exception:
        pass
    return found_skills

def scan_repo():
    config = load_config()
    if not config:
        return set()
    scan_paths = config.get('scanPaths', [])
    all_found = set()
    for path in scan_paths:
        if os.path.isfile(path):
            all_found.update(scan_file_for_skills(path))
        elif os.path.isdir(path):
            for root, _, files in os.walk(path):
                for file in files:
                    if not file.startswith('.') and not file.endswith(('.png', '.jpg', '.pyc', '.o', '.gexf')):
                        all_found.update(scan_file_for_skills(os.path.join(root, file)))
    return all_found
