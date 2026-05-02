---
id: gaiabot/repo-docs-before-pr
name: Repo Docs Before PR
contributor: gaiabot
origin: false
genericSkillRef: write-report
status: awakened
level: II
description: Builds and validates repository documentation as a pre-PR guardrail by running the local docs pipeline (including stale-doc checks), then surfaces actionable diffs so pull requests do not fail CI on documentation freshness.
links:
  docs: https://github.com/mbtiongson1/gaia-skill-tree#docs
tags:
  - documentation
  - ci
  - pre-pr
  - quality-gate
  - repo-maintenance
createdAt: "2026-05-01"
updatedAt: "2026-05-01"
---

## Overview

Repo Docs Before PR is a repository hygiene skill that enforces docs freshness before opening a pull request. It runs the project's local docs build command, checks whether generated documentation is stale, and asks the agent to stage regenerated files as part of the same change set.

## Notes

This implementation targets repositories that expose a dedicated docs build command (for Gaia: `gaia docs build`), and is intended to prevent avoidable CI failures caused by stale generated docs.
