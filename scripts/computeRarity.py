import json
import argparse
import sys
import os
import glob

def get_rarity(percentage):
    if percentage > 0.40:
        return 'common'
    elif percentage > 0.20:
        return 'uncommon'
    elif percentage > 0.05:
        return 'rare'
    elif percentage >= 0.01:
        return 'epic'
    else:
        return 'legendary'

def main():
    parser = argparse.ArgumentParser(description="Compute skill rarity based on user trees")
    parser.add_argument('--users-dir', default="users", help="Directory containing user trees")
    parser.add_argument('--graph', default="graph/gaia.json", help="Path to gaia.json")
    parser.add_argument('--apply', action='store_true', help="Apply changes to gaia.json")
    
    args = parser.parse_args()
    
    user_files = glob.glob(os.path.join(args.users_dir, '*', 'skill-tree.json'))
    
    if not user_files:
        print("{}")
        return
        
    total_users = len(user_files)
    skill_counts = {}
    
    for fpath in user_files:
        try:
            with open(fpath, 'r') as f:
                data = json.load(f)
                for unlock in data.get('unlockedSkills', []):
                    sid = unlock.get('skillId')
                    if sid:
                        skill_counts[sid] = skill_counts.get(sid, 0) + 1
        except Exception as e:
            pass
            
    rarity_table = {}
    for sid, count in skill_counts.items():
        percentage = count / total_users
        rarity_table[sid] = {
            'prevalence': percentage,
            'count': count,
            'computedRarity': get_rarity(percentage)
        }
        
    print(json.dumps(rarity_table, indent=2))
    
    if args.apply:
        with open(args.graph, 'r') as f:
            graph_data = json.load(f)
            
        changed = False
        for skill in graph_data.get('skills', []):
            sid = skill['id']
            if sid in rarity_table:
                new_rarity = rarity_table[sid]['computedRarity']
                if skill.get('rarity') != new_rarity:
                    skill['rarity'] = new_rarity
                    changed = True
                    
        if changed:
            with open(args.graph, 'w') as f:
                json.dump(graph_data, f, indent=2)

if __name__ == '__main__':
    main()
