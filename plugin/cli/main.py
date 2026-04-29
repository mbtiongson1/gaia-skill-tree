import argparse
import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

try:
    from plugin.cli.scanner import scan_repo, load_config
    from plugin.cli.resolver import resolve_skills
    from plugin.cli.combinator import get_combinations
    from plugin.cli.treeManager import load_tree, save_tree, show_status, show_tree
    from plugin.cli.prWriter import open_pr, open_intake_pr
    from plugin.cli.push import build_skill_batch, write_skill_batch
except ModuleNotFoundError:
    from cli.scanner import scan_repo, load_config
    from cli.resolver import resolve_skills
    from cli.combinator import get_combinations
    from cli.treeManager import load_tree, save_tree, show_status, show_tree
    from cli.prWriter import open_pr, open_intake_pr
    from cli.push import build_skill_batch, write_skill_batch

def init_command(args):
    config_dir = '.gaia'
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, 'config.json')
    if os.path.exists(config_path):
        print("Gaia is already initialized in this repository.")
        return
    config = {
        "gaiaUser": "gaiabot",
        "gaiaRegistryRef": "https://github.com/gaia-registry/gaia",
        "scanPaths": ["scripts", "plugin"],
        "autoPromptCombinations": False
    }
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=2)
    print(f"Initialized Gaia configuration at {config_path}")

def scan_command(args):
    config = load_config()
    if not config:
        print("Gaia not initialized. Run `gaia init` first.")
        return
    print("Scanning repository...")
    raw_tokens = scan_repo()
    resolved = resolve_skills(raw_tokens, registry_path=os.path.join(args.registry, 'graph/gaia.json'))
    print(f"Found {len(resolved)} skills referenced in the repository.")
    if resolved:
        print(", ".join(resolved))
    username = config.get('gaiaUser')
    tree = load_tree(username, registry_path=args.registry)
    if tree:
        with open(os.path.join(args.registry, 'graph/gaia.json'), 'r') as f:
            graph_data = json.load(f)
        unlocked = [s.get('skillId') for s in tree.get('unlockedSkills', [])]
        combos = get_combinations(graph_data, unlocked, resolved)
        if combos:
            print("\nNew combination candidates detected:")
            for c in combos:
                print(f"- {c['candidateResult']} (Requires: {', '.join(c['detectedSkills'])})")
            print("Run `gaia fuse [skillId]` to confirm and add to your tree.")

def status_command(args):
    config = load_config()
    if not config:
        print("Gaia not initialized.")
        return
    tree = load_tree(config.get('gaiaUser'), registry_path=args.registry)
    show_status(tree)

def tree_command(args):
    config = load_config()
    if not config:
        print("Gaia not initialized.")
        return
    tree = load_tree(config.get('gaiaUser'), registry_path=args.registry)
    show_tree(tree)

def fuse_command(args):
    config = load_config()
    if not config:
        return
    username = config.get('gaiaUser')
    tree = load_tree(username, registry_path=args.registry)
    if not tree:
        return
    pending = tree.get('pendingCombinations', [])
    target = args.skillId
    match = next((p for p in pending if p.get('candidateResult') == target), None)
    if not match:
        print(f"Skill {target} is not in your pending combinations.")
        return
    print(f"Fusing {target}...")
    tree.setdefault('unlockedSkills', []).append({
        "skillId": target,
        "level": match.get('levelFloor'),
        "unlockedAt": "2026-04-26",
        "unlockedIn": "local-repo",
        "combinedFrom": match.get('detectedSkills', [])
    })
    tree['pendingCombinations'] = [p for p in pending if p.get('candidateResult') != target]
    stats = tree.get('stats', {})
    stats['totalUnlocked'] = stats.get('totalUnlocked', 0) + 1
    tree['stats'] = stats
    save_tree(username, tree, registry_path=args.registry)
    open_pr(username, tree, candidate_result=target)

def push_command(args):
    config = load_config()
    if not config:
        print("Gaia not initialized. Run `gaia init` first.", file=sys.stderr)
        sys.exit(1)

    raw_tokens = scan_repo()
    batch = build_skill_batch(raw_tokens, config, args.registry)

    if args.dry_run:
        print(json.dumps(batch, indent=2))
        return

    batch_path = write_skill_batch(batch, args.registry)
    print(f"Wrote skill batch intake record: {batch_path}")
    if args.no_pr:
        print("Skipped PR creation (--no-pr).")
        return
    open_intake_pr(config.get('gaiaUser'), batch, batch_path=batch_path)

def main():
    parser = argparse.ArgumentParser(prog="gaia", description="Gaia Plugin CLI")
    parser.add_argument('--registry', default=".", help="Path to local Gaia registry clone for testing")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.add_parser('init')
    subparsers.add_parser('scan')
    subparsers.add_parser('status')
    subparsers.add_parser('tree')
    fuse_parser = subparsers.add_parser('fuse')
    fuse_parser.add_argument('skillId', help="ID of the pending skill to fuse")
    push_parser = subparsers.add_parser('push')
    push_parser.add_argument('--dry-run', action='store_true', help="Print the skill batch without writing it")
    push_parser.add_argument('--no-pr', action='store_true', help="Write intake record without creating a PR")
    args = parser.parse_args()
    if args.command == 'init':
        init_command(args)
    elif args.command == 'scan':
        scan_command(args)
    elif args.command == 'status':
        status_command(args)
    elif args.command == 'tree':
        tree_command(args)
    elif args.command == 'fuse':
        fuse_command(args)
    elif args.command == 'push':
        push_command(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
