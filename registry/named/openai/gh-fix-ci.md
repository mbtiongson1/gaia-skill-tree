---
id: openai/gh-fix-ci
name: GH Fix CI
contributor: openai
origin: false
genericSkillRef: error-interpretation
status: named
title: "The Checkrunner Surgeon"
catalogRef: openai-gh-fix-ci
level: II
description: Debugs failing GitHub Actions checks on pull requests using GitHub CLI evidence, logs, and focused remediation steps.
links:
  docs: https://officialskills.sh/openai/skills/gh-fix-ci
tags:
  - github-actions
  - ci
  - debugging
  - pull-requests
createdAt: "2026-05-01"
updatedAt: "2026-05-01"
---

## Overview

GH Fix CI is a pull-request repair workflow for turning GitHub Actions logs into concrete fixes. It inspects failed checks, narrows root causes, patches the branch, and reruns or summarizes verification.

## Notes

Curated from the OpenAI official skills index surfaced by PR 108.
