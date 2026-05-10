---
id: addy-osmani/test-driven-development
name: Test-Driven Development
contributor: addy-osmani
origin: true
genericSkillRef: test-driven-development
status: named
title: "The Red-Green Oath"
catalogRef: addy-osmani-test-driven-development
level: "2★"
description: Forces the AI agent to follow a strict red-green-refactor TDD workflow — writing failing tests before any implementation code, blocking code generation that skips the test step, and enforcing coverage thresholds before completing a task.
links:
  github: https://github.com/addyosmani/agent-skills/blob/main/skills/test-driven-development/SKILL.md
tags:
  - tdd
  - testing
  - red-green-refactor
  - workflow-enforcement
  - software-quality
createdAt: "2026-04-30"
updatedAt: "2026-04-30"
---

## Overview

TDD by Addy Osmani is a workflow-enforcement skill that constrains the agent to the classic red-green-refactor cycle. Before writing any implementation, the agent must write a failing test that specifies the desired behavior. It is blocked from proceeding until the test exists and fails for the right reason — preventing the common failure mode where agents write code first and retrofit tests after.

## Origin

First published by @addyosmani (Addy Osmani). This is the origin implementation for the `test-driven-development` skill bucket.
