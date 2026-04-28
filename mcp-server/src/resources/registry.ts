import { loadGraph, loadUserTree } from "../graph/loader.js";
import type { GaiaGraph, UserSkillTree } from "../graph/types.js";

export async function getRegistryResource(): Promise<string> {
  const graph = await loadGraph();
  const summary = {
    version: graph.version,
    generatedAt: graph.generatedAt,
    totalSkills: graph.skills.length,
    byType: {
      atomic: graph.skills.filter((s) => s.type === "atomic").length,
      composite: graph.skills.filter((s) => s.type === "composite").length,
      legendary: graph.skills.filter((s) => s.type === "legendary").length,
    },
    totalEdges: graph.edges.length,
    skills: graph.skills.map((s) => ({
      id: s.id,
      name: s.name,
      type: s.type,
      level: s.level,
      rarity: s.rarity,
      prerequisites: s.prerequisites,
    })),
  };
  return JSON.stringify(summary, null, 2);
}

export async function getUserTreeResource(username: string): Promise<string> {
  const rawTree = await loadUserTree(username);
  if (!rawTree) {
    return JSON.stringify({ error: `No skill tree found for user "${username}"` });
  }
  return JSON.stringify(rawTree, null, 2);
}
