import type { DemeritId, Skill } from "./types.js";

const LEVEL_ORDER = ["0", "I", "II", "III", "IV", "V", "VI"] as const;
const DEMERIT_ORDER: readonly DemeritId[] = [
  "niche-integration",
  "experimental-feature",
  "heavyweight-dependency",
];
const DEMERIT_ELIGIBLE_LEVELS = new Set(["II", "III", "IV", "V", "VI"]);
const MIN_EFFECTIVE_LEVEL = "I";

function levelIndex(level: string): number {
  return LEVEL_ORDER.indexOf(level as (typeof LEVEL_ORDER)[number]);
}

function demeritPenalty(skill: Pick<Skill, "demerits">): number {
  const demerits = skill.demerits ?? [];
  return demerits.filter((item) => DEMERIT_ORDER.includes(item)).length;
}

export function effectiveLevel(skill: Pick<Skill, "level" | "demerits">): Skill["level"] {
  if (!DEMERIT_ELIGIBLE_LEVELS.has(skill.level)) {
    return skill.level;
  }
  const baseIdx = levelIndex(skill.level);
  const floorIdx = levelIndex(MIN_EFFECTIVE_LEVEL);
  const lowered = Math.max(floorIdx, baseIdx - demeritPenalty(skill));
  return LEVEL_ORDER[lowered];
}
