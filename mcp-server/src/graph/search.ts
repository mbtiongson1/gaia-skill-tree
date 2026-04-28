import type { Skill, GaiaGraph } from "./types.js";

function trigrams(s: string): Set<string> {
  const padded = `  ${s.toLowerCase()}  `;
  const set = new Set<string>();
  for (let i = 0; i < padded.length - 2; i++) {
    set.add(padded.slice(i, i + 3));
  }
  return set;
}

function similarity(a: string, b: string): number {
  const ta = trigrams(a);
  const tb = trigrams(b);
  let intersection = 0;
  for (const t of ta) {
    if (tb.has(t)) intersection++;
  }
  const union = ta.size + tb.size - intersection;
  return union === 0 ? 0 : intersection / union;
}

export function searchSkills(graph: GaiaGraph, query: string, limit = 5): Skill[] {
  const q = query.toLowerCase().trim();

  const exact = graph.skills.find(
    (s) => s.id === q || s.name.toLowerCase() === q
  );
  if (exact) return [exact];

  const scored = graph.skills
    .map((skill) => ({
      skill,
      score: Math.max(
        similarity(q, skill.id),
        similarity(q, skill.name),
        similarity(q, skill.description.slice(0, 80))
      ),
    }))
    .filter((x) => x.score > 0.15)
    .sort((a, b) => b.score - a.score);

  return scored.slice(0, limit).map((x) => x.skill);
}

export function findSkillById(graph: GaiaGraph, id: string): Skill | undefined {
  return graph.skills.find((s) => s.id === id);
}
