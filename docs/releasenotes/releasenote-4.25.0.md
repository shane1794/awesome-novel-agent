# v4.25.0 Release Notes

> **Keywords:** Short-story writing pipeline (first wave): standalone project type + seven-stage flow + per-story writing contract + short-story-specific de-AI criteria

---

## In One Sentence

When the author says "write me a short story", they can now walk the full flow inside a short-story project independent of long-form novels: "set the emotion, concept and outline, assemble the writing contract, independent contract audit, write in batches, de-AI polish, payoff check, acceptance and delivery (revise or write the next story)", producing a finished main text ready for submission. Authors who know short stories go straight through in one sentence; those who do not are guided item by item.

## What Changed in This Release

| Change | Description |
|------|------|
| **Short-story project type** | `init.py --length short`: generates a `stories/{slug}/` per-story skeleton (setting, outline, contract, and main text, one directory per story), fully mutually exclusive with the long-form volume-and-chapter system; the default is still long-form, with zero changes to long-form output. 10 short-story genres in the registry (pinyin identifiers); mixing long and short in one init is rejected with a prompt |
| **Short-story agent group (5+1)** | short-agent as commander-in-chief / short-planner for concept and contract assembly / short-writer as the writer / short-editor as the editor / short-verifier for contract audit plus payoff checks, reusing reader for experience acceptance. Mutually exclusive duties: the auditor does not assemble, the checker neither writes nor cleans, the assembler does not audit itself |
| **Per-story writing contract** | `stories/{slug}/prompt.md`: six-element structure, a flat "rules that must not be violated" list in descending priority; assembly must complete the four-step transformation from general techniques to this story's writing, deduplicate after assembly, and inline a conflict-adjudication table (five numeric items + **logical consistency takes priority over payoffs**). The contract is also the acceptance baseline: after the final draft, each item is checked for payoff one by one, and unfulfilled items roll back with quoted source evidence |
| **Structural hard validation** | Two machine-checkable gates at the outline stage: the reversal reveal must sit past 60% to pass (below 50% counts as invalid); foreshadowing re-check (every ending element must have an earlier setup, and a throughline prop must appear three times with semantic progression: harmless, draws attention, reveals the truth). Also requires a catalytic breakdown (a contradictory body at the 60-75% position), a technique landing table, and no functionless sections |
| **Writing hard floor** | Each section >= 800 words (high-information-density genres >= 500), the whole story >= 8000 words, and a fixed section count, all measured by machine (cross-platform Python character counting), with model estimation banned; before each writing batch, the contract's hard-rules zone is re-injected to prevent rules from decaying across batches |
| **Short-story-specific de-AI criteria** | A separate track from long-form: keep direct emotion words, first-person judgment sentences, "crematorium" previews, and heart-death chapter endings (criterion: "does it carry the protagonist's subjective emotion right now"); delete vague emotional summary sentences and neutral author explanations. New: first-person possessive cleanup ("my heart" becomes "heart"), a character-naming ban list (stable across drafts, names do not change on revision), per-thousand-word caps on both extremes of degree adverbs, a modern-word list for historical-style genres, and paragraph-shape upper and lower bounds (guarding against telegram style) |
| **Check toolchain** | init length switch and deployment branches, check-agents dual-length product simulation (short-story knowledge no longer false-positives as orphaned), sync-project syncing by project length plus a fallback that detects project-side tampering, and a SKILL.md entry-point short-story branch |

## First-Wave Scope (Completed in Later Builds)

- Platforms: **claude** fully usable end to end; the other 6 platforms show an explicit "not yet supported" prompt at init (the skeleton is still generated)
- Genres: the **zhuiqi (wife-chasing crematorium)** style pack is fully delivered (including 3 emotion chains, 7 formulaic techniques, era variants, and school branches); selecting any of the other 9 genres in the registry warns "style pack to be added"
- Porting the list-scanning, text-teardown, and cross-genre check tools is not in this release; each gets its own proposal

## Compatibility

- Zero impact on the long-form path: without `--length`, all output matches v4.24.1 (guarded by E2E regression assertions)
- Short-story assets (agents/skills/knowledge/templates) deploy mutually exclusively with long-form and do not contaminate each other
- Source: the short-story methodology is a gifted asset; its files carry a provenance header, and the original author must confirm before public or commercial use

## Tests

- check-agents / check-conflicts / check-version / py_compile all green; test_platforms **331/331** (40+ new short-story E2E assertions: layout, long-short mutual exclusion, numbering overflow, illegal values, sync followed by --check regression)
- review-agent review: all 11 findings (3xP1, 4xP2, 4xP3) fixed; the test gap the review flagged ("--check assertions are all exit-1 scenarios") has been filled
- Walkthrough: a simulated full session verifies the seven-stage product structure and gate behavior (the section-length threshold genuinely blocks under-length sections)
- **To-do**: a real AI terminal writing one complete story end to end is left for the author to run (tasks 19.4)
