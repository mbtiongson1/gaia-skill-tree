import json
import os
import datetime

def main():
    with open('graph/gaia.json', 'r') as f:
        data = json.load(f)
    
    version = data.get('version', '0.1.0')
    timestamp = data.get('generatedAt', datetime.datetime.now().isoformat() + 'Z')
    skills = data.get('skills', [])
    
    skills.sort(key=lambda x: x['id'])
    
    os.makedirs('skills/atomic', exist_ok=True)
    os.makedirs('skills/composite', exist_ok=True)
    os.makedirs('skills/legendary', exist_ok=True)
    
    skill_map = {s['id']: s for s in skills}
    
    for skill in skills:
        skill_type = skill.get('type', 'atomic')
        skill_id = skill.get('id')
        file_path = f"skills/{skill_type}/{skill_id}.md"
        
        with open(file_path, 'w') as f:
            f.write(f"# {skill.get('name')}\n")
            f.write(f"**ID:** {skill_id}  \n")
            f.write(f"**Type:** {skill_type.capitalize()}  \n")
            f.write(f"**Level:** {skill.get('level')}  \n")
            f.write(f"**Rarity:** {skill.get('rarity').capitalize()}  \n")
            f.write(f"**Status:** {skill.get('status').capitalize()}\n\n")
            f.write("---\n\n")
            
            f.write("## Description\n")
            f.write(f"{skill.get('description', '')}\n\n")
            
            f.write("## Prerequisites\n")
            prereqs = skill.get('prerequisites', [])
            if not prereqs:
                f.write("_None._\n\n")
            else:
                for prereq_id in prereqs:
                    prereq = skill_map.get(prereq_id)
                    if prereq:
                        prereq_type = prereq.get('type', 'atomic')
                        f.write(f"- [{prereq.get('name')}](../{prereq_type}/{prereq_id}.md)\n")
                    else:
                        f.write(f"- {prereq_id}\n")
                f.write("\n")
                
            f.write("## Unlocks\n")
            unlocks = skill.get('derivatives', [])
            if not unlocks:
                f.write("_None._\n\n")
            else:
                for unlock_id in unlocks:
                    unlock = skill_map.get(unlock_id)
                    if unlock:
                        unlock_type = unlock.get('type', 'atomic')
                        f.write(f"- [{unlock.get('name')}](../{unlock_type}/{unlock_id}.md)\n")
                    else:
                        f.write(f"- {unlock_id}\n")
                f.write("\n")
                
            if skill_type in ['composite', 'legendary']:
                f.write("## Fusion Condition\n")
                conditions = skill.get('conditions', '')
                if not conditions:
                    f.write("_None specified._\n\n")
                else:
                    f.write(f"{conditions}\n\n")
            
            f.write("## Evidence\n")
            evidence = skill.get('evidence', [])
            if not evidence:
                f.write("_None._\n\n")
            else:
                f.write("| Class | Source | Evaluator | Date |\n")
                f.write("|---|---|---|---|\n")
                for ev in evidence:
                    f.write(f"| {ev.get('class', '')} | {ev.get('source', '')} | {ev.get('evaluator', '')} | {ev.get('date', '')} |\n")
                f.write("\n")
                
            f.write("## Known Agents\n")
            agents = skill.get('knownAgents', [])
            if not agents:
                f.write("_None verified yet._\n\n")
            else:
                for agent in agents:
                    f.write(f"- {agent}\n")
                f.write("\n")
                
            f.write("---\n")
            date_str = timestamp.split('T')[0] if 'T' in timestamp else timestamp
            f.write(f"*Generated from gaia.json v{version} on {date_str}. Do not edit directly.*\n")
            
    # generate registry.md
    with open('registry.md', 'w') as f:
        f.write("# Gaia Skill Registry\n\n")
        f.write("| Name | Type | Level | Rarity | Status |\n")
        f.write("|---|---|---|---|---|\n")
        for skill in skills:
            f.write(f"| {skill.get('name')} | {skill.get('type').capitalize()} | {skill.get('level')} | {skill.get('rarity').capitalize()} | {skill.get('status').capitalize()} |\n")
        f.write(f"\n*Generated from gaia.json v{version}.*\n")
        
    # generate combinations.md
    with open('combinations.md', 'w') as f:
        f.write("# Combinations\n\n")
        f.write("| Composite/Legendary | Prerequisites | Level Floor | Conditions |\n")
        f.write("|---|---|---|---|\n")
        for skill in skills:
            if skill.get('type') in ['composite', 'legendary']:
                prereqs = [skill_map.get(pid, {}).get('name', pid) for pid in skill.get('prerequisites', [])]
                prereq_str = ", ".join(prereqs)
                f.write(f"| {skill.get('name')} | {prereq_str} | {skill.get('level')} | {skill.get('conditions')} |\n")
        f.write(f"\n*Generated from gaia.json v{version}.*\n")

if __name__ == '__main__':
    main()
