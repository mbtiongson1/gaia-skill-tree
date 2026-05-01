import argparse
import sys
import os
import json
import subprocess
from datetime import date
from contextlib import redirect_stdout
from io import StringIO
from importlib.metadata import PackageNotFoundError, version as package_version
from pathlib import Path

from gaia_cli.scanner import scan_repo, scan_repo_detailed, load_config
from gaia_cli.resolver import resolve_skills
from gaia_cli.combinator import get_combinations
from gaia_cli.treeManager import load_tree, save_tree, show_status, show_tree
from gaia_cli.prWriter import open_pr, open_intake_pr
from gaia_cli.push import build_skill_batch, write_skill_batch
from gaia_cli.embeddings import generate_embeddings
from gaia_cli.semantic_search import search as semantic_search, load_embeddings
from gaia_cli.name import find_awakened_skill, promote_to_named, update_batch_lifecycle
from gaia_cli.install import install_skill, sync_skills, uninstall_skill, list_installed, interactive_install, list_available
from gaia_cli.graph import graph_command
from gaia_cli.registry import (
    generated_output_dir,
    embeddings_path,
    named_skills_dir,
    promotion_candidates_path,
    registry_graph_path,
    skill_batches_dir,
    user_tree_path,
    require_explicit_writable_registry,
    resolve_registry_path,
    write_global_registry,
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
    load_promotion_candidates,
    promote_from_candidates,
    promote_skill,
    promotable_candidates,
    promotion_state,
    write_promotion_candidates,
    next_level,
    LEVEL_NAMES,
)
from gaia_cli.hook import hook_entry

DEFAULT_REGISTRY_REF = "https://github.com/mbtiongson1/gaia-skill-tree"

COMMAND_USAGE = """\
Quick usage:
  gaia init [--user <name>] [--scan <path>] [--yes]
  gaia scan [--quiet] [--auto-promote]
  gaia pull
  gaia tree [--named] [--title]
  gaia push [--dry-run] [--no-pr]
  gaia version
  gaia mcp
  gaia release <patch|minor|major>
  gaia graph [--format html|svg|json] [-o <path>] [--no-open]
  gaia appraise [<skillId>]
  gaia promote [<skillId>] [--all] [--name <name>]
  gaia docs build [--check]
  gaia skills <list|search|info|install|uninstall>
  gaia skills list [--exclude-pending]
  gaia skills search <query> [--exclude-pending]
  gaia skills info <skill_id> [--exclude-pending]
  gaia skills install <skill_id> [--global | --local]
  gaia skills uninstall <skill_id>
"""

SKILLS_USAGE = """\
Quick usage:
  gaia skills list [--exclude-pending]
  gaia skills search <query> [--exclude-pending]
  gaia skills info <skill_id> [--exclude-pending]
  gaia skills install <skill_id> [--global | --local]
  gaia skills uninstall <skill_id>
"""

PUBLIC_COMMANDS = (
    "help",
    "init",
    "scan",
    "pull",
    "tree",
    "push",
    "version",
    "mcp",
    "release",
    "graph",
    "appraise",
    "promote",
    "docs",
    "skills",
)

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
    config_path = os.path.join(config_dir, 'config.toml')
    if os.path.exists(config_path):
        print("Gaia is already initialized in this repository.")
        return

    username = args.user or _detect_github_username()
    if not username and sys.stdin.isatty() and not getattr(args, "yes", False):
        username = input("Gaia username: ").strip()
    username = username or "gaiabot"

    # Auto-detect skill files if no --scan flags given
    if args.scan:
        scan_paths = args.scan
    else:
        detected = _detect_skill_files()
        scan_paths = detected if detected else ["scripts", "packages/cli-npm"]

    local_registry_path = os.path.abspath(".")
    with open(config_path, 'w', encoding='utf-8') as f:
        f.write(f'username = "{username}"\n')
        f.write(f'gaiaRegistryRef = "{args.registry_ref or DEFAULT_REGISTRY_REF}"\n')
        f.write(f'localRegistryPath = "{local_registry_path}"\n')
        f.write(f'autoPromptCombinations = {"true" if args.auto_prompt_combinations else "false"}\n')
        f.write("scanPaths = [" + ", ".join(json.dumps(path) for path in scan_paths) + "]\n")
    print(f"Initialized Gaia configuration at {config_path}")
    print(f"  user:       {username}")
    print(f"  scanPaths:  {scan_paths}")

    # If we're inside a registry clone, register its path globally so that
    # commands like `gaia push` work from any project without --registry.
    tree_path = user_tree_path(".", username)
    if os.path.exists("registry/gaia.json") and not os.path.exists(tree_path):
        save_tree(username, {
            "userId": username,
            "updatedAt": date.today().isoformat(),
            "unlockedSkills": [],
            "pendingCombinations": [],
            "stats": {"totalUnlocked": 0, "highestRarity": "common", "deepestLineage": 0},
        }, registry_path=".")
        print(f"  skill tree: {tree_path}")

    if os.path.exists("registry/gaia.json"):
        registry_abs = os.path.abspath(".")
        write_global_registry(registry_abs)
        print(f"  registry:   {registry_abs} (saved to ~/.gaia/config.json)")
        
        # Auto-install git hooks
        hook_script = os.path.join(registry_abs, "scripts", "install-git-hooks.sh")
        if os.path.exists(hook_script):
            try:
                subprocess.run(["bash", hook_script], check=True)
                print("  git hooks:  installed automatically")
            except subprocess.CalledProcessError:
                print("  git hooks:  failed to install automatically")


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
            print('Tip: try `gaia skills search "code review"` or expand scanPaths.')
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
        candidate_path = write_promotion_candidates(args.registry, username, eligible)
        if not quiet:
            print(f"Wrote promotion candidates: {candidate_path}")
        if eligible:
            for promo in eligible[:2]:
                skill = skill_map.get(promo["skillId"])
                if skill:
                    print(render_promotion_prompt(skill, promo.get("suggestedLevel", "II")))
        render_user_tree_outputs(username, tree, graph_data, args.registry, quiet=quiet)
        if getattr(args, "auto_promote", False) and eligible:
            promoted = promote_all_candidates(username, args.registry)
            if promoted and not quiet:
                print(f"Auto-promoted {len(promoted)} skill(s).")
            tree = load_tree(username, registry_path=args.registry)
            render_user_tree_outputs(username, tree, graph_data, args.registry, quiet=quiet)


def render_user_tree_outputs(username: str, tree: dict | None, graph_data: dict | None, registry_path: str, quiet: bool = False) -> tuple[str, str] | None:
    if not tree:
        return None
    mode = "default"
    buf = StringIO()
    with redirect_stdout(buf):
        show_tree(tree, graph_data=graph_data, registry_path=registry_path, mode=mode)
    text = buf.getvalue()
    out_dir = generated_output_dir(registry_path)
    os.makedirs(out_dir, exist_ok=True)
    md_path = os.path.join(out_dir, "tree.md")
    html_path = os.path.join(out_dir, "tree.html")
    with open(md_path, "w", encoding="utf-8") as f:
        f.write("# Gaia Skill Tree\n\n```text\n")
        f.write(text)
        f.write("```\n")
    html = (
        "<!doctype html><html lang=\"en\"><head><meta charset=\"utf-8\">"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">"
        f"<title>Gaia Skill Tree - {username}</title>"
        "<style>body{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;margin:2rem;line-height:1.45}"
        "pre{white-space:pre-wrap}</style></head><body>"
        f"<h1>Gaia Skill Tree - {username}</h1><pre>"
        + text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        + "</pre></body></html>\n"
    )
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    if not quiet:
        print(f"Wrote tree render: {html_path}")
        print(f"Wrote tree render: {md_path}")
    return html_path, md_path


def promote_all_candidates(username: str, registry_path: str) -> list[dict]:
    promoted = []
    for candidate in promotable_candidates(registry_path, username=username):
        promoted.append(promote_from_candidates(
            username,
            candidate["skillId"],
            registry_path,
        ))
    return promoted

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
        print(f"Or create skill-trees/{username}/skill-tree.json in the registry.")
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
    try:
        candidates = load_promotion_candidates(args.registry).get("candidates", [])
        matching = [c for c in candidates if c.get("skillId") == skill_id]
        if matching:
            labels = ", ".join(c.get("suggestedLevel", "?") for c in matching)
            print(f"\nLast scan flagged this skill as promotable to: {labels}")
    except ValueError:
        pass


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

    try:
        if getattr(args, "all", False):
            results = promote_all_candidates(username, args.registry)
            if not results:
                print("No skills eligible for promotion.")
                return
            for result in results:
                print(f"Promoted {result['skillId']} to Level {result['newLevel']}.")
            return
        if not skill_id:
            print("Usage: gaia promote <skill> or gaia promote --all", file=sys.stderr)
            sys.exit(2)
        result = promote_from_candidates(username, skill_id, args.registry, new_display_name=display_name)
    except ValueError as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(1)

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
            print(f"  ○ {o.get('name', o['skillId'])} - missing: {o.get('missingPrereq', '?')}")
        if len(one_away) > 8:
            print(f"  ... and {len(one_away) - 8} more")
        print()


def hook_command(args):
    """Internal command invoked by Claude Code hook."""
    hook_entry(event=getattr(args, 'event', 'file_edit'))


def doctor_command(args):
    config_path = ".gaia/config.toml"
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
    tree_path = user_tree_path(registry_path, username or '')
    print(f"Skill tree: {'found' if os.path.exists(tree_path) else 'missing'}")
    emb_path = embeddings_path(registry_path)
    print(f"Embeddings: {'found' if os.path.exists(emb_path) else 'missing'}")
    print("Scan paths:")
    for path in config.get('scanPaths', []):
        print(f"  - {path} {'exists' if os.path.exists(path) else 'missing'}")

def tree_command(args):
    config = load_config()
    if not config:
        print("Gaia not initialized.")
        return
    graph_data = None
    graph_path = registry_graph_path(args.registry)
    if os.path.exists(graph_path):
        with open(graph_path, 'r', encoding='utf-8') as f:
            graph_data = json.load(f)
    tree = load_tree(config.get('gaiaUser'), registry_path=args.registry)
    mode = "named" if getattr(args, 'named', False) else ("title" if getattr(args, 'title', False) else "default")
    show_tree(tree, graph_data=graph_data, registry_path=args.registry, mode=mode)
    if tree:
        render_user_tree_outputs(config.get('gaiaUser'), tree, graph_data, args.registry, quiet=False)

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
            gaia skills search "<your query>"

  Tip: Re-run `gaia embed` whenever new skills are added to the registry.\
"""

_EMBEDDINGS_MISSING_STEPS = """\

  +----------------------------------------------------------------+
  |  Embeddings have not been generated yet.                       |
  +----------------------------------------------------------------+

  Generate them now (run once from the registry root, ~30 seconds):
    gaia embed

  Then retry:
    gaia skills search "{query}"

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
    emb_path = embeddings_path(args.registry)
    try:
        results = semantic_search(args.query, emb_path, top_k=args.top_k)
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
        interactive_install(args.registry)
        return
    if not args.skill_id:
        print("Error: provide a skill ID (contributor/skill-name) or use --list to browse.", file=sys.stderr)
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


def _load_json_file(path: str, default=None):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return default


def _pending_skills(registry_path: str, username: str | None = None) -> list[dict]:
    batches_root = Path(skill_batches_dir(registry_path))
    paths = []
    if batches_root.is_dir():
        paths.extend(batches_root.glob("*.json"))
        paths.extend(batches_root.glob("*/*.json"))
    pending = []
    for path in sorted(paths):
        batch = _load_json_file(str(path), default={}) or {}
        if username and batch.get("userId") not in (None, username):
            continue
        for skill in batch.get("proposedSkills", []):
            if skill.get("lifecycle", "pending") == "pending":
                pending.append({
                    "id": skill.get("id"),
                    "name": skill.get("name", skill.get("id")),
                    "description": skill.get("description", ""),
                    "level": skill.get("level", "I"),
                    "pending": True,
                })
    return pending


def skills_command(args):
    config = load_config() or {}
    username = config.get("gaiaUser") or config.get("username")
    pending = [] if getattr(args, "exclude_pending", False) else _pending_skills(args.registry, username)
    verb = getattr(args, "skills_command", None)
    if verb == "install":
        success = install_skill(args.skill_id, args.registry)
        if not success:
            sys.exit(1)
        return
    if verb == "uninstall":
        success = uninstall_skill(args.skill_id)
        if not success:
            sys.exit(1)
        return

    available = [
        {"id": sid, "name": meta.get("name") or sid, "level": meta.get("level", "?"), "description": meta.get("description", "")}
        for sid, meta in list_available(args.registry)
    ]
    items = available + pending
    query = getattr(args, "query", None)
    if verb == "search" and query:
        q = query.lower()
        items = [
            item for item in items
            if q in str(item.get("id", "")).lower()
            or q in str(item.get("name", "")).lower()
            or q in str(item.get("description", "")).lower()
        ]
    if verb == "info":
        q = args.skill_id
        match = next((item for item in items if item.get("id") == q), None)
        if not match:
            print(f"Skill '{q}' not found.", file=sys.stderr)
            sys.exit(1)
        suffix = " (pending)" if match.get("pending") else ""
        print(f"{match['id']}{suffix}")
        print(f"Name: {match.get('name', match['id'])}")
        print(f"Level: {match.get('level', '?')}")
        if match.get("description"):
            print(match["description"])
        return
    if not items:
        print("No skills found.")
        return
    width = max(5, *(len(str(item.get("id", ""))) for item in items))
    print(f"{'Skill':<{width}}  Level  Name")
    print("-" * (width + 14))
    for item in items:
        suffix = " (pending)" if item.get("pending") else ""
        print(f"{item.get('id', ''):<{width}}  {item.get('level', '?'):<5}  {item.get('name', '')}{suffix}")


def pull_command(args):
    subprocess.run(["git", "-C", args.registry, "pull", "--ff-only", "origin"], check=True)


def version_command(args):
    pyproject = Path(args.registry) / "pyproject.toml"
    if pyproject.exists():
        text = pyproject.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("version = "):
                print(line.split("=", 1)[1].strip().strip('"'))
                return
    try:
        print(package_version("gaia-cli"))
    except PackageNotFoundError:
        pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
        text = pyproject.read_text(encoding="utf-8") if pyproject.exists() else ""
        for line in text.splitlines():
            if line.startswith("version = "):
                print(line.split("=", 1)[1].strip().strip('"'))
                return
        print("unknown")


def mcp_command(args):
    script = Path(args.registry) / "packages" / "mcp" / "dist" / "bin" / "gaia-mcp.js"
    if not script.exists():
        print(f"MCP server build not found: {script}", file=sys.stderr)
        print("Run `npm run build` in packages/mcp first.", file=sys.stderr)
        sys.exit(1)
    raise SystemExit(subprocess.call(["node", str(script)]))


def docs_command(args):
    script = Path(args.registry) / "scripts" / "build_docs.py"
    cmd = [sys.executable, str(script)]
    if getattr(args, "check", False):
        cmd.append("--check")
    raise SystemExit(subprocess.call(cmd))


def release_command(args):
    from gaia_cli.versioning import bump_versions

    new_version = bump_versions(args.registry, args.release_type)
    print(f"Gaia version bumped to {new_version}.")


def main():
    # Ensure UTF-8 output on Windows (avoids cp1252 UnicodeEncodeError for box-drawing)
    if sys.platform == "win32" and hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(
        prog="gaia",
        description="Gaia Registry CLI",
        epilog=COMMAND_USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        '--registry',
        default=None,
        help="Path to a local Gaia registry checkout. Defaults to auto-resolved local or global registry.",
    )
    parser.add_argument(
        '--global', '-g',
        dest='global_flag',
        action='store_true',
        help="Use global GAIA_HOME registry, ignoring any local .gaia/ config.",
    )
    parser.add_argument(
        '--version', '-v',
        action='store_true',
        help="Print the Gaia CLI version and exit.",
    )
    subparsers = parser.add_subparsers(dest='command', metavar="{" + ",".join(PUBLIC_COMMANDS) + "}")
    subparsers.add_parser('help', help="Show command help")
    init_parser = subparsers.add_parser('init', help="Create or update local Gaia config")
    init_parser.add_argument('--user', help='Gaia username to write into .gaia/config.toml')
    init_parser.add_argument('--registry-ref', help='Gaia registry URL to write into .gaia/config.toml')
    init_parser.add_argument('--scan', action='append', help='Path to scan; repeat for multiple paths')
    init_parser.add_argument('--yes', action='store_true', help='Use non-interactive defaults')
    init_parser.add_argument(
        '--auto-prompt-combinations',
        action='store_true',
        help='Enable automatic prompts for detected skill combinations',
    )
    scan_parser = subparsers.add_parser('scan', help="Scan configured paths for skill evidence")
    scan_parser.add_argument('--quiet', action='store_true', help="Suppress scan output; only show notifications")
    scan_parser.add_argument('--auto-promote', action='store_true', help="Promote every scan-recommended candidate after scanning")
    subparsers.add_parser('pull', help="Refresh registry data from origin")
    tree_parser = subparsers.add_parser('tree', help="Show your Gaia skill tree")
    tree_parser.add_argument('--named', action='store_true', help="Show only skills that have a named implementation")
    tree_parser.add_argument('--title', action='store_true', help="Show display name instead of slash command / contributor ID")
    push_parser = subparsers.add_parser('push', help="Prepare detected skills for review")
    push_parser.add_argument('--dry-run', action='store_true', help="Print the skill batch without writing it")
    push_parser.add_argument('--no-pr', action='store_true', help="Write intake record without creating a PR")
    subparsers.add_parser('version', help="Print the Gaia CLI version")
    subparsers.add_parser('mcp', help="Run the bundled Gaia MCP server")
    release_parser = subparsers.add_parser('release', help="Bump release version files")
    release_parser.add_argument('release_type', choices=('patch', 'minor', 'major'))
    graph_parser = subparsers.add_parser('graph', help="Generate and open the Gaia skill graph")
    graph_parser.add_argument('--format', choices=('html', 'svg', 'json'), default='html', help="Graph artifact format (default: html)")
    graph_parser.add_argument('-o', '--output', help="Output path (default: registry/render/gaia.html)")
    graph_parser.add_argument('--open', dest='open', action='store_true', default=True, help="Open the generated graph (default)")
    graph_parser.add_argument('--no-open', dest='open', action='store_false', help="Do not open the generated graph")
    appraise_parser = subparsers.add_parser('appraise', help="Inspect a skill card with status and actions")
    appraise_parser.add_argument('skillId', nargs='?', default=None, help="Skill ID to appraise (default: most recent)")
    promote_parser = subparsers.add_parser('promote', help="Promote a skill eligible for level-up")
    promote_parser.add_argument('skillId', nargs='?', default=None, help="Skill ID to promote")
    promote_parser.add_argument('--all', action='store_true', help="Promote every candidate from the last scan")
    promote_parser.add_argument('--name', help="Optional display name for the promoted skill")
    docs_parser = subparsers.add_parser('docs', help="Documentation maintenance commands")
    docs_sub = docs_parser.add_subparsers(dest='docs_command')
    docs_build = docs_sub.add_parser('build', help="Regenerate generated documentation regions")
    docs_build.add_argument('--check', action='store_true', help="Fail if docs are stale without writing")
    skills_parser = subparsers.add_parser(
        'skills',
        help="Browse and manage named skills",
        epilog=SKILLS_USAGE,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    skills_sub = skills_parser.add_subparsers(dest='skills_command')
    skills_list = skills_sub.add_parser('list', help="List available named skills")
    skills_list.add_argument('--exclude-pending', action='store_true', help="Hide pending skill proposals")
    skills_search = skills_sub.add_parser('search', help="Search named skills")
    skills_search.add_argument('query', help="Search query")
    skills_search.add_argument('--exclude-pending', action='store_true', help="Hide pending skill proposals")
    skills_info = skills_sub.add_parser('info', help="Show details for a named skill")
    skills_info.add_argument('skill_id', help="Skill ID to inspect")
    skills_info.add_argument('--exclude-pending', action='store_true', help="Hide pending skill proposals")
    skills_install = skills_sub.add_parser('install', help="Install a named skill")
    skills_install.add_argument('skill_id', help="Skill ID to install")
    skills_install.add_argument('--global', dest='install_global', action='store_true', help='Install to ~/.gaia/skills')
    skills_install.add_argument('--local', dest='install_local', action='store_true', help='Install to project .gaia/skills')
    skills_uninstall = skills_sub.add_parser('uninstall', help="Uninstall a named skill")
    skills_uninstall.add_argument('skill_id', help="Skill ID to uninstall")
    hook_parser = subparsers.add_parser('_hook', help=argparse.SUPPRESS)
    subparsers._choices_actions = [
        action for action in subparsers._choices_actions if action.dest != '_hook'
    ]
    hook_parser.add_argument('--event', default='file_edit', help=argparse.SUPPRESS)
    args = parser.parse_args()
    args.registry = resolve_registry_path(args.registry, global_flag=args.global_flag)
    require_explicit_writable_registry(parser, args)
    if args.version:
        version_command(args)
        return
    if args.command == 'init':
        init_command(args)
    elif args.command == 'help':
        parser.print_help()
    elif args.command == 'scan':
        scan_command(args)
    elif args.command == 'pull':
        pull_command(args)
    elif args.command == 'tree':
        tree_command(args)
    elif args.command == 'push':
        push_command(args)
    elif args.command == 'version':
        version_command(args)
    elif args.command == 'mcp':
        mcp_command(args)
    elif args.command == 'release':
        release_command(args)
    elif args.command == 'graph':
        graph_command(args)
    elif args.command == 'appraise':
        appraise_command(args)
    elif args.command == 'promote':
        promote_command(args)
    elif args.command == 'docs' and getattr(args, 'docs_command', None) == 'build':
        docs_command(args)
    elif args.command == 'skills':
        if not getattr(args, 'skills_command', None):
            skills_parser.print_help()
            return
        skills_command(args)
    elif args.command == '_hook':
        hook_command(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
