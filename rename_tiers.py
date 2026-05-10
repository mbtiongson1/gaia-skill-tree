import os
import re
import subprocess
import glob

def run_git(cmd):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, encoding='utf-8')
    if result.returncode != 0:
        print(f"Error ({result.returncode}): {result.stderr}")
    return result

# Mapping for string replacements
# Ordered from longest to shortest to avoid partial replacements (e.g. III before II)
romans = [
    ("III", "3★"),
    ("VII", "7★"), # just in case
    ("VIII", "8★"),
    ("IV", "4★"),
    ("VI", "6★"),
    ("II", "2★"),
    ("IX", "9★"),
    ("V", "5★"),
    ("I", "1★"),
    ("0", "0★")
]

def apply_replacements_to_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return False
        
    new_content = content
    
    # specific fix for ranges and special cases BEFORE general regex
    new_content = new_content.replace('Level 0-I', '0★-1★')
    new_content = new_content.replace('Level 0–I', '0★–1★')
    new_content = new_content.replace('Level 0 -> I', '0★ -> 1★')
    new_content = new_content.replace('Levels I-VI', '1★-6★')
    new_content = new_content.replace('Levels I–VI', '1★–6★')
    new_content = new_content.replace('Level I-VI', '1★-6★')
    new_content = new_content.replace('Level I–VI', '1★–6★')
    new_content = new_content.replace('Lv.II→I', '2★→1★')
    new_content = new_content.replace('Level V/VI', '5★/6★')
    new_content = new_content.replace('level 0/I', '0★/1★')
    new_content = new_content.replace('level II+', '2★+')
    new_content = new_content.replace('Level II+', '2★+')
    new_content = new_content.replace('Levels II-VI', '2★-6★')

    # 1. JSON and Object properties: "level": "II", level: "II", "levelFloor": "II", levelFloor: "II"
    for r, s in romans:
        new_content = re.sub(rf'("level"\s*:\s*)"{r}"', rf'\1"{s}"', new_content)
        new_content = re.sub(rf'(level\s*:\s*)"{r}"', rf'\1"{s}"', new_content)
        new_content = re.sub(rf'("levelFloor"\s*:\s*)"{r}"', rf'\1"{s}"', new_content)
        new_content = re.sub(rf'(levelFloor\s*:\s*)"{r}"', rf'\1"{s}"', new_content)
        
    # 2. Textual references: "Level II", "Level I", "level I"
    for r, s in romans:
        new_content = re.sub(rf'(?<![a-zA-Z])(Level|Levels|level)\s+{r}(?![a-zA-Z])', rf'\1 {s}', new_content)
        
    # 3. Bracketed tiers in markdown tables/diagrams: " [III]", " [0]"
    if filepath.endswith('.md') or filepath.endswith('.html'):
        for r, s in romans:
            new_content = new_content.replace(f" [{r}]", f" [{s}]")
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

def process_files(patterns):
    changed = 0
    for pattern in patterns:
        for filepath in glob.glob(pattern, recursive=True):
            if os.path.isfile(filepath) and not '.git' in filepath and not 'node_modules' in filepath:
                if apply_replacements_to_file(filepath):
                    changed += 1
                    run_git(f"git add {filepath}")
    return changed

def main():
    # 1. Schema Updates
    run_git("git checkout -b schema/rename-tiers")
    changed = process_files(['registry/schema/*.json', 'src/gaia_cli/data/registry/schema/*.json'])
    if changed:
        run_git('git commit -m "schema: convert level enums to star notation (1★-6★)"')
    
    # 2. review/meta/rename-tiers
    run_git("git checkout -b review/meta/rename-tiers")
    changed = process_files(['registry/**/*.json', 'registry-for-review/**/*.json'])
    if changed:
        run_git('git commit -m "meta: update all skill levels to star notation in registry"')
        
    # 3. cli/rename-tiers
    run_git("git checkout -b cli/rename-tiers")
    changed = process_files([
        'scripts/**/*.py', 'src/**/*.py', 'tests/**/*.py', 'tests/**/*.json',
        'packages/mcp/**/*.ts', 'packages/mcp/**/*.json'
    ])
    if changed:
        run_git('git commit -m "cli: update tests and scripts to use star notation"')
        
    # 4. docs/rename-tiers
    run_git("git checkout -b docs/rename-tiers")
    changed = process_files([
        '*.md', 'docs/**/*.md', 'docs/**/*.html', 'docs/**/*.css', 'docs/**/*.js', 'hero_stats_variations.md'
    ])
    if changed:
        run_git('git commit -m "docs: update documentation to reference star tiers"')
        
    # 5. dev/rename-tiers
    run_git("git checkout -b dev/rename-tiers")
    print("Rigorous migration complete. Currently on dev/rename-tiers.")

if __name__ == "__main__":
    main()
