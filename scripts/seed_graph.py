#!/usr/bin/env python3
"""Seed graph generator for Gaia Skill Registry.

Produces graph/gaia.json with the canonical seed taxonomy:
- 25 atomic skills
- 8 composite skills
- 3 legendary stubs (Level I, provisional)

Run: python scripts/seed_graph.py
"""

import json
import os
from datetime import date

TODAY = "2026-04-26"
VERSION = "0.1.0"

def atomic(id_, name, desc, derivatives=None, level="II", rarity="common", evidence_class="C"):
    """Create an atomic skill node."""
    ev = []
    if level != "I":
        ev = [{
            "class": evidence_class,
            "source": f"https://github.com/gaia-registry/gaia/blob/main/docs/evidence/{id_}.md",
            "evaluator": "mbtiongson1",
            "date": TODAY,
            "notes": f"Seed evidence for {name}."
        }]
    return {
        "id": id_,
        "name": name,
        "type": "atomic",
        "level": level,
        "rarity": rarity,
        "description": desc,
        "prerequisites": [],
        "derivatives": derivatives or [],
        "conditions": "",
        "evidence": ev,
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    }

def composite(id_, name, desc, prereqs, derivatives=None, level="III", rarity="uncommon",
              evidence_class="B", conditions=""):
    """Create a composite skill node."""
    return {
        "id": id_,
        "name": name,
        "type": "composite",
        "level": level,
        "rarity": rarity,
        "description": desc,
        "prerequisites": prereqs,
        "derivatives": derivatives or [],
        "conditions": conditions,
        "evidence": [{
            "class": evidence_class,
            "source": f"https://github.com/gaia-registry/gaia/blob/main/docs/evidence/{id_}.md",
            "evaluator": "mbtiongson1",
            "date": TODAY,
            "notes": f"Seed evidence for {name}."
        }],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    }

def legendary_stub(id_, name, desc, prereqs):
    """Create a legendary stub (Level I, provisional, no evidence)."""
    return {
        "id": id_,
        "name": name,
        "type": "legendary",
        "level": "I",
        "rarity": "legendary",
        "description": desc,
        "prerequisites": prereqs,
        "derivatives": [],
        "conditions": "Requires extensive multi-system validation before level advancement.",
        "evidence": [],
        "knownAgents": [],
        "status": "provisional",
        "createdAt": TODAY,
        "updatedAt": TODAY,
        "version": VERSION,
    }

def build_edges(skills):
    """Generate edge records from skill prerequisite relationships."""
    edges = []
    for s in skills:
        for prereq in s["prerequisites"]:
            edges.append({
                "sourceSkillId": prereq,
                "targetSkillId": s["id"],
                "edgeType": "prerequisite",
                "condition": s.get("conditions", ""),
                "levelFloor": "II",
                "evidenceRefs": [f"{s['id']}#evidence[0]"] if s["evidence"] else []
            })
    return edges

def main():
    # === ATOMIC LAYER (25 skills) ===
    atomics = [
        atomic("tokenize", "Tokenize",
               "Splits input text into discrete tokens suitable for downstream processing by language models.",
               derivatives=["rag-pipeline"]),
        atomic("classify", "Classify",
               "Assigns one or more categorical labels to an input based on learned or rule-based criteria.",
               derivatives=["route-intent"]),
        atomic("retrieve", "Retrieve",
               "Fetches relevant documents or passages from an indexed corpus given a query.",
               derivatives=["rag-pipeline"]),
        atomic("rank", "Rank",
               "Orders a set of candidate items by relevance, quality, or fitness for a given objective.",
               derivatives=["rag-pipeline"]),
        atomic("parse-json", "Parse JSON",
               "Extracts structured data from JSON-formatted input, handling nested objects and arrays.",
               derivatives=["document-analyst"]),
        atomic("parse-html", "Parse HTML",
               "Extracts structured content from raw HTML, navigating DOM trees and handling malformed markup.",
               derivatives=["web-scrape"]),
        atomic("execute-bash", "Execute Bash",
               "Runs shell commands in a sandboxed environment, captures stdout/stderr, and handles exit codes.",
               derivatives=["autonomous-debug"]),
        atomic("generate-text", "Generate Text",
               "Produces coherent natural language output given a prompt, instruction, or context window.",
               derivatives=["ghostwrite"]),
        atomic("summarize", "Summarize",
               "Condenses longer input into a shorter representation that preserves key information and intent.",
               derivatives=["research", "document-analyst"]),
        atomic("cite-sources", "Cite Sources",
               "Attributes claims to specific sources with proper references, URLs, or bibliographic entries.",
               derivatives=["research"]),
        atomic("extract-entities", "Extract Entities",
               "Identifies and extracts named entities such as people, organizations, dates, and locations from text.",
               derivatives=["web-scrape", "knowledge-harvest", "document-analyst"]),
        atomic("route-intent", "Route Intent",
               "Classifies user intent and directs execution to the appropriate handler, tool, or sub-agent.",
               derivatives=["plan-and-execute"]),
        atomic("evaluate-output", "Evaluate Output",
               "Assesses the quality, correctness, or safety of generated output against defined criteria.",
               derivatives=[]),
        atomic("embed-text", "Embed Text",
               "Converts text into dense vector representations suitable for similarity search and clustering.",
               derivatives=["rag-pipeline", "knowledge-harvest"]),
        atomic("chunk-document", "Chunk Document",
               "Splits a document into semantically meaningful segments optimized for embedding and retrieval.",
               derivatives=["rag-pipeline"]),
        atomic("plan-decompose", "Plan and Decompose",
               "Breaks a complex objective into an ordered sequence of executable sub-tasks.",
               derivatives=["plan-and-execute"]),
        atomic("write-report", "Write Report",
               "Produces structured, multi-section written output with headings, citations, and coherent narrative.",
               derivatives=["ghostwrite"]),
        atomic("audience-model", "Audience Model",
               "Adapts tone, complexity, and framing of output to match a target audience profile.",
               derivatives=["ghostwrite"]),
        atomic("tool-select", "Tool Select",
               "Chooses the most appropriate tool or API from a set of available options given a task description.",
               derivatives=["plan-and-execute"]),
        atomic("error-interpretation", "Error Interpretation",
               "Diagnoses error messages, stack traces, and failure modes to identify root causes and suggest fixes.",
               derivatives=["autonomous-debug"]),
        atomic("code-generation", "Code Generation",
               "Produces syntactically correct and functionally appropriate source code from specifications or prompts.",
               derivatives=["autonomous-debug"]),
        atomic("web-search", "Web Search",
               "Queries external search engines or APIs and retrieves relevant result sets.",
               derivatives=["web-scrape", "research"]),
        atomic("score-relevance", "Score Relevance",
               "Assigns a numerical relevance score to candidate items relative to a query or objective.",
               derivatives=["rag-pipeline"]),
        atomic("format-output", "Format Output",
               "Structures raw output into a specified format such as markdown, JSON, CSV, or HTML.",
               derivatives=["document-analyst"]),
        atomic("diff-content", "Diff Content",
               "Compares two versions of content and produces a structured delta highlighting additions, deletions, and modifications.",
               derivatives=[]),
    ]

    # === COMPOSITE LAYER (8 skills) ===
    composites = [
        composite("web-scrape", "Web Scrape",
                  "Retrieves and structures data from web pages into usable entities.",
                  ["web-search", "parse-html", "extract-entities"],
                  derivatives=["knowledge-harvest"],
                  conditions="Structured output mode required."),
        composite("research", "Research",
                  "Conducts multi-source information gathering, synthesis, and citation for a given topic.",
                  ["web-search", "summarize", "cite-sources"],
                  derivatives=["ghostwrite"]),
        composite("ghostwrite", "Ghostwrite",
                  "Produces audience-tailored, research-backed long-form written content.",
                  ["research", "write-report", "audience-model"],
                  level="IV", rarity="rare",
                  conditions="Requires research output as input context."),
        composite("autonomous-debug", "Autonomous Debug",
                  "Independently identifies, diagnoses, and fixes software bugs through code generation and execution.",
                  ["code-generation", "execute-bash", "error-interpretation"],
                  rarity="rare"),
        composite("plan-and-execute", "Plan and Execute",
                  "Decomposes complex objectives into sub-tasks, selects tools, and orchestrates execution.",
                  ["route-intent", "plan-decompose", "tool-select"],
                  rarity="rare"),
        composite("knowledge-harvest", "Knowledge Harvest",
                  "Extracts, structures, and embeds knowledge from web sources into a searchable corpus.",
                  ["web-scrape", "extract-entities", "embed-text"],
                  level="IV", rarity="rare"),
        composite("rag-pipeline", "RAG Pipeline",
                  "End-to-end retrieval-augmented generation combining document chunking, embedding, retrieval, and relevance scoring.",
                  ["retrieve", "chunk-document", "embed-text", "score-relevance"],
                  rarity="uncommon"),
        composite("document-analyst", "Document Analyst",
                  "Parses, extracts entities from, summarizes, and formats structured documents.",
                  ["parse-json", "extract-entities", "summarize", "format-output"],
                  rarity="uncommon"),
    ]

    # === LEGENDARY STUBS (3 skills) ===
    legendaries = [
        legendary_stub("recursive-self-improvement", "Recursive Self-Improvement",
                        "Agent iteratively refines its own prompts, tools, or strategies based on performance feedback loops.",
                        ["autonomous-debug", "evaluate-output", "plan-and-execute"]),
        legendary_stub("multi-agent-orchestration-v", "Multi-Agent Orchestration V",
                        "Coordinates multiple specialized agents across complex workflows with dynamic task allocation and conflict resolution.",
                        ["plan-and-execute", "route-intent", "tool-select"]),
        legendary_stub("autonomous-research-agent", "Autonomous Research Agent",
                        "Independently conducts end-to-end research cycles including hypothesis generation, evidence gathering, synthesis, and reporting.",
                        ["research", "knowledge-harvest", "ghostwrite"]),
    ]

    all_skills = atomics + composites + legendaries

    # Build edges from prerequisites
    edges = build_edges(all_skills)

    # Assemble canonical graph
    graph = {
        "$schema": "./schema/skill.schema.json",
        "version": VERSION,
        "generatedAt": f"{TODAY}T00:00:00Z",
        "skills": all_skills,
        "edges": edges,
    }

    # Write to graph/gaia.json
    out_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "graph", "gaia.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(graph, f, indent=2)
    
    print(f"✅ Wrote {len(atomics)} atomics, {len(composites)} composites, {len(legendaries)} legendaries")
    print(f"   Total skills: {len(all_skills)}")
    print(f"   Total edges: {len(edges)}")
    print(f"   Output: {out_path}")

if __name__ == "__main__":
    main()
