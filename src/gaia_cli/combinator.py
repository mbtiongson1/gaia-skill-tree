def detect_combinations(graph_data, owned_skills, detected_skills):
    combinations = []

    owned_skill_ids = set()
    for skill in owned_skills:
        if isinstance(skill, dict) and 'skillId' in skill:
            owned_skill_ids.add(skill['skillId'])
        elif isinstance(skill, str):
            owned_skill_ids.add(skill)

    combined_available = owned_skill_ids.union(set(detected_skills))

    for skill in graph_data.get('skills', []):
        if skill.get('type') not in ['extra', 'ultimate']:
            continue

        prereqs = skill.get('prerequisites', [])
        if not prereqs:
            continue

        if all(prereq in combined_available for prereq in prereqs):
            if skill['id'] not in owned_skill_ids:
                combinations.append({
                    'candidateResult': skill['id'],
                    'levelFloor': skill.get('level'),
                    'detectedSkills': [p for p in prereqs if p in detected_skills] or prereqs,
                    'status': 'new_fusion'
                })

    return combinations

def get_combinations(graph_data, owned_skills, detected_skills):
    return detect_combinations(graph_data, owned_skills, detected_skills)
