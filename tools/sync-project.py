#!/usr/bin/env python3
"""
Sync a project workspace's agent/skill/knowledge base to the latest version.

Usage:
  python tools/sync-project.py <project-path>            # sync (fingerprint auto-updates)
  python tools/sync-project.py <project-path> --check    # freshness check only
  python tools/sync-project.py <project-path> --sync     # force sync (same as default)

Check mode (--check) reports the result with its exit code:
  0 = up to date
  1 = updates available (or the project has no fingerprint)
  2 = invalid project

Does not touch settings/ volumes/ chapters/ archives/ prompts/ story.md.

Garbled Windows Chinese paths:
  If `python tools/sync-project.py .` reports a garbled path, run from the skill directory with an explicit path instead:
  cd C:\\Users\\modoo\\.claude\\skills\\awesome-novel
  python tools\\sync-project.py "d:\\novels\\daily\\novel-project"
"""

from __future__ import annotations  # str | None and other annotations are lazily evaluated under Python 3.9, avoiding a TypeError on import

import hashlib
import subprocess
import sys
import os
import shutil
from pathlib import Path

from platforms import (
    Platform,
    convert_agent_to_platform,
    detect_platform,
    deploy_codex_skills,
    deploy_inline_skills,
    deploy_standalone_skills,
    SHORT_STANDALONE_SKILLS,
    _convert_standalone_skill,
    ensure_yaml,
    rewrite_refs,
    resolve_skill_home,
)

for s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        s.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


SKILL_HOME = resolve_skill_home()
AGENT_DIR = SKILL_HOME / "agents"
SKILL_DIR = SKILL_HOME / "skills"
KNOWLEDGE_DIR = SKILL_HOME / "knowledge"
TEMPLATE_SETTINGS_DIR = SKILL_HOME / "templates" / "settings"
FINGERPRINT_FILE = Path(".agent") / ".sync-fingerprint"
VERSION_FILE = Path(".agent") / ".sync-version"


def main():
    if "-h" in sys.argv or "--help" in sys.argv or len(sys.argv) < 2:
        print(__doc__.strip())
        return

    check_only = "--check" in sys.argv

    # Platform: --platform > NOVEL_PLATFORM > SKILL_HOME path recognition > claude
    platform_override = None
    if "--platform" in sys.argv:
        idx = sys.argv.index("--platform")
        if idx + 1 < len(sys.argv) and not sys.argv[idx + 1].startswith("--"):
            platform_override = sys.argv[idx + 1]
        else:
            print("Error: --platform needs a platform name (claude|opencode|reasonix|codex|zcode|dsh|grok)")
            sys.exit(1)
    platform_override = platform_override or os.environ.get("NOVEL_PLATFORM")
    try:
        platform = detect_platform(SKILL_HOME, platform_override)
    except ValueError as e:
        print(e)
        sys.exit(1)
    ensure_yaml(platform)

    # Handle garbled Windows Chinese paths: re-read the current directory from os.environ
    raw_arg = sys.argv[1]
    if raw_arg == "." and os.environ.get("PWD"):
        pwd = os.environ["PWD"]
        if os.path.exists(pwd):
            raw_arg = pwd
    project_path = Path(raw_arg).resolve()
    if not project_path.exists():
        print(f"Error: path does not exist: {project_path}")
        sys.exit(2)

    status_file = project_path / ".agent" / "status.md"
    if not status_file.exists():
        print(f"Error: {project_path} is not a valid novel project (missing .agent/status.md)")
        sys.exit(2)

    # Project length marker (a story.md containing length: short means a short-form project); decides the sync and check object sets
    story_file = project_path / "story.md"
    is_short = story_file.exists() and "**length:** short" in story_file.read_text(encoding="utf-8")

    if check_only:
        check_freshness(project_path, platform, is_short)
        return

    do_sync(project_path, platform, is_short)


# ============================================================
# Fingerprint mechanism
# ============================================================

def get_latest_version() -> str | None:
    """Get the skill's latest version number from git tags"""
    try:
        result = subprocess.run(
            ["git", "-C", str(SKILL_HOME), "describe", "--tags", "--abbrev=0"],
            capture_output=True, text=True, timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return None


def get_version_info() -> tuple[str | None, str | None]:
    """Return (latest_tag, version_summary); version_summary is for display"""
    tag = get_latest_version()
    if tag:
        return tag, tag
    return None, "unknown"


def compute_fingerprint() -> str:
    """Hash all agent/skill/knowledge/templates/settings files in the skill source directories"""
    files = []
    for base in [AGENT_DIR, SKILL_DIR, KNOWLEDGE_DIR]:
        if base.exists():
            for f in sorted(base.rglob("*")):
                if f.is_file() and f.name != ".gitkeep":
                    files.append(f)
    # Style assets (same deployment scope as sync_style_assets: main card + style-profiles/**);
    # non-style settings templates (world-setting and friends) are neither deployed nor fingerprinted, to avoid a permanent "updates available".
    main_tpl = TEMPLATE_SETTINGS_DIR / "writing-style.md"
    if main_tpl.is_file():
        files.append(main_tpl)
    profiles = TEMPLATE_SETTINGS_DIR / "style-profiles"
    if profiles.exists():
        for f in sorted(profiles.rglob("*.md")):
            files.append(f)
    # Scaffold templates (templates/ root + .agent/, excluding migration/ and settings/): the sync_scaffold sync scope
    # (review #17: without fingerprinting, existing projects' CLAUDE.md would forever say "8 agents" and skill_version would never update)
    tpl = SKILL_HOME / "templates"
    if tpl.exists():
        for f in sorted(tpl.rglob("*")):
            if f.is_file() and f.name != ".gitkeep" and "migration" not in f.parts and "settings" not in f.parts:
                files.append(f)
    # Body-text check scripts (the sync_tools deployment scope; without fingerprinting, existing projects would not get the scripts after an upgrade)
    for name in ("check-prose.py", "check-chapter.py"):
        tool = SKILL_HOME / "tools" / name
        if tool.is_file():
            files.append(tool)

    h = hashlib.sha256()
    for f in files:
        rel = f.relative_to(SKILL_HOME)
        h.update(str(rel).encode("utf-8"))
        h.update(f.read_bytes())
    return h.hexdigest()


def read_project_fingerprint(project: Path) -> tuple[str | None, str | None]:
    """Return (fingerprint, version)"""
    fp = project / FINGERPRINT_FILE
    vp = project / VERSION_FILE
    finger = None
    version = None
    if fp.exists():
        finger = fp.read_text(encoding="utf-8").strip()
    if vp.exists():
        version = vp.read_text(encoding="utf-8").strip()
    return finger, version


def write_project_fingerprint(project: Path, fingerprint: str, version: str | None = None):
    fp = project / FINGERPRINT_FILE
    fp.parent.mkdir(parents=True, exist_ok=True)
    fp.write_text(fingerprint + "\n", encoding="utf-8")

    vp = project / VERSION_FILE
    if version:
        vp.parent.mkdir(parents=True, exist_ok=True)
        vp.write_text(version + "\n", encoding="utf-8")
    elif vp.exists():
        vp.unlink(missing_ok=True)


# ============================================================
# Checks
# ============================================================

def check_freshness(project: Path, platform: Platform, is_short=False):
    current = compute_fingerprint()
    stored, stored_ver = read_project_fingerprint(project)
    latest_ver, _ = get_version_info()

    if stored is None:
        print("The project has no sync fingerprint, so freshness cannot be judged. Run sync-project.py to sync and generate one.")
        sys.exit(1)

    version_diff = latest_ver and stored_ver and stored_ver != latest_ver
    version_info = ""
    if version_diff:
        version_info = f"  [version] project records: {stored_ver}  ->  latest: {latest_ver}"
    elif latest_ver and not stored_ver:
        version_info = f"  [version] latest: {latest_ver} (project records no version)"

    if current == stored:
        if version_diff:
            print(f"Files are up to date. {version_info}")
            sys.exit(1)
        # The fingerprint only covers repo sources; project-side file edits (e.g. the author accidentally editing a deployed product) need a diff fallback.
        # Short-form sync does not overwrite existing knowledge products, so side edits cannot be found via fingerprint; diff explicitly.
        changes = find_changes(project, platform, is_short)
        if changes:
            lines = [f"Detected project-side files differing from the source ({len(changes)}):"]
            for f in changes:
                lines.append(f"  - {f}")
            print("\n".join(lines))
            print("Tip: run sync-project.py (without --check) to restore from the source.")
            sys.exit(1)
        print("Up to date.")
        sys.exit(0)
    else:
        changes = find_changes(project, platform, is_short)
        if not changes and platform.key in ("reasonix", "codex", "zcode", "dsh", "grok"):
            print("Updates available (source files changed; platform-derived products regenerate at sync time).")
        elif not changes:
            # The fingerprint includes style assets (writing-style.md + style-profiles/**, lines 143-149) while find_changes only scans
            # agents/skills/knowledge, so any remaining change can only be a style asset.
            # Sync uses the "never overwrite an existing card" policy (review #16): a missing file can sync; an existing card is not overwritten, only a note about source evolution is shown.
            if _missing_style_assets(project):
                print("Updates available (new style-asset files will sync to settings/).")
            else:
                print("The style-asset source has updates, but sync uses the no-overwrite policy (existing cards are not updated). To refresh a writing-style card, handle it manually.")
        else:
            lines = [f"Updates available ({len(changes)} files changed):"]
            for f in changes:
                lines.append(f"  - {f}")
            if version_info:
                lines.append(version_info)
            print("\n".join(lines))
        sys.exit(1)


def find_changes(project: Path, platform: Platform, is_short=False) -> list[str]:
    """Return the list of files differing from the source (relative paths). reasonix/zcode/dsh skills are derived products and are not listed."""
    changed = []
    if is_short:
        # Short-form projects: agents (short-form set + reader) + short knowledge products
        agent_names = {p.stem for p in AGENT_DIR.glob("*.md")
                       if p.stem.startswith(SHORT_AGENT_PREFIX) or p.stem in SHORT_SHARED_AGENTS}
        for src in sorted(AGENT_DIR.glob("*.md")):
            if src.stem not in agent_names or platform.key not in ("claude", "opencode", "codex", "grok"):
                continue
            dst = platform.agents_dir(project)
            if dst is None:
                break
            rel = src.stem + (".toml" if platform.key == "codex" else ".md")
            target = dst / rel
            if platform.key == "claude":
                if not target.exists() or target.read_bytes() != src.read_bytes():
                    changed.append(f"agents/{rel}")
            else:
                # Converted products are checked for existence only (content comparison is in the sync_agents conversion logic)
                if not target.exists():
                    changed.append(f"agents/{rel}")
        src_root = SKILL_HOME / "knowledge" / "short"
        know = platform.knowledge_dir(project)
        if src_root.exists() and know.exists():
            anti = know / "short-anti-ai.md"
            anti_src = src_root / "anti-ai" / "short-deslop.md"
            if anti_src.exists() and (not anti.exists()
                                      or anti.read_text(encoding="utf-8") != anti_src.read_text(encoding="utf-8")):
                changed.append("knowledge/short-anti-ai.md")
            for sub, dst_name in (("craft", "short-craft"), ("genres", "short-genres")):
                s = src_root / sub
                d = know / dst_name
                if s.exists() and d.exists():
                    for f in sorted(s.rglob("*.md")):
                        rel = f.relative_to(s)
                        t = d / rel
                        if not t.exists() or t.read_bytes() != f.read_bytes():
                            changed.append(f"knowledge/{dst_name}/{rel}")
        # Standalone tools (ranking-scan / text-teardown): compare verbatim against the expected content computed by the deploy conversion (the same conversion as sync)
        sdir = platform.skills_dir(project)
        if sdir is not None:
            for name in SHORT_STANDALONE_SKILLS:
                src = SKILL_HOME / "skills" / f"{name}.md"
                dst = sdir / name / "SKILL.md"
                if not src.exists():
                    continue
                expected = rewrite_refs(
                    _convert_standalone_skill(src.read_text(encoding="utf-8"), name,
                                              platform.key), platform)
                if not dst.exists() or dst.read_text(encoding="utf-8") != expected:
                    changed.append(f"skills/{name}/SKILL.md")
        return changed
    targets = {
        "agents": platform.agents_dir(project),
        "skills": platform.skills_dir(project),
        "knowledge": platform.knowledge_dir(project),
    }
    src_dirs = {
        "agents": AGENT_DIR,
        "skills": SKILL_DIR,
        "knowledge": KNOWLEDGE_DIR,
    }
    for name in ("agents", "skills", "knowledge"):
        dst_base = targets[name]
        src_dir = src_dirs[name]
        if dst_base is None or not src_dir.exists():
            continue
        if platform.key in ("reasonix", "zcode", "dsh") and name == "skills":
            continue  # derived products are detected via the source fingerprint and regenerated at sync time
        if platform.key in ("codex", "grok") and name in ("agents", "skills"):
            continue  # TOML/SKILL.md are derived products, detected via the source fingerprint and regenerated at sync time
        for item in sorted(src_dir.rglob("*.md")):
            if item.name == ".gitkeep":
                continue
            rel = item.relative_to(src_dir)
            if name == "agents" and rel.parts[0].startswith("short-"):
                continue  # short-form agents are excluded from long-form comparison (consistent with the mutually exclusive filter in the sync_agents long-form branch)
            if name == "knowledge" and rel.parts[0] == "short":
                continue  # knowledge/short/ is short-form source; long-form projects neither deploy nor compare it
            # format-specs deploys flattened on the project side (the FLAT_SUBDIRS convention), so the comparison target drops the subdirectory level
            if name == "knowledge" and rel.parts[0] == "format-specs":
                rel = Path(rel.name)
            target = dst_base / rel
            if name == "agents" and platform.key == "opencode":
                expected = convert_agent_to_platform(item.read_text(encoding="utf-8"),
                                                     platform)
                if not target.exists() or target.read_text(encoding="utf-8") != expected:
                    changed.append(f"{name}/{rel}")
            else:
                if not target.exists() or target.read_bytes() != item.read_bytes():
                    changed.append(f"{name}/{rel}")
    return changed


# ============================================================
# Sync
# ============================================================

def do_sync(project: Path, platform: Platform, is_short=False):
    print(f"Project: {project}")
    print(f"Type: {'short-form' if is_short else 'long-form'}")
    print(f"Source: {SKILL_HOME}")

    latest_ver, _ = get_version_info()
    if latest_ver:
        print(f"Version: {latest_ver}")
    print()

    current_fp = compute_fingerprint()
    stored_fp, stored_ver = read_project_fingerprint(project)

    version_changed = latest_ver and stored_ver and stored_ver != latest_ver

    if stored_fp == current_fp and not version_changed:
        if is_short:
            # Short-form standalone tools are runtime products: even with an unchanged fingerprint they may have been deleted or edited project-side, so redeploy them idempotently
            deploy_standalone_skills(project, SKILL_HOME, platform,
                                     SHORT_STANDALONE_SKILLS)
        print("[i] Already up to date; no sync needed.")
        return

    changes = []
    changes.append(sync_agents(project, platform, is_short))
    changes.append(sync_skills(project, platform, is_short))
    changes.append(sync_knowledge(project, platform, is_short))
    if not is_short:
        # Short-form projects have no long-form scaffolding or distillation assets (the settings/ volume/chapter system does not exist)
        changes.append(sync_scaffold(project, platform))
        changes.append(sync_style_assets(project))
    changes.append(sync_tools(project, platform))

    total = sum(c for c in changes if c > 0)

    if total > 0 or stored_fp != current_fp or version_changed:
        write_project_fingerprint(project, current_fp, latest_ver)

    print(f"\nDone. Synced {total} files in total. Version: {latest_ver or 'unknown'}")
    if total > 0:
        print("Tip: takes effect at the next writing session.")


SHORT_AGENT_PREFIX = "short-"
SHORT_SHARED_AGENTS = {"reader"}


def sync_agents(project_path: Path, platform: Platform, is_short=False) -> int:
    """Sync agent definitions to the directory for the current platform (short-form projects sync only the short-form set + reader)"""
    if not AGENT_DIR.exists():
        print("  [!] agents source directory does not exist, skipping")
        return 0
    target = platform.agents_dir(project_path)
    if target is None:
        print(f"  [i] The {platform.label} platform has no agents directory (agents are skills)")
        return 0
    target.mkdir(parents=True, exist_ok=True)
    if platform.key in ("opencode", "codex", "grok"):
        # Converted products (opencode: permission format + reference rewriting; codex: TOML; grok: agent Markdown);
        # the conversion logic is single-sourced in platforms.convert_agent_to_platform (same as init.deploy_agents)
        count = 0
        for item in sorted(AGENT_DIR.rglob("*.md")):
            if item.name == ".gitkeep":
                continue
            if is_short != (item.stem.startswith(SHORT_AGENT_PREFIX) or item.stem in SHORT_SHARED_AGENTS):
                continue    # long/short agent sets are mutually exclusive: short-form projects sync only the short-form set + reader, long-form projects only the long-form set
            rel = item.relative_to(AGENT_DIR)
            dest = target / (item.stem + ".toml") if platform.key == "codex" else target / rel
            content = convert_agent_to_platform(item.read_text(encoding="utf-8"),
                                                platform, SKILL_HOME)
            if dest.exists() and dest.read_text(encoding="utf-8") == content:
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(content, encoding="utf-8")
            count += 1
    else:
        count = _sync_dir(
            AGENT_DIR, target, "*.md",
            skip=lambda p: is_short != (p.stem.startswith(SHORT_AGENT_PREFIX) or p.stem in SHORT_SHARED_AGENTS))
    if count > 0:
        print(f"  [OK] agent definitions: {count} files updated ({platform.root}/agents)")
    else:
        print("  [i] agent definitions: already up to date")
    return count


def sync_skills(project_path: Path, platform: Platform, is_short=False) -> int:
    if is_short:
        n = 0
        if platform.key in ("reasonix", "zcode", "dsh"):
            # Short-form inline skills are derived products: regenerate (6 agents + 2 standalone tools)
            deploy_inline_skills(project_path, SKILL_HOME, platform, "short")
            n = len(list(platform.skills_dir(project_path).rglob("SKILL.md")))
            print(f"  [OK] {platform.key} skills: {n} SKILL.md files regenerated (short-form set)")
        else:
            # Standalone tools (ranking-scan / text-teardown) redeploy idempotently; other short-form SOPs are inlined in agents and need no sync
            n = deploy_standalone_skills(project_path, SKILL_HOME, platform,
                                         SHORT_STANDALONE_SKILLS)
            print(f"  [OK] standalone tools: {n} updated" if n else "  [i] standalone tools: already up to date")
        return n
    if platform.key in ("reasonix", "zcode", "dsh"):
        deploy_inline_skills(project_path, SKILL_HOME, platform)
        n = len(list(platform.skills_dir(project_path).rglob("SKILL.md")))
        print(f"  [OK] {platform.key} skills: {n} SKILL.md files regenerated")
        return n
    if platform.key in ("codex", "grok"):
        deploy_codex_skills(project_path, SKILL_HOME, platform)
        n = len(list(platform.skills_dir(project_path).rglob("SKILL.md")))
        print(f"  [OK] {platform.key} skills: {n} SKILL.md files regenerated")
        return n
    target = platform.skills_dir(project_path)
    target.mkdir(parents=True, exist_ok=True)
    if not SKILL_DIR.exists():
        print("  [!] skills source directory does not exist, skipping")
        return 0
    count = _sync_dir(SKILL_DIR, target, "*.md")
    if count > 0:
        print(f"  [OK] skill files: {count} files updated")
    else:
        print("  [i] skill files: already up to date")
    return count


def _sync_short_knowledge(project_path: Path, platform: Platform, target) -> int:
    """Short-form knowledge sync: same layout as init.deploy_knowledge(short)."""
    src_root = SKILL_HOME / "knowledge" / "short"
    if not src_root.exists():
        print("  [!] knowledge/short source directory does not exist, skipping")
        return 0
    count = 0
    anti_ai_src = src_root / "anti-ai" / "short-deslop.md"
    if anti_ai_src.exists():
        dst = target / "short-anti-ai.md"
        content = anti_ai_src.read_text(encoding="utf-8")
        if not dst.exists() or dst.read_text(encoding="utf-8") != content:
            dst.write_text(content, encoding="utf-8")
            print(f"  [+] short-anti-ai.md")
        count += 1
    for sub, dst_name in (("craft", "short-craft"), ("genres", "short-genres")):
        src = src_root / sub
        if src.exists() and src.is_dir():
            dst = target / dst_name
            dst.mkdir(parents=True, exist_ok=True)
            for f in sorted(src.rglob("*.md")):
                rel = f.relative_to(src)
                if _sync_file(f, dst / rel):
                    count += 1
    return count


def sync_knowledge(project_path: Path, platform: Platform, is_short=False) -> int:
    target = platform.knowledge_dir(project_path)
    target.mkdir(parents=True, exist_ok=True)
    if is_short:
        # Short-form projects: short/ sources to short-anti-ai.md + short-craft/ + short-genres/ (same as init.deploy_knowledge)
        return _sync_short_knowledge(project_path, platform, target)
    if not KNOWLEDGE_DIR.exists():
        print("  [!] knowledge source directory does not exist, skipping")
        return 0
    count = 0

    # Directories flattened to the platform knowledge root (the deployment convention matches init.py's deploy_knowledge).
    FLAT_SUBDIRS = {"format-specs"}

    for f in KNOWLEDGE_DIR.glob("*.md"):
        if _sync_file(f, target / f.name):
            count += 1
    for subdir in KNOWLEDGE_DIR.iterdir():
        if subdir.is_dir() and not subdir.name.startswith("."):
            if subdir.name == "short":
                continue  # knowledge/short/ is short-form source; long-form projects do not deploy it (same as init.deploy_knowledge)
            if subdir.name in FLAT_SUBDIRS:
                for f in sorted(subdir.glob("*.md")):
                    if _sync_file(f, target / f.name):
                        count += 1
            else:
                sub_target = target / subdir.name
                sub_target.mkdir(parents=True, exist_ok=True)
                count += _sync_dir(subdir, sub_target, "*.md")
    if count > 0:
        print(f"  [OK] knowledge base: {count} files updated")
    else:
        print("  [i] knowledge base: already up to date")
    return count


def sync_tools(project_path: Path, platform: Platform) -> int:
    """Sync the body-text check scripts to <platform>/tools/ (skip when the source is missing; anti-ai falls back to the model's own eyes)"""
    count = 0
    for name in ("check-prose.py", "check-chapter.py"):
        src = SKILL_HOME / "tools" / name
        if not src.exists():
            continue
        dst = project_path / platform.root / "tools" / name
        if dst.exists() and dst.read_bytes() == src.read_bytes():
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        print(f"  [OK] body-text check script: updated ({platform.root}/tools/{name})")
        count += 1
    return count


def _missing_style_assets(project: Path) -> list[Path]:
    """Style assets missing from the project's settings/ (same deployment scope as sync_style_assets)."""
    missing = []
    src_settings = TEMPLATE_SETTINGS_DIR
    if not src_settings.exists():
        return missing
    candidates = [src_settings / "writing-style.md"]
    profiles = src_settings / "style-profiles"
    if profiles.exists():
        candidates.extend(sorted(profiles.rglob("*.md")))
    for f in candidates:
        if f.is_file():
            rel = f.relative_to(src_settings)
            if not (project / "settings" / rel).exists():
                missing.append(rel)
    return missing


def sync_scaffold(project: Path, platform: Platform) -> int:
    """Sync the templates/ root scaffolding (CLAUDE.md/AGENTS.md/.agent/status.md and friends) to the project root.

    Same rules as init.py create_skeleton: only CLAUDE.md/AGENTS.md/AGENTS.codex.md refresh with the templates (overwritten);
    other files (.agent/status.md, .agent/task/* and the rest) are not overwritten. status.md only has its skill_version line
    updated when it exists (review #17: without fingerprinting/syncing scaffolding, existing projects' CLAUDE.md would forever
    say "8 agents" and skill_version would never update). Skip migration/ and settings/ (settings is handled by sync_style_assets);
    platform special cases (codex has no CLAUDE.md; AGENTS.md uses the AGENTS.codex.md template).
    """
    import re as _re
    src = SKILL_HOME / "templates"
    if not src.exists():
        return 0
    try:
        from init import _GENERATED_SCAFFOLD, _rewrite_template_refs
    except ImportError:
        _GENERATED_SCAFFOLD = None
        _rewrite_template_refs = None
    generated = _GENERATED_SCAFFOLD if _GENERATED_SCAFFOLD is not None \
        else {"CLAUDE.md", "AGENTS.md", "AGENTS.codex.md"}
    status_tpl = src / ".agent" / "status.md"
    status_ver = None
    if status_tpl.is_file():
        m = _re.search(r"- \*\*skill_version:\*\*\s*(\S+)", status_tpl.read_text(encoding="utf-8"))
        if m:
            status_ver = m.group(1)
    count = 0
    for item in sorted(src.rglob("*")):
        if not item.is_file() or item.name == ".gitkeep":
            continue
        rel = item.relative_to(src)
        if rel.parts[0] in ("migration", "settings", "short"):
            continue  # the short subtree is the standalone short-form template tree; long-form project scaffolding does not copy it (same as init.create_skeleton)
        target = project / rel
        # .agent/status.md: project status is not overwritten, only its skill_version line is updated
        if item.name == "status.md" and target.exists() and status_ver:
            cur = target.read_text(encoding="utf-8")
            new = _re.sub(r"- \*\*skill_version:\*\*.*", f"- **skill_version:** {status_ver}", cur, count=1)
            if new != cur:
                target.write_text(new, encoding="utf-8")
                count += 1
            continue
        if target.exists() and item.name not in generated:
            continue          # non-scaffold-generated files are not overwritten (project status / task templates and the rest)
        if platform.key == "codex" and item.name == "CLAUDE.md":
            continue
        if item.name == "AGENTS.codex.md":
            continue          # template source, not copied directly into the project
        if platform.key == "codex" and item.name == "AGENTS.md":
            codex_tpl = src / "AGENTS.codex.md"
            if not codex_tpl.exists():
                continue
            content = codex_tpl.read_text(encoding="utf-8")
        else:
            content = item.read_text(encoding="utf-8")
        if _rewrite_template_refs is not None and item.name in ("CLAUDE.md", "AGENTS.md") \
                and platform.key != "claude":
            content = _rewrite_template_refs(content, platform)
        if target.exists() and target.read_text(encoding="utf-8") == content:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        count += 1
    if count > 0:
        print(f"  [OK] project scaffolding: {count} files updated (CLAUDE.md/AGENTS.md/skill_version and friends)")
    return count


def sync_style_assets(project: Path) -> int:
    """Sync style-distiller assets: main card + scene cards + genre-baselines (pure reference, no runtime references) + the old-card migration hook.

    Only fill in missing files (never overwrite existing ones), with the same semantics as init.py's seed guard:
    upgrades/migrations must not break a writing-style card the user has edited.

    Scope is strictly limited to style assets (templates/settings/writing-style.md + style-profiles/**);
    non-style templates such as world-setting/genre-setting/timeline/foreshadowing are not deployed (those travel with the init
    skeleton and contain unseeded {..} placeholders, which this function must not inject).
    """
    count = 0
    src_settings = TEMPLATE_SETTINGS_DIR
    if src_settings.exists():
        # Main card + style-profiles tree (scene cards + genre-baselines, pure reference, no runtime references)
        candidates = [src_settings / "writing-style.md"]
        profiles = src_settings / "style-profiles"
        if profiles.exists():
            candidates.extend(sorted(profiles.rglob("*.md")))
        for f in candidates:
            if not f.is_file():
                continue
            rel = f.relative_to(src_settings)
            dst = project / "settings" / rel
            if not dst.exists():
                dst.parent.mkdir(parents=True, exist_ok=True)
                content = f.read_text(encoding="utf-8")
                if rel == Path("writing-style.md"):
                    # Main card missing: do not write a bare {role} placeholder template (review #15); placeholders would be injected with prompts,
                    # use the "（待设定）" placeholder value instead, to be filled in during setup
                    for tok in ("{role}", "{principle_1}", "{mistake_1}", "{depiction_techniques}"):
                        content = content.replace(tok, "（待设定）")
                dst.write_text(content, encoding="utf-8")
                count += 1
    try:
        from init import migrate_writing_style   # init.py main has a __main__ guard, so importing is safe
        migrate_writing_style(project)
    except ImportError as e:
        print(f"  [SKIP] style-card migration skipped (init import failed): {e}")
    if count:
        print(f"  [OK] style assets synced: {count} new files")
    return count


def _sync_dir(src: Path, dst: Path, pattern: str, skip=None) -> int:
    count = 0
    for item in sorted(src.rglob(pattern)):
        if item.name == ".gitkeep":
            continue
        if skip is not None and skip(item):
            continue
        rel = item.relative_to(src)
        target = dst / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        if _sync_file(item, target):
            count += 1
    return count


def _sync_file(src: Path, dst: Path) -> bool:
    if dst.exists() and dst.read_bytes() == src.read_bytes():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


if __name__ == "__main__":
    main()
