# v4.20.0 Release Notes

> **Keywords:** 7th platform: Grok Build support with native agent deployment + spawn_subagent dispatch + hard constraints on sub-agent permissions

---

## In One Sentence

Grok Build support is added ([Grok Build](https://docs.x.ai/build/overview), SpaceXAI's coding-agent TUI, PR #118, by author @BillChenIDY): the skill itself installs at user level to `~/.grok/skills/awesome-novel/`, the 9 custom agents deploy at project level through Grok's native discovery path `.grok/agents/*.md`, and novel-agent dispatches sub-agents with `spawn_subagent` (must run in the main session; Grok sub-agents are limited to depth 1). The order-file protocol is exactly the same as the other six platforms.

---

## What Changed in This Release

| Change | Description |
|------|------|
| **Platform support** | `install.sh` / `install.ps1` add `grok` (the skill installs to `~/.grok/skills/awesome-novel/`); `init.py --platform grok` initializes and `sync-project.py --platform grok` upgrades and syncs; the pyyaml install threshold and runtime check cover grok too (the grok agent conversion depends on frontmatter parsing) |
| **Agent conversion (convert_to_grok)** | Claude Code agent frontmatter becomes Grok agent Markdown: tool-name mapping `Read→read_file` / `Write→write` / `Edit→search_replace` / `Glob→list_dir` / `Grep→grep` / `Bash→run_terminal_command`; `Agent` keeps its instruction spelling (the authorized dispatch tool family); Claude-private fields (role/react/memory/knowledge) are dropped; SOPs are inlined into the main text (the skills field format is incompatible between the two sides); references are rewritten to `.grok/knowledge\|memory` |
| **Dispatch model** | novel-agent injects a Grok dispatch adapter section: dispatch with `spawn_subagent(subagent_type=<sub-agent name>, isolation="none")` (shared workspace; the sub-agent writes back to the same project), one task at a time, waiting for `status: DONE` before dispatching the next. novel-agent must run in the main session: Grok sub-agents cannot dispatch sub-agents of their own (depth limit 1), so treating novel-agent as a sub-agent breaks the dispatch chain |
| **Hard constraints on sub-agent permissions** | Sub-agents have the `Agent` instruction removed from their `tools`, plus `disallowedTools: [Agent]` (deny by instruction spelling, stripping the dispatch tool family) and `agentsMd: false`; the main text leads with an injected dispatch ban: no dispatch or recursion of any kind, no writing orders or progress fields beyond authority, and report to novel-agent in the reply when collaboration is needed |
| **Standalone tools** | memory-recording and roleplay-sandbox deploy as `.grok/skills/<name>/SKILL.md` (outside the dispatch chain, isomorphic with codex) |
| **Docs and wording** | README / README-en / SKILL.md / ARCHITECTURE.md / AGENTS.md / install scripts / memory-format-spec all synced to the seven-platform wording |

---

## Compatibility

- Purely a new platform; the six existing platforms (claude/opencode/reasonix/codex/zcode/dsh) behave unchanged, and already-initialized projects need no action.
- New Grok Build users: `./install.sh grok` (on Windows, `install.ps1 grok`) installs the skill, then `python ~/.grok/skills/awesome-novel/tools/init.py <project path> --platform grok` initializes.
- Like the other conversion platforms, grok needs pyyaml (missing the dependency makes install and initialization fail fast with an error, producing no damaged output).
- Upgrade an existing grok project with `python tools/sync-project.py <project path> --platform grok`; skill_version will update to 4.20.0.

---

## How It Was Verified

- `test_platforms.py` adds full grok chain assertions: init/sync E2E (9 agent Markdown files + standalone tool skills + reference rewriting + no leftover .claude), frontmatter parsed with `yaml.safe_load` (sub-agents unauthorized and denying `Agent`, novel-agent authorized for `Agent`, anti-ai keeping `run_terminal_command`): **253 passed, 0 failed**.
- Static checks all green: check-agents / check-conflicts / check-version / py_compile.
- review-agent closed three review rounds: 2 issues fixed before merging, a P1 (the tools call name `spawn_subagent` matched no tool, leaving novel-agent unable to dispatch; reverted to the `Agent` instruction spelling) and a P3 (sub-agents emitting authorization and deny at the same time, a contradictory config; the guard condition was fixed in sync). Tool authorization semantics were verified line by line against the xai-org/grok-build source.
- Still for the author: run one dispatch on a real Grok Build machine, "install, then novel-agent dispatches the updater" (all semantics verified statically against source; not yet run on a real machine).
