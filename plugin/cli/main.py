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
    from plugin.cli.embeddings import generate_embeddings
    from plugin.cli.semantic_search import search as semantic_search, load_embeddings
    from plugin.cli.name import find_awakened_skill, promote_to_named, update_batch_lifecycle
    from plugin.cli.install import install_skill, sync_skills, uninstall_skill, list_installed
except ModuleNotFoundError:
    from cli.scanner import scan_repo, load_config
    from cli.resolver import resolve_skills
    from cli.combinator import get_combinations
    from cli.treeManager import load_tree, save_tree, show_status, show_tree
    from cli.prWriter import open_pr, open_intake_pr
    from cli.push import build_skill_batch, write_skill_batch
    from cli.embeddings import generate_embeddings
    from cli.semantic_search import search as semantic_search, load_embeddings
    from cli.name import find_awakened_skill, promote_to_named, update_batch_lifecycle
    from cli.install import install_skill, sync_skills, uninstall_skill, list_installed

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

def embed_command(args):
    generate_embeddings(registry_path=args.registry)

def search_command(args):
    embeddings_path = os.path.join(args.registry, 'graph', 'embeddings.json')
    try:
        results = semantic_search(args.query, embeddings_path, top_k=args.top_k)
    except FileNotFoundError as e:
        print(str(e))
        return
    except ImportError as e:
        print(str(e))
        return
    if not results:
        print("No results found.")
        return
    col_id = max(len(r['id']) for r in results)
    col_id = max(col_id, 4)  # at least width of "Skill"
    header = f"{'Rank':<5}  {'Skill':<{col_id}}  {'Score'}"
    print(header)
    print("-" * len(header))
    for rank, r in enumerate(results, start=1):
        print(f"{rank:<5}  {r['id']:<{col_id}}  {r['score']:.4f}")

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
    open_intake_pr(config.get('gaiaUser'), batch, batch_path=batch_path, repo_root=args.registry)

def name_command(args):
    with open(args.batch_file, "r") as f:
        batch = json.load(f)

    proposed_skills = batch.get("proposedSkills", [])
    if args.skill_index < 0 or args.skill_index >= len(proposed_skills):
        print(
            f"Error: skill-index {args.skill_index} is out of range "
            f"(batch has {len(proposed_skills)} proposed skills).",
            file=sys.stderr,
        )
        sys.exit(1)

    skill_data = proposed_skills[args.skill_index]
    lifecycle = skill_data.get("lifecycle", "pending")
    if lifecycle not in ("pending", "awakened"):
        print(
            f"Error: skill '{skill_data['id']}' has lifecycle '{lifecycle}'. "
            "Only 'pending' or 'awakened' skills can be promoted to named.",
            file=sys.stderr,
        )
        sys.exit(1)

    parts = args.named_id.split("/", 1)
    if len(parts) != 2 or not parts[0] or not parts[1]:
        print(
            f"Error: named ID must be in the form 'contributor/skill-name', "
            f"got '{args.named_id}'.",
            file=sys.stderr,
        )
        sys.exit(1)
    contributor, skill_name = parts

    named_path = promote_to_named(skill_data, contributor, skill_name, args.registry)
    update_batch_lifecycle(args.batch_file, skill_data["id"], "named")
    print(f"Named skill created: {named_path}")
    print(f"Batch lifecycle updated: '{skill_data['id']}' -> named")

def install_command(args):
    if args.list:
        list_installed()
        return
    if not args.skill_id:
        print("Error: provide a skill ID (contributor/skill-name) or use --list.", file=sys.stderr)
        sys.exit(1)
    success = install_skill(args.skill_id, args.registry)
    if not success:
        sys.exit(1)


def sync_command(args):
    sync_skills(args.registry)


def uninstall_command(args):
    success = uninstall_skill(args.skill_id)
    if not success:
        sys.exit(1)


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
    subparsers.add_parser('embed')
    search_parser = subparsers.add_parser('search')
    search_parser.add_argument('query', help="Search query string")
    search_parser.add_argument('--top-k', type=int, default=10, help="Number of results to return (default: 10)")
    name_parser = subparsers.add_parser(
        'name',
        help="Promote an awakened skill to a named skill",
    )
    name_parser.add_argument('batch_file', help="Path to the intake batch JSON file")
    name_parser.add_argument('skill_index', type=int, help="0-based index of the proposed skill in the batch")
    name_parser.add_argument(
        'named_id',
        metavar='contributor/skill-name',
        help="Named skill ID to create (e.g. karpathy/autoresearch)",
    )
    install_parser = subparsers.add_parser('install', help="Install a named skill from the registry")
    install_parser.add_argument(
        'skill_id',
        nargs='?',
        default=None,
        help="Named skill ID to install (e.g. karpathy/autoresearch)",
    )
    install_parser.add_argument('--list', action='store_true', help="List all installed named skills")
    subparsers.add_parser('sync', help="Sync installed named skills with the registry")
    uninstall_parser = subparsers.add_parser('uninstall', help="Uninstall a named skill")
    uninstall_parser.add_argument('skill_id', help="Named skill ID to uninstall (e.g. karpathy/autoresearch)")
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
    elif args.command == 'embed':
        embed_command(args)
    elif args.command == 'search':
        search_command(args)
    elif args.command == 'name':
        name_command(args)
    elif args.command == 'install':
        install_command(args)
    elif args.command == 'sync':
        sync_command(args)
    elif args.command == 'uninstall':
        uninstall_command(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
