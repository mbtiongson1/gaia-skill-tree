# @gaia-registry/mcp-server

MCP server for the Gaia Skill Registry — agent-native skill detection, fusion, and progression.

## Installation

Add to your MCP configuration (Claude Code, Cursor, VS Code, etc.):

```json
{
  "mcpServers": {
    "gaia": {
      "command": "npx",
      "args": ["@gaia-registry/mcp-server"],
      "env": { "GAIA_USER": "your-github-username" }
    }
  }
}
```

## Tools

| Tool | Description |
|------|-------------|
| `gaia_lookup` | Look up a skill by ID or fuzzy name. Returns metadata, prerequisites, derivatives, evidence. |
| `gaia_suggest` | Get fusion recommendations based on your context — connected tools and project signals. |
| `gaia_scan_context` | Detect skills from connected MCP tools and project descriptions. Identifies fusion opportunities and novel capabilities. |
| `gaia_my_tree` | Show your skill tree — unlocked skills, pending fusions, stats. |
| `gaia_propose` | Claim a fusion or propose a novel skill to the registry. Opens a PR on GitHub. |

## Resources

| URI | Description |
|-----|-------------|
| `gaia://registry` | Full skill graph (all skills with types, levels, rarities, prerequisites) |
| `gaia://tree/{username}` | A user's skill tree |

## Configuration

The server reads identity from (in priority order):

1. `GAIA_USER` environment variable
2. `.gaia/config.json` in the current working directory
3. `~/.gaia/config.json` (global)

For `gaia_propose`, set `GITHUB_TOKEN` or `GH_TOKEN` to enable PR creation.

## How It Works

1. The server fetches `gaia.json` from the registry on GitHub (cached locally with ETag)
2. When you call `gaia_suggest` or `gaia_scan_context`, it maps your connected MCP tools to Gaia skill IDs
3. It checks if your detected skills satisfy prerequisites for any composite/legendary skill
4. If a fusion is available, it tells you — and `gaia_propose` can claim it by opening a PR

## Development

```bash
cd mcp-server
npm install
npm run build    # Compile TypeScript
npm test         # Run tests (vitest)
npm run dev      # Watch mode
```

## Architecture

```
src/
├── index.ts              ← Server setup, tool/resource registration
├── graph/                ← Registry data layer (loader, types, search, DAG)
├── tools/                ← MCP tool handlers (lookup, suggest, propose, etc.)
├── advisor/              ← Skill detection engine (fusion, detector, novelty)
├── config/               ← Identity resolution, ETag cache
├── resources/            ← MCP resource handlers
└── utils/                ← GitHub API helpers
```
