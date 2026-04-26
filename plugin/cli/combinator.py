import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    from scripts.detectCombinations import detect_combinations
except ImportError:
    detect_combinations = None

def get_combinations(graph_data, owned_skills, detected_skills):
    if detect_combinations is None:
        print("Error: detectCombinations module not found.", file=sys.stderr)
        return []
    combos = detect_combinations(graph_data, owned_skills, detected_skills)
    return combos
