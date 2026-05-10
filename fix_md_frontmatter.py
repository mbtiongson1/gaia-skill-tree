import glob
import re
import os

files = glob.glob('registry/named/**/*.md', recursive=True) + glob.glob('docs/**/*.md', recursive=True)

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
        # Frontmatter level: II -> level: 2★
        new_content = re.sub(rf'^level:\s*[\'"]?{r}[\'"]?\s*$', rf'level: "{s}"', new_content, flags=re.MULTILINE)
        
        # Also replace standalone instances if they are in array etc, but safer just to fix level:
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as file:
            file.write(new_content)
        print(f"Updated {filepath}")
