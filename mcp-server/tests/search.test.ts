import { describe, it, expect } from "vitest";
import { searchSkills, findSkillById } from "../src/graph/search.js";
import type { GaiaGraph } from "../src/graph/types.js";

const mockGraph: GaiaGraph = {
  version: "0.2.0",
  generatedAt: "2026-04-28",
  meta: { typeLabels: {}, levelLabels: {}, rarityLabels: {} },
  skills: [
    { id: "web-search", name: "Web Search", type: "atomic", level: "II", rarity: "common", description: "Searches the web", prerequisites: [], derivatives: [], conditions: "", evidence: [], knownAgents: [], status: "validated", createdAt: "", updatedAt: "", version: "0.1.0" },
    { id: "web-scrape", name: "Web Scrape", type: "composite", level: "III", rarity: "uncommon", description: "Scrapes websites for data", prerequisites: ["web-search"], derivatives: [], conditions: "", evidence: [], knownAgents: [], status: "validated", createdAt: "", updatedAt: "", version: "0.1.0" },
    { id: "code-generation", name: "Code Generation", type: "atomic", level: "III", rarity: "common", description: "Generates source code", prerequisites: [], derivatives: [], conditions: "", evidence: [], knownAgents: [], status: "validated", createdAt: "", updatedAt: "", version: "0.1.0" },
  ],
  edges: [],
};

describe("search", () => {
  it("finds exact match by ID", () => {
    const results = searchSkills(mockGraph, "web-search");
    expect(results).toHaveLength(1);
    expect(results[0].id).toBe("web-search");
  });

  it("finds exact match by name (case-insensitive)", () => {
    const results = searchSkills(mockGraph, "Web Search");
    expect(results).toHaveLength(1);
    expect(results[0].id).toBe("web-search");
  });

  it("fuzzy matches similar terms", () => {
    const results = searchSkills(mockGraph, "web scraping");
    expect(results.length).toBeGreaterThan(0);
    expect(results[0].id).toBe("web-scrape");
  });

  it("returns empty for completely unrelated query", () => {
    const results = searchSkills(mockGraph, "zzzzzzzzz");
    expect(results).toHaveLength(0);
  });
});

describe("findSkillById", () => {
  it("returns skill for valid ID", () => {
    const skill = findSkillById(mockGraph, "code-generation");
    expect(skill).toBeDefined();
    expect(skill!.name).toBe("Code Generation");
  });

  it("returns undefined for invalid ID", () => {
    expect(findSkillById(mockGraph, "nonexistent")).toBeUndefined();
  });
});
