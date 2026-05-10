---
id: mattpocock/tdd
name: TDD
contributor: mattpocock
origin: false
genericSkillRef: test-driven-development
status: named
title: "Vertical-Slice TDD"
catalogRef: mattpocock-tdd
level: "3★"
description: Enforces strict vertical-slice TDD — one test then one implementation at a time — explicitly blocking horizontal slicing (all tests first, then all code). Tests verify behaviour through public interfaces only; mocking internal collaborators is treated as an anti-pattern.
links:
  github: https://github.com/mattpocock/skills/blob/main/skills/engineering/tdd/SKILL.md
tags:
  - tdd
  - red-green-refactor
  - vertical-slicing
  - tracer-bullet
  - public-interface-testing
createdAt: "2026-04-30"
updatedAt: "2026-04-30"
---

## Overview

Matt Pocock's TDD skill distinguishes itself from generic TDD by making the vertical-slice constraint explicit and enforced. The agent is explicitly blocked from the "horizontal slicing" anti-pattern (writing all tests first, then all code), which produces tests that verify imagined behaviour and become insensitive to real changes. Each cycle follows a tracer-bullet model: one failing test → minimal code to pass → repeat, never anticipating future tests.

Tests must be written against public interfaces only and must survive internal refactors. The skill includes checklists per RED→GREEN cycle and a separate REFACTOR phase that only activates after all current tests are green.

## Origin

Second named implementation of the `test-driven-development` skill bucket (origin: addy-osmani). Matt Pocock's version adds the explicit anti-horizontal-slicing constraint and the interface-stability rule.
