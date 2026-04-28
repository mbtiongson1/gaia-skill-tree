import type { GaiaGraph, Skill } from "./types.js";

export function getAncestors(graph: GaiaGraph, skillId: string): Skill[] {
  const visited = new Set<string>();
  const result: Skill[] = [];

  function walk(id: string): void {
    const skill = graph.skills.find((s) => s.id === id);
    if (!skill) return;
    for (const prereq of skill.prerequisites) {
      if (!visited.has(prereq)) {
        visited.add(prereq);
        const parent = graph.skills.find((s) => s.id === prereq);
        if (parent) {
          result.push(parent);
          walk(prereq);
        }
      }
    }
  }

  walk(skillId);
  return result;
}

export function getDescendants(graph: GaiaGraph, skillId: string): Skill[] {
  const visited = new Set<string>();
  const result: Skill[] = [];

  function walk(id: string): void {
    const skill = graph.skills.find((s) => s.id === id);
    if (!skill) return;
    for (const deriv of skill.derivatives) {
      if (!visited.has(deriv)) {
        visited.add(deriv);
        const child = graph.skills.find((s) => s.id === deriv);
        if (child) {
          result.push(child);
          walk(deriv);
        }
      }
    }
  }

  walk(skillId);
  return result;
}

export function getLineageDepth(graph: GaiaGraph, skillId: string): number {
  const skill = graph.skills.find((s) => s.id === skillId);
  if (!skill || skill.prerequisites.length === 0) return 0;
  return 1 + Math.max(...skill.prerequisites.map((p) => getLineageDepth(graph, p)));
}

export function getSkillsAtLevel(graph: GaiaGraph, level: string): Skill[] {
  return graph.skills.filter((s) => s.level === level);
}

export function getSkillsByType(graph: GaiaGraph, type: Skill["type"]): Skill[] {
  return graph.skills.filter((s) => s.type === type);
}
