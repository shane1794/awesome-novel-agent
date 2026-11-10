# v4.18.0 Release Notes

> **Keywords:** Transplanting the human feel: positive methodology + de-performancing + separating generation from cleanup + deterministic detection

---

## In One Sentence

This release ports the human-writing skill's complete approach to "human feel" into the anti-AI pipeline: **first describe what the writing should look like (positive method), remove the quota rules that manufacture formulaic human feel, stop stuffing negative lists into the generation stage, and add a script-checkable checker**. The four changes land separately (#112-#115, tracking issue #111), turning "reads like a human wrote it" from a matter of luck into something with a method, acceptance criteria, and a tool.

---

## What Changed in This Release

| Change | Description |
|------|------|
| **Deterministic detection tool** (#112) | Added `tools/check-prose.py` (ported from human-writing, MIT, credited): hard bans on reversal sentences (including seven disguised variants of "not A but B" flagged as suspected), sentence-length coefficient of variation, short-paragraph bursts, repeated paragraph openings, metaphor clustering within 800 words, conjunction density, isomorphic parallelism, nominalization, insight signposts, and more. One run produces a report with exit codes 0/1/2; 10 unit tests run in CI (`test_check_prose.py`). Standalone tool, not a pipeline stage |
| **Positive methodology for human feel** (#113) | Added `knowledge/anti-ai/living-voice.md` and put it **first** in the anti-ai merge chain: three layers of human feel (characters have something to do right now > details follow the character's point of view > sentence rhythm), dialogue while doing things, settings explained only when characters run into them, scenes alternating with summaries, and idle brushstrokes and misalignments that must have a source. common-rules gains a **disguise-recognition table** in section T1 (seven types: literal reversal, word-saving, cross-sentence, word-swapping, "thought" style, "let/turn" style, "price-raising" style). What is banned is the rhetorical move, not the literal words |
| **De-performancing** (#114) | All 7 quota-style acceptance rules such as "at least 1 idle brushstroke" and "emotional misalignment >= 1" are changed to "allowed if present; must come from the character's personality, scene pressure, or the current scene and character point of view; formulaic padding counts as a failure". Pass 3's "add idle brushstrokes/add misalignments" becomes "add only if the situation calls for it", only when diagnosis finds the whole text uniform or reasonable throughout. Quotas force the model to perform on cue in every chapter, which is the opposite of human feel |
| **Separating generation from cleanup** (#115) | Writer prompts no longer inject fatigue-word thresholds, T2/T3 tiers, or second-tier banned words; they only get the positive human-feel points, a short table of the most toxic T1 sentence patterns, the meta-narration ban, and positive and negative genre anti-AI examples (with a new acceptance line, "anti-AI injection scope", to check). The negative lists are cleaned up by the anti-ai agent after the draft is done. Phase 3 adds a front-loaded "save the person before cleaning the sentences" step: prioritize passages that "any other model could have written verbatim"; passages that already feel alive only get hard violations cleaned, not rewritten |
| **Engineering fixes** | `test_util.load_module` registers sys.modules before exec (fixing an importlib crash loading @dataclass modules on Python 3.9); the AGENTS.md tool list adds the new files |

---

## Compatibility

- Pure prompt-text and tool-script changes, with no schema or workflow-structure changes; new projects take effect on initialization.
- Existing initialized projects take effect after running `python tools/sync-project.py <project path>` to sync (skill_version will update to 4.18.0); existing projects' merged anti-ai.md file gains the living-voice section.
- `check-prose.py` is an optional tool (standard library only) that the author and agents can run manually; it is not wired into a pipeline gate.
- Ported content is brought in under GPLv3-compatible terms with MIT attribution kept (living-voice.md header + check-prose.py docstring).

---

## How It Was Verified

- `check-agents.py` / `check-conflicts.py` / `check-version.py` / `check-python.py` / `check-yaml.py` all green
- `test_platforms.py` 198 passed, 0 failed; `test_check_prose.py` 10 cases passed (including zero false positives on the clean "Chen Fang's IOU" text)
- Init E2E run confirms the deployed `.claude/knowledge/anti-ai.md` merge order: positive human-feel method, then the general tiered ban table, methodology, false-positive protection, then genre
- review-agent review closed: the only P3 (AGENTS.md list omission) fixed before merging (ae41c04); merge-tree simulation of main against each branch is clean pairwise
- Still for the author: run one chapter on any AI terminal to verify in practice (confirm the prompt contains no threshold table, and idle brushstrokes and misalignments have a source)
