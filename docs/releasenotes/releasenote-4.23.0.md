# v4.23.0 Release Notes

> **Keywords:** Source constraints wired into the pipeline: structural-heat-source knowledge enters the writing, prompt, and de-AI stages; the project sandbox gains evolution-mechanism files

---

## In One Sentence

The structural-heat-source laws and chapter check tool added in v4.22.0 are now wired into the writing pipeline: the writer answers a "five-line anti-closed-loop card" before writing, prompts inject structural red lines (with a conflict-adjudication statement), anti-ai scans structure before cleaning sentences and runs the dual-script pre-screen; the project `sandbox/` gains three new files, the detection-battle log, the regression pattern library, and the locked-lines whitelist, so each book starts accumulating its own "failure-string library" from chapter one.

## What Changed in This Release

| Change | Description |
|------|------|
| **Writer five-line anti-closed-loop card** | `writing-execution.md` writing rules add: before each writing session, answer five questions (what does the character need to do / who does the resistance come from / at what point in the performance do we stop / what is not explained / what is left for the next scene). If questions 3-5 cannot be answered, do not start writing |
| **Prompt structural red lines** | `prompt-crafting.md` writing methodology adds item 5 and injects it into the task instructions: a cap on question-answer ping-pong beats (running alongside the existing "insert action every 6-8 sentences" sentence-count scale without replacing it), cold chapter openings, one receipt per scene (with a payoff-delivery exemption), bans on bridge chains and proof chains, and no summary, elevation, or preview at chapter end (the chapter-end landing takes priority). The whole passage carries an adjudication-order statement: author settings and chapter outline > genre knowledge > structural defaults > detection optimization |
| **Anti-AI structural scan first** | Phase 1 performs a structural-heat-source scan before Gates A-F; hits are marked `[S]`, listed separately in the report, and counted once. Phase 3 fixes structure before cleaning sentences. Gate A-F numbering and existing thresholds are unchanged |
| **Dual-script pre-screen** | The Phase 2 machine pre-screen calls check-chapter.py alongside check-prose.py; hard hits merge into the Gate A/B list to be cleared first. Degradation semantics follow the existing conventions |
| **Sandbox evolution-mechanism files** | `templates/sandbox/` adds `detect-battles.md` (round-by-round detection-battle log plus distilled patterns), `prose-regressions.txt` (failure-string library, with `#` comments inert), and `locked-lines.txt` (whitelist of lines the author approved to keep); init generates them automatically and sync backfills them into existing projects |
| **check-chapter comment support** | Lines starting with `#` in the regression library and whitelist files do not take part in matching, so the templates' own explanation lines stay inert |

## Anti-Conflict Design

The structural laws come from live tests on a single book, and injecting them directly would create dual wordings against existing rules. This release follows three disciplines: (1) a single authoritative source, the details live in the knowledge files and the pipeline only references them without copying; (2) new scales are not redefined, only "question-answer round beats" is added, while existing sentence-count, punctuation, and chapter-end wordings are all referenced; (3) the adjudication order is stated explicitly, so the writer never has to guess priorities in a conflict.

## Compatibility

- Purely incremental: Gates A-F, quantitative metrics, and grading rules are unchanged; `status.md` gains no new fields.
- Existing projects automatically gain the three new `sandbox/` files plus updated scripts and knowledge after running `sync-project`, with no manual action needed.

## Tests

- `tools/test_check_chapter.py` adds comment-line assertions (20 items).
- `tools/test_platforms.py` 290 assertions all green (adding seven-platform sandbox-skeleton assertions).
- check-agents / check-conflicts / check-version / py_compile all green.
