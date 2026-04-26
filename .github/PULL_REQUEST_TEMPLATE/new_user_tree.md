## New User Skill Tree

### User Details
- **GitHub Username:** `username`
- **Directory:** `users/username/`

### Initial Skills
List the skills you are claiming with evidence of detection:

| Skill ID | Level | Detected In (repo) | Date |
|---|---|---|---|
| `skillId` | II | `username/repo-name` | YYYY-MM-DD |

### Checklist

**Contributor:**
- [ ] `skill-tree.json` validates against `schema/skillTree.schema.json`.
- [ ] GitHub username matches the PR author.
- [ ] All claimed skill IDs exist in `gaia.json`.
- [ ] Stats fields (`totalUnlocked`, `highestRarity`, `deepestLineage`) are accurate.
- [ ] I have run `python scripts/validate.py` locally and it passes.

**Reviewer:**
- [ ] Username matches verified PR author identity.
- [ ] All skill IDs reference valid entries in the registry.
- [ ] Stats are consistent with the unlocked skills list.
- [ ] JSON validates against schema.
