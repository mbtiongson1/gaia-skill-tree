---
id: upsonic/unittest-generator
name: Unittest Generator
contributor: upsonic
origin: true
genericSkillRef: generate-test
status: named
title: "The Test Weaver"
catalogRef: upsonic-unittest-generator
level: "2⭐"
description: Autonomous Claude agent that generates comprehensive unittest.TestCase suites from source code, organising tests into concept-based subfolders under a tests/ directory with proper imports, fixtures, and edge-case coverage.
links:
  github: https://github.com/Upsonic/Upsonic
tags:
  - unit-testing
  - unittest
  - test-generation
  - python
  - autonomous-agent
createdAt: "2026-04-30"
updatedAt: "2026-04-30"
---

## Overview

Unittest Generator is a Claude Code agent shipped with the Upsonic autonomous agent framework. Given a source module (e.g. `auth.py`), it analyses the code, identifies functions and classes, generates a complete `unittest.TestCase` suite, and writes it into a concept-organised `tests/` folder structure. It handles imports, mocking, and edge-case scenarios automatically.

## Key Capabilities

- **TestCase generation**: produces `unittest.TestCase` classes with `setUp`, `tearDown`, and individual test methods
- **Concept-based layout**: groups tests into subfolders that mirror the conceptual structure of the source
- **Edge-case coverage**: identifies boundary conditions and error paths from the source code
- **Autonomous**: runs without per-file prompting once triggered

## Origin

First published by @Upsonic as a prebuilt Claude Code agent. This is the origin implementation for the `generate-test` skill bucket.

Sourced from the SkillsMP marketplace entry for `summarization`/`unittest-generator` (Upsonic/Upsonic, 7 836 stars).
