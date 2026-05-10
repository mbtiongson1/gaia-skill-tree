import glob
import re

files = glob.glob('packages/mcp/**/*.ts', recursive=True) + glob.glob('packages/mcp/**/*.json', recursive=True)

romans = [
    ("III", "3★"),
    ("VII", "7★"), 
    ("VIII", "8★"),
    ("IV", "4★"),
    ("VI", "6★"),
    ("II", "2★"),
    ("IX", "9★"),
    ("V", "5★"),
    ("I", "1★"),
    ("0", "0★")
]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        continue
        
    new_content = content
    
    # We replace strict string values like "II" -> "2★"
    for r, s in romans:
        new_content = new_content.replace(f'"{r}"', f'"{s}"')
        new_content = new_content.replace(f"'{r}'", f"'{s}'")

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
