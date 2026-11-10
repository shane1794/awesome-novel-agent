# short-story-bootstrap Delta

## Purpose

Make short stories a standalone project type: when the author says "write a short story", they get a short-story-specific skeleton, agent group, genre system, and knowledge base, four parts that together form the short story's own runtime environment, depending on and polluting no assets of any other writing type.

## ADDED Requirements

### Requirement: A1 The initialization entry point must route by length

`tools/init.py` MUST accept `--length short|long`. The entry-point skill's detection flow (the repo-root `SKILL.md`) MUST take the short-story branch when the author expresses short-story intent, and its boundary-condition table MUST list how each short-story scenario is handled. Once the length is decided, it MUST be written into the project `story.md` as the basis for sync tools to judge what to sync later.

Short stories MUST NOT become the default: when no length is explicitly specified, `init.py` MUST keep the existing behavior (short stories not enabled).

#### Scenario: A1.1 Short-story intent enters the short-story branch
- **WHEN** the author says short-story intent such as "write a short story", "write a Yanxuan story", or "write a short tale" in the project directory, and the current directory has no `story.md`
- **THEN** the entry-point skill asks whether to create a **short-story** project in this directory, and after confirmation runs `init.py` with `--length short`, then loads the short-story commander after completion

#### Scenario: A1.2 Existing projects are recognized by their length marker
- **WHEN** the project directory already has a `story.md` marked `length: short`
- **THEN** the entry-point skill loads the short-story commander directly, without entering any non-short-story flow

#### Scenario: A1.3 Short stories are not the default
- **WHEN** running `python tools/init.py <path>` without `--length`
- **THEN** initialization does not enable short stories, and `story.md` contains no short-story marker

#### Scenario: A1.4 Illegal length values are rejected
- **WHEN** passing `--length medium` or any other value that is not `short`/`long`
- **THEN** `init.py` prints a prompt of the allowed values and exits non-zero, creating no files

### Requirement: A2 The short-story skeleton must be a complete set of its own

A new template tree carries the short-story skeleton. With `--length short`, it MUST generate only the short-story skeleton: the project index, story directories, sandbox, dispatch directory, genre settings, and platform directories.

Short stories MUST generate short-story versions of the project-level instruction files and a short-story-form state machine; the short-story skeleton MUST NOT contain directories the short-story flow does not use.

#### Scenario: A2.1 Short-story skeleton directory set
- **WHEN** initializing a project with `--length short`
- **THEN** the project contains the project index (with the length marker), story directories, sandbox, `.agent/task/`, `tools/`, genre settings, and platform directories

#### Scenario: A2.2 The skeleton contains only short-story assets
- **WHEN** checking the project root after `--length short` initialization
- **THEN** every top-level directory belongs to what the short-story flow needs, and no directory the short-story flow does not use exists

#### Scenario: A2.3 Project-level instructions are the short-story version
- **WHEN** reading the project-level instruction file at the short-story project root
- **THEN** the agent composition, writing flow (emotion, concept, contract, writing, polish, payoff check, acceptance), and directory map it describes are all in short-story form

#### Scenario: A2.4 The state machine is in short-story form
- **WHEN** reading the short-story project's `.agent/status.md`
- **THEN** it contains `phase` (covering setup / planning / contract / writing / polishing / verifying / delivered), the current story identifier, and story-status fields, with no volume-or-chapter fields

### Requirement: A3 The short-story genre system must be numbered independently

Short stories MUST have an independent genre registry and genre style-pack collection. With `--length short`, the genre parameter's numbering space MUST be the short-story genres, and an out-of-range number MUST report the short-story range of options.

#### Scenario: A3.1 The short-story genre registry is complete
- **WHEN** checking the short-story genre registry
- **THEN** the registry lists all short-story genres, each with a number, an identifier, and a Chinese name, and the numbers correspond one-to-one with style-pack files, all of which exist

#### Scenario: A3.2 Genre numbers switch to the short-story space
- **WHEN** initializing with `--length short --genre 1`
- **THEN** the deployed genre is short-story registry genre no. 1, and the genre references in the knowledge products come from the short-story style packs

#### Scenario: A3.3 Out-of-range numbers prompt the short-story range
- **WHEN** passing a number beyond the short-story genre count with `--length short`
- **THEN** it errors, prompts the short-story range of available numbers, and exits non-zero

### Requirement: A4 The short-story agent group must have independent duties and deploy to all platforms

The short-story agent group MUST consist of 5 short-story-specific agents and 1 reused experience-acceptance agent:

| agent | Duty | Independence requirement |
|---|---|---|
| Commander | phase routing and dispatch | Writes no content files |
| Concept | Framework / outline / writing-contract assembly | None |
| Writer | Main-text writing | Does not assemble contracts |
| Editor | De-AI pass and polish | Does not take part in contract assembly or writing |
| Verifier | Contract audit + final-draft payoff check | Does not take part in contract assembly, writing, or cleanup |
| Experience acceptance (reused) | Harsh reader experience acceptance | Does not take part in structure checks |

No duty MUST be performed by an executor carrying another duty. All 7 platforms MUST support deploying the short-story agent group, and short-story projects MUST NOT deploy any non-short-story agent.

#### Scenario: A4.1 Short-story agent definitions are complete
- **WHEN** checking the repo agent directory
- **THEN** definitions exist for the five short-story agents, commander, concept, writer, editor, and verifier, each with a frontmatter structure (name/description/role/tools/skills/knowledge) isomorphic with existing agents

#### Scenario: A4.2 Duty independence is traceable
- **WHEN** comparing the input/output contracts of each short-story agent definition
- **THEN** contract audit and payoff checks are executed by the verifier agent, contract assembly by the concept agent, and the two are not the same agent; the verifier agent writes no content files

#### Scenario: A4.3 Claude and OpenCode platforms deploy to the agents directory
- **WHEN** initializing with `--length short --platform claude` (or `opencode`)
- **THEN** the platform agents directory contains the short-story agent group

#### Scenario: A4.4 Codex platform deploys as TOML
- **WHEN** initializing with `--length short --platform codex`
- **THEN** the platform agents directory generates TOML products for the short-story agent group, containing names, descriptions, and the inlined full SOP text

#### Scenario: A4.5 Grok platform deploys as Markdown
- **WHEN** initializing with `--length short --platform grok`
- **THEN** the platform agents directory generates Markdown products for the short-story agent group, with sub-agents carrying the no-further-dispatch constraint

#### Scenario: A4.6 Reasonix, Zcode, and DSH platforms deploy as inlined skills
- **WHEN** initializing with `--length short --platform zcode` (or `reasonix`, `dsh`)
- **THEN** the platform skills directory generates a `SKILL.md` for each short-story agent group member, matching the short-story agent group in count, and the commander's SKILL.md contains that platform's dispatch adapter section

#### Scenario: A4.7 No non-short-story agents are deployed
- **WHEN** checking any platform product of a short-story project
- **THEN** no non-short-story writing agent exists

### Requirement: A5 The short-story knowledge base must deploy independently

The short-story knowledge base MUST deploy as its own product collection: grammar and format specs, writing references, genre style packs, and the short story's own de-AI criteria product. The short-story anti-AI criteria MUST be merged separately into a standalone product file.

#### Scenario: A5.1 The short-story anti-AI product is standalone
- **WHEN** checking the platform knowledge directory after `--length short` initialization
- **THEN** a standalone short-story anti-AI merged product exists, its content coming from the short story's own de-AI criteria files

#### Scenario: A5.2 Three kinds of writing assets land in place
- **WHEN** checking the platform knowledge directory after `--length short` initialization
- **THEN** the short-story format specs, short-story writing references, and short-story genre style packs are all reachable through post-deployment paths

#### Scenario: A5.3 Reference paths resolve
- **WHEN** running the static checks
- **THEN** all short-story agent references to knowledge files resolve successfully

#### Scenario: A5.4 Genre style-pack content is complete
- **WHEN** checking the short-story genre style packs
- **THEN** each genre pack contains at least: narrative voice, opening paradigm, hook motifs, emotional intensity, dialogue style, **emotion-chain library**, technique library, pacing skeleton, and ending paradigm. The emotion-chain library gives several named emotional arcs (each with 4-6 stages, each stage named), and each technique-library entry is an applicable formula plus one concrete example; it MUST NOT list only technique names

### Requirement: A6 Sync tools must sync by project length

Sync tools MUST read the length marker from the project index and choose sync targets by length. Syncing a short-story project MUST NOT bring in any non-short-story skeleton or non-short-story agent.

#### Scenario: A6.1 Short-story project sync keeps short-story form
- **WHEN** running the sync tool on a short-story project
- **THEN** the synced agent group, knowledge base, and project-level instructions remain in short-story form

#### Scenario: A6.2 Change detection covers short-story assets
- **WHEN** a repo-side short-story agent or short-story knowledge file changes
- **THEN** the sync check reports updates and exits non-zero

### Requirement: A7 The static check chain must cover short-story assets

Repo static checks MUST cover short-story agents and short-story knowledge: reference paths MUST resolve, short-story knowledge files MUST NOT be judged orphaned, short-story deployment paths MUST be inside the post-deployment path allowlist, and short-story quantitative thresholds MUST not conflict with this repo's existing threshold system (when they conflict, they MUST go through an explicit exemption with the reason recorded).

#### Scenario: A7.1 Reference checks pass
- **WHEN** running the agent reference check
- **THEN** all short-story agent references resolve successfully, exit code 0

#### Scenario: A7.2 Short-story knowledge is not judged orphaned
- **WHEN** running the orphaned-knowledge check
- **THEN** every deployed short-story knowledge file is referenced by a short-story agent or the entry-point skill, or belongs to an explicit author-reference exemption list

#### Scenario: A7.3 Rule-conflict checks pass
- **WHEN** running the rule-conflict check
- **THEN** exit code 0; if a short-story threshold and an existing repo threshold cover the same object with different numbers, it must already be in an explicit exemption with its reason stated, and must not pass silently

#### Scenario: A7.4 Platform E2E assertions pass
- **WHEN** running the platform test suite
- **THEN** all short-story initialization product assertions pass on every platform

### Requirement: A8 One short-story project must hold multiple stories, with stories isolated from each other

Short-story projects MUST organize finished work as "one directory per story", with stories isolated from each other at file level (each story's settings, outline, contract, and main text never overwrite another's), and shared resources (genre style packs, project-level instructions, status files) MUST sit at project level. Starting a new story in the same project MUST NOT affect the files of already-delivered stories.

#### Scenario: A8.1 Story directories are isolated
- **WHEN** writing two stories in sequence in the same short-story project
- **THEN** each story occupies its own story directory, each with its own settings, outline, contract, and main text, and no file of one story overwrites the other's

#### Scenario: A8.2 Shared resources sit at project level
- **WHEN** checking the short-story project structure
- **THEN** project-level instructions, status files, and genre knowledge sit at project-level paths and are not copied into each story's directory

#### Scenario: A8.3 A new story does not affect old stories
- **WHEN** starting the next story after one has been delivered
- **THEN** the delivered story's main-text file is byte-for-byte unchanged
