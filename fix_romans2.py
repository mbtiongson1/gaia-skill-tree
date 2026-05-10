import glob
import re
import os

files = []
patterns = [
    'docs/**/*.json'
]
for p in patterns:
    files.extend(glob.glob(p, recursive=True))

romans = [
    ("VI", "6★"),
    ("IV", "4★"),
    ("III", "3★"),
    ("II", "2★"),
    ("V", "5★"),
    ("I", "1★"),
    ("0", "0★")
]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.read()
    except Exception as e:
        continue
        
    new_content = content
    
    for r, s in romans:
        new_content = re.sub(rf'(["\']){r}\1', rf'\g<1>{s}\g<1>', new_content)
        new_content = re.sub(rf'data-level=(["\']){r}\1', rf'data-level=\g<1>{s}\g<1>', new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Updated {filepath}")
