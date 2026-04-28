import type { GaiaGraph, FusionCandidate } from "../graph/types.js";

export function detectCombinations(
  graph: GaiaGraph,
  ownedSkillIds: string[],
  detectedSkillIds: string[]
): FusionCandidate[] {
  const available = new Set([...ownedSkillIds, ...detectedSkillIds]);
  const owned = new Set(ownedSkillIds);
  const candidates: FusionCandidate[] = [];

  for (const skill of graph.skills) {
    if (skill.type === "atomic") continue;
    if (owned.has(skill.id)) continue;
    if (skill.prerequisites.length === 0) continue;

    const met = skill.prerequisites.filter((p) => available.has(p));
    const missing = skill.prerequisites.filter((p) => !available.has(p));

    if (missing.length === 0) {
      candidates.push({
        candidateResult: skill.id,
        levelFloor: skill.level,
        detectedSkills: met,
        missingSkills: [],
        status: "ready",
      });
    } else if (missing.length === 1) {
      candidates.push({
        candidateResult: skill.id,
        levelFloor: skill.level,
        detectedSkills: met,
        missingSkills: missing,
        status: "one_away",
      });
    }
  }

  return candidates.sort((a, b) => {
    if (a.status === "ready" && b.status !== "ready") return -1;
    if (b.status === "ready" && a.status !== "ready") return 1;
    const rarityOrder = ["legendary", "epic", "rare", "uncommon", "common"];
    const aSkill = graph.skills.find((s) => s.id === a.candidateResult);
    const bSkill = graph.skills.find((s) => s.id === b.candidateResult);
    const aIdx = rarityOrder.indexOf(aSkill?.rarity ?? "common");
    const bIdx = rarityOrder.indexOf(bSkill?.rarity ?? "common");
    return aIdx - bIdx;
  });
}
