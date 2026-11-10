## Why

The `add-zhuque-source-defense` change landed structural-heat-source knowledge and the chapter check tool, but without pipeline references they have no effect: the writer still drafts with no structural constraints, anti-ai still starts scanning at sentence level, and the project has no skeleton files to carry the "battle log to rules" evolution mechanism. The main course of source-level detection reduction is generation-time constraints, so this change wires the knowledge into the pipeline and templatizes the memory mechanism.

## What Changes

- `skills/writing-execution.md`: add a "five-line anti-closed-loop card per scene" before writing (what the character needs to do / who the resistance comes from / how far the performance goes before stopping / what is not explained / what is left for the next scene); if items 3-5 cannot be answered, do not start writing.
- `skills/prompt-crafting.md`: inject structural bans into the pre-writing constraints (question-answer chain beat cap, cold chapter openings, minimal chapter endings with no summary, micro-closed-loop / bridge-chain / proof-chain bans), referencing `structural-heat.md`.
- `skills/anti-ai.md`: add a structural-heat-source scan step before the Phase 1 scan (read structural-heat.md; fix structure first, then clean sentences), and call `check-chapter.py` alongside the Phase 2 machine pre-screen.
- `templates/sandbox/` adds three skeletons: the detection-battle log (`detect-battles.md`), the regression pattern library (`prose-regressions.txt`), and the locked-lines whitelist (`locked-lines.txt`).
- `tools/init.py` generates these skeleton files when initializing a project; `tools/sync-project.py` / `test_platforms.py` cover them.

## Capabilities

### New Capabilities

- `source-constraint-pipeline`: the source structural-constraint pipeline, the wiring contract for the writer's pre-writing anti-closed-loop card, prompt structural-ban injection, and anti-ai structural-heat-source scanning.

### Modified Capabilities

(No existing spec. This repo has no archived specs yet; all of them are newly created in this batch.)

## Impact

- Changed: `skills/writing-execution.md`, `skills/prompt-crafting.md`, `skills/anti-ai.md`, `tools/init.py`, `tools/test_platforms.py`.
- Added: `templates/sandbox/detect-battles.md`, `templates/sandbox/prose-regressions.txt`, `templates/sandbox/locked-lines.txt`.
- Depends on: the `add-zhuque-source-defense` change merged first (it references that change's knowledge file and tool).
- Wording constraint: author-visible text in skills must not contain internal terms (slices, heat windows, regression libraries, and the like); it must pass the `knowledge/format-specs/author-communication.md` reference table.
