import json
import argparse
import sys

def detect_combinations(graph_data, owned_skills, detected_skills):
    combinations = []
    
    owned_skill_ids = set()
    for s in owned_skills:
        if isinstance(s, dict) and 'skillId' in s:
            owned_skill_ids.add(s['skillId'])
        elif isinstance(s, str):
            owned_skill_ids.add(s)

    combined_available = owned_skill_ids.union(set(detected_skills))
    
    for skill in graph_data.get('skills', []):
        if skill.get('type') in ['composite', 'legendary']:
            prereqs = skill.get('prerequisites', [])
            if not prereqs:
                continue
                
            if all(p in combined_available for p in prereqs):
                if skill['id'] not in owned_skill_ids:
                    combinations.append({
                        'candidateResult': skill['id'],
                        'levelFloor': skill.get('level'),
                        'detectedSkills': [p for p in prereqs if p in detected_skills] or prereqs,
                        'status': 'new_fusion'
                    })
                    
    return combinations

def main():
    parser = argparse.ArgumentParser(description="Detect skill combinations")
    parser.add_argument('--graph', required=True, help="Path to gaia.json")
    parser.add_argument('--detected', required=False, default="", help="Comma-separated detected skill IDs")
    parser.add_argument('--owned', required=True, help="Path to user skill-tree.json")
    
    args = parser.parse_args()
    
    with open(args.graph, 'r') as f:
        graph_data = json.load(f)
        
    with open(args.owned, 'r') as f:
        user_data = json.load(f)
        
    detected_skills = [s.strip() for s in args.detected.split(',')] if args.detected else []
    owned_skills = user_data.get('unlockedSkills', [])
    
    results = detect_combinations(graph_data, owned_skills, detected_skills)
    
    print(json.dumps(results, indent=2))

if __name__ == '__main__':
    main()
