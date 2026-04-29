/**
 * Type definitions for Gaia CLI
 */

export interface GaiaConfig {
  gaiaUser: string;
  gaiaRegistryRef: string;
  scanPaths: string[];
  autoPromptCombinations?: boolean;
}

export interface Skill {
  skillId: string;
  name?: string;
  type?: string;
  description?: string;
}

export interface SkillBatch {
  batchId: string;
  userId: string;
  sourceRepo: string;
  generatedAt: string;
  knownSkills: Skill[];
  proposedSkills: Skill[];
  similarity: Array<{
    sourceSkillId: string;
    targetSkillId: string;
    score: number;
    reason: string;
  }>;
}
