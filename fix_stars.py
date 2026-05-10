import os
import re

def fix_stars():
    # 1. Global replace ⭐ with ★
    # 2. Fix the HUD Roman numerals in docs/js/skill-graph.js
    
    root = os.getcwd()
    
    # Files to ignore (scripts I created, .git, etc.)
    ignore_dirs = {'.git', '.agents', '.gemini', '__pycache__', 'venv', '.venv'}
    ignore_files = {'fix_stars.py'}
    
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ignore_dirs]
        for filename in filenames:
            if filename in ignore_files:
                continue
            
            filepath = os.path.join(dirpath, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace stars
                new_content = content.replace('⭐', '★')
                
                # If it's the specific HUD file, fix the Roman numerals
                if filepath.endswith('skill-graph.js') and 'docs\\js' in filepath:
                    # Replace I, II, III, IV, V, VI with 1★, 2★, 3★, 4★, 5★, 6★ inside the rank-pill spans
                    new_content = re.sub(r'data-legend-rank="1★" [^>]*>I</span>', 'data-legend-rank="1★" style="background:rgba(56,189,248,.12);color:#38bdf8">1★</span>', new_content)
                    new_content = re.sub(r'data-legend-rank="2★" [^>]*>II</span>', 'data-legend-rank="2★" style="background:rgba(99,202,183,.12);color:#63cab7">2★</span>', new_content)
                    new_content = re.sub(r'data-legend-rank="3★" [^>]*>III</span>', 'data-legend-rank="3★" style="background:rgba(167,139,250,.12);color:#a78bfa">3★</span>', new_content)
                    new_content = re.sub(r'data-legend-rank="4★" [^>]*>IV</span>', 'data-legend-rank="4★" style="background:rgba(232,121,249,.12);color:#e879f9">4★</span>', new_content)
                    new_content = re.sub(r'data-legend-rank="5★" [^>]*>V</span>', 'data-legend-rank="5★" style="background:rgba(251,191,36,.12);color:#fbbf24">5★</span>', new_content)
                    new_content = re.sub(r'data-legend-rank="6★" [^>]*>VI</span>', 'data-legend-rank="6★" style="background:rgba(251,191,36,.20);color:#fbbf24">6★</span>', new_content)

                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Updated: {filepath}")
            except (UnicodeDecodeError, PermissionError):
                continue

if __name__ == "__main__":
    fix_stars()
