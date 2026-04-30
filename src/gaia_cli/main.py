import argparse
import sys
import os
import json

from gaia_cli.scanner import scan_repo, scan_repo_detailed, load_config
from gaia_cli.resolver import resolve_skills
from gaia_cli.combinator import get_combinations
from gaia_cli.treeManager import load_tree, save_tree, show_status, show_tree
from gaia_cli.prWriter import open_pr, open_intake_pr
from gaia_cli.push import build_skill_batch, write_skill_batch
from gaia_cli.embeddings import generate_embeddings
from gaia_cli.semantic_search import search as semantic_search, load_embeddings
from gaia_cli.name import find_awakened_skill, promote_to_named, update_batch_lifecycle
from gaia_cli.install import install_skill, sync_skills, uninstall_skill, list_installed
from gaia_cli.graph import graph_command
from gaia_cli.registry import (
    registry_graph_path,
    require_explicit_writable_registry,
    resolve_registry_path,
)
from gaia_cli.pathEngine import compute_paths, load_paths, save_paths, diff_paths
from gaia_cli.cardRenderer import (
    render_card,
    render_appraise_card,
    render_unlock_card,
    render_path_summary,
    render_promotion_prompt,
    load_and_render,
)
from gaia_cli.promotion import (
    check_promotion_eligibility,
    promote_skill,
    promotion_state,
    next_level,
    LEVEL_NAMES,
)
from gaia_cli.hook import hook_entry

DEFAULT_REGISTRY_REF = "https://github.com/mbtiongson1/gaia-skill-tree"

# Known skill-convention files/dirs, in priority order
_SKILL_CANDIDATES = [
    'AGENTS.md',                         # OpenAI Codex
    'SKILLS.md',                         # generic
    'SKILL.md',                          # single named-skill file
    'agents.md',
    'skills.md',
    '.claude/skills',                    # Claude Code skill directory
    '.gemini',                           # Gemini skill directory (*.yml inside)
    '.github/copilot-instructions.md',   # GitHub Copilot
    'codex.yml',
    'gemini.yml',
    '.cursor/rules',                     # Cursor rules directory
]


def _detect_github_username():
    """Detect GitHub username from git remote URL, email, or display name."""
    import subprocess
    import re
    # Most reliable: parse github.com/USERNAME from origin remote URL
    try:
        r = subprocess.run(['git', 'remote', 'get-url', 'origin'],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            m = re.search(r'github\.com[:/]([^/]+?)(?:\.git)?(?:/|$)', r.stdout.strip())
            if m:
                return m.group(1)
    except Exception:
        pass
    # Fallback: noreply GitHub email (e.g. 12345+username@users.noreply.github.com)
    try:
        r = subprocess.run(['git', 'config', 'user.email'],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            m = re.match(r'^(?:\d+\+)?([^@]+)@users\.noreply\.github\.com$', r.stdout.strip())
            if m:
                return m.group(1)
    except Exception:
        pass
    # Fallback: git display name → slug
    try:
        r = subprocess.run(['git', 'config', 'user.name'],
                           capture_output=True, text=True, timeout=5)
        if r.returncode == 0:
            slug = re.sub(r'[^a-zA-Z0-9-]', '', r.stdout.strip().lower().replace(' ', '-'))
            if slug:
                return slug
    except Exception:
        pass
    return None


def _detect_skill_files():
    """Return existing skill-related paths in the current working directory."""
    return [c for c in _SKILL_CANDIDATES if os.path.exists(c)]


def init_command(args):
    config_dir = '.gaia'
    os.makedirs(config_dir, exist_ok=True)
    config_path = os.path.join(config_dir, 'config.json')
    if os.path.exists(config_path):
        print("Gaia is already initialized in this repository.")
        return

    # Auto-detect username if not provided
    username = args.user or _detect_github_username() or "gaiabot"

    # Auto-detect skill files if no --scan flags given
    if args.scan:
        scan_paths = args.scan
    else:
        detected = _detect_skill_files()
        scan_paths = detected if detected else ["scripts", "plugin"]

    config = {
        "gaiaUser": username,
        "gaiaRegistryRef": args.registry_ref or DEFAULT_REGISTRY_REF,
        "scanPaths": scan_paths,
        "autoPromptCombinations": args.auto_prompt_combinations,
    }
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2)
    print(f"Initialized Gaia configuration at {config_path}")
    print(f"  user:       {username}")
    print(f"  scanPaths:  {scan_paths}")


def scan_command(args):
    config = load_config()
    if not config:
        print("Gaia not initialized. Run `gaia init` first.")
        return
    quiet = getattr(args, 'quiet', False)
    if not quiet:
        print("Scanning repository...")
    scan_result = scan_repo_detailed()
    raw_tokens = scan_result["tokens"]
    graph_path = registry_graph_path(args.registry)
    resolved = resolve_skills(raw_tokens, registry_path=graph_path)
    if not quiet:
        print(
            f"Scanned {scan_result['files_scanned']} file(s) across "
            f"{len(scan_result['paths_found'])} configured path(s)."
        )
        if scan_result["paths_missing"]:
            print("Missing scan paths: " + ", ".join(scan_result["paths_missing"]))
        print(f"Found {scan_result['candidate_count']} candidate token(s).")
        print(f"Matched {len(resolved)} canonical skill(s).")
        if resolved:
            print(", ".join(resolved))
        else:
            print('Tip: try `gaia search "code review"` or expand scanPaths.')
    username = config.get('gaiaUser')
    tree = load_tree(username, registry_path=args.registry)
    if tree:
        with open(graph_path, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
        unlocked = [s.get('skillId') for s in tree.get('unlockedSkills', [])]
        combos = get_combinations(graph_data, unlocked, resolved)
        if combos and not quiet:
            print("\nNew combination candidates detected:")
            for c in combos:
                print(f"- {c['candidateResult']} (Requires: {', '.join(c['detectedSkills'])})")
            print("Run `gaia fuse [skillId]` to confirm and add to your tree.")

        # Path engine integration
        old_paths = load_paths()
        owned_ids = [s.get('skillId') for s in tree.get('unlockedSkills', [])]
        new_paths = compute_paths(graph_data, owned_ids, resolved)
        new_paths["userId"] = username
        changes = diff_paths(old_paths, new_paths)
        save_paths(new_paths)

        # Show unlock cards for newly reachable skills
        skill_map = {s['id']: s for s in graph_data.get('skills', [])}
        if changes.get("new_near_unlocks"):
            print()
            for sid in changes["new_near_unlocks"]:
                skill = skill_map.get(sid)
                if skill:
                    opened = [p for p in new_paths.get("availablePaths", []) if p.get("distance", 99) <= 2]
                    print(render_unlock_card(skill, opened[:3]))
                    print()

        # Path summary
        if new_paths.get("nearUnlocks") or new_paths.get("oneAway"):
            print(render_path_summary(new_paths))

        # Promotion hints
        eligible = check_promotion_eligibility(graph_data, tree)
        if eligible:
            for promo in eligible[:2]:
                skill = skill_map.get(promo["skillId"])
                if skill:
                    print(render_promotion_prompt(skill, promo.get("nextLevel", "II")))

def status_command(args):
    config = load_config()
    if not config:
        print("Gaia not initialized.")
        return
    username = config.get('gaiaUser')
    tree = load_tree(username, registry_path=args.registry)
    if not tree:
        print(f'No skill tree found for user "{username}".')
        print("Next steps:")
        print("  gaia scan")
        print("  gaia push --dry-run")
        print("  gaia push --no-pr")
        print(f"Or create users/{username}/skill-tree.json in the registry.")
        return
    show_status(tree)


def appraise_command(args):
    """Render an appraise card for a skill."""
    config = load_config()
    if not config:
        print("Gaia not initialized. Run `gaia init` first.")
        return

    graph_path = registry_graph_path(args.registry)
    if not os.path.exists(graph_path):
        print("Registry graph not found.")
        return

    with open(graph_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)

    skill_map = {s['id']: s for s in graph_data.get('skills', [])}
    username = config.get('gaiaUser')
    tree = load_tree(username, registry_path=args.registry)

    # Determine which skill to appraise
    skill_id = getattr(args, 'skillId', None)
    if not skill_id:
        # Default: most recently unlocked skill
        if tree and tree.get('unlockedSkills'):
            sorted_skills = sorted(
                tree['unlockedSkills'],
                key=lambda s: s.get('unlockedAt', ''),
                reverse=True,
            )
            skill_id = sorted_skills[0]['skillId']
        else:
            # Fall back to most recent near-unlock from paths
            paths = load_paths()
            if paths and paths.get('nearUnlocks'):
                skill_id = paths['nearUnlocks'][0]['skillId']
            else:
                print("No skill to appraise. Pass a skill ID or run `gaia scan` first.")
                return

    skill = skill_map.get(skill_id)
    if not skill:
        print(f"Skill '{skill_id}' not found in registry.")
        return

    # Build prereq status
    owned_ids = set()
    if tree:
        owned_ids = {s['skillId'] for s in tree.get('unlockedSkills', [])}
    # Also include detected skills from paths
    paths = load_paths()
    detected_ids = set()
    if paths:
        for nu in paths.get("nearUnlocks", []):
            detected_ids.update(nu.get("satisfiedPrereqs", []))
        for oa in paths.get("oneAway", []):
            detected_ids.update(oa.get("satisfiedPrereqs", []))
    available = owned_ids | detected_ids

    prereq_status = {}
    for p in skill.get('prerequisites', []):
        prereq_status[p] = p in available

    # Derivatives
    derivatives = []
    for d_id in skill.get('derivatives', []):
        d_skill = skill_map.get(d_id)
        if d_skill:
            derivatives.append(d_skill)
        else:
            derivatives.append({"id": d_id, "name": d_id, "type": "unknown"})

    # Contextual actions
    owned = skill_id in owned_ids
    actions = []
    if not owned and all(prereq_status.values()) and prereq_status:
        actions.append("[F] Fuse")
    if owned:
        state = promotion_state(skill_id, tree, graph_data)
        if state == "eligible":
            actions.append("[P] Promote")
    actions.append("[S] Scan")
    if derivatives:
        actions.append("[→] Paths")

    print(render_appraise_card(skill, prereq_status, derivatives, actions, owned=owned))


def promote_command(args):
    """Run promotion flow for an eligible skill."""
    config = load_config()
    if not config:
        print("Gaia not initialized.")
        return

    username = config.get('gaiaUser')
    graph_path = registry_graph_path(args.registry)

    if not os.path.exists(graph_path):
        print("Registry graph not found.")
        return

    with open(graph_path, 'r', encoding='utf-8') as f:
        graph_data = json.load(f)

    tree = load_tree(username, registry_path=args.registry)
    if not tree:
        print(f"No skill tree found for user '{username}'.")
        return

    skill_id = getattr(args, 'skillId', None)
    display_name = getattr(args, 'name', None)

    if not skill_id:
        # Auto-select first eligible
        eligible = check_promotion_eligibility(graph_data, tree)
        if not eligible:
            print("No skills eligible for promotion.")
            return
        skill_id = eligible[0]["skillId"]
        print(f"Auto-selected: {skill_id}")

    # Check state
    state = promotion_state(skill_id, tree, graph_data)
    if state == "not_unlocked":
        print(f"Skill '{skill_id}' is not in your tree.")
        return
    elif state == "max_level":
        print(f"Skill '{skill_id}' is already at maximum level.")
        return
    elif state == "blocked":
        print(f"Skill '{skill_id}' cannot be promoted (evidence requirements not met).")
        return

    # Execute promotion
    result = promote_skill(username, skill_id, args.registry, new_display_name=display_name)

    # Show celebration
    skill_map = {s['id']: s for s in graph_data.get('skills', [])}
    skill = skill_map.get(skill_id, {"id": skill_id, "name": skill_id, "type": "basic"})
    level_name = LEVEL_NAMES.get(result["newLevel"], result["newLevel"])
    print(f"\n✦ {skill.get('name', skill_id)} promoted to Level {result['newLevel']} ({level_name})!")
    if display_name:
        print(f"  Renamed to: {display_name}")
    print()


def paths_command(args):
    """Display current progression paths."""
    paths = load_paths()
    if not paths:
        print("No paths computed yet. Run `gaia scan` first.")
        return

    print(render_path_summary(paths))
    print()

    near = paths.get("nearUnlocks", [])
    if near:
        print("Ready to fuse:")
        for n in near:
            print(f"  ◇ {n.get('name', n['skillId'])} ({n.get('type', '?')})")
            prereqs = n.get('satisfiedPrereqs', [])
            if prereqs:
                print(f"    from: {', '.join(prereqs)}")
        print()

    one_away = paths.get("oneAway", [])
    if one_away:
        print("One prerequisite away:")
        for o in one_away[:8]:
            print(f"  ○ {o.get('name', o['skillId'])} — missing: {o.get('missingPrereq', '?')}")
        if len(one_away) > 8:
            print(f"  ... and {len(one_away) - 8} more")
        print()


def hook_command(args):
    """Internal command invoked by Claude Code hook."""
    hook_entry(event=getattr(args, 'event', 'file_edit'))


def doctor_command(args):
    config_path = ".gaia/config.json"
    config = load_config()
    registry_path = os.path.abspath(str(args.registry))
    print("Gaia CLI: OK")
    print(f"Registry path: {args.registry}")
    print(f"Registry graph: {'found' if os.path.exists(registry_graph_path(registry_path)) else 'missing'}")
    print(f"Config: {config_path if os.path.exists(config_path) else 'missing'}")
    if not config:
        print("User: unknown")
        print("Skill tree: unknown")
        return

    username = config.get('gaiaUser')
    print(f"User: {username}")
    tree_path = os.path.join(registry_path, 'users', username or '', 'skill-tree.json')
    print(f"Skill tree: {'found' if os.path.exists(tree_path) else 'missing'}")
    embeddings_path = os.path.join(registry_path, 'graph', 'embeddings.json')
    print(f"Embeddings: {'found' if os.path.exists(embeddings_path) else 'missing'}")
    print("Scan paths:")
    for path in config.get('scanPaths', []):
        print(f"  - {path} {'exists' if os.path.exists(path) else 'missing'}")

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

_EMBEDDINGS_INSTALL_STEPS = """\

  +----------------------------------------------------------------+
  |  Semantic search requires the embeddings package.              |
  +----------------------------------------------------------------+

  Step 1 -- Install the embeddings library:
            pip install "gaia-cli[embeddings]"

  Step 2 -- Generate embeddings (run once, ~30 seconds):
            gaia embed

  Step 3 -- Search:
            gaia search "<your query>"

  Tip: Re-run `gaia embed` whenever new skills are added to the registry.\
"""

_EMBEDDINGS_MISSING_STEPS = """\

  +----------------------------------------------------------------+
  |  Embeddings have not been generated yet.                       |
  +----------------------------------------------------------------+

  Generate them now (run once from the registry root, ~30 seconds):
    gaia embed

  Then retry:
    gaia search "{query}"

  Tip: Re-run `gaia embed` whenever new skills are added to the registry.\
"""


def embed_command(args):
    try:
        import sentence_transformers  # noqa: F401
    except ImportError:
        print(_EMBEDDINGS_INSTALL_STEPS)
        sys.exit(1)
    generate_embeddings(registry_path=args.registry)

def search_command(args):
    embeddings_path = os.path.join(args.registry, 'graph', 'embeddings.json')
    try:
        results = semantic_search(args.query, embeddings_path, top_k=args.top_k)
    except FileNotFoundError:
        print(_EMBEDDINGS_MISSING_STEPS.format(query=args.query))
        return
    except ImportError:
        print(_EMBEDDINGS_INSTALL_STEPS)
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
    # Ensure UTF-8 output on Windows (avoids cp1252 UnicodeEncodeError for box-drawing)
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(prog="gaia", description="Gaia Plugin CLI")
    parser.add_argument(
        '--registry',
        default=None,
        help="Path to a local Gaia registry checkout. Defaults to bundled read-only registry data.",
    )
    subparsers = parser.add_subparsers(dest='command')
    init_parser = subparsers.add_parser('init')
    init_parser.add_argument('--user', help='Gaia username to write into .gaia/config.json')
    init_parser.add_argument('--registry-ref', help='Gaia registry URL to write into .gaia/config.json')
    init_parser.add_argument('--scan', action='append', help='Path to scan; repeat for multiple paths')
    init_parser.add_argument('--yes', action='store_true', help='Use non-interactive defaults')
    init_parser.add_argument(
        '--auto-prompt-combinations',
        action='store_true',
        help='Enable automatic prompts for detected skill combinations',
    )
    scan_parser = subparsers.add_parser('scan')
    scan_parser.add_argument('--quiet', action='store_true', help="Suppress scan output; only show notifications")
    subparsers.add_parser('status')
    subparsers.add_parser('doctor')
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
    graph_parser = subparsers.add_parser('graph', help="Generate and open the Gaia skill graph")
    graph_parser.add_argument('--format', choices=('svg', 'json'), default='svg', help="Graph artifact format (default: svg)")
    graph_parser.add_argument('-o', '--output', help="Output path (default: graph/gaia.svg)")
    graph_parser.add_argument('--open', dest='open', action='store_true', default=True, help="Open the generated graph (default)")
    graph_parser.add_argument('--no-open', dest='open', action='store_false', help="Do not open the generated graph")
    uninstall_parser = subparsers.add_parser('uninstall', help="Uninstall a named skill")
    uninstall_parser.add_argument('skill_id', help="Named skill ID to uninstall (e.g. karpathy/autoresearch)")
    # --- New commands ---
    appraise_parser = subparsers.add_parser('appraise', help="Inspect a skill card with status and actions")
    appraise_parser.add_argument('skillId', nargs='?', default=None, help="Skill ID to appraise (default: most recent)")
    promote_parser = subparsers.add_parser('promote', help="Promote a skill eligible for level-up")
    promote_parser.add_argument('skillId', nargs='?', default=None, help="Skill ID to promote (default: first eligible)")
    promote_parser.add_argument('--name', help="Optional display name for the promoted skill")
    subparsers.add_parser('paths', help="Show progression paths from current state")
    hook_parser = subparsers.add_parser('_hook', help=argparse.SUPPRESS)
    hook_parser.add_argument('--event', default='file_edit', help=argparse.SUPPRESS)
    args = parser.parse_args()
    args.registry_explicit = args.registry is not None
    args.registry = resolve_registry_path(args.registry)
    require_explicit_writable_registry(parser, args)
    if args.command == 'init':
        init_command(args)
    elif args.command == 'scan':
        scan_command(args)
    elif args.command == 'status':
        status_command(args)
    elif args.command == 'doctor':
        doctor_command(args)
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
    elif args.command == 'graph':
        graph_command(args)
    elif args.command == 'uninstall':
        uninstall_command(args)
    elif args.command == 'appraise':
        appraise_command(args)
    elif args.command == 'promote':
        promote_command(args)
    elif args.command == 'paths':
        paths_command(args)
    elif args.command == '_hook':
        hook_command(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
