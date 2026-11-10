#!/usr/bin/env python3
"""
awesome-novel-agent project initialization tool

Usage: python init.py [project-path] [--genre <number>] [--platform <claude|opencode|reasonix|codex|zcode|dsh|grok>]

Platform default: --platform, then NOVEL_PLATFORM, then SKILL_HOME path detection, then claude.

Copy agent definitions, genre knowledge, and memory rules from the skill repository into the user's project directory,
creating a complete novel-writing project skeleton.

With no arguments, initialize in the current directory.
"""

import sys
import os
import re
import shutil
from pathlib import Path

from platforms import (
    Platform,
    convert_agent_to_platform,
    detect_platform,
    deploy_codex_agents,
    deploy_codex_skills,
    deploy_inline_skills,
    deploy_standalone_skills,
    SHORT_STANDALONE_SKILLS,
    deploy_standalone_skills,
    ensure_yaml,
    rewrite_refs,
    resolve_skill_home,
)

from style_common import frontmatter_text   # frontmatter single-source parsing (review #35/#38)

# Force UTF-8 encoding to avoid garbled Chinese on Windows terminals
for s in (sys.stdin, sys.stdout, sys.stderr):
    try:
        s.reconfigure(encoding="utf-8")
    except AttributeError:
        pass


# Keep in sync with the knowledge/genre-example/index.md genre registry (index is the authoritative source).
# Note: some genre IDs reuse the same corpus file (e.g. urban-* maps to urban.md); a missing same-name file is normal.
GENRES = [
    "xianxia", "xuanhuan", "urban", "urban-romance", "urban-daily",
    "urban-farming", "urban-brained", "urban-cultivation", "urban-high-martial",
    "war-god", "western-fantasy", "ancient-politics", "historical",
    "historical-ancient", "historical-brained", "anti-japanese-war",
    "scifi-apocalypse", "suspense-crime", "suspense-paranormal", "suspense-brained",
    "game-sports", "anime-derivative", "derivative", "male-derivative",
]

# Genre display names (shown to the author; one-to-one with GENRES; same source as the knowledge/genre-example files)
GENRE_LABELS = {
    "xianxia": "Eastern Xianxia (xianxia, immortal-hero fantasy)",
    "xuanhuan": "Traditional Xuanhuan (xuanhuan, Eastern fantasy)",
    "urban": "Urban (general)",
    "urban-romance": "Urban Romance",
    "urban-daily": "Urban Daily Life",
    "urban-farming": "Urban Farming",
    "urban-brained": "Urban Brainstorm",
    "urban-cultivation": "Urban Cultivation",
    "urban-high-martial": "Urban High Martial",
    "war-god": "War God Son-in-Law",
    "western-fantasy": "Western Fantasy",
    "ancient-politics": "Ancient Political Intrigue",
    "historical": "Historical (general)",
    "historical-ancient": "Historical Ancient",
    "historical-brained": "Historical Brainstorm",
    "anti-japanese-war": "War of Resistance Espionage",
    "scifi-apocalypse": "Sci-Fi Apocalypse",
    "suspense-crime": "Suspense Crime",
    "suspense-paranormal": "Suspense Paranormal",
    "suspense-brained": "Suspense Brainstorm",
    "game-sports": "Gaming and Sports",
    "anime-derivative": "Anime Derivative",
    "derivative": "Derivative (general)",
    "male-derivative": "Male-Oriented Derivative",
}

# Short-form genres (the numbering space for --length short; same source as the knowledge/short/genres/index.md registry, where index is authoritative).
SHORT_GENRES = ["zhuiqi", "shiqing", "fuchou", "zongcai", "zhaidou",
                "minsu", "xuanyi", "tianchong", "shuangnan", "shadiao"]
SHORT_GENRE_LABELS = {
    "zhuiqi": "Chasing Wife Crematorium",
    "shiqing": "Everyday Life 打脸 (face-slapping)",
    "fuchou": "Revenge 打脸 (face-slapping)",
    "zongcai": "CEO Romance",
    "zhaidou": "Inner-Courtyard Intrigue",
    "minsu": "Folk Tales and Strange Stories",
    "xuanyi": "Suspense",
    "tianchong": "Sweet Romance",
    "shuangnan": "Two Male Leads",
    "shadiao": "Absurd Comedy",
}

# Long-form and short-form agent sets are mutually exclusive (the first short-form wave only ships the claude product chain; other platforms follow in later builds).
SHORT_AGENTS = ("short-agent", "short-planner", "short-writer", "short-editor", "short-verifier", "reader")

# Anti-AI rules are reused across genres (declared in the "适用题材" comment at the top of each genre file; a missing same-name file is by design)
_ANTI_AI_REUSE = {
    "urban-cultivation": "urban-brained",
    "urban-high-martial": "urban-brained",
}

SKILL_HOME = resolve_skill_home()

SOURCE_AGENTS = SKILL_HOME / "agents"
SOURCE_KNOWLEDGE = SKILL_HOME / "knowledge"
SOURCE_TEMPLATES = SKILL_HOME / "templates"
SOURCE_ANTI_AI = SKILL_HOME / "knowledge" / "anti-ai"
SOURCE_GENRE_EXAMPLE = SKILL_HOME / "knowledge" / "genre-example"
SOURCE_FORMAT_SPECS = SKILL_HOME / "knowledge" / "format-specs"


def main():
    args = sys.argv[1:]
    if "-h" in args or "--help" in args:
        print(__doc__.strip())
        return

    project_arg = None
    platform_override = None
    genre_num = None
    length = None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--platform":
            if i + 1 >= len(args) or args[i + 1].startswith("--"):
                print("Error: --platform needs a platform name (claude|opencode|reasonix|codex|zcode|dsh|grok)")
                sys.exit(1)
            platform_override = args[i + 1]
            i += 2
            continue
        if a == "--length":
            if i + 1 >= len(args) or args[i + 1] not in ("short", "long"):
                print("Error: --length needs a length value (short|long)")
                sys.exit(1)
            length = args[i + 1]
            i += 2
            continue
        if a == "--genre":
            if i + 1 < len(args) and not args[i + 1].startswith("--"):
                genre_num = args[i + 1]
                i += 2
                continue
            print("Error: --genre needs a genre number")
            sys.exit(1)
        if not a.startswith("--") and project_arg is None:
            project_arg = a
        i += 1

    project_path = Path(project_arg).resolve() if project_arg else Path.cwd()
    platform_override = platform_override or os.environ.get("NOVEL_PLATFORM")
    try:
        platform = detect_platform(SKILL_HOME, platform_override)
    except ValueError as e:
        print(e)
        sys.exit(1)
    ensure_yaml(platform)
    print(f"Platform: {platform.label}")

    # Parse the optional arguments
    genre = None
    if genre_num is not None:
        if length == "short":
            pool = SHORT_GENRES
            if not genre_num.isdigit() or not (1 <= int(genre_num) <= 10):
                print("Invalid genre number; short-form options are 1-10")
                sys.exit(1)
            genre = pool[int(genre_num) - 1]
        else:
            try:
                genre = GENRES[int(genre_num) - 1]
            except (IndexError, ValueError):
                print(f"Invalid genre number; options are 1-{len(GENRES)}")
                sys.exit(1)
    if length == "short":
        if genre is None:
            genre = select_genre(SHORT_GENRES, SHORT_GENRE_LABELS)
        else:
            print(f"Genre: {SHORT_GENRE_LABELS.get(genre, genre)} ({genre})")

    if project_path.exists():
        # Long/short mixing guard: reject when the existing project type differs from this run's --length (directories and flows are mutually exclusive)
        existing_story = project_path / "story.md"
        if existing_story.exists():
            has_short = "**length:** short" in existing_story.read_text(encoding="utf-8")
            if has_short != (length == "short"):
                kind_exist = "short-form" if has_short else "long-form"
                kind_now = "short-form" if length == "short" else "long-form"
                print(f"Error: this directory is already a {kind_exist} project (the story.md type marker does not match),"
                      f"it cannot be re-initialized with the {kind_now} flow; please use another directory or keep the original flow")
                sys.exit(1)
        print("Directory already exists; missing files and directories will be created in it")
    else:
        project_path.mkdir(parents=True)

    print(f"Initializing novel project: {project_path}")
    print(f"Skill repository: {SKILL_HOME}")

    # Step 1: Pick a genre (no interactive picking for short-form length; the first short-form registry wave has only 1 item, already parsed above)
    if length != "short":
        if genre is None:
            genre = select_genre()
        else:
            print(f"Genre: {GENRE_LABELS.get(genre, genre)} ({genre})")
        gaps = _genre_gaps(genre)
        if gaps:
            print(f"  ⚠️ The knowledge base for this genre is incomplete: {', '.join(gaps)}"
                  f"(genres marked with ⚠️ in the picker have the same gaps; the author needs to fill them in during the setup phase)")

    # Step 1.5: Old 4-field writing-style.md to the new format (must run before template copying / genre pre-fill, or the old card gets overwritten)
    if length != "short":
        migrate_writing_style(project_path)

    # Step 2: Create the skeleton
    create_skeleton(project_path, platform, length)

    # Step 3: Deploy agent definitions (codex uses TOML-converted products; for reasonix/zcode/dsh the agents are the skills)
    if platform.key == "codex":
        deploy_codex_agents(project_path, SKILL_HOME, platform, length)
    else:
        deploy_agents(project_path, platform, length)

    # Step 3.5: Deploy platform skills (reasonix/zcode/dsh generate an inline SKILL.md; codex/grok only deploy standalone tools)
    if platform.key in ("codex", "grok"):
        deploy_codex_skills(project_path, SKILL_HOME, platform, length)
    else:
        deploy_inline_skills(project_path, SKILL_HOME, platform, length)   # non-inline platforms skip this internally

    # Step 3.6: Short-form standalone tools (ranking-scan/text-breakdown), triggered by the author, not part of the dispatch chain (inline platforms already deployed them in 3.5)
    if length == "short":
        n = deploy_standalone_skills(project_path, SKILL_HOME, platform, SHORT_STANDALONE_SKILLS)
        if n:
            print(f"  ✅ Deployed short-form standalone tools ({n}: {'/'.join(SHORT_STANDALONE_SKILLS)})")

    # Step 4: Inherit knowledge for the genre
    deploy_knowledge(project_path, genre, platform, length)

    # Step 4.5: Deploy the body-text check scripts (for anti-ai machine first-pass; falls back to the model's own eyes when missing)
    deploy_tools(project_path, platform)

    if length != "short":
        # Step 5.5: Pre-fill settings defaults for the genre
        seed_settings_from_genre(project_path, genre, platform)

        # Step 6: Generate the MEMORY.md index
        write_memory_index(project_path, platform)

        # Step 7: Initialize the writing-memory files
        init_memory_files(project_path, platform)

        # Step 8: Initialize the status
        write_status(project_path)
    else:
        # Short-form status file (the short-form state machine, shipped with the template and copied with the skeleton)
        if (project_path / ".agent" / "status.md").exists():
            print("  ✅ Short-form status file is ready (.agent/status.md)")
        else:
            print("  ⚠️ Missing .agent/status.md; the state-machine file was not generated. Please check templates/short/")

        # Cross-story author preference memory (read when assembling contracts, appended after delivery)
        feedback = platform.memory_dir(project_path) / "author-feedback.md"
        if not feedback.exists():
            feedback.write_text(
                "# 跨篇作者偏好记忆\n\n"
                "> Preferences confirmed by the author after short-story delivery, appended by short-agent at delivery time;\n"
                "> short-planner takes the \"作者偏好记忆\" field of the assembled contract from here.\n\n"
                "---\n\n## 条目列表\n",
                encoding="utf-8")
            print(f"  ✅ Initialized cross-story preference memory ({platform.root}/memory/author-feedback.md)")

    print("\nInitialization complete!")
    print(f"Project path: {project_path}")
    if length == "short":
        print("Type @short-agent to start writing, or just say \"help me write a short story\"")
    elif platform.key == "claude":
        print("Type @novel-agent to start writing (Claude Code)")
    elif platform.key == "opencode":
        print("Start writing in OpenCode via @novel-agent")
    elif platform.key == "codex":
        print("Open the project directory in Codex and call @novel-agent to start writing")
    elif platform.key == "zcode":
        print("Open the project directory in ZCode, say \"help me write a novel\", or call the novel-agent skill to start writing")
    elif platform.key == "dsh":
        print("Open the project directory in DeepSeek Harness (dsh), say \"help me write a novel\", or call the novel-agent skill to start writing")
    elif platform.key == "grok":
        print("Open the project directory in Grok Build, type /awesome-novel, or say \"help me write a novel\" to start writing")
    else:
        print("In Reasonix, run `reasonix code`, then call @novel-agent to start writing")


def _genre_gaps(genre: str) -> list:
    """Genre support gaps (missing knowledge-base files) to a list of gap labels; empty means complete.

    Anti-AI rules may be reused across genres (see the "适用题材" comment in the corresponding _ANTI_AI_REUSE file).
    The picker labels and deployment warnings share this list, so an empty-shell genre is never picked silently.
    """
    gaps = []
    if not (SOURCE_GENRE_EXAMPLE / f"{genre}.md").exists():
        gaps.append("genre file to be added")
    if genre not in _ANTI_AI_REUSE and not (SOURCE_ANTI_AI / f"{genre}.md").exists():
        gaps.append("anti-AI rules to be added")
    return gaps


def select_genre(pool=None, labels=None) -> str:
    """Pick a genre interactively (genres with incomplete knowledge bases are marked with their gaps, so an empty shell is never picked silently)"""
    pool = pool if pool is not None else GENRES
    labels = labels if labels is not None else GENRE_LABELS
    print("\nAvailable genres:")
    for i, g in enumerate(pool, 1):
        gaps = _genre_gaps(g) if pool is GENRES else []
        mark = f"　⚠️ {', '.join(gaps)}" if gaps else ""
        print(f"  {i:2d}. {labels[g]} ({g}){mark}")

    while True:
        try:
            choice = input("\nChoose a genre number: ").strip()
        except EOFError:
            # Non-interactive environment (AI terminal/pipe): fall back to registry no. 1 with an explicit note, not a bare traceback
            print("\nNon-interactive environment, cannot pick a genre interactively; using genre no. 1 ("
                  f"{labels[pool[0]]}). For another genre, pass --genre 1-{len(pool)} explicitly")
            return pool[0]
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(pool):
                return pool[idx]
        except ValueError:
            pass
        print("Invalid choice, please try again")


def _rewrite_template_refs(text: str, platform: Platform) -> str:
    """Rewrite Claude Code/OpenCode path references in project templates to platform paths. claude is returned as-is."""
    if platform.key == "claude":
        return text
    if platform.key == "reasonix":
        text = text.replace(".claude/agents/", ".reasonix/skills/")
        text = text.replace(".opencode/agents/", ".reasonix/skills/")
    elif platform.key == "zcode":
        text = text.replace(".claude/agents/", ".zcode/skills/")
        text = text.replace(".opencode/agents/", ".zcode/skills/")
    elif platform.key == "dsh":
        text = text.replace(".claude/agents/", ".dsh/skills/")
        text = text.replace(".opencode/agents/", ".dsh/skills/")
    elif platform.key == "codex":
        text = text.replace(".claude/agents/", ".codex/agents/")
        text = text.replace(".opencode/agents/", ".codex/agents/")
    else:  # opencode / grok and other standalone agents directories
        text = text.replace(".claude/agents/", f"{platform.root}/agents/")
        text = text.replace(".opencode/agents/", f"{platform.root}/agents/")
    return rewrite_refs(text, platform)


# Root-level scaffolding (platform agent configs / template products) refreshes with the templates; user content under settings/ and elsewhere is never overwritten
_GENERATED_SCAFFOLD = {"CLAUDE.md", "AGENTS.md", "AGENTS.codex.md"}


def create_skeleton(project_path: Path, platform: Platform, length=None):
    """Create the project directory structure. When length=short, the template tree root switches to templates/short/, and the directory set switches with the length."""
    short = length == "short"
    template_root = SOURCE_TEMPLATES / "short" if short else SOURCE_TEMPLATES
    if short:
        dirs = [
            "stories",
            "sandbox",
            ".agent/task",
            "tools",
            str(platform.memory_dir(project_path)),
            str(platform.knowledge_dir(project_path)),
        ]
    else:
        dirs = [
            "settings/character-setting",
            "volumes",
            "chapters",
            "prompts",
            "sandbox",
            "novel-samples",    # style-distillation samples (the author puts articles to distill here; for style-distill only)
            "archives",
            ".agent/task",
            "tools",
            str(platform.memory_dir(project_path)),
            str(platform.knowledge_dir(project_path)),
        ]
    for d in dirs:
        (project_path / d).mkdir(parents=True, exist_ok=True)

    # Copy template files into project (the short tree has no migration/; the long tree skips migration/)
    if template_root.exists():
        for item in template_root.rglob("*"):
            if item.is_file() and item.name != ".gitkeep":
                rel_path = item.relative_to(template_root)
                if not short and rel_path.parts[0] == "migration":
                    continue
                if not short and rel_path.parts[0] == "short":
                    continue          # templates/short/ is the standalone short-form template tree; long-form projects do not copy it
                # Path-traversal defense: normalize first (resolve symlinks/..), then verify the target is inside the project root
                target = (project_path / rel_path).resolve()
                if not target.is_relative_to(project_path.resolve()):
                    continue
                if target.exists() and item.name not in _GENERATED_SCAFFOLD:
                    continue          # Never overwrite existing files (settings/ and other user content); scaffold files refresh with the templates
                target.parent.mkdir(parents=True, exist_ok=True)
                if platform.key == "codex" and item.name == "CLAUDE.md":
                    # Codex projects do not generate CLAUDE.md (Codex only reads AGENTS.md)
                    continue
                if item.name == "AGENTS.codex.md":
                    # The template source is only used to generate a codex project's AGENTS.md, not copied into the project
                    continue
                if platform.key == "codex" and item.name == "AGENTS.md":
                    codex_tpl = template_root / "AGENTS.codex.md"
                    if codex_tpl.exists():
                        content = codex_tpl.read_text(encoding="utf-8")
                        content = _rewrite_template_refs(content, platform)
                        target.write_text(content, encoding="utf-8")
                        continue
                if item.name in ("CLAUDE.md", "AGENTS.md") and platform.key != "claude":
                    with open(item, encoding="utf-8", newline="") as f:
                        content = f.read()
                    content = _rewrite_template_refs(content, platform)
                    target.write_text(content, encoding="utf-8")
                else:
                    shutil.copy2(item, target)
        print("  ✅ Project templates copied")


def deploy_agents(project_path: Path, platform: Platform, length=None):
    """Copy agent definitions to the right directory for the current platform. When length=short, only the short-form agent set is deployed."""
    if not SOURCE_AGENTS.exists():
        print("  ⚠️  agent directory does not exist, skipping")
        return
    agent_dir = platform.agents_dir(project_path)
    if agent_dir is None:
        # reasonix/zcode: the agents are the skills (generated by deploy_*_skills); .claude/agents is not deployed
        print(f"  ℹ️  The {platform.label} platform does not deploy agent definitions (the agents are {platform.root}/skills/)")
        return
    agent_dir.mkdir(parents=True, exist_ok=True)
    for item in SOURCE_AGENTS.rglob("*"):
        if item.is_file() and item.suffix == ".md":
            if length == "short" and item.stem not in SHORT_AGENTS:
                continue    # short-form projects do not deploy long-form-only agents
            if length != "short" and item.stem.startswith("short-"):
                continue    # long-form projects do not deploy short-form-only agents (the long/short agent sets are mutually exclusive)
            rel_path = item.relative_to(SOURCE_AGENTS)
            dest = agent_dir / rel_path
            # Path-traversal defense: after normalization the target must still be inside the agent directory (prevents symlink/.. escapes)
            if not dest.resolve().is_relative_to(agent_dir.resolve()):
                continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            content = convert_agent_to_platform(
                item.read_text(encoding="utf-8"), platform, SKILL_HOME)
            dest.write_text(content, encoding="utf-8")
    print(f"  ✅ Agent definitions deployed to {agent_dir}")


def deploy_tools(project_path: Path, platform: Platform):
    """Deploy the body-text check scripts to <platform>/tools/ (for anti-ai machine first-pass and chapter-delivery checks; falls back to the model's own eyes when missing)"""
    dst_dir = project_path / platform.root / "tools"
    dst_dir.mkdir(parents=True, exist_ok=True)
    for name, missing_hint in (
        ("check-prose.py", "anti-ai machine first-pass will fall back to the model's own eyes"),
        ("check-chapter.py", "chapter-delivery hard-defect checks unavailable"),
    ):
        src = SKILL_HOME / "tools" / name
        if not src.exists():
            print(f"  ⚠️  Missing tools/{name}: {missing_hint}")
            continue
        shutil.copy2(src, dst_dir / name)
        print(f"  ✅ Body-text check script deployed ({platform.root}/tools/{name})")


def deploy_knowledge(project_path: Path, genre: str, platform: Platform, length=None):
    """Copy reference material + anti-AI/style rules for the genre to <platform>/knowledge/. Short length uses the short-form knowledge base branch."""
    knowledge_dir = platform.knowledge_dir(project_path)
    count = 0

    if length == "short":
        # Short-form: the short-form knowledge base deploys independently, not merged with long-form anti-AI products
        src_root = SKILL_HOME / "knowledge" / "short"
        anti_ai_src = src_root / "anti-ai" / "short-deslop.md"
        if anti_ai_src.exists():
            # Write the source file contents directly to disk (the source carries its own H1 title), matching the sync._sync_short_knowledge layout
            shutil.copy2(anti_ai_src, knowledge_dir / "short-anti-ai.md")
            count += 1
            print("  ✅ Short-form anti-AI rules deployed (short-anti-ai.md)")
        else:
            print("  ⚠️  Missing knowledge/short/anti-ai/short-deslop.md: short-form de-AI rules are missing")
        for sub in ("craft", "genres"):
            src = src_root / sub
            if src.exists() and src.is_dir():
                dst = knowledge_dir / ("short-craft" if sub == "craft" else "short-genres")
                shutil.copytree(src, dst, dirs_exist_ok=True)
                n = sum(1 for _ in src.rglob("*") if _.is_file())
                count += n
                print(f"  ✅ Deployed short-{sub}/ ({n} files)")
        print(f"  ✅ Short-form knowledge deployment complete ({count} files)")
        return

    # Copy format specs from knowledge/format-specs/
    if SOURCE_FORMAT_SPECS.exists():
        for f in SOURCE_FORMAT_SPECS.glob("*.md"):
            shutil.copy2(f, knowledge_dir / f.name)
            count += 1

    # Genre examples
    genre_example_src = SOURCE_GENRE_EXAMPLE / f"{genre}.md"
    if genre_example_src.exists():
        shutil.copy2(genre_example_src, knowledge_dir / "genre-example.md")
        count += 1
    else:
        print(f"  ⚠️  Missing genre file knowledge/genre-example/{genre}.md;"
              f"genre-example.md will not be generated, and settings keeps placeholders (please fill them in with the author during setup)")

    # Anti-AI rules: positive method + general + genre + methodology + false-positive protection + structural heat (merged into a single anti-ai.md)
    # Note: living-voice / common-rules / anti-ai-writing / boundary-cases / structural-heat
    #     are required inputs for the anti-ai agent, merged together into .claude/knowledge/anti-ai.md
    #     to avoid multiple dead paths after deployment.
    #     living-voice goes first: the positive methodology (what the writing should look like) is pinned at the top, followed by the ban list.
    anti_ai_content = []
    anti_ai_content.append("# Anti-AI Rules\n\n[community-defaults]\n")
    for fname in ("living-voice.md", "common-rules.md", "anti-ai-writing.md",
                  "boundary-cases.md", "structural-heat.md"):
        f = SOURCE_ANTI_AI / fname
        if f.exists():
            anti_ai_content.append(f"\n---\n\n{f.read_text(encoding='utf-8')}")

    genre_rules = SOURCE_ANTI_AI / f"{genre}.md"
    if genre_rules.exists():
        anti_ai_content.append(f"\n---\n\n[community-defaults] Genre: {genre}\n")
        anti_ai_content.append(genre_rules.read_text(encoding="utf-8"))
    elif genre in _ANTI_AI_REUSE:
        reuse = _ANTI_AI_REUSE[genre]
        anti_ai_content.append(
            f"\n---\n\n[community-defaults] Genre: {genre} (reusing rules from {reuse}.md)\n"
        )
        anti_ai_content.append(
            (SOURCE_ANTI_AI / f"{reuse}.md").read_text(encoding="utf-8")
        )
    else:
        print(f"  ⚠️  Missing genre anti-AI rules knowledge/anti-ai/{genre}.md; only the general rules are inherited"
              f"(when this genre is picked, anti-AI checks have no genre-specific positive/negative examples)")

    if anti_ai_content:
        (knowledge_dir / "anti-ai.md").write_text(
            "\n".join(anti_ai_content), encoding="utf-8"
        )
        count += 1
        print(f"  ✅ Anti-AI rules inherited (general + {genre})")

    # Permanent-memory placeholder file (empty; the updater fills it by promotion later)
    permanent_memory = knowledge_dir / "permanent-memory.md"
    if not permanent_memory.exists():
        content = rewrite_refs(
            "# 永久记忆\n\n> High-frequency entries promoted from .claude/memory/."
            "The content format matches memory entries, maintained by the updater during fallback sweeps.\n\n"
            "---\n\n## 条目列表\n",
            platform,
        )
        permanent_memory.write_text(content, encoding="utf-8")
        count += 1

    # Writing-methodology directories (plot-craft / scene-craft / character-craft / title-craft)
    craft_dirs = ["plot-craft", "scene-craft", "character-craft", "title-craft"]
    for dir_name in craft_dirs:
        src = SOURCE_KNOWLEDGE / dir_name
        if src.exists() and src.is_dir():
            dst = knowledge_dir / dir_name
            shutil.copytree(src, dst, dirs_exist_ok=True)
            file_count = sum(1 for _ in src.rglob("*") if _.is_file())
            count += file_count
            print(f"  ✅ Deployed {dir_name}/ ({file_count} files)")

    # style-distill prompt templates (distillation phase 2 / Gate G checklist / injection templates)
    style_distill_src = SKILL_HOME / "knowledge" / "style-distill"
    if style_distill_src.exists():
        dst = knowledge_dir / "style-distill"
        shutil.copytree(style_distill_src, dst, dirs_exist_ok=True)
        count += sum(1 for _ in style_distill_src.rglob("*") if _.is_file())
        print("  ✅ style-distill/ prompt templates deployed")

    print(f"  ✅ Inherited {count} knowledge files")


def _md_section(text: str, title: str) -> str:
    """Extract the body text under a markdown heading (any ## or ### level) up to
    the next same- or higher-level heading.

    title is the bare heading name (without #), e.g. "叙事者角色" or "满足类型".
    Matching rule: a heading line is some # characters + a space + the heading
    name, with an optional trailing #.
    """
    m = re.search(r"^(#{1,6})\s+%s\s*#*\s*$" % re.escape(title), text, re.M)
    if not m:
        return ""
    level = len(m.group(1))
    body = []
    for ln in text[m.end():].splitlines():
        h = re.match(r"^(#{1,6})\s+", ln.strip())
        if h and len(h.group(1)) <= level:
            break
        body.append(ln)
    return "\n".join(body).strip()


def _md_bullets(sec: str) -> list:
    """Extract `- xxx` list-item contents from a markdown paragraph."""
    return [
        ln.strip().lstrip("- ").strip()
        for ln in sec.splitlines()
        if ln.strip().startswith("- ")
    ]


def _style_card_frontmatter() -> str:
    """9-dimension schema, single-sourced (review #35): read from the template
    settings/writing-style.md, so the built-in strings in init cannot drift from
    the template. Falls back to a built-in copy when the template is missing
    (defensive; should not happen)."""
    tpl = SOURCE_TEMPLATES / "settings" / "writing-style.md"
    if tpl.exists():
        fm = frontmatter_text(tpl.read_text(encoding="utf-8-sig"))
        if fm:
            return fm
    return (
        'profile_version: "1.0"\nscene_type: general\nsource_sample_length: 0\n'
        'confidence: 0\nlast_updated: ""\nlocked: []\n\n'
        "# 9 大维度（PRD 定义；0/空 = 未蒸馏，首次蒸馏后由 style-distiller 填充）\n"
        "lexicon: { adj_density_per_100: 0, adv_density_per_100: 0, four_phrase_freq_per_100: 0, preferred_words: [], banned_words: [], name_pronoun_ratio: 0 }\n"
        "syntax: { avg_sentence_length: 0, sentence_length_dist: {}, single_sentence_paragraph_pct: 0, avg_sentences_per_paragraph: 0, question_ratio: 0, exclamation_ratio: 0 }\n"
        "rhythm: { dialogue_pct: 0, action_pct: 0, environment_pct: 0, inner_thought_pct: 0, narration_pct: 0 }\n"
        "rhetoric: { metaphor_density_per_100: 0, metaphor_preference: \"\", sensory_dist: \"\" }\n"
        "emotion_expression: { direct_pct: 0, action_physiology_pct: 0, environment_projection_pct: 0 }\n"
        "narrative: { perspective: \"\", focal_character: \"\", inner_monologue_style: \"\" }\n"
        "dialogue_style: { tag_style: \"\", avg_dialogue_length: 0, interrupt_freq_per_100: 0, subtext_ratio: 0 }\n"
        "cohesion: { conjunction_freq_per_100: 0, transition_sentence_ratio: 0, paragraph_bridge_style: \"\" }\n"
        "verb_style: { action_verb_ratio: 0, mental_verb_ratio: 0, state_verb_ratio: 0, strength: \"\" }"
    )


def _write_new_style_card(path: Path, role: str, principles: list, mistakes: list,
                          depiction: str, seeded: bool = True) -> None:
    """Write a new-format writing-style card (frontmatter quantitative layer +
    body qualitative layer). confidence=0 means prompts use only the
    qualitative layer until the first distillation."""
    prefix = "> [auto-seeded] Pre-filled by init.py for this genre; the quantitative layer is left empty and will be filled by style-distiller after the first distillation.\n\n" if seeded else ""
    principles_txt = "\n".join(f"- {p}" for p in principles) if principles else ("" if not seeded else "- （待设定）")
    mistakes_txt = "\n".join(f"- {m}" for m in mistakes) if mistakes else ("" if not seeded else "- （待设定）")
    content = f"""---
{_style_card_frontmatter()}
---

# 写作风格

{prefix}## 叙事身份（原 role）

{role}

## 硬约束（原 core_principles）

{principles_txt}

## AI 易犯错误（原 possible_mistakes）

{mistakes_txt}

## 描写层次和手法（原 depiction_techniques）

{depiction}

## few-shot 例句

- (signature examples to be filled in by style-distiller after distillation)
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def seed_settings_from_genre(project_path: Path, genre: str, platform: Platform):
    """Pre-fill default values in settings/genre-setting.md + writing-style.md for the genre.

    genre-example/{genre}.md was already copied by deploy_knowledge to
    <platform>/knowledge/genre-example.md. Extract the narrator role / style
    blueprint / genre taboos / genre config from it and replace the placeholders
    under settings/, so writer/prompt-crafter cannot inject raw `{placeholder}`
    into prompts when the setup phase has not run. Output is marked [auto-seeded];
    the updater confirms and adjusts it with the author during setup.
    """
    ex = platform.knowledge_dir(project_path) / "genre-example.md"
    if not ex.exists():
        return
    text = ex.read_text(encoding="utf-8")
    if "placeholder" in text.lower() or len(text.strip()) < 100:
        print(f"  ⚠️  genre-example/{genre}.md is an empty template; settings keeps placeholders (please fill them in during setup)")
        return

    # Genre display name: prefer the title line "# 类型档案：X", fall back to **label:**, then to the Chinese registry name
    label = GENRE_LABELS.get(genre, genre)
    title_m = re.match(r"^#\s+类型档案[:：]\s*(.+)$", text, re.M)
    if title_m:
        title = title_m.group(1).strip()
        if title != "unknown":
            label = title
    else:
        lm = re.search(r"\*\*label:\*\*\s*(\S+)", text)
        if lm:
            label = lm.group(1)

    sat = _md_bullets(_md_section(text, "满足类型"))
    rhythm = _md_section(text, "节奏规则") or "- 待设定"
    clich = _md_bullets(_md_section(text, "反套路"))
    taboo = _md_bullets(_md_section(text, "类型禁忌"))

    # genre-setting.md
    genre_out = [
        "# 题材设定",
        "",
        f"> [auto-seeded] Generated by init.py from genre-example/{genre}.md; please confirm and adjust it with the author during setup.",
        "",
        f"## 选定类型",
        "",
        f"{genre}: {label}",
        "",
        "## 满足类型",
        "",
    ]
    genre_out += [f"- {s}" for s in sat] or ["- （待设定）"]
    genre_out += ["", "## 节奏规则", "", rhythm, "", "## 避免套路", ""]
    genre_out += [f"- {c}" for c in clich] or ["- （待设定）"]
    genre_out += ["", "## 类型禁忌", ""]
    genre_out += [f"- {t}" for t in taboo] or ["- （待设定）"]
    (project_path / "settings" / "genre-setting.md").write_text(
        "\n".join(genre_out) + "\n", encoding="utf-8"
    )

    # writing-style.md to the new format (frontmatter quantitative layer + body qualitative layer)
    # Guard (three states, fixing review #13/#14 misjudgments/overwrites): distinguish bare templates / seed cards / author or migrated cards.
    #   - Bare template (copied by create_skeleton, no [auto-seeded] mark, contains {role} and other placeholders): unfilled, so pre-fill for the genre.
    #   - Seed card (has an [auto-seeded] mark) with leftover placeholders: fill in place (keep the author's edits; never overwrite the whole card).
    #   - Everything else (no mark and no placeholders = author/migrated card; mark but no placeholders = filled seed card): keep as-is, never overwritten by seeding.
    # Note: the frontmatter quantitative layer always contains `{ ... }` inline dicts, so `"{" in text` cannot be used to judge unfilled.
    role = _md_section(text, "叙事者角色") or "（待设定）"
    blueprint = _md_section(text, "文风蓝图") or "（待设定）"
    style_card = project_path / "settings" / "writing-style.md"
    _STYLE_PLACEHOLDERS = ("{role}", "{principle_1}", "{mistake_1}", "{depiction_techniques}")
    _st_text = style_card.read_text(encoding="utf-8") if style_card.exists() else ""
    _seeded_card = "[auto-seeded]" in _st_text
    _has_ph = any(tok in _st_text for tok in _STYLE_PLACEHOLDERS)
    if not _seeded_card and _has_ph:
        # Bare template: pre-fill for the genre (no author content, so rebuilding the whole card is safe)
        _write_new_style_card(
            style_card,
            role=role,
            principles=[blueprint] if blueprint != "（待设定）" else [],
            mistakes=taboo,
            depiction=blueprint if blueprint != "（待设定）" else "",
        )
        print(f"  ✅ Pre-filled settings/genre-setting.md + writing-style.md defaults for the genre ({genre})")
    elif _seeded_card and _has_ph:
        # Seed card with leftover placeholders: fill in place, keeping the author's edits
        _backfill_style_card(style_card, role, blueprint, taboo)
        print("  ✅ Leftover placeholders in writing-style.md filled in place (existing edits kept); genre-setting.md updated for the new genre")
    else:
        print("  ✅ writing-style.md already has real content, so genre pre-fill is skipped (migration/edit results kept); genre-setting.md updated for the new genre")


def _backfill_style_card(path: Path, role: str, blueprint: str, taboo: list) -> None:
    """Fill leftover placeholders in a seed card in place (without overwriting
    the whole card, keeping the author's edits). Used for old cards where a
    seed card fell back to writing {role} and other placeholders when the
    genre file was missing a section."""
    text = path.read_text(encoding="utf-8")
    repl = {
        "{role}": role or "（待设定）",
        "{principle_1}": blueprint or "（待设定）",
        "{mistake_1}": (taboo[0] if taboo else "（待设定）"),
        "{depiction_techniques}": blueprint or "（待设定）",
    }
    for tok, val in repl.items():
        text = text.replace(tok, val)
    path.write_text(text, encoding="utf-8")


def migrate_writing_style(project_path: Path) -> None:
    """Old 4-field writing-style.md to the new format (only when in the old
    format: no frontmatter). The old version is backed up to
    settings/.style-versions/v0_migrated.md."""
    card = project_path / "settings" / "writing-style.md"
    if not card.exists():
        return
    # utf-8-sig: strip the BOM a Windows editor may have written; otherwise BOM+--- is judged as the old format and rewritten empty
    text = card.read_text(encoding="utf-8-sig")
    if text.lstrip().startswith("---"):          # already in the new format
        return
    # Old headings carry a Chinese suffix (e.g. "## role（叙事身份）"); extract by the full heading
    # Paragraph fallback: old seeds wrote core_principles/possible_mistakes as bare paragraphs (not bullets);
    # _md_bullets returns [] when it finds no bullets, and then the whole original paragraph is kept (zero loss).
    # A missing section (_md_section returns empty) falls back to an empty string, not the {role}/{depiction_techniques} placeholders;
    # placeholders would be misjudged as unfilled by the seed guard and overwrite the migration product in the same run.
    role = _md_section(text, "role（叙事身份）") or ""
    _core = _md_section(text, "core_principles（不可违背的写作信条）")
    _mist = _md_section(text, "possible_mistakes（AI 易犯错误）")
    principles = _md_bullets(_core) or ([_core.strip()] if _core.strip() else [])
    mistakes = _md_bullets(_mist) or ([_mist.strip()] if _mist.strip() else [])
    depiction = _md_section(text, "depiction_techniques（描写层次和手法）") or ""
    vers = project_path / "settings" / ".style-versions"
    vers.mkdir(parents=True, exist_ok=True)
    (vers / "v0_migrated.md").write_text(text, encoding="utf-8")
    _write_new_style_card(card, role, principles, mistakes, depiction, seeded=False)
    print("  ✅ Old 4-field writing-style.md migrated to the new format (confidence=0; old version backed up)")


def write_status(project_path: Path):
    """Initialize .agent/status.md"""
    status = """# 项目状态

- **skill_version:** 4.28.0
- **phase:** setup
- **current_step:** setting        # volume-planning / chapter-planning / prompt-crafting / writing / anti-ai / reviewing / archiving
# phase values: setup / outline / draft / anti-ai / review / archive / finished
# last_volume_completed and phase: finished are written by novel-agent (volume-completion decision); the updater does not write completion bits
- **current_volume:**
- **current_chapter:**
- **last_archived:**
- **last_quality_gap:**        # most recent word-count downgrade record (synced by novel-agent from writing-order)
- **next_task:** 填写基础设定（世界观/角色/写作风格）
"""
    (project_path / ".agent" / "status.md").write_text(status, encoding="utf-8")


def write_memory_index(project_path: Path, platform: Platform):
    """Generate the <platform>/memory/MEMORY.md placeholder index"""
    memory_dir = platform.memory_dir(project_path)
    (memory_dir / "MEMORY.md").write_text("# 写作记忆库\n\n(no memories yet)\n", encoding="utf-8")


MEMORY_FILES = {
    "volume-memory.md": (
        "# 卷纲写作记忆\n\n> Records the author's feedback during volume-outline planning"
        " (conflict design, rhythm distribution, chapter structure, etc.).\n\n**Related Agent:** volume-planner\n"
        "**Related Skill:** volume-arc, volume-direction, volume-writing\n\n"
        "---\n\n## 条目列表\n"
    ),
    "chapter-memory.md": (
        "# 章纲写作记忆\n\n> Records the author's feedback during chapter-outline planning"
        " (scene design, emotional rhythm, foreshadowing, etc.).\n\n**Related Agent:** chapter-planner\n"
        "**Related Skill:** chapter-reference, chapter-outline, chapter-verify\n\n"
        "---\n\n## 条目列表\n"
    ),
    "prompt-memory.md": (
        "# 提示词写作记忆\n\n> Records the author's feedback during prompt-assembly"
        " (layer structure, injection rules, instruction clarity, etc.).\n\n**Related Agent:** prompt-crafter\n"
        "**Related Skill:** prompt-crafting\n\n"
        "---\n\n## 条目列表\n"
    ),
    "writing-memory.md": (
        "# 正文写作记忆\n\n> Records the author's feedback during body-text writing and reader review"
        " (style, 爽点, rhythm, description, etc.).\n\n**Related Agent:** writer, reader\n"
        "**Related Skill:** writing-execution, reader-review\n\n"
        "---\n\n## 条目列表\n"
    ),
}


def init_memory_files(project_path: Path, platform: Platform):
    """Initialize the 4 writing-memory files"""
    memory_dir = platform.memory_dir(project_path)
    for filename, content in MEMORY_FILES.items():
        filepath = memory_dir / filename
        if not filepath.exists():
            filepath.write_text(content, encoding="utf-8")
    print("  ✅ Initialized the 4 writing-memory files")





if __name__ == "__main__":
    main()
