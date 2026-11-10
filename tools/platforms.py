#!/usr/bin/env python3
"""Platform adapter layer: different coding agents use different directory
conventions for agent/skill/knowledge/memory. init.py / sync-project.py share
this module for platform detection, directory dispatch, reference rewriting,
and skill generation.

Supported platforms (directory conventions declared one line each in the
PLATFORMS registry):
  - claude   → .claude/   agents=agents, knowledge, memory
  - opencode → .opencode/ agents=agents, knowledge, memory
  - reasonix → .reasonix/ agents=None (agents are skills), skills=skills, knowledge, memory
  - codex    → .codex/    agents=agents (TOML conversion product), skills=skills, knowledge, memory
  - zcode    → .zcode/    agents=None (agents are skills; ZCode has no project-level agents directory),
                          skills=skills, knowledge, memory
  - dsh      → .dsh/      agents=None (agents are skills; DeepSeek Harness has no project-level
                          agents directory, .dsh/skills is its project-level skill root), skills=skills,
                          knowledge, memory
  - grok     → .grok/     agents=agents (Markdown conversion product, the Grok Build native discovery path),
                          skills=skills, knowledge, memory

Adding a new platform (besides one line in PLATFORMS, pick one of the two
conventions):
  - agents-are-skills type: add a dispatch adapter section to _DISPATCH_SECTIONS
    + a description suffix in _convert_standalone_skill; deploy_inline_skills
    then covers it automatically
  - standalone-agents-directory type: write a converter modeled on
    convert_to_opencode/convert_to_codex/convert_to_grok, and wire one dispatch
    line each in init.main and sync-project.sync_agents/sync_skills

The module is named platforms (plural) deliberately to avoid colliding with
the standard-library platform (singular).
"""

from __future__ import annotations

import os
import sys
from dataclasses import dataclass
from pathlib import Path

from style_common import frontmatter_text, split_frontmatter   # single-source frontmatter parsing (review #38)


@dataclass(frozen=True)
class Platform:
    key: str                 # "claude" | "opencode" | "reasonix" | "grok"
    label: str               # display name
    root: str                # platform root directory, e.g. ".reasonix"
    agents: str | None       # agents subdirectory; None for reasonix (agents are skills)
    skills: str | None       # skills subdirectory
    knowledge: str           # knowledge subdirectory
    memory: str              # memory subdirectory
    detect_keywords: tuple   # SKILL_HOME path-recognition keywords

    def agents_dir(self, project: Path) -> Path | None:
        if self.agents is None:
            return None
        return project / self.root / self.agents

    def skills_dir(self, project: Path) -> Path | None:
        if self.skills is None:
            return None
        return project / self.root / self.skills

    def knowledge_dir(self, project: Path) -> Path:
        return project / self.root / self.knowledge

    def memory_dir(self, project: Path) -> Path:
        return project / self.root / self.memory


PLATFORMS = {
    "claude":   Platform("claude", "Claude Code", ".claude",   agents="agents",
                         skills="skills", knowledge="knowledge", memory="memory", detect_keywords=()),
    "opencode": Platform("opencode", "OpenCode", ".opencode", agents="agents",
                         skills="skills", knowledge="knowledge", memory="memory", detect_keywords=("opencode",)),
    "reasonix": Platform("reasonix", "Reasonix", ".reasonix", agents=None,
                         skills="skills", knowledge="knowledge", memory="memory", detect_keywords=("reasonix",)),
    "codex":    Platform("codex", "Codex", ".codex", agents="agents",
                         skills="skills", knowledge="knowledge", memory="memory", detect_keywords=(".codex",)),
    "zcode":    Platform("zcode", "ZCode", ".zcode", agents=None,
                         skills="skills", knowledge="knowledge", memory="memory", detect_keywords=(".zcode",)),
    "dsh":      Platform("dsh", "DeepSeek Harness", ".dsh", agents=None,
                         skills="skills", knowledge="knowledge", memory="memory", detect_keywords=(".dsh",)),
    "grok":     Platform("grok", "Grok Build", ".grok", agents="agents",
                         skills="skills", knowledge="knowledge", memory="memory", detect_keywords=(".grok",)),
}


def platform_from_key(key: str) -> Platform:
    if key not in PLATFORMS:
        raise ValueError(f"Unknown platform: {key}; options: {', '.join(PLATFORMS)}")
    return PLATFORMS[key]


def detect_platform(skill_home: Path, override: str | None = None) -> Platform:
    """Platform detection: explicit override > SKILL_HOME path keywords > default claude."""
    if override:
        return platform_from_key(override)
    p = str(skill_home).lower()
    for plat in PLATFORMS.values():
        if any(kw in p for kw in plat.detect_keywords):
            return plat
    return PLATFORMS["claude"]


def rewrite_refs(text: str, platform: Platform) -> str:
    """Rewrite Claude Code path references in deployed content to platform paths.
    claude is returned as-is.

    After precisely replacing knowledge/memory, any remaining bare .claude/
    (no-write zones, directory-tree notes, etc.) is replaced wholesale with
    the platform root, so deployed products keep no dead references.
    """
    if platform.key == "claude":
        return text
    text = text.replace(".claude/knowledge/", f"{platform.root}/knowledge/")
    text = text.replace(".claude/memory/", f"{platform.root}/memory/")
    text = text.replace(".claude/", f"{platform.root}/")
    return text


def ensure_yaml(platform: Platform) -> None:
    """Agent conversion on non-claude platforms needs pyyaml; exit with a clear
    error when it is missing.

    The claude platform copies without converting and does not need pyyaml.
    init.py / sync-project.py call this function after platform detection to
    avoid the silent failure of "exit 0 but damaged output".
    """
    if platform.key == "claude":
        return
    try:
        import yaml  # noqa: F401
    except ImportError:
        print(f"Error: the {platform.label} platform needs pyyaml (pip install pyyaml), which is not installed in the current environment.",
              file=sys.stderr)
        sys.exit(1)


def resolve_skill_home() -> Path:
    """The skill repository root. Scripts always live under the skill root's tools/.

    Deriving it from __file__ is the correct source (repo / installed copy /
    reasonix project-level install); NOVEL_SKILL_HOME is only an exceptional
    fallback (when __file__ fails to resolve) and must not take priority:
    install.sh persists it to the profile, where it may point at a stale
    installed copy.
    """
    by_file = Path(__file__).resolve().parent.parent
    if (by_file / "agents").is_dir() and (by_file / "tools").is_dir():
        return by_file
    env_home = os.environ.get("NOVEL_SKILL_HOME")
    if env_home:
        cand = Path(env_home)
        if (cand / "agents").is_dir() and (cand / "tools").is_dir():
            return cand
    return by_file


# ---------------------------------------------------------------
# inline-skill platform generation (reasonix / zcode / dsh)
# agents + skills sources to <platform root>/skills/<name>/SKILL.md (11)
# The three platforms' products are isomorphic; differences live in the _INLINE_PLATFORM_SPEC difference table:
#   - frontmatter: zcode carries allowed-tools (bare names); reasonix also carries runAs, and tool names
#     are mapped through _REASONIX_TOOL_MAP, with planning agents also getting read_skill; dsh keeps only name/description
#   - the novel-agent dispatch adapter text is injected per platform
# ---------------------------------------------------------------

_REASONIX_TOOL_MAP = {
    "Read": "read_file",
    "Write": "write_file",
    "Edit": "edit_file",
    "Glob": "glob",
    "Grep": "grep",
}

# Single source for the subagent list: shared by the novel-agent dispatch adapter sections on all platforms and the Codex dispatch notes
# (adding an execution agent only changes this + EXEC_AGENT_SOPS; no per-platform copy changes needed)
SUBAGENT_NAMES = (
    "writer", "volume-planner", "chapter-planner", "prompt-crafter",
    "anti-ai", "reader", "updater", "style-distiller",
)

# Short-form pipeline: dispatcher short-agent + the short-form subagent set (reader is shared by long and short)
SHORT_SUBAGENT_NAMES = (
    "short-planner", "short-writer", "short-editor", "short-verifier", "reader",
)

# Single source for dispatchers: name to the subagents that dispatcher may dispatch
# (novel-agent = long-form volume/chapter pipeline; short-agent = short-form story pipeline)
DISPATCHER_AGENTS = {
    "novel-agent": SUBAGENT_NAMES,
    "short-agent": SHORT_SUBAGENT_NAMES,
}

# Long-form-only agents (not deployed for short-form projects; reader is shared by long and short and is not listed)
LONG_ONLY_AGENTS = frozenset({
    "novel-agent", "writer", "volume-planner", "chapter-planner",
    "prompt-crafter", "anti-ai", "updater", "style-distiller",
})

# Single source for the agent-to-dedicated-SOP mapping (shared contract for the three-platform deploy and the Codex SOP inline)
EXEC_AGENT_SOPS = {
    "writer": ["writing-execution"],
    "volume-planner": ["volume-arc", "volume-direction", "volume-writing"],
    "chapter-planner": ["chapter-reference", "chapter-outline", "chapter-verify"],
    "prompt-crafter": ["prompt-crafting", "prompt-audit"],
    "anti-ai": ["anti-ai"],
    "reader": ["reader-review"],
    "updater": ["updater-archive", "updater-setting", "updater-rollback"],
    "style-distiller": ["style-distill"],
}

# Short-form agent-to-dedicated-SOP mapping (isomorphic to EXEC_AGENT_SOPS; reader reuses the long-form SOP)
SHORT_EXEC_AGENT_SOPS = {
    "short-planner": ["short-plan", "short-craft-prompt"],
    "short-writer": ["short-write"],
    "short-editor": ["short-polish"],
    "short-verifier": ["short-audit", "short-verify"],
    "reader": ["reader-review"],
}

# Agents on reasonix that need to load a shared SOP (frontmatter gains the read_skill tool)
_READ_SKILL_AGENTS = ("volume-planner", "chapter-planner", "prompt-crafter", "updater")

# Standalone interactive tools outside the dispatch chain (deployed as inline skills on every platform)
STANDALONE_SKILLS = ("memory-recording", "roleplay-sandbox")

# Short-form standalone tools (ranking-scan / text-teardown): triggered by the author, outside the dispatch chain; deployed on all platforms as SKILL.md under the platform skills directory
SHORT_STANDALONE_SKILLS = ("short-scan", "short-analyze")

# Per-platform novel-agent dispatch adapter sections ({names} injects SUBAGENT_NAMES)
_DISPATCH_SECTIONS = {
    "reasonix": (
        "\n\n## Reasonix dispatch adapter (no Agent tool in this environment)\n"
        "To dispatch a subagent in the Reasonix environment, use the `run_skill` tool:\n"
        "- `run_skill(name=\"<subagent name>\", arguments=\"{order contents}\")` dispatches one subagent\n"
        "- A subagent's name is the skill name under .reasonix/skills/ ({names})\n"
        "- A subagent is of the subagent type; run_skill's arguments become its only task input\n"
        "- Read-only subagents can be dispatched concurrently with `parallel_tasks`; the order-file protocol (status: DONE) is unchanged\n"
    ),
    "zcode": (
        "\n\n## ZCode dispatch adapter (subagents are skills in this environment)\n"
        "To dispatch a subagent in the ZCode environment, use the `Agent` tool:\n"
        "- A subagent's name is the skill name under `.zcode/skills/` ({names})\n"
        "- Use the Agent tool to spawn by subagent name, passing the order file contents as its task input\n"
        "- A subagent runs in an isolated context and only reads the order and the specified files; the order-file protocol (status: DONE) is unchanged\n"
        "- Dispatch only one task at a time; wait for DONE before dispatching the next; never dispatch novel-agent itself as a subagent\n"
    ),
    "dsh": (
        "\n\n## DeepSeek Harness dispatch adapter (subagents are skills in this environment)\n"
        "To dispatch a subagent in the dsh environment, use the `subagent` tool:\n"
        "- A subagent's name is the skill name under `.dsh/skills/` ({names})\n"
        "- A subagent runs in an isolated context; in the prompt, ask it to first call `skill(name=\"<subagent name>\")` "
        "to load its own instructions, then carry out the order file task\n"
        "- Write the order file path and the task requirements into the prompt; the order-file protocol (status: DONE) is unchanged\n"
        "- Dispatch only one task at a time; wait for DONE before dispatching the next; never dispatch novel-agent itself as a subagent\n"
    ),
}


def _allowed_tools(data: dict, name: str, platform_key: str) -> list | None:
    """agent frontmatter tools to the platform allowed-tools list. dsh has no
    such field, so None is returned.

    The Agent (dispatch tool) is always dropped: subagents have no dispatch
    rights. reasonix maps through _REASONIX_TOOL_MAP to platform tool names
    and adds read_skill for planning agents (to load the shared SOP).
    """
    if platform_key == "dsh":
        return None
    tools_raw = str(data.get("tools", "") or "")
    tool_map = _REASONIX_TOOL_MAP if platform_key == "reasonix" else {}
    allowed = []
    for t in tools_raw.split(","):
        t = t.strip()
        if not t or t == "Agent":
            continue
        mapped = tool_map.get(t, t)
        if mapped not in allowed:
            allowed.append(mapped)
    if platform_key == "reasonix" and name in _READ_SKILL_AGENTS \
            and "read_skill" not in allowed:
        allowed.append("read_skill")
    return allowed


def _convert_agent_to_skill(text: str, platform_key: str, inline_sops=None) -> str:
    """Claude Code agent frontmatter to an inline-skill platform (reasonix/zcode/dsh)
    skill.

    - frontmatter: keep name/description; drop role/react/memory/knowledge;
      tool-field differences are in _allowed_tools (reasonix also carries runAs:
      novel-agent=inline, everything else subagent)
    - body: the agent identity section + the novel-agent dispatch adapter section
      + the full text of the dedicated SOP, inlined
    """
    data, body = split_frontmatter(text)    # single-source parsing (review #38: the broken split is deprecated)
    if not data:
        return text

    name = str(data.get("name", "unknown")).strip()
    desc = str(data.get("description", "") or "").strip().replace('"', "'")
    allowed = _allowed_tools(data, name, platform_key)

    fm_lines = [
        "---",
        f"name: {name}",
        f'description: "{desc}"',
    ]
    if platform_key == "reasonix":
        fm_lines.append(f"runAs: {'inline' if name in DISPATCHER_AGENTS else 'subagent'}")
    if allowed is not None:
        joined = ", ".join(allowed)
        fm_lines.append(f"allowed-tools: [{joined}]" if platform_key == "reasonix"
                        else f"allowed-tools: {joined}")
    fm = "\n".join(fm_lines) + "\n---\n"

    agent_body = body.strip()
    dispatcher_names = DISPATCHER_AGENTS.get(name)
    if dispatcher_names:
        # {names} injects this dispatcher's subagent list; the adapter copy replaces the novel-agent wording with the dispatcher's own name
        agent_body += _DISPATCH_SECTIONS[platform_key].replace(
            "{names}", " / ".join(dispatcher_names)).replace("novel-agent", name)
    sop_sections = []
    for sop in (inline_sops or []):
        if sop and sop.exists():
            sop_sections.append(
                f"\n---\n\n## Execution SOP: {sop.name}\n\n{sop.read_text(encoding='utf-8').strip()}"
            )
    return fm + "\n" + agent_body + "\n".join(sop_sections)


def _convert_standalone_skill(text: str, name: str, platform_key: str) -> str:
    """Plain-text SOP to a platform inline skill (a standalone interactive tool outside the dispatch chain)."""
    desc = ""
    for ln in text.split("\n"):
        if ln.strip().startswith("# ") and not ln.strip().startswith("## "):
            desc = ln.strip().lstrip("# ").strip()
            break
    suffix = {
        "reasonix": "(auto-generated inline skill by awesome-novel)",
        "zcode": "(auto-generated ZCode skill by awesome-novel)",
        "dsh": "(auto-generated dsh skill by awesome-novel)",
        "codex": "(auto-generated Codex skill by awesome-novel)",
        "grok": "(auto-generated Grok Build skill by awesome-novel)",
    }.get(platform_key, "(auto-generated skill by awesome-novel)")
    fm = (
        f"---\n"
        f"name: {name}\n"
        f"description: \"{desc or name}{suffix}\"\n"
    )
    if platform_key == "reasonix":
        fm += "runAs: inline\n"
    fm += "---\n"
    return fm + "\n" + text.strip()


def deploy_inline_skills(project: Path, skill_home: Path, platform: Platform,
                         length=None) -> bool:
    """Generate <project>/<platform.root>/skills/<name>/SKILL.md, rewriting references
    to platform paths.

    Called only for reasonix/zcode/dsh (agents=None, agents are skills); other
    platforms return False.
    length=long (default): the product is 9 agents (EXEC_AGENT_SOPS 8 executors
    + novel-agent with novel-dispatch inlined) + STANDALONE_SKILLS standalone
    tools, 11 in total.
    length=short: the product is 8 (SHORT_EXEC_AGENT_SOPS 5, dispatcher
    short-agent with short-dispatch inlined, reader reusing reader-review, plus
    SHORT_STANDALONE_SKILLS standalone tools short-scan / short-analyze).
    frontmatter/dispatch-adapter differences are in the difference-table comments.
    """
    if platform.key not in _DISPATCH_SECTIONS:
        return False
    agents_dir = skill_home / "agents"
    skills_dir = skill_home / "skills"
    target = platform.skills_dir(project)
    if target is None:
        return False
    target.mkdir(parents=True, exist_ok=True)

    if length == "short":
        exec_sops_map = SHORT_EXEC_AGENT_SOPS
        dispatcher_name, dispatcher_sop = "short-agent", "short-dispatch"
    else:
        exec_sops_map = EXEC_AGENT_SOPS
        dispatcher_name, dispatcher_sop = "novel-agent", "novel-dispatch"

    for agent_name, sops in exec_sops_map.items():
        agent_file = agents_dir / f"{agent_name}.md"
        if not agent_file.exists():
            continue
        sop_files = [skills_dir / f"{s}.md" for s in sops]
        body = _convert_agent_to_skill(agent_file.read_text(encoding="utf-8"),
                                       platform.key, inline_sops=sop_files)
        body = rewrite_refs(body, platform)
        skill_dir = target / agent_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")

    novel_file = agents_dir / f"{dispatcher_name}.md"
    if novel_file.exists():
        body = _convert_agent_to_skill(novel_file.read_text(encoding="utf-8"),
                                       platform.key,
                                       inline_sops=[skills_dir / f"{dispatcher_sop}.md"])
        body = rewrite_refs(body, platform)
        skill_dir = target / dispatcher_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")

    if length == "short":
        deploy_standalone_skills(project, skill_home, platform, SHORT_STANDALONE_SKILLS)
        return True

    for skill_name in STANDALONE_SKILLS:
            sf = skills_dir / f"{skill_name}.md"
            if sf.exists():
                body = _convert_standalone_skill(sf.read_text(encoding="utf-8"), skill_name,
                                                 platform.key)
                body = rewrite_refs(body, platform)
                skill_dir = target / skill_name
                skill_dir.mkdir(parents=True, exist_ok=True)
                (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    return True


# ---------------------------------------------------------------
# OpenCode agent conversion (Claude Code agent frontmatter to OpenCode syntax)
# ---------------------------------------------------------------

_OPENCODE_TOOL_TO_PERM = {
    "Read": "read",
    "Write": "edit",   # OpenCode's edit covers write/edit/apply_patch
    "Edit": "edit",
    "Glob": "glob",
    "Grep": "grep",
    "Agent": "task",   # Claude Code Agent tool maps to OpenCode task
}
# Permission keys explicitly denied under OpenCode outside the allowlist (to avoid the default ask popup)
_OPENCODE_DENY_KEYS = ["bash", "webfetch", "websearch", "list", "lsp", "skill"]


def convert_to_opencode(text: str) -> str:
    """Claude Code agent frontmatter to OpenCode syntax (tools: to permission:).

    Key differences:
    - Claude Code uses a `tools: Read, Write, ...` comma string (allowlist;
      the default is to inherit everything)
    - OpenCode uses a `permission:` map (allow/ask/deny; the default is ask)
    Only the `tools:` field is handled, becoming `permission:`; all other fields
    (name/description/role and the rest) are kept as-is.
    """
    if not text.startswith("---"):
        return text
    fm = frontmatter_text(text)              # single-source parsing (review #38: the broken split is deprecated)
    if fm is None or "tools:" not in fm:
        return text
    _, body = split_frontmatter(text)

    tools_line = None
    new_lines = []
    for ln in fm.splitlines():
        if ln.strip().startswith("tools:"):
            tools_line = ln
            continue
        new_lines.append(ln)

    allowed = []
    if tools_line:
        val = tools_line.split(":", 1)[1].strip()
        allowed = [t.strip() for t in val.split(",") if t.strip()]

    perm = {}
    for key in _OPENCODE_DENY_KEYS:
        perm[key] = "deny"
    for tool in allowed:
        p = _OPENCODE_TOOL_TO_PERM.get(tool)
        if p:
            perm[p] = "allow"
    if not perm:
        perm = {"*": "deny"}

    perm_text = "permission:\n" + "".join(
        f"  {k}: {v}\n" for k, v in sorted(perm.items())
    )
    new_fm = "\n".join(new_lines).rstrip() + "\n" + perm_text
    return "---" + new_fm + "---" + body


def convert_agent_to_platform(text: str, platform: Platform,
                              skill_home: Path | None = None) -> str:
    """Agent source content to platform deployment content (shared single logic for
    init.deploy_agents / sync.sync_agents / find_changes).

    - opencode: frontmatter to permission format + reference rewriting
    - codex: to TOML (SOP inlining needs skill_home; convert_to_codex already
      rewrites references internally)
    - grok: to Grok Build agent Markdown (SOP inlining needs skill_home;
      convert_to_grok already rewrites references internally)
    - other platforms (claude): as-is (pure copy)
    """
    if platform.key == "opencode":
        return rewrite_refs(convert_to_opencode(text), platform)
    if platform.key == "codex":
        if skill_home is None:
            raise ValueError("codex platform agent conversion needs skill_home (SOP inlining)")
        return convert_to_codex(text, skill_home)
    if platform.key == "grok":
        if skill_home is None:
            raise ValueError("grok platform agent conversion needs skill_home (SOP inlining)")
        return convert_to_grok(text, skill_home)
    return text


# ---------------------------------------------------------------
# Codex agent conversion (Claude Code agent frontmatter to Codex custom agent TOML)
# ---------------------------------------------------------------

_CODEX_TOOL_MAP = {
    "Read": "Read",
    "Write": "Write",
    "Edit": "Edit",
    "Glob": "Glob",
    "Grep": "Grep",
    "Agent": "spawn_agent",   # Claude Code Agent tool maps to Codex spawn_agent
}

# Subagent injection section: Codex TOML has no tool-allowlist field, so the hard constraint must be declared in instruction text.
# Placed at the very top of developer_instructions, before the source body and the SOP.
_CODEX_DISPATCH_BAN = """## Dispatch-permission hard constraint (highest priority, ahead of everything else in this file)

You are an execution subagent with no dispatch rights. **Never use the `spawn_agent` tool to spawn subagents**
(including dispatching an agent with your own name; no form of recursive spawning is allowed). You actually have the full tool set,
but this ban does not lapse because the tools are available.

Also forbidden:
- Writing any file under `.agent/task/` other than this order
- Writing the `phase` / `current_step` / `last_volume_completed` fields of `.agent/status.md`
  (only novel-agent may write these fields)
- Advancing the pipeline on novel-agent's behalf (writing new orders, updating phase)

You only do:
1. Read the order file and carry out the task it specifies
2. Write the files the order's `outputs` point to
3. When done, overwrite the order's `status` with `DONE` and finish

When a task needs another agent's help (e.g. new settings, archiving, or review turn out to be needed), do not dispatch it yourself.
Tell novel-agent in your reply "who should be dispatched next, and why", and let novel-agent dispatch."""


def _toml_escape(s: str) -> str:
    """Single-line TOML basic-string escaping."""
    return s.replace("\\", "\\\\").replace('"', '\\"')


def _toml_multiline(s: str) -> str:
    """Multi-line TOML basic-string escaping (backslash + closing-delimiter conflicts)."""
    return s.replace("\\", "\\\\").replace('"""', '\\"\\"\\"')


def _agent_skill_paths(data: dict) -> list:
    """Extract skills/*.md relative paths from the agent frontmatter skills list."""
    paths = []
    skills = data.get("skills") or []
    if not isinstance(skills, list):
        return paths
    for s in skills:
        if isinstance(s, dict):
            path = s.get("path")
        elif isinstance(s, str):
            path = s
        else:
            continue
        if isinstance(path, str) and path.startswith("skills/"):
            paths.append(Path(path))
    return paths


def convert_to_codex(text: str, skill_home: Path) -> str:
    """Claude Code agent frontmatter to a Codex custom agent TOML.

    - Required fields: name / description / developer_instructions (the Codex official convention)
    - tools: Codex agent TOML has no tool-allowlist field; subagents get the
      "dispatch-permission hard constraint" injected (no spawn_agent / no
      writing files beyond their authority), and the declared tool range is
      only a hint; Agent maps to spawn_agent (only novel-agent holds it; see
      the adapter section for the dispatch notes)
    - skills: the SOP declared in frontmatter is inlined into
      developer_instructions (same as reasonix)
    - Path rewriting: .claude/knowledge and .claude/memory to the matching
      .codex/ directories
    """
    data, _body = split_frontmatter(text)    # single-source parsing (review #38: the broken split is deprecated)
    if not data:
        return text

    name = str(data.get("name", "unknown")).strip()
    desc = str(data.get("description", "") or "").strip()

    tools_raw = str(data.get("tools", "") or "")
    allowed = []
    for t in tools_raw.split(","):
        t = t.strip()
        if not t:
            continue
        mapped = _CODEX_TOOL_MAP.get(t, t)
        if mapped not in allowed:
            allowed.append(mapped)

    body = _body.strip()
    dispatcher_names = DISPATCHER_AGENTS.get(name)
    if dispatcher_names:
        body += (
            "\n\n## Codex dispatch adapter (no Agent tool in this environment)\n"
            "To dispatch a subagent in the Codex environment, use the `spawn_agent` tool:\n"
            f"- A subagent's name is the TOML name under `.codex/agents/` ({' / '.join(dispatcher_names)})\n"
            "- Pass the order file contents to the subagent as the task message; the order-file protocol (status: DONE) is unchanged\n"
            f"- Dispatch only one task at a time; wait for DONE before dispatching the next; never dispatch {name} itself as a subagent\n"
            "- You are the only dispatcher in this project: after spawning, watch the agent tree; if a subagent tries to spawn again, interrupt it immediately and re-dispatch per the rules\n"
        )
    else:
        body = _CODEX_DISPATCH_BAN + "\n\n" + body

    tool_line = ""
    if allowed:
        if dispatcher_names:
            tool_line = (
                "\n\n(Auto-generated) The tool range this agent declares: "
                + ", ".join(allowed)
                + f". You are the only dispatcher; spawn_agent is only for dispatching subagents, never to spawn {name} itself."
            )
        else:
            tool_line = (
                "\n\n(Auto-generated) The tool range this agent declares: "
                + ", ".join(allowed)
                + ". Codex custom agent TOML has no tool-allowlist field, so this declaration does not trim the actual tool set; "
                "the real constraints are the forbidden items under \"Dispatch-permission hard constraint\" above."
            )
    body += tool_line

    sop_sections = []
    for rel in _agent_skill_paths(data):
        sop = skill_home / rel
        if sop.exists():
            sop_sections.append(
                f"\n---\n\n## Execution SOP: {sop.name}\n\n{sop.read_text(encoding='utf-8').strip()}"
            )
    instructions = body + "\n".join(sop_sections)
    instructions = rewrite_refs(instructions, PLATFORMS["codex"])

    lines = [
        f"# Auto-generated by awesome-novel, source file: agents/{name}.md",
        f'name = "{name}"',
        f'description = "{_toml_escape(desc)}"',
        "",
        'developer_instructions = """',
        _toml_multiline(instructions).rstrip(),
        '"""',
        "",
    ]
    return "\n".join(lines)


# ---------------------------------------------------------------
# Grok Build agent conversion (Claude Code agent frontmatter to Grok .grok/agents/*.md)
# Grok discovery path: project .grok/agents/*.md; dispatch tool: spawn_subagent (depth limit 1)
# ---------------------------------------------------------------

_GROK_TOOL_MAP = {
    "Read": "read_file",
    "Write": "write",
    "Edit": "search_replace",
    "Glob": "list_dir",
    "Grep": "grep",
    "Agent": "Agent",            # frontmatter instruction; the model still calls spawn_subagent
    "Bash": "run_terminal_command",
}

_GROK_DISPATCH_BAN = """## Dispatch-permission hard constraint (highest priority, ahead of everything else in this file)

You are an execution subagent with no dispatch rights. **Never use the `spawn_subagent` tool to spawn subagents**
(including dispatching an agent with your own name; no form of recursive spawning is allowed). Grok Build's subagent depth limit is 1,
so even a call would fail; this ban does not lapse because the tools are visible.

Also forbidden:
- Writing any file under `.agent/task/` other than this order
- Writing the `phase` / `current_step` / `last_volume_completed` fields of `.agent/status.md`
  (only novel-agent may write these fields)
- Advancing the pipeline on novel-agent's behalf (writing new orders, updating phase)

You only do:
1. Read the order file and carry out the task it specifies
2. Write the files the order's `outputs` point to
3. When done, overwrite the order's `status` with `DONE` and finish

When a task needs another agent's help (e.g. new settings, archiving, or review turn out to be needed), do not dispatch it yourself.
Tell novel-agent in your reply "who should be dispatched next, and why", and let novel-agent dispatch.

Tool mapping: use `write` to create/overwrite files, `search_replace` for local edits, `list_dir` to list directories, `grep` to search."""


def _yaml_quote(s: str) -> str:
    """YAML double-quoted scalar escaping."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def convert_to_grok(text: str, skill_home: Path) -> str:
    """Claude Code agent frontmatter to Grok Build project-level agent Markdown.

    - Required fields: name / description (the Grok official convention)
    - tools: YAML list; Agent is kept as Grok's subagent-authorization instruction
    - disallowedTools: subagents use Agent to ban the subagent tool family
    - skills: Claude's path-object list is incompatible with Grok's skill-name
      list, so the SOP is inlined into the body and then dropped
    - Other Claude-private fields (role/react/memory/knowledge) are dropped to
      avoid Grok parse failures
    - novel-agent gets the spawn_subagent dispatch adapter section injected;
      subagents get the dispatch hard constraint injected
    - Path rewriting: .claude/knowledge and .claude/memory to the matching
      .grok/ directories
    """
    data, _body = split_frontmatter(text)
    if not data:
        return rewrite_refs(text, PLATFORMS["grok"])

    name = str(data.get("name", "unknown")).strip()
    desc = str(data.get("description", "") or "").strip()

    tools_raw = str(data.get("tools", "") or "")
    allowed = []
    dispatcher_names = DISPATCHER_AGENTS.get(name)
    for t in tools_raw.split(","):
        t = t.strip()
        if not t:
            continue
        mapped = _GROK_TOOL_MAP.get(t, t)
        if not dispatcher_names and mapped == "Agent":
            continue
        if mapped not in allowed:
            allowed.append(mapped)

    body = _body.strip()
    if dispatcher_names:
        body += (
            "\n\n## Grok Build dispatch adapter (no Agent tool in this environment)\n"
            "To dispatch a subagent in the Grok Build environment, use the `spawn_subagent` tool:\n"
            f"- A subagent's name is the Markdown name under `.grok/agents/` ({' / '.join(dispatcher_names)})\n"
            "- Call `spawn_subagent(subagent_type=\"<subagent name>\", prompt=<order path and task requirements>, "
            "isolation=\"none\")`\n"
            "- isolation must be none (shared workspace; the subagent writes back to the same project); no worktree\n"
            "- Write the order file path and the task requirements into the prompt; the order-file protocol (status: DONE) is unchanged\n"
            f"- Dispatch only one task at a time; wait for DONE before dispatching the next; never dispatch {name} itself as a subagent\n"
            "- You must run in the **main session**: a Grok subagent cannot spawn another subagent (depth limit 1), "
            "and if the dispatcher is spawned as a subagent, the dispatch chain breaks\n"
            "- Tool mapping: read files with `read_file`, write/overwrite with `write`, search with `grep`, list directories with `list_dir`\n"
        )
    else:
        body = _GROK_DISPATCH_BAN + "\n\n" + body

    if allowed:
        if dispatcher_names:
            body += (
                "\n\n(Auto-generated) The tool range this agent declares: "
                + ", ".join(allowed)
                + f". You are the only dispatcher; spawn_subagent is only for dispatching subagents, never to spawn {name} itself."
            )
        else:
            body += (
                "\n\n(Auto-generated) The tool range this agent declares: "
                + ", ".join(allowed)
                + ". Subagents must not use spawn_subagent."
            )

    sop_sections = []
    for rel in _agent_skill_paths(data):
        sop = skill_home / rel
        if sop.exists():
            sop_sections.append(
                f"\n---\n\n## Execution SOP: {sop.name}\n\n{sop.read_text(encoding='utf-8').strip()}"
            )
    instructions = body + "\n".join(sop_sections)
    instructions = rewrite_refs(instructions, PLATFORMS["grok"])

    fm_lines = [
        "---",
        f"name: {name}",
        f"description: {_yaml_quote(desc)}",
    ]
    if allowed:
        fm_lines.append("tools:")
        for t in allowed:
            fm_lines.append(f"  - {t}")
    if not dispatcher_names:
        fm_lines.append("disallowedTools:")
        fm_lines.append("  - Agent")
        fm_lines.append("agentsMd: false")
    else:
        fm_lines.append("agentsMd: true")
    fm_lines.append("---")
    return "\n".join(fm_lines) + "\n\n" + instructions + "\n"


def deploy_codex_agents(project: Path, skill_home: Path, platform: Platform,
                        length=None) -> None:
    """Generate <project>/<platform.root>/agents/<name>.toml, rewriting references
    to platform paths.

    Called only for the codex platform. Claude agent frontmatter to Codex TOML,
    consistent with sync. length=long (default) deploys 9 long-form agents;
    length=short deploys 6 short-form agents (SHORT_AGENTS + reader), mutually
    exclusive.
    """
    if platform.key != "codex":
        return
    agents_dir = skill_home / "agents"
    target = platform.agents_dir(project)
    if target is None:
        return
    target.mkdir(parents=True, exist_ok=True)
    count = 0
    for item in sorted(agents_dir.rglob("*.md")):
        if item.name == ".gitkeep":
            continue
        if length == "short":
            if item.stem in LONG_ONLY_AGENTS:
                continue    # short-form projects do not deploy long-form-only agents
        elif item.stem.startswith("short-"):
            continue    # long-form projects do not deploy short-form-only agents (the long/short agent sets are mutually exclusive)
        dest = target / (item.stem + ".toml")
        dest.write_text(
            convert_to_codex(item.read_text(encoding="utf-8"), skill_home),
            encoding="utf-8",
        )
        count += 1
    print(f"  ✅ Deployed {count} Codex agent definitions to {target}")


def _convert_codex_inline_skill(text: str, name: str) -> str:
    """Plain-text SOP to a Codex skill (SKILL.md, name/description frontmatter)."""
    desc = ""
    for ln in text.split("\n"):
        if ln.strip().startswith("# ") and not ln.strip().startswith("## "):
            desc = ln.strip().lstrip("# ").strip()
            break
    desc_clean = desc.replace('"', "'")
    fm = (
        f"---\n"
        f"name: {name}\n"
        f"description: \"{desc_clean or name} (auto-generated Codex skill by awesome-novel)\"\n"
        f"---\n"
    )
    return fm + "\n" + text.strip()


def deploy_standalone_skills(project: Path, skill_home: Path, platform: Platform,
                             names) -> int:
    """Deploy standalone tools as <platform.skills_dir>/<name>/SKILL.md (the same
    shape on all platforms).

    For short-form standalone tools (ranking-scan / text-teardown): claude/opencode
    create the skills directory on first use, codex/grok land in the existing
    standalone-tool directory, and inline platforms are routed through
    deploy_inline_skills. An existing file with identical content is skipped
    (idempotent; sync may call this repeatedly).
    """
    target = platform.skills_dir(project)
    if target is None:
        return 0
    target.mkdir(parents=True, exist_ok=True)
    count = 0
    for skill_name in names:
        sf = skill_home / "skills" / f"{skill_name}.md"
        if not sf.exists():
            continue
        body = _convert_standalone_skill(sf.read_text(encoding="utf-8"), skill_name,
                                         platform.key)
        body = rewrite_refs(body, platform)
        skill_dir = target / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        out = skill_dir / "SKILL.md"
        if out.exists() and out.read_text(encoding="utf-8") == body:
            continue
        out.write_text(body, encoding="utf-8")
        count += 1
    return count


def deploy_codex_skills(project: Path, skill_home: Path, platform: Platform,
                        length=None) -> None:
    """Generate standalone interactive tools as skills
    (<project>/<platform.root>/skills/<name>/SKILL.md).

    Called for codex / grok. The 9 agents use the standalone agents directory;
    this only deploys the standalone tools outside the dispatch chain
    (memory-recording, roleplay-sandbox). Short-form projects have no standalone
    tools (skipped when length=short: the short-form SOPs are already inlined
    into the agents, and the memory/sandbox tools are tied to long-form
    volume/chapter assets).
    """
    if platform.key not in ("codex", "grok"):
        return
    if length == "short":
        print(f"  [i] Short-form projects have no standalone tools ({platform.root}/skills skipped)")
        return
    skills_dir = skill_home / "skills"
    target = platform.skills_dir(project)
    if target is None:
        return
    target.mkdir(parents=True, exist_ok=True)
    for skill_name in ("memory-recording", "roleplay-sandbox"):
        sf = skills_dir / f"{skill_name}.md"
        if sf.exists():
            body = _convert_codex_inline_skill(sf.read_text(encoding="utf-8"), skill_name)
            if platform.key == "grok":
                body = body.replace("Codex skill", "Grok Build skill")
            body = rewrite_refs(body, platform)
            skill_dir = target / skill_name
            skill_dir.mkdir(parents=True, exist_ok=True)
            (skill_dir / "SKILL.md").write_text(body, encoding="utf-8")
    print(f"  ✅ Deployed {platform.label} standalone-tool skills to {target}")
