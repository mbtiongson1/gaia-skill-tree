import type { DemeritId, Skill } from "./types.js";

const LEVEL_ORDER = ["0⭐", "1⭐", "2⭐", "3⭐", "4⭐", "5⭐", "6⭐"] as const;
const DEMERIT_ORDER: readonly DemeritId[] = [
  "niche-integration",
  "experimental-feature",
  "heavyweight-dependency",
];
const DEMERIT_ELIGIBLE_LEVELS = new Set(["2⭐", "3⭐", "4⭐", "5⭐", "6⭐"]);
const MIN_EFFECTIVE_LEVEL = "1⭐";

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
