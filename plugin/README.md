# Gaia Plugin

The Gaia Plugin is a set of tools to integrate your local development environment and CI/CD pipelines with the Gaia Skill Registry.

## CLI Usage

The Gaia CLI provides commands to manage your skill tree directly from your repository.

### Commands

- `gaia init`: Initializes `.gaia/config.json` in the current repo. Prompts for GitHub username and scan paths.
- `gaia scan`: Scans repo for skill references, resolves them against the Gaia registry, and identifies new skills or combination candidates.
- `gaia status`: Displays a summary of your current skill tree.
- `gaia tree`: Renders your skill tree (use `--depth N` for limited views).
- `gaia load [username]`: Fetches and caches a user's skill tree.
- `gaia fuse [skillId]`: Confirms a pending combination and opens a PR to update your skill tree in the registry.
- `gaia diff`: Shows skills detected in the current scan that are not yet in your skill tree.

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

## Installation

Currently, the plugin is in early access. You can run it directly from the Gaia repository or use the GitHub Action.

```bash
# Clone the gaia registry
git clone https://github.com/gaia-registry/gaia.git

# Run the CLI
python gaia/plugin/cli/main.py --help
```
