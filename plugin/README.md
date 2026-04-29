# Gaia CLI

The Gaia CLI integrates local development repositories and CI pipelines with the Gaia Skill Registry.

> **Prefer the MCP server?** If you use Claude Code, Cursor, or any MCP-compatible agent, see [`mcp-server/`](../mcp-server/) for zero-config agent-native integration — no CLI needed.

## Installation

Install the Gaia CLI via npm:

```bash
npm install -g @gaia-registry/cli
# or locally
npm install @gaia-registry/cli
```

### Requirements

- **Node.js 18+** — for running the npm package
- **Python 3.8+** — the CLI shells out to Python for the core implementation

The npm wrapper automatically detects your Python installation and will provide instructions if Python is not found.

## CLI Usage

Run the Python CLI from a Gaia registry checkout:

```bash
python3 plugin/cli/main.py --help
```

From another project, pass the local registry checkout path:

```bash
python3 /path/to/gaia-skill-tree/plugin/cli/main.py \
  --registry /path/to/gaia-skill-tree \
  scan
```

If you have a shell wrapper named `gaia`, use the same commands directly:

```bash
gaia --registry /path/to/gaia-skill-tree scan
gaia --registry /path/to/gaia-skill-tree push --dry-run
gaia --registry /path/to/gaia-skill-tree push
```

### Commands

- `gaia init`: Initializes `.gaia/config.json` in the current repo. Prompts for GitHub username and scan paths.
- `gaia scan`: Scans repo for skill references, resolves them against the Gaia registry, and identifies new skills or combination candidates.
- `gaia push`: Submits a batch intake record with detected canonical skills, proposed new skills, and similarity hints.
- `gaia status`: Displays a summary of your current skill tree.
- `gaia tree`: Lists unlocked skills for your configured user.
- `gaia fuse [skillId]`: Confirms a pending combination and opens a PR to update your skill tree in the registry.

Preview a batch before writing it:

```bash
gaia push --dry-run
```

## GitHub Action

Integrate Gaia into your CI/CD to automatically detect skills on every push.

### Configuration

Add `.github/workflows/gaia.yml` to your repo:

```yaml
name: Gaia Skill Sync

on: [push]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: gaia-registry/gaia/plugin/github-action@main
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          username: 'your-github-username'
```

### Plugin Configuration (`.gaia/config.json`)

The plugin is configured via a `.gaia/config.json` file in your repository root:

```json
{
  "gaiaUser": "mbtiongson1",
  "gaiaRegistryRef": "main",
  "scanPaths": [
    "src/",
    "docs/",
    "tools/"
  ]
}
```

## Local Use

```bash
# Clone the Gaia registry
git clone https://github.com/gaia-registry/gaia.git

# In the project repo you want Gaia to scan
python3 /path/to/gaia/plugin/cli/main.py --registry /path/to/gaia init
python3 /path/to/gaia/plugin/cli/main.py --registry /path/to/gaia scan
python3 /path/to/gaia/plugin/cli/main.py --registry /path/to/gaia push --dry-run
```

The npm wrapper is in `src/bin/gaia.ts` and shells out to the Python CLI in `cli/main.py`.
