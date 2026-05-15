#!/usr/bin/env python3
import json
import os
import shutil

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NAMED_SKILLS_PATH = os.path.join(ROOT_DIR, 'registry', 'named-skills.json')
GAIA_JSON_PATH = os.path.join(ROOT_DIR, 'registry', 'gaia.json')
OUT_DIR = os.path.join(ROOT_DIR, 'docs', 'u')

def build():
    if not os.path.exists(NAMED_SKILLS_PATH):
        print(f"File not found: {NAMED_SKILLS_PATH}")
        return

    with open(NAMED_SKILLS_PATH, 'r') as f:
        named_skills = json.load(f)

    with open(GAIA_JSON_PATH, 'r') as f:
        gaia_graph = json.load(f)

    # Group by contributor
    contributors = {}
    buckets = named_skills.get('buckets', {})
    for bucket_name, skills_list in buckets.items():
        for info in skills_list:
            named_id = info.get('id')
            handle = info.get('contributor')
            if not handle or not named_id:
                continue
            if handle not in contributors:
                contributors[handle] = []
            contributors[handle].append((named_id, info))

    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)

    template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{handle} — Gaia Contributor</title>
  <link rel="stylesheet" href="../../css/styles.css">
  <link rel="stylesheet" href="../../css/plaque.css">
</head>
<body class="profile-page">
  <nav>
    <div class="nav-logo">
      <img src="../../assets/marks/diamond-seal.svg" alt="Diamond Seal" width="24" height="24">
      GAIA
    </div>
    <ul>
      <li><a href="../../index.html#registry">Registry</a></li>
      <li><a href="../../index.html#hall-of-heroes">Hall of Heroes</a></li>
      <li><a href="../../codex.html">The Codex</a></li>
    </ul>
  </nav>

  <section style="margin: 8rem auto; max-width: 800px; padding: 0 1.5rem;">
    <h1 style="color: var(--honor-red); font-family: 'Departure Mono', monospace; font-size: 2.5rem; margin-bottom: 0.5rem;">{handle}</h1>
    <p style="color: var(--muted); font-size: 1.1rem; margin-bottom: 3rem;">Origin contributor · Joined 2026</p>

    <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 2rem;">
      {plaques}
    </div>
  </section>
</body>
</html>"""

    for handle, skills in contributors.items():
        user_dir = os.path.join(OUT_DIR, handle)
        os.makedirs(user_dir, exist_ok=True)
        
        plaques_html = ""
        for skill_id, info in skills:
            # find tier in gaia.json
            base_skill_id = skill_id.split('/')[-1]
            node = gaia_graph.get('nodes', {}).get(base_skill_id, {})
            evidence_class = "C"
            stars = 2
            # Very naive extraction
            
            plaques_html += f"""
            <div class="plaque-plate" style="transform: scale(0.8); transform-origin: top left;">
              <img src="../../assets/marks/diamond-seal.svg" class="plaque-seal" alt="Diamond Seal">
              <div class="plaque-name">{skill_id.split('/')[-1]}</div>
              <div class="plaque-handle">{handle}</div>
              <div class="plaque-stars">{'★' * stars}</div>
              <div class="plaque-class">CLASS {evidence_class}</div>
            </div>
            """

        html_content = template.replace('{handle}', handle).replace('{plaques}', plaques_html)
        
        with open(os.path.join(user_dir, 'index.html'), 'w') as f:
            f.write(html_content)
        
        print(f"Generated profile for {handle}")

if __name__ == "__main__":
    build()
