# Design: 2026-09-10-add-short-scan-analyze

## Context

The short-story pipeline (v4.25-v4.26) only does "writing". This change adds the list-scanning and text-teardown standalone tools. The archived change `2026-09-10-add-short-story-pipeline`'s proposal "later changes" section explicitly records both items (cross-genre check-tool porting was not in that change).

Constraints (following the mainline spec and repo conventions):
- Standalone tools deploy to all 7 platforms and MUST NOT enter the short-agent dispatch chain or take a phase (an extension of the same convention as mainline spec `A5`)
- Tools use only the Python standard library + pyyaml; the Node collection script is not ported (the existing D8 ruling)
- Knowledge references always use the `.claude/knowledge/...` base path; copyright attribution follows D9
- The teardown methodology comes from the gifted story-short-analyze pack (SKILL.md 3.0 + material-decomposition 34K + output-templates 24K and more), brought into the SOP under the "compress and inline" strategy

## Goals / Non-Goals

**Goals:**
- Both tools can be called independently by the author on 7 platforms (outside the dispatch chain)
- Teardown output connects to writing-stage consumption: `_meta.json` genre identification auto-loads the matching short-genres style pack; the output directory `analysis/{book title}/` is shared at project level (reusable across stories, aligned with the bootstrap main spec `A8.2` shared-resource positioning)
- Crash safety and the three gates land as the existing spec designs them

**Non-Goals:**
- Do not build a live collector (CDP / crawler). Live collection depends on runtime-environment capability (an agent with a browser uses its own tools); when unavailable, use the three-tier degradation
- Do not wire automatic recall of teardown output in the writing stage (the concept agent proactively recommending benchmarks). That is pipeline spec `D2.5` benchmark discovery, wired after both tools merge
- Do not port the pack's JS scripts (cdp-utils / dz-browse-scraper / heiyan-booklist-scraper)

## Decisions

### D1: Implement as self-contained SOPs, with the methodology inlined rather than hung on knowledge files

The pack's teardown methodology is 60,000+ words (material-decomposition 34K / output-templates 24K / output-contract 9K). Hanging all of it outside would add a knowledge directory (wiring in three places: init/check/sync) and most of it is template detail. Ruling: **compress the pipeline protocol, the five-stage templates, and the acceptance gates and inline them into `skills/short-analyze.md`** (about 300 lines), and inline market knowledge into the `skills/short-scan.md` appendix. The tools are self-contained units; deployment makes them complete.

- Alternative (add `knowledge/short/scan/` + `analyze/` directories) was rejected: three places of wiring cost buys no reuse benefit, since these files have only one consumer (the tools themselves).

### D2: Deployment form for standalone tools: all platforms use the same "platform skills directory + SKILL.md"

Of the mainline v4.26 short-story deployment's three forms, codex/grok already have standalone-tool skills directories; claude/opencode have a skills_dir convention that was never used; for the three inline platforms, skills are everything. Ruling: add a shared `deploy_standalone_skills(project, skill_home, platform, names)` helper that deploys `SHORT_STANDALONE_SKILLS = ("short-scan", "short-analyze")` as `<skills_dir>/<name>/SKILL.md` via `_convert_standalone_skill` + rewrite_refs, with all 7 platforms using it; `deploy_inline_skills(short)` also calls it (inline platforms generate 6+2 in one pass).

- Alternative (support only inline + codex/grok, with claude relying on the repo skills/) was rejected: Claude projects have no repo skills/, so the tools would be unreachable.

### D3: Three-tier data sources for list scanning: collection capability belongs to the runtime environment

"Live collection" is defined in the SOP as: if the current agent environment has a browser or scraping tool, collect per the appendix field list; otherwise move to the next tier. The repo implements no collector (aligned with the v4.23 detect-loop "platform-independent" precedent). Degradation marking is a hard requirement: built-in-knowledge products MUST carry an unverified statement, to prevent them from "looking real".

### D4: The teardown genre yardstick uses the short-genres style packs; no new comparison file

The pack's genre-catalog.md (21K) heavily overlaps our short-genres. Ruling: after identifying the genre, load the "narrative voice / hook motifs / pacing skeleton" sections of `.claude/knowledge/short-genres/{genre}.md` directly as the "does this story meet the standard" yardstick; when nothing is identified, mark it general. The output `_meta.json.genre` aligns with the registry slug, and the writing stage auto-loads the same pack from it.

### D5: The teardown report passes through the short-story criteria itself

The pack scans reports with banned-words plus anti-ai-writing; we have only one file, `.claude/knowledge/short-anti-ai.md`. Ruling: gate 1 scans against it (the analyst's wording, skipping quoted source text), which is semantically equivalent. Reports land outside `.agent/task/`, in `analysis/{book title}/` (with the output, where the author can read them directly).

### D6: Standalone tools stay out of the dispatch chain; the entry point is SKILL.md and the project instructions

How the author triggers them: say "scan a list" or "tear this story apart" in conversation. The SKILL.md short-story branch adds one optional-tool note; the `templates/short` project-level instructions do not add it (to avoid a three-file sync burden; one statement in SKILL.md is enough for the entry-point skill to sense).

## Risks / Trade-offs

- [After the teardown SOP is inlined and grows long, the model's compliance drops in the later stages] → Each of the five stages writes to disk in its own small step, independent of orders (driven directly by the author's conversation), with each stage's instructions self-contained; live verification is listed as a follow-up item for this PR
- [Built-in list-scan knowledge goes stale and misleads reports] → The freshness trio (sample date, confidence, re-scan time) is a MUST, and degradation marking is a MUST
- [Is the teardown output directory `analysis/` one of the skeleton directory set in bootstrap spec mainline `A2.1`?] → Yes (since v4.25, `templates/short` already contains an analysis/ placeholder directory); this change fills it in, with no skeleton changes
- [Standalone-skill deployment adds a `.claude/skills/` directory for Claude, which long-form projects do not have] → Only the short flow calls the deployment helper; the long-form path is unchanged (guarded by test assertions)

## Migration Plan

1. platforms.py: `SHORT_STANDALONE_SKILLS` + the `deploy_standalone_skills` helper; `deploy_inline_skills(short)` mounts the standalone tools inside.
2. init.py: the short flow's Step 3.6 calls the deployment helper (all platforms).
3. sync-project.py: the short sync_skills branch adds standalone-tool re-deployment; the find_changes short branch adds the two-file comparison.
4. SOP content: self-contained short-scan / short-analyze implementations.
5. SKILL.md: short-story branch optional-tool note.
6. test_platforms: standalone-tool E2E (7 platforms + inline count 6 to 8 + codex/grok skills directories).
7. After full regression is green, push the PR and review it; **do not merge** (author-specified: merge timing waits for a decision after live-testing the short-story main chain).

## Open Questions

(None.)
