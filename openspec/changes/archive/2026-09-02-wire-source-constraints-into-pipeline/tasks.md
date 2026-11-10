## 1. Writer pre-writing anti-closed-loop card

- [x] 1.1 Add the "five-line anti-closed-loop card per scene" step and the do-not-start condition to the drafting section of `skills/writing-execution.md` (verify: the step is executable; wording passes the author-communication reference table)
- [x] 1.2 Reference `.claude/knowledge/anti-ai/structural-heat.md` as the card's decision basis (verify: `check-agents.py` exit 0)

## 2. Prompt structural-ban injection

- [x] 2.1 Add the structural-ban section to the pre-writing constraint list in `skills/prompt-crafting.md`: a default cap on question-answer round beats (a new scale, noted as running in parallel with the Gate E5 sentence-count scale), cold chapter openings, a ban on stacking multiple payoff receipts in the same scene (with the single-receipt payoff exemption), bridge-chain/proof-chain bans, and chapter-end bans on summary/elevation/preview (referencing Gate F plus chapter-outline landing-point priority), with the whole section carrying an adjudication-order statement (verify: entries complete, no full copy of the knowledge file)
- [x] 2.2 Conflict cross-check: check each entry against the existing wordings (Gates A-F, common-rules numeric values, existing prompt pacing rules) to confirm the ban section has no repeated definitions and no instructions pointing in opposite directions (verify: the cross-check list shows zero contradictions, including the three special checks on punctuation, dialogue frequency, and chapter endings)
- [x] 2.3 Add the new internal terms to the `knowledge/format-specs/author-communication.md` reference table (verify: author-visible text has no untranslated internal terms)

## 3. anti-ai structural scan and dual-script pre-screen

- [x] 3.1 Add a structural-heat-source scan step before `skills/anti-ai.md` Phase 1, with a dedicated "structural hits" section in the report format (verify: Gate A-F numbering unchanged)
- [x] 3.2 Call `check-chapter.py` alongside the Phase 2 machine pre-screen, following the existing degradation semantics (verify: the call and degradation wording match check-prose)
- [x] 3.3 `python tools/check-agents.py` (verify: exit 0)

## 4. Skeleton templates and deployment

- [x] 4.1 Add `templates/sandbox/detect-battles.md`, `templates/sandbox/prose-regressions.txt`, and `templates/sandbox/locked-lines.txt` (verify: templates contain usage notes and examples in author-readable language)
- [x] 4.2 `tools/init.py` generates the three skeletons; `tools/sync-project.py` covers detection (verify: the files exist after init in a temp directory, and sync --check behaves correctly)
- [x] 4.3 `tools/test_platforms.py` E2E assertions for the three files (verify: seven-platform tests exit 0)

## 5. Wrap-up and release

- [x] 5.1 Full checks: `check-agents.py` + `check-conflicts.py` + `py_compile` + `test_platforms.py` (verify: all green)
- [x] 5.2 Live test on at least one AI terminal: initialize a new project and walk through the writer/prompt/anti-ai wiring points (verify: per the repo contribution guide)
  - Live test of the anti-ai wiring point in a headless Claude session on 2026-08-31: the structural-heat-source scan hit 4 places and listed them separately, and both scripts actually ran with consistent cross conclusions (check-prose all green / check-chapter red, meaning the heat source is in structure, not wording, matching the design claim)
- [x] 5.3 Release `chore: bump version to v4.23.0`, updating `VERSION` and `docs/releasenotes/releasenote-4.23.0.md` (verify: `check-version.py` passes)
