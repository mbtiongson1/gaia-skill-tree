import { loadGraph } from "../graph/loader.js";
import { searchSkills, findSkillById } from "../graph/search.js";
import { getAncestors, getDescendants } from "../graph/dag.js";
import type { Skill } from "../graph/types.js";

function formatSkill(skill: Skill, ancestors: Skill[], descendants: Skill[]): string {
  const lines: string[] = [
    `# ${skill.name}`,
    `**ID:** ${skill.id}  `,
    `**Type:** ${skill.type}  `,
    `**Level:** ${skill.level}  `,
    `**Rarity:** ${skill.rarity}  `,
    `**Status:** ${skill.status}`,
    "",
    `## Description`,
    skill.description,
    "",
  ];

  if (skill.prerequisites.length > 0) {
    lines.push("## Prerequisites");
    for (const p of skill.prerequisites) {
      lines.push(`- ${p}`);
    }
    lines.push("");
  }

  if (skill.derivatives.length > 0) {
    lines.push("## Unlocks");
    for (const d of skill.derivatives) {
      lines.push(`- ${d}`);
    }
    lines.push("");
  }

  if (skill.conditions) {
    lines.push("## Conditions");
    lines.push(skill.conditions);
    lines.push("");
  }

  if (skill.evidence.length > 0) {
    lines.push("## Evidence");
    for (const e of skill.evidence) {
      lines.push(`- [${e.class}] ${e.source} (${e.evaluator}, ${e.date})`);
    }
    lines.push("");
  }

  if (ancestors.length > 0) {
    lines.push(`## Lineage (${ancestors.length} ancestors)`);
    for (const a of ancestors.slice(0, 10)) {
      lines.push(`- ${a.name} (${a.type}, ${a.level})`);
    }
    lines.push("");
  }

  if (descendants.length > 0) {
    lines.push(`## Derivatives (${descendants.length} skills build on this)`);
    for (const d of descendants.slice(0, 10)) {
      lines.push(`- ${d.name} (${d.type}, ${d.level})`);
    }
  }

  return lines.join("\n");
}

export async function lookupSkill(query: string): Promise<string> {
  const graph = await loadGraph();

  const direct = findSkillById(graph, query);
  if (direct) {
    const ancestors = getAncestors(graph, direct.id);
    const descendants = getDescendants(graph, direct.id);
    return formatSkill(direct, ancestors, descendants);
  }

  const results = searchSkills(graph, query);
  if (results.length === 0) {
    return `No skills found matching "${query}". The registry has ${graph.skills.length} skills. Try a broader search term.`;
  }

  if (results.length === 1) {
    const skill = results[0];
    const ancestors = getAncestors(graph, skill.id);
    const descendants = getDescendants(graph, skill.id);
    return formatSkill(skill, ancestors, descendants);
  }

  const lines = [`Found ${results.length} skills matching "${query}":\n`];
  for (const s of results) {
    lines.push(`- **${s.name}** (${s.id}) — ${s.type}, ${s.level}, ${s.rarity}`);
    lines.push(`  ${s.description.slice(0, 100)}...`);
  }
  lines.push("\nUse the exact ID for full details.");
  return lines.join("\n");
}
