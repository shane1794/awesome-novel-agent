# v4.26.0 Release Notes

> **Keywords:** Short-story knowledge completed: 11 in-depth writing references, all ten genre style packs delivered, cross-story author-preference memory

---

## In One Sentence

The short-story pipeline's "software" is completed: the writer now has 11 in-depth references to consult when designing hooks, emotion, and reversals; all ten genre style packs are delivered (each with an emotion-chain library); and the author's taste preferences across stories are remembered for the first time, so they no longer have to restate them for every story.

## What Changed in This Release

| Change | Description |
|------|------|
| **11 in-depth writing references** | `knowledge/short/craft/` adds: the hooks trio (chapter-hook type library / paragraph hooks / suspense design), emotional-methods (the three emotional boards: bond laying / emotional tearing / lingering dull pain), reversal-toolkit (reversal types and setup), villain-and-reveal (villain templates plus four reveal mechanisms), dialogue-mastery (dialogue power games / subtext / voice), genre-writing-formulas (structural skeletons as a fallback for niche genres), genre-writing-techniques (cross-genre techniques), submission-craft (submission forms: four-dimensional lede skeleton / pay-point placement), and quality-checklist (finished-draft checklist). All wired into short-planner / short-writer / short-editor |
| **All ten genre style packs delivered** | 9 new packs added: worldly face-slapping / revenge face-slapping / CEO and wealthy families / household and palace intrigue / folk horror / suspense / sweet pampering / dual male leads / absurdist comedy (pinyin slugs). On top of each pack's original 10 sections, each pack adds an **emotion-chain library** (2-3 named emotional arcs, each with 5 named stages, distilled from the pacing skeleton), with the technique library keeping its "formula plus real example" pairs. `init.py --length short --genre 1-10` all work, and interactive genre selection supports them too |
| **Cross-story author-preference memory** | `<platform>/memory/author-feedback.md`: init generates the seed, then short-agent appends the author's explicit feedback at each story delivery ("original text -> conclusion", one line, nothing invented), and short-planner draws on the relevant entries when assembling a contract. Fixes the structural gap of "restating preferences for every story" |

## Compatibility

- Purely incremental: zero changes to the long-form path; short-story product layout is unchanged (the craft directory goes from 2 to 13 files and the genres directory from 2 to 11 files; sync auto-covers them by directory-level comparison)
- Non-interactive environments (AI terminals) initializing a short story without `--genre`: automatically fall back to registry no. 1 (wife-chasing crematorium, zhuiqi) with an explicit prompt; other genres need an explicit `--genre 1-10`
- Source: the new content is a rewrite of gifted assets, with provenance headers; the original author must confirm before public or commercial use

## Tests

- check-agents / check-conflicts / check-version / py_compile all green; test_platforms **516/516** (new: craft 13 files, genres 11 files, memory seed, genre 2 availability assertions)
- review-agent review: all 8 findings fixed (2xP1: bare EOF traceback in non-interactive mode, leftover teardown-pipeline fields; P2 broken links and stale comments; P3 wording)
