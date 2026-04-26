# Gaia Governance

This document outlines how the Gaia Skill Registry is managed, how decisions are made, and how disputes are resolved.

## 1. Maintainer Roles

### 1.1 Taxonomy Maintainers
Taxonomy Maintainers are responsible for:
- Reviewing and merging skill submissions.
- Ensuring graph integrity (DAG correctness, reference validity).
- Verifying evidence quality against the Gaia Evidence Policy.
- Managing reclassifications and deprecations.

### 1.2 Plugin Maintainers
Plugin Maintainers are responsible for:
- Developing and maintaining the Gaia CLI and GitHub Action.
- Ensuring compatibility with various agent frameworks and repos.
- Optimizing scan performance and accuracy.

### 1.3 Core Maintainers
Core Maintainers have final approval authority and manage:
- Project vision and roadmap.
- Repository settings and branch protection.
- Dispute resolution.
- Legendary skill validation (requires two Core Maintainer approvals).

## 2. Decision Making

Decisions are made through Pull Requests. Most PRs require one Maintainer approval.
- **Atomic/Composite Skills**: 1 Maintainer approval.
- **Legendary Skills**: 2 Core Maintainer approvals.
- **Schema Changes**: 2 Core Maintainer approvals.

## 3. Dispute Resolution

If a skill's definition, level, or evidence is disputed:
1. A GitHub Issue is opened with the label `disputed`.
2. Both sides present evidence and rationale.
3. The skill status is set to `disputed` in `gaia.json`.
4. If no consensus is reached after 14 days, a Core Maintainer makes a final determination based on the **Evidence Hierarchy** (Class A > B > C).

## 4. Audit Schedule

### 4.1 Quarterly Re-Audit
Every 90 days, the maintainers will conduct a full re-audit of the registry to:
- Review `provisional` skills for potential validation.
- Re-assess `disputed` skills.
- Verify legendary status requirements.
- Identify stale skills (not updated or referenced in 180 days).

## 5. Release Cadence

### 5.1 Registry Snapshots
The registry is updated continuously as PRs are merged. Every month, a new version (e.g., `v1.1.0`) is tagged as a **Frontier Release**, including:
- A summary of all new skills.
- Updated rarity scores based on real user tree data.
- The **Frontier Report** (graph analytics and gaps).

## 6. Code of Conduct

All contributors and maintainers are expected to follow the project's Code of Conduct. We prioritize technical accuracy, evidence over opinion, and respectful debate.
