import glob
import re

files = glob.glob('docs/**/*.html', recursive=True) + \
        glob.glob('docs/**/*.css', recursive=True) + \
        glob.glob('docs/**/*.js', recursive=True) + \
        ['DESIGN.md']

romans = [('0', '0★'), ('I', '1★'), ('II', '2★'), ('III', '3★'), ('IV', '4★'), ('V', '5★'), ('VI', '6★')]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        continue
    
    new_content = content
    for r, s in romans:
        # replace data-level="I" to data-level="1★"
        new_content = new_content.replace(f'data-level="{r}"', f'data-level="{s}"')
        
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f'Updated {filepath}')
