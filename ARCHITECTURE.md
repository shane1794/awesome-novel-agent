# awesome-novel-agent Architecture

> For developers who want to understand the implementation details. User-facing content lives in [README.md](./README.md).
> Current version: v4.28.0

---

## 1. System architecture

### 1.1 Overview: state-driven ReAct loop

The core architecture is a **state-driven loop**. Every agent (novel-agent and all sub-agents) runs in ReAct mode: `OBSERVE → THINK → ACT → VERIFY → LOOP` (the only exception: `reader` declares `react: false`, because review is a one-off read and evaluation, not a state-driven loop; see the Invocation Integration notes in `agents/reader.md`).

- **OBSERVE**: rebuild state from the file system, never relying on cached context from the previous run (Context Isolation)
- **THINK**: read the `phase` field in `.agent/status.md` to decide what to do now and who should do it
- **ACT**: write an order file, then dispatch the sub-agent through the Agent tool (novel-agent); or execute this phase's task directly (sub-agents)
- **VERIFY**: check that output files exist and that the order file `status` is `DONE`
- **LOOP**: return to OBSERVE until the current phase is done

**Routing is based on `.agent/status.md#phase`** (setup/outline/draft/anti-ai/review/archive/finished), not on `chapter.md#status`. `chapter.md#status` (outline→draft→archived) only describes the chapter's own lifecycle and does not affect agent dispatch routing.

Volume completion and the finished-book end state: after archiving, updater **only outputs a volume completion report** and writes no completion flag; `last_volume_completed` and `phase: finished` are **decided and written by novel-agent** (comparing archived chapter count vs. the volume's planned chapter count). phase=finished is the end state; nothing more is dispatched.

### 1.2 Entry detection (SKILL.md)

The skill entry (after the main agent loads SKILL.md) first detects the project state, then hands off to novel-agent:

```
Detect project state
├─ story.yaml exists → legacy 2.x → run automatic migration (backup → init.py → convert per templates/migration mapping)
├─ story.md does not exist → ask the author → python tools/init.py [path] [--genre N] → @novel-agent
└─ story.md exists → existing project
    ├─ python tools/sync-project.py . --check → exit 1 → ask the author whether to sync updates
    └─ → @novel-agent continues writing
```

Sync freshness is recorded in `.agent/.sync-fingerprint`, used to detect whether skill repository updates need syncing into the project.

### 1.3 Main agent and sub-agents

| Role | Responsibility |
|-----|------|
| **novel-agent** | Top-level director (loaded into the main AI via `@novel-agent`). Detects phase, writes order files, dispatches sub-agents through the Agent tool. **Does not do sub-agents' work for them, does not use Bash, does not write any content files** |
| **Sub-agents × 8** | volume-planner / chapter-planner / prompt-crafter / writer / anti-ai / reader / updater / style-distiller. Each owns one phase, is dispatched by novel-agent, and marks its order `status: DONE` when finished |

> **Writing base spec** (`knowledge/format-specs/writing-base.md`, deployed as `.claude/knowledge/writing-base.md`, not an agent, cannot be dispatched): permanently loaded, must not be altered.
> Before writing, the writer's writing sub-agent loads this base first, then layers the chapter prompt on top; when the two conflict, the base wins.

### 1.4 Agent responsibilities

| Agent | Responsibility | Dispatched by |
|-------|------|----------|
| `volume-planner` | Main-arc breakdown + volume outline planning (four-dimension methodology) | novel-agent |
| `chapter-planner` | Chapter outline generation (memo + emotional design + scene cards + hooks) | novel-agent |
| `prompt-crafter` | 6-element prompt assembly (conflict priority + four-step transformation + sparse injection) | novel-agent |
| `writer` | Prose generation + AI-flavor self-check (writing sub-agent goes through the writing-base base first) | novel-agent |
| `anti-ai` | Gate A-F pipeline detection + quantified scoring and grading + item-by-item removal | novel-agent |
| `reader` | Deep review (optional, dispatched when the author wants it) | novel-agent |
| `updater` | Archive lore-keeping + setting changes + memory fallback | novel-agent |
| `style-distiller` | Style distillation (LLM dual-mode: the script statistics engine is retired; produces distillation master cards / scene cards / version snapshots) | novel-agent |

### 1.5 Dispatch architecture

> The order type list takes `skills/novel-dispatch.md` as its single authority; this diagram is a main-flow summary. Per-branch decision rules live in the THINK tree in `agents/novel-agent.md`.

```
Main AI (loaded with @novel-agent)
  │
  ├── Read status.md → decide the current phase
  ├── Write an order file to .agent/task/{type}-order.md (input/output paths only, no execution steps)
  ├── Dispatch the sub-agent through the Agent tool
  │     ├── setup   → updater          (setting-update-order.md)
  │     ├── setup   → style-distiller  (style-distill-order.md, when the style-setting decision flow picks distillation)
  │     ├── any phase → style-distiller (style-distill-order.md, triggered when the author says "change the style settings" or similar)
  │     ├── outline → volume-planner   (volume-plan-order.md)
  │     ├── outline → chapter-planner  (chapter-plan-order.md)
  │     ├── draft   → prompt-crafter   (prompt-craft-order.md)
  │     ├── draft   → writer           (writing-order.md)
  │     ├── anti-ai → anti-ai          (anti-ai-order.md)
  │     ├── anti-ai FAIL → writer      (writing-order.md, rewrite_of + round + violations, round<3)
  │     ├── review  → reader           (reader-review-order.md, optional)
  │     ├── archive → updater          (archive-order.md)
  │     ├── rewrite a chapter after archiving → updater (rollback-order.md, undo that chapter's archive, status back to outline)
  │     ├── volume done → updater      (memory-sweep-order.md, memory fallback)
  │     └── # Freeze card: no incremental style updates after archiving
  ├── After finishing, the sub-agent overwrites its order as status: DONE
  └── When an order is detected as DONE → advance to the next phase (setup is the exception: after setting-update-order is DONE, the author must confirm the settings before the phase advances)
```

**Key rules:**
- novel-agent is the only dispatcher, **dispatches one task at a time**, and waits for it to finish before dispatching the next
- Order files contain only input file paths + output target paths + `status: pending`, **no execution steps, rules, or methodology** (SOPs live in the sub-agents' skill definitions)
- After finishing, a sub-agent uses Write to overwrite the order's `status: pending` as `status: DONE` (**do not delete the file**: sub-agents have no delete permission, and deleting it would mean the completion signal never fires)
- novel-agent's completion check: order exists and `status: DONE` and all outputs exist and are non-empty means done; order missing means the sub-agent was interrupted unexpectedly, so retry
- Archive idempotency: before appending, updater deduplicates by chapter anchor; after a whole chapter is done, it writes `.agent/archiving/{chapter}.done`, and a re-dispatch resumes from the checkpoint (see §2 Data flow)
- novel-agent must not be dispatched as a sub-agent by the Agent tool (it would lose its Agent tool permission and the dispatch chain would break)

---

## 2. Data flow

```
[Entry] Detect → init.py init / 2.x migration / sync
  │
[setup] Discuss settings with the author → updater writes settings/
  │
[outline] story.md → volumes/volume-{N}.md (emotional arc / conflict ladder / information gap / scene cards)
  │        volume → chapters/vol-{N}-ch-{M}.md (in-chapter micro-arc / scene cards / hooks)
  │
[draft]  chapter.md → prompt-crafting (6-element assembly) → prompts/vol-{N}-ch-{M}-prompt.md
  │        → writer (writing sub-agent reads the writing-base base + prompt first) → archives/*.draft.md
  │
[anti-ai] draft → Phase 1-4 pipeline → archives/*.anti-ai.md
  │
[review] reader deep review (optional)
  │
[archive] updater archives (**idempotent**, see §1.5 key rules):
  │        First build a snapshot `.agent/{chapter}-draft-ai.md` (copied from .draft.md, audit baseline) → check `.agent/archiving/{chapter}.done`; if it exists, only fill in missing items
  │        Decide the finalized draft and Write archives/*.md (intermediate .draft.md/.anti-ai.md are kept, not deleted)
  │        chapter.md#status → archived
  │        Append character status to character-setting (deduplicate by the `## vol-N-ch-M` anchor) → append events to timeline (deduplicated)
  │        Snapshot vs. finalized draft diff → semantically merge into .claude/knowledge/anti-ai.md + dynamic memory (writing-memory.md) (deduplicated)
  │        Write {chapter}.done → advance status.md → mark the order DONE
```

---

## 3. File structure

```
{project-name}/
├── story.md              # Project index (metadata + main-arc breakdown)
├── settings/
│   ├── world-setting.md  # World building
│   ├── writing-style.md  # Writing style (quantified master card after distillation)
│   ├── genre-setting.md  # Genre configuration
│   ├── foreshadowing.md  # Cross-volume foreshadowing ledger (empty ledger generated by init / maintained by updater Step 8, aggregated from chapter.md#payoff_plan)
│   ├── timeline.md       # Timeline (appended at archive time)
│   ├── character-setting/
│   │   └── <id>.md       # One file per character
│   ├── style-profiles/   # Per-scene style cards (style-distiller output: dialogue/fight/group-scene/…)
│   │   └── genre-baselines/  # Genre style baselines (base/benchmark/delta)
│   └── .style-versions/  # Distillation version snapshots (created at distill time)
├── volumes/
│   └── volume-{N}.md     # Volume outline
├── chapters/
│   └── vol-{N}-ch-{M}.md # Chapter outline (status: outline → draft → archived)
├── prompts/
│   └── vol-{N}-ch-{M}-prompt.md  # 6-element prompt
├── sandbox/              # Roleplay sandbox records (optional, roleplay-sandbox output)
├── novel-samples/        # Style distillation samples (author puts articles to learn from here, style-distiller only)
├── archives/
│   ├── *.draft.md        # Drafts (writer output, kept as history)
│   ├── *.anti-ai.md      # AI-flavor-removed version (kept as history)
│   └── *.md              # Finalized prose (written by updater with Write at archive time; after archiving, always read this file for prose, intermediate drafts are not deleted)
├── .agent/
│   ├── status.md         # ★ phase routing basis (the only persistent state)
│   ├── task/             # Order files (temporary, kept after completion with status→DONE pending deletion)
│   ├── archiving/        # Archive checkpoints ({chapter}.done, prevents replay duplication)
│   └── {chapter}-draft-ai.md  # AI original snapshot (audit baseline, kept after archiving, distinguished as stale by the .done marker)
├── .claude/ or .opencode/ or .zcode/ or .dsh/
│   ├── agents/           # Agent definitions (deployed by init.py; zcode/dsh have no agents, agents are .zcode/skills/ / .dsh/skills/)
│   ├── knowledge/        # Anti-AI rules / style preferences / scene methodology / permanent memory / format specs
│   └── memory/           # Dynamic writing memory (volume/chapter/prompt/writing)
```

---

## 4. Skill repository structure and deployment

### 4.1 Repository directories

```
agents/          # Agent definitions (frontmatter: role / react / skills / knowledge)
skills/          # Sub-agent SOPs (anti-ai, prompt-crafting, memory-recording, volume-arc, etc.)
knowledge/       # Static reference knowledge → deployed to project .claude/knowledge/
templates/       # Project skeleton templates (settings/volumes/chapters/migration/…)
tools/           # init.py (init), sync-project.py (sync updates)
```

### 4.2 knowledge/ two-layer classification (by purpose)

| Directory | Purpose | Decided by |
|------|------|------|
| `scene-craft/` | Scene writing methodology: matched by scene type, injected into the prompt after four-step transformation | **AI automatic** |
| `format-specs/` | Format specs: chapter outline / volume outline / prompt / memory formats | System fixed |
| `genre-example/` | Genre examples: inherited into the project after init | Automatic after the genre is decided |
| `plot-craft/` | Plot design methodology (conflict escalation / hooks / reversals / tragedy) | **Author decision** |
| `character-craft/` | Character setting methodology (6-layer cognition model / villain templates) | **Author decision** |
| `title-craft/` | Book title methodology | **Author decision** |
| `anti-ai/` | Anti-AI rules (common-rules / boundary-cases / {genre} good-vs-bad examples) | **AI automatic** |

**Scene methodology directories**: `scene-craft/{type}/universal.md` + `{genre}.md` specializations, containing `prose/` and `pov/` (always loaded, sparsely injected) plus `dialogue/`, `fight/`, `appearance/`, `inner-mono/`, `death-scene/`, `environment/`, `group-scene/`, and `transition/` (triggered by scene type).

### 4.3 Deployment

- **Claude Code**: init.py deploys agent definitions to `.claude/agents/`, knowledge to `.claude/knowledge/`, and builds `.claude/memory/` dynamic memory stubs
- **OpenCode**: init.py also deploys to `.opencode/agents/`; OpenCode auto-discovers `@novel-agent` and the rest
- **Codex**: init.py deploys the 9 custom agents as `.codex/agents/*.toml` (TOML conversion output, references rewritten to `.codex/knowledge|memory`), standalone tools as `.codex/skills/<name>/SKILL.md`; novel-agent dispatches sub-agents with `spawn_agent`
- **ZCode**: init.py deploys the 9 agents as `.zcode/skills/<name>/SKILL.md` (skill conversion output, references rewritten to `.zcode/knowledge|memory`; ZCode has no project-level agents directory, agents are skills, same layout as Reasonix); novel-agent dispatches sub-agents with the `Agent` tool by skill name
- **dsh (DeepSeek Harness)**: init.py deploys the 9 agents as `.dsh/skills/<name>/SKILL.md` (skill conversion output, frontmatter keeping only the `name`/`description` keys dsh recognizes, references rewritten to `.dsh/knowledge|memory`; dsh has no project-level agents directory, agents are skills, same layout as ZCode); novel-agent dispatches sub-agents with the `subagent` tool (the prompt tells the sub-agent to load its own instructions with `skill(name=...)` first)
- **Grok Build**: init.py deploys the 9 custom agents as `.grok/agents/*.md` (Grok's native discovery path, frontmatter mapped to Grok tool names, SOPs inlined, references rewritten to `.grok/knowledge|memory`), standalone tools as `.grok/skills/<name>/SKILL.md`; novel-agent dispatches sub-agents with `spawn_subagent` (must run in the main session, Grok sub-agent depth limit is 1)
- **Install**: `install.sh` / `install.ps1` install the skill into the user-level skills directory

---

## 5. prompt-crafting prompt assembly pipeline

### 5.1 Flow

```
Step 1  Read input sources (writing-style / volume / chapter / involved character settings / genre-example / anti-ai rules)
Step 1.5 Load the global conflict-resolution priority (resolves later rule conflicts, produces no prompt text)
Step 2  Fill the 6-element structure: characters / task instruction / background info / examples / input / output
Step 3  Conflict detection (before/after consistency check)
Step 4  Acceptance self-check → write prompts/vol-{N}-ch-{M}-prompt.md
```

### 5.2 Conflict-resolution priority (highest to lowest)

| Priority | Rule | Notes |
|--------|------|------|
| 1 | Hard constraint lines | Plot red lines / character forbidden zones / boundary bans; no compression may delete a red line |
| 2 | Word count | Hard target word-count constraint; when over the limit, compress by the "compress low-weight scenes before secondary elements of high-weight scenes" strategy |
| 3 | T1 words (modifier class) | 仿佛 (as if), 一丝 (a trace of), 不禁 (cannot help but), 不由得 (involuntarily), etc. (突然/忽然/猛然, suddenly/abruptly/with a start, are context-sensitive, at most 4 times per chapter, relaxed in red-line passages); when over the threshold, keep ones that serve the narrative |
| 4 | Cognition verbs | 意识到 (realize), 发现 (notice), 明白 (understand), 感到 (feel); replace with external actions or direct perception; key emotional beats may use them briefly (at most 2 times per chapter, see narrative-rules.md rule 2), no concession otherwise |
| 5 | Senses / "X了一下" ("X a little") | At most 2 kinds of sensory detail per scene (a sound clue may be exempted if it is red-line key information) |
| 6 | Writing specs | All other writing specs and techniques; yield automatically when they conflict with the above |

### 5.3 Scene methodology loading (four-step transformation)

Scene methodology must not be copied into the prompt in full. It must be **sparsely extracted** (at most 2 items per type) and passed through four transformation steps:

1. **Anchor the characters**: fit "Character A / Character B" to specific people (personality, small habits)
2. **Anchor the information gap**: who is hiding what, and why (decides the direction of "not telling the truth")
3. **Anchor the emotional rhythm**: tense / oppressive / relaxed passages map to different sentence patterns and action-interleaving frequency
4. **Fuse the output**: produce concrete writing guidance that can go straight into the "Output: Writing Specs" section

### 5.4 Output structure (flattened)

- **Rules that must not be violated**: hard constraint lines + word count + T1 words / cognition verbs / senses + narrative rules + writing specs, combined into one list to reduce nesting
- **Scene writing guidance**: scene writing after four-step transformation (standalone subsection)
- **Texture requirements**: imperfection constraints (useless details / half-finished lines / paragraph precision layering)

---

## 6. Memory system

### 6.1 Two-level architecture

```
.claude/memory/               Dynamic memory (recorded live at each phase, maintained by updater as fallback)
  ├── volume-memory.md         Volume outline feedback
  ├── chapter-memory.md        Chapter outline feedback
  ├── prompt-memory.md         Prompt feedback
  └── writing-memory.md        Prose writing feedback (recorded by writer/reader)
         │ use_count >= 4 promotes
         ▼
.claude/knowledge/permanent-memory.md   Permanent memory (high-frequency entries settle here)
         │ 3 consecutive sweeps without a reference → demote and delete after author confirmation
```

### 6.2 Capture moments (memory-recording)

The following count as feedback worth recording; each agent appends it directly to the matching memory file during conversation:

| Moment | Test |
|------|---------|
| Author explicitly rejects something | Says "不对" ("that's wrong"), "不好" ("not good"), or "不是这样" ("not like this") and gives an alternative direction |
| Author states a rule proactively | Says "以后都这样" ("do it this way from now on") or "记住这个" ("remember this") |
| Author revises accepted content | Goes back and changes output that was already confirmed |
| Author gives a positive example | Says "这就对" ("that's right") or "就是这样" ("exactly like this"), or points to reference material |

**Not memory:** casual rhetorical questions in passing, purely functional operation confirmations, or an explicit "leave it like this for now, revisit later".

### 6.3 Lifecycle

```
Write to memory/ → referenced by an agent (use_count++) → use_count >= 4
→ Promoted to permanent-memory.md (all fields kept + [promoted YYYY-MM-DD])
→ 3 consecutive sweeps without a reference → show to the author for confirmation → delete
```

- A single file with more than 50 entries → updater compresses it: keep the most recent 30 entries, summarize the rest grouped by (domain + type)
- Deduplicate before appending: skip when the conclusion + scenario match an existing entry

### 6.4 Archive semantic merge (updater diff)

At archive time, compare the AI original snapshot (`.agent/{chapter}-draft-ai.md`) against the finalized draft (`archives/*.md`):

1. Identical → skip
2. Semantically duplicated → merge into one entry, using the better wording
3. Scenarios overlap → extend the existing entry's scenario range
4. Conflict → ask the writer to confirm

Results go into `.claude/knowledge/anti-ai.md` and the writing memory (`.claude/memory/writing-memory.md`), tagged `[writer-preference]`.

---

## 7. AI-flavor removal pipeline (anti-ai)

anti-ai is a standalone sub-agent. It takes `archives/*.draft.md` as input and outputs `archives/*.anti-ai.md`. **It changes expression only, never plot.**

```
Phase 1  Scan      Tag AI-flavor spots by Gate A-F
         A banned words / B sentence clichés / C psychological description / D pacing / E dialogue / F endings
Phase 2  Diagnose  Machine first pass (check-prose.py, may degrade) + 6 quantified metrics scored, graded (light / medium / heavy)
Phase 3  Remove    Fix gate by gate within the grade's range, converging over multiple rounds (skip a paragraph after two consecutive rounds with no change; at most 3 rounds for the whole text)
Phase 4  Report    Word-count change + edit statistics + before/after comparison + machine re-run verification
```

- **False-positive protection**: before editing, read `knowledge/anti-ai/boundary-cases.md` and apply the exemption check; on a hit, skip and tag `[SKIP: 误杀防护]` (false-positive protection)
- **Deletion cap**: light at most 15% / medium at most 25% / heavy at most 35%
- **Whitelist**: when a `.anti-ai-whitelist` file exists in the same directory, its paragraphs skip all Gates

---

## 8. Tools and engineering

| Tool | Purpose | When it runs |
|------|------|---------|
| `tools/init.py` | Project init (pick genre → build skeleton → deploy agents/skills/knowledge/tool scripts → build memory stubs → generate CLAUDE.md/AGENTS.md → write status.md) | New project / after 2.x migration |
| `tools/sync-project.py` | Sync skill repository updates into an existing project (`--check` only detects) | When entry detection finds a stale fingerprint |
| `install.sh` / `install.ps1` | Install the skill into the user-level directory | First install |
| `.github/workflows/static.yml` | CI static checks | On push |

---

## 9. Extension points

### Contributing community defaults

1. A writer accumulates their own patterns in `.claude/memory/`
2. Say "contribute this pattern"
3. It is generated in community-ready format
4. Submit a PR to `knowledge/anti-ai/`

### Adding a new genre type

1. Add a genre example in `knowledge/genre-example/`
2. Add anti-AI default patterns in `knowledge/anti-ai/`
3. Add a `scene-craft/{type}/{genre}.md` genre-specialized methodology

---

## 10. Key constraints

- **`.agent/status.md#phase`**: agent dispatch routing basis, the only persistent state
- **`chapters/*.md#status`**: chapter lifecycle `outline → draft → archived`
- **order files**: `.agent/task/*-order.md`; after finishing, sub-agents overwrite `status: pending → DONE` (do not delete), and novel-agent confirms completion on `status: DONE`
- **`archives/*.md`**: the only place for prose; `.draft.md` = draft; `.anti-ai.md` = AI-flavor-removed; after archiving, always read the finalized `.md`, with `.draft.md`/`.anti-ai.md` kept as history (not deleted)
- **`.agent/{chapter}-draft-ai.md`**: AI original snapshot, the archive diff baseline; kept after archiving (audit record, distinguished as stale by the `.agent/archiving/{chapter}.done` marker)
- **`.agent/archiving/{chapter}.done`**: archive completion checkpoint; a re-dispatch resumes from the checkpoint and prevents append replay duplication
- **`.claude/memory/*.md`**: append-only, never overwrite
- **novel-agent**: does not use Bash, does not write content files, does not overstep its authority, never accesses paths outside the project
- **Setting writes**: settings/ must go through updater (setting-update mode); novel-agent must not write them directly. Exception: style-distiller holds an exclusive write whitelist for settings/writing-style.md, settings/style-profiles/, and settings/.style-versions/; all other settings still belong to updater
- **The writer's local records take priority over references defaults**
