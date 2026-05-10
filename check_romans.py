import glob

files = glob.glob('docs/js/*.js') + glob.glob('docs/css/*.css') + glob.glob('registry/**/*.json', recursive=True) + glob.glob('src/gaia_cli/data/registry/**/*.json', recursive=True)
found_in = []
for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            if '"I"' in content or '"II"' in content or "'II'" in content or "'I'" in content or 'data-level="II"' in content:
                found_in.append(f)
    except Exception as e:
        pass
print("Found in:")
for f in found_in:
    print(f)
