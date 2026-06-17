import os
import json
import yaml
import glob
import subprocess

# Live-verified star count cache to speed up and fallback
STARS_CACHE = {
    'mattpocock/skills': 133210,
    'ruvnet/ruflo': 59957,
    'garrytan/gstack': 110930,
    'obra/superpowers': 230818,
    'ruvnet/agentdb': 66,
    'pbakaus/impeccable': 39158,
    '0xDarkMatter/claude-mods': 22,
    'browser-use/browser-harness': 15008,
    'browser-use/browser-use': 99295,
    'addyosmani/agent-skills': 62101
}

def get_live_stars(repo_path):
    if repo_path in STARS_CACHE:
        return STARS_CACHE[repo_path]
    try:
        # Run gh CLI to query stargazers count
        out = subprocess.check_output(['gh', 'repo', 'view', repo_path, '--json', 'stargazerCount'], text=True)
        data = json.loads(out)
        stars = data.get('stargazerCount', 0)
        STARS_CACHE[repo_path] = stars
        return stars
    except Exception as e:
        print(f"Warning: Could not fetch stars for {repo_path}: {e}")
        return None

def parse_repo_path(url):
    if not url or 'github.com/' not in url:
        return None
    try:
        path = url.split('github.com/')[1]
        parts = [p for p in path.split('/') if p]
        if len(parts) >= 2:
            # handle case where it's owner/repo/blob/...
            return f"{parts[0]}/{parts[1]}"
    except Exception:
        pass
    return None

def main():
    print("Loading registry files...")
    # Load named-skills.json
    try:
        named_skills_data = json.load(open('registry/named-skills.json'))
    except Exception as e:
        print(f"Error loading named-skills.json: {e}")
        return

    # Load gaia.json (generic skills)
    try:
        gaia_data = json.load(open('registry/gaia.json'))
    except Exception as e:
        print(f"Error loading gaia.json: {e}")
        return

    # Gather generic skills evidence maps
    generic_evidence = {}
    for s in gaia_data.get('skills', []):
        if 'id' in s:
            generic_evidence[s['id']] = s.get('evidence') or []

    # Map each named skill by level
    tier_groups = {
        '6★': [],
        '5★': [],
        '4★': [],
        '3★': [],
        '2★': [],
        '1★': [],
        'provisional': []
    }

    print("Parsing named skills and compiling evidence...")
    # Read files from registry/named/ for rich evidence since JSON might be compiled
    named_files = glob.glob('registry/named/**/*.md', recursive=True)
    parsed_skills = {}

    for file_path in named_files:
        try:
            content = open(file_path).read()
            if not content.startswith('---'):
                continue
            parts = content.split('---')
            if len(parts) < 3:
                continue
            meta = yaml.safe_load(parts[1])
            if not meta or 'id' not in meta:
                continue
            
            skill_id = meta['id']
            level = meta.get('level', '2★')
            
            # Combine skill's own evidence and generic inherited evidence
            own_evidence = meta.get('evidence') or []
            generic_ref = meta.get('genericSkillRef')
            inherited = generic_evidence.get(generic_ref) or []
            
            # De-duplicate evidence by source URL
            seen_sources = set()
            merged_evidence = []
            
            # Helper to add evidence with source cleaning
            def add_entry(entry):
                src = entry.get('source')
                if src and src not in seen_sources:
                    seen_sources.add(src)
                    
                    # Update repo star counts if it is a github repo source
                    repo_path = parse_repo_path(src)
                    if repo_path:
                        live_stars = get_live_stars(repo_path)
                        if live_stars is not None:
                            entry['stars_verified'] = live_stars
                    merged_evidence.append(entry)

            for e in own_evidence:
                add_entry(e)
            for e in inherited:
                add_entry(e)
                
            meta['compiled_evidence'] = merged_evidence
            parsed_skills[skill_id] = meta
            
            if level in tier_groups:
                tier_groups[level].append(meta)
            else:
                tier_groups['provisional'].append(meta)
        except Exception as e:
            print(f"Error parsing file {file_path}: {e}")

    # Write source lists grouped by tier
    for level, skills in tier_groups.items():
        if not skills:
            continue
            
        filename = f"founder/sources/tier_{level.replace('★', '')}.md"
        print(f"Writing {filename} with {len(skills)} skills...")
        
        with open(filename, 'w') as f:
            f.write(f"# Evidence Sources: Tier {level}\n\n")
            f.write(f"This file lists the raw evidence sources for named skills rated at {level}.\n\n")
            
            for s in sorted(skills, key=lambda x: x['id']):
                ev_list = s.get('compiled_evidence') or []
                if not ev_list:
                    continue
                    
                f.write(f"## Skill: `{s['id']}`\n")
                f.write(f"- **Name:** {s.get('name')}\n")
                f.write(f"- **Contributor:** `{s.get('contributor')}`\n")
                
                # List other github repo link from links.github
                gh_link = s.get('links', {}).get('github')
                if gh_link:
                    repo_path = parse_repo_path(gh_link)
                    if repo_path:
                        live_stars = get_live_stars(repo_path)
                        if live_stars is not None:
                            f.write(f"- **Primary GitHub Repository:** [{gh_link}]({gh_link}) ({live_stars:,} stars)\n")
                        else:
                            f.write(f"- **Primary GitHub Repository:** [{gh_link}]({gh_link})\n")
                
                f.write("\n### Evidence Rows:\n\n")
                for i, e in enumerate(ev_list, 1):
                    f.write(f"#### E{i}: `{e.get('type', 'unknown')}`\n")
                    f.write(f"- **Source:** [{e.get('source')}]({e.get('source')})\n")
                    f.write(f"- **Date:** {e.get('date', 'unknown')}\n")
                    
                    if 'stars_verified' in e:
                        f.write(f"- **Verified Stars:** {e['stars_verified']:,} stars\n")
                    elif e.get('trustNumber'):
                        f.write(f"- **Trust Metric:** {e.get('trustNumber')}\n")
                        
                    f.write(f"- **Description:** {e.get('notes', 'No notes.')}\n\n")
                
                f.write("---\n\n")

    # Generate master report
    print("Writing master report...")
    with open('founder/sources/source_report_2026_06_18.md', 'w') as f:
        f.write("# Consolidated Trust Methodology Source Report\n\n")
        f.write("**Date:** June 18, 2026  \n")
        f.write("**Subject:** Complete Dump of Verified Evidence Sources across all Gaia named skills\n\n")
        
        f.write("## 1. Summary Metrics\n\n")
        total_skills = sum(len(skills) for skills in tier_groups.values())
        total_sources = 0
        skills_with_sources = 0
        
        for level, skills in sorted(tier_groups.items(), reverse=True):
            level_sources = 0
            level_skills_with_sources = 0
            for s in skills:
                evs = len(s.get('compiled_evidence') or [])
                if evs > 0:
                    level_skills_with_sources += 1
                    level_sources += evs
            total_sources += level_sources
            skills_with_sources += level_skills_with_sources
            f.write(f"- **Tier {level}:** {len(skills)} skills total, {level_skills_with_sources} have verified sources ({level_sources} raw source entries)\n")
            
        f.write(f"\n- **Total Skills Evaluated:** {total_skills}\n")
        f.write(f"- **Total Skills with Active Sources:** {skills_with_sources}\n")
        f.write(f"- **Total Evidence Entries Dumped:** {total_sources}\n\n")
        
        f.write("## 2. Directory Index\n\n")
        f.write("All raw sources are partitioned by level for fast consumption:\n")
        for level in sorted(tier_groups.keys(), reverse=True):
            if tier_groups[level]:
                f.write(f"- [Tier {level} Source Dump](file:///Users/marcotiongson/Documents/gaia-skill-tree/founder/sources/tier_{level.replace('★', '')}.md)\n")

if __name__ == '__main__':
    main()
