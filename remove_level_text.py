import glob
import re

files = glob.glob('**/*.py', recursive=True) + \
        glob.glob('**/*.json', recursive=True) + \
        glob.glob('**/*.md', recursive=True) + \
        glob.glob('**/*.html', recursive=True) + \
        glob.glob('**/*.js', recursive=True) + \
        glob.glob('**/*.css', recursive=True)

# ignore node_modules or .git
files = [f for f in files if '.git' not in f and 'node_modules' not in f and '.gemini' not in f]

for filepath in files:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue
        
    new_content = content
    
    # Replace 1★ with 1★
    new_content = re.sub(r'Lv\.([0-9]★)', r'\1', new_content)
    
    # Replace 1★ with 1★, 1★ with 1★
    new_content = re.sub(r'[Ll]evel(s)?\s+([0-9]★)', r'\2', new_content)
    
    # Special ranges like 1★-6★ -> 1★-6★
    new_content = re.sub(r'[Ll]evel(s)?\s+([0-9]★[-–][0-9]★)', r'\2', new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
