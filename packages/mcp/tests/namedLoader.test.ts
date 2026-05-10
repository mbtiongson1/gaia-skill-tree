import { describe, it, expect, beforeEach, afterEach } from "vitest";
import { writeFileSync, mkdirSync, rmSync, existsSync } from "node:fs";
import { join } from "node:path";
import { tmpdir } from "node:os";
import {
  loadNamedIndex,
  getNamedSkillsForGeneric,
  searchNamedSkills,
  getAllNamedSkills,
  invalidateCache,
} from "../src/graph/namedLoader.js";
import type { NamedSkill, NamedIndex } from "../src/graph/types.js";

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

const TEST_SKILL_A: NamedSkill = {
  id: "karpathy/autoresearch",
  name: "AutoResearch",
  contributor: "karpathy",
  origin: true,
  genericSkillRef: "autonomous-research-agent",
  status: "named",
  level: "2★",
  description: "Autonomous research agent that synthesizes academic papers.",
  tags: ["research", "autonomous", "paper-synthesis"],
  createdAt: "2026-04-29",
  updatedAt: "2026-04-29",
};

const TEST_SKILL_B: NamedSkill = {
  id: "devin-ai/autonomous-swe",
  name: "Autonomous SWE",
  contributor: "devin-ai",
  origin: true,
  genericSkillRef: "autonomous-debug",
  status: "named",
  level: "3★",
  description: "Autonomous software engineering agent for end-to-end debugging.",
  tags: ["software-engineering", "autonomous", "debugging"],
  createdAt: "2026-04-29",
  updatedAt: "2026-04-29",
};

const TEST_INDEX: NamedIndex = {
  generatedAt: "2026-04-29",
  buckets: {
    "autonomous-research-agent": [TEST_SKILL_A],
    "autonomous-debug": [TEST_SKILL_B],
  },
};

function makeTempIndex(): { dir: string; indexPath: string } {
  const dir = join(tmpdir(), `gaia-test-${Date.now()}-${Math.random().toString(36).slice(2)}`);
  mkdirSync(dir, { recursive: true });
  const indexPath = join(dir, "index.json");
  writeFileSync(indexPath, JSON.stringify(TEST_INDEX, null, 2), "utf-8");
  return { dir, indexPath };
}

// ---------------------------------------------------------------------------
// Tests
// ---------------------------------------------------------------------------

describe("namedLoader", () => {
  let tempDir: string;
  let indexPath: string;

  beforeEach(() => {
    // Reset cache before each test so tests are independent
    invalidateCache();
    const tmp = makeTempIndex();
    tempDir = tmp.dir;
    indexPath = tmp.indexPath;
  });

  afterEach(() => {
    invalidateCache();
    if (existsSync(tempDir)) {
      rmSync(tempDir, { recursive: true, force: true });
    }
  });

  // -------------------------------------------------------------------------
  // loadNamedIndex
  // -------------------------------------------------------------------------

  describe("loadNamedIndex", () => {
    it("returns correct structure from a valid index file", () => {
      const index = loadNamedIndex(indexPath);
      expect(index.generatedAt).toBe("2026-04-29");
      expect(Object.keys(index.buckets)).toHaveLength(2);
    });

    it("returns empty index when file does not exist", () => {
      const index = loadNamedIndex("/nonexistent/path/index.json");
      expect(index.generatedAt).toBe("");
      expect(index.buckets).toEqual({});
    });

    it("caches the result on subsequent calls", () => {
      const index1 = loadNamedIndex(indexPath);
      const index2 = loadNamedIndex(indexPath);
      // Same object reference due to cache
      expect(index1).toBe(index2);
    });

    it("contains the expected bucket keys", () => {
      const index = loadNamedIndex(indexPath);
      expect("autonomous-research-agent" in index.buckets).toBe(true);
      expect("autonomous-debug" in index.buckets).toBe(true);
    });
  });

  // -------------------------------------------------------------------------
  // getNamedSkillsForGeneric
  // -------------------------------------------------------------------------

  describe("getNamedSkillsForGeneric", () => {
    it("returns skills for a known bucket", () => {
      const skills = getNamedSkillsForGeneric("autonomous-research-agent", indexPath);
      expect(skills).toHaveLength(1);
      expect(skills[0].id).toBe("karpathy/autoresearch");
    });

    it("returns skills for another known bucket", () => {
      const skills = getNamedSkillsForGeneric("autonomous-debug", indexPath);
      expect(skills).toHaveLength(1);
      expect(skills[0].id).toBe("devin-ai/autonomous-swe");
    });

    it("returns empty array for an unknown bucket", () => {
      const skills = getNamedSkillsForGeneric("web-search", indexPath);
      expect(skills).toHaveLength(0);
    });

    it("returns empty array for an empty string key", () => {
      const skills = getNamedSkillsForGeneric("", indexPath);
      expect(skills).toHaveLength(0);
    });

    it("returns named skill with correct fields", () => {
      const [skill] = getNamedSkillsForGeneric("autonomous-research-agent", indexPath);
      expect(skill.contributor).toBe("karpathy");
      expect(skill.origin).toBe(true);
      expect(skill.level).toBe("2★");
      expect(skill.status).toBe("named");
    });
  });

  // -------------------------------------------------------------------------
  // searchNamedSkills
  // -------------------------------------------------------------------------

  describe("searchNamedSkills", () => {
    it("finds a skill by exact name (case-insensitive)", () => {
      const results = searchNamedSkills("AutoResearch", indexPath);
      expect(results.some((s) => s.id === "karpathy/autoresearch")).toBe(true);
    });

    it("finds a skill by partial description match", () => {
      const results = searchNamedSkills("academic papers", indexPath);
      expect(results.some((s) => s.id === "karpathy/autoresearch")).toBe(true);
    });

    it("finds a skill by tag", () => {
      const results = searchNamedSkills("debugging", indexPath);
      expect(results.some((s) => s.id === "devin-ai/autonomous-swe")).toBe(true);
    });

    it("finds a skill by contributor/id substring", () => {
      const results = searchNamedSkills("devin-ai", indexPath);
      expect(results.some((s) => s.id === "devin-ai/autonomous-swe")).toBe(true);
    });

    it("returns empty array for unrelated query", () => {
      const results = searchNamedSkills("zzzznotarealthing", indexPath);
      expect(results).toHaveLength(0);
    });

    it("finds multiple skills when query matches several", () => {
      // Both skills have 'autonomous' in description/tags/name
      const results = searchNamedSkills("autonomous", indexPath);
      expect(results.length).toBeGreaterThanOrEqual(2);
    });
  });

  // -------------------------------------------------------------------------
  // getAllNamedSkills
  // -------------------------------------------------------------------------

  describe("getAllNamedSkills", () => {
    it("returns all skills across all buckets", () => {
      const skills = getAllNamedSkills(indexPath);
      expect(skills).toHaveLength(2);
    });

    it("result contains skills from different buckets", () => {
      const skills = getAllNamedSkills(indexPath);
      const ids = skills.map((s) => s.id);
      expect(ids).toContain("karpathy/autoresearch");
      expect(ids).toContain("devin-ai/autonomous-swe");
    });

    it("returns empty array when no buckets exist", () => {
      const emptyIndex: NamedIndex = { generatedAt: "2026-04-29", buckets: {} };
      const emptyDir = join(tmpdir(), `gaia-empty-${Date.now()}`);
      mkdirSync(emptyDir, { recursive: true });
      const emptyPath = join(emptyDir, "index.json");
      writeFileSync(emptyPath, JSON.stringify(emptyIndex), "utf-8");

      invalidateCache();
      const skills = getAllNamedSkills(emptyPath);
      expect(skills).toHaveLength(0);

      rmSync(emptyDir, { recursive: true, force: true });
    });
  });

  // -------------------------------------------------------------------------
  // invalidateCache
  // -------------------------------------------------------------------------

  describe("invalidateCache", () => {
    it("forces a fresh load after cache invalidation", () => {
      // Load once to populate cache
      const index1 = loadNamedIndex(indexPath);
      invalidateCache();

      // Write a modified index to the same file
      const modifiedIndex: NamedIndex = {
        generatedAt: "2026-05-01",
        buckets: {
          "web-search": [
            {
              id: "user/web-skill",
              name: "Web Skill",
              contributor: "user",
              origin: true,
              genericSkillRef: "web-search",
              status: "named",
              level: "2★",
              description: "A web search skill.",
              createdAt: "2026-05-01",
              updatedAt: "2026-05-01",
            },
          ],
        },
      };
      writeFileSync(indexPath, JSON.stringify(modifiedIndex), "utf-8");

      const index2 = loadNamedIndex(indexPath);
      // Should have loaded the new data
      expect(index2.generatedAt).toBe("2026-05-01");
      expect(index1.generatedAt).toBe("2026-04-29");
      // Should not be the same cached object
      expect(index1).not.toBe(index2);
    });

    it("can be called multiple times without error", () => {
      invalidateCache();
      invalidateCache();
      invalidateCache();
      // Should still work after multiple invalidations
      const index = loadNamedIndex(indexPath);
      expect(index.generatedAt).toBe("2026-04-29");
    });
  });
});
