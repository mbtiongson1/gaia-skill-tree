---
id: mattpocock/grill-with-docs
name: Grill With Docs
contributor: mattpocock
origin: true
genericSkillRef: design-review
status: named
title: "The Domain-Aware Interrogator"
catalogRef: mattpocock-grill-with-docs
level: "3★"
description: Stress-tests a plan against the project's domain model by relentlessly questioning each design decision one at a time, surfacing language conflicts with CONTEXT.md, cross-referencing code contradictions, and crystallising decisions as inline CONTEXT.md updates and ADRs as they are resolved.
links:
  github: https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md
tags:
  - design-review
  - domain-model
  - ubiquitous-language
  - adr
  - context-md
  - socratic-method
createdAt: "2026-04-30"
updatedAt: "2026-04-30"
---

## Overview

Grill With Docs is the domain-aware variant of the design-grilling pattern. It begins by locating the project's CONTEXT.md and docs/adr/ (supporting both flat and CONTEXT-MAP.md multi-context repos), then conducts a relentless one-question-at-a-time interview.

During the session the agent actively challenges language: when the user uses a term that conflicts with the glossary it calls it out immediately. It cross-references code to catch contradictions between stated intent and actual behaviour. Decisions are written to CONTEXT.md in real time — not batched — using a strict format. ADRs are offered only when a decision is hard-to-reverse, surprising without context, and the result of a genuine trade-off; all three conditions must hold.

## Origin

First published by @mattpocock (Matt Pocock, Total TypeScript). This is the origin implementation for the `design-review` skill bucket.
