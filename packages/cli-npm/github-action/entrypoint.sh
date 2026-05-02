#!/bin/bash
set -e

echo "Starting Gaia Skill Scanner..."

# Ensure we are in a git repo
if [ ! -d ".git" ]; then
  echo "❌ Error: Not a git repository."
  exit 1
fi

# Run the scanner
python3 -m gaia_cli.main scan

echo "Scan complete."
