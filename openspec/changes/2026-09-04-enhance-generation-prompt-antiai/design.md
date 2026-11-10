# Design: 2026-09-04-enhance-generation-prompt-antiai

## Context

The repo's anti-AI system has three layers: the knowledge layer (`knowledge/anti-ai/*.md`, merged by init.py from a fixed list into the deployed product `anti-ai.md`), the generation layer (`skills/prompt-crafting.md`, where prompt-crafter assembles prompts and injects only the parts of anti-ai.md needed at generation time), and the cleanup layer (`skills/anti-ai.md` pipeline + check-prose.py). The asset-pack comparison conclusions are in the proposal's Why section; this change only touches the generation-layer entry point and the knowledge-layer files it references.

Key existing constraints (must not be broken during implementation):
- Generation and cleanup stay separated: the writer does not write against a negative list, and T2/T3 tiers and fatigue-word thresholds do not enter prompts (prompt-crafting Step 1.6 + Step 4 self-check).
- living-voice.md carries a responsibility statement: "defines no thresholds or tiers".
- The structural-heat spec enumerates seven laws plus at least 13 structures; additions must be embedded inside the existing laws.
- check-conflicts.py has two gates: SCAN_GLOBS cross-file threshold conflicts + METHODOLOGY_FILES (anti-ai-writing / boundary-cases) out-of-bounds quantity-line detection (in the form `N times/chapter`).
- Deployment references always use the `.claude/knowledge/...` base path (verified by check-agents.py).

## Goals / Non-Goals

**Goals:**
- All five generation-side increments land and are verifiable through the existing check chain (check-agents / check-conflicts / test_platforms).
- New knowledge is traceable (file headers mark the source and license constraints) and calibratable (numbers stated as single-book measured defaults).
- Generation injection and cleanup scanning share one source (the ornate-emptiness family is defined in one place in T1 and used on both sides).

**Non-Goals:**
- Do not bring in the asset pack's cleanup-side wordlist increments (no emotion-voice families, enumeration with dunhao (Chinese enumeration-comma) lists, empty colon turns, zero-subject comments at paragraph starts, translationese, or the four other families). Those wait for later changes.
- Do not bring in `_precheck.py` / `check_chapter.py` / detection battle history / Zhuque submission operations content.
- Do not change the anti-ai pipeline (skills/anti-ai.md) or check-prose.py.
- Do not bring in 3-gram repetition detection (it has wording tension with "key nouns keep one wording"; the detection-side adjudication goes in a separate change, see Decisions D5).

## Decisions

### D1: Statistical anchors go in a standalone knowledge file, `knowledge/anti-ai/statistical-anchor.md`

Alternative A (write them into prompt-crafting.md) was rejected: the skill is a flow SOP, knowledge belongs in the knowledge layer, and a flow file should not carry calibratable numbers. Alternative B (merge them into living-voice.md) was rejected: statistical anchors are quantitative thresholds, which conflict with that file's "defines no thresholds or tiers" responsibility statement. A standalone file makes it easy to trace everything back to the asset pack as a whole and to change only one place when calibrating per book later. init.py's merge list (the tuple at L402) gains the file, with its comment updated.

### D2: Statistical anchors are homed separately: rhythm anchors go into texture requirements, the key-noun rule goes into writing standards

Prompt-audit dimension F (de-AI check, warmth balance) has a PASS standard of "no hard metric on single-sentence paragraph share", and dimension I requires suggestive techniques to sink to the bottom and not enter the hard-rules zone; prompt-crafting output is a flat structure, and "writing standards" merges into the "rules that must not be violated" list. So the four rhythm anchors (sentence length / paragraph / commas / sentence openings) are injected into the "texture requirements" sub-section, which is already home to tendency-style requirements such as half-finished sentences and imperfection constraints. All wording uses distribution tendencies ("about every 5 sentences", "0-4, varying"), with no share floor, plus a concession statement (yield first when conflicting with red lines, word-count compression, T1, cognitive verbs, or senses; compression paragraphs in low-weight scenes are exempt). The key-noun rule is different in nature: it is a prohibitive hard constraint (banning synonym rotation), so it goes into "output: writing standards", with its objects limited to core nouns, terms, and personal names, which do not intersect with common-rules' emotion-word caps and metaphor-reuse entries, so the writer does not read "repetition is good" and "repetition of 3 times or fewer" as a contradiction. The alternative (all five categories into writing standards) was rejected: it would trigger a dimension F warmth-balance FAIL and a telegram-style risk (the asset pack's own warning about over-deletion pattern 9).

Deduplication wording: prompts already have "alternating narrative rhythm" (banning uniform paragraph lengths throughout) and texture-requirements "paragraph precision layering", so statistical anchors only add three microscopic distribution objects (sentence length, commas, sentence openings) and do not repeat the paragraph-alternation semantics (dimension H treats same-format repetition as FAIL); prompt-crafting's "post-assembly deduplication check" is updated with the same prompt.

### D3: Ornate emptiness goes into common-rules T1; positive principles go into living-voice

"More than 3 adjectives in a single sentence" and "cut opening descriptions to two or three strokes" are thresholds, and by repo rules thresholds may only be defined in common-rules.md (the check-conflicts double gate). They go into the T1 family (with "why it is banned + what to change it to"), are picked up on the generation side through the existing T1 short-table injection channel, and are scanned directly on the cleanup side, so both sides share one source. "Emotion-list ban / deviant expression / description visibility" have no numeric lines, so they are added to living-voice as additions only (git diff shows only added lines), and prompt-crafter injects 1-2 sentences each through the positive human-feel points channel.

### D4: structural-heat data is embedded in laws 2 and 3, with no new law numbers

The structural-heat spec (`openspec/specs/structural-heat/spec.md`) enumerates "seven laws" as MUST content; adding an eighth law would require changing that spec. The dialogue-density line passing zone and the mid-section measured data are data additions to the existing laws 2 and 3, so embedding them in the original text keeps the spec untouched. The file header's existing statements ("single-book measured defaults, calibrate by style and genre" and "author side takes priority over detection optimization") are followed; prompt-crafter only references the knowledge when ordering scenes and does not turn it into a hard quota (the author's chapter-outline order takes priority).

### D5: Asset-pack exclusion list (with reasons recorded)

| Excluded item | Reason |
|---|---|
| Point-of-view mixing anchors (first person dominant with occasional switches to second person) | Directly conflicts with the point-of-view system decided by the chapter outline's `outline.pov` |
| Suggestions to insert ellipses/dashes | Conflicts with common-rules' current dash-usage ruling |
| 3-gram repetition zero tolerance | Has wording tension with "key nouns keep one wording"; the adjudication wording (functional anchor-word repetition is human flavor, non-functional phrase reuse is a fingerprint) needs a separately designed detection implementation, left for a later change |
| Human-flavor ammunition, translationese, high-frequency word lists, and other cleanup-side content | Duplicates texture requirements, living-voice, and common-rules, or belongs to the cleanup scope; see the proposal Why |

### D6: Rhythm parameters are instantiated per chapter: ranges + emotional-curve derivation + staggered across chapters

Fixed parameters are themselves a new fingerprint: uniformity is prevented within a chapter, but if every chapter uses the same values, a detector doing cross-chapter statistics sees identical rhythm characteristics in every chapter. And real human writing rhythm is not a constant: tense scenes have dense fragments and gentle scenes have slow long sentences, so parameters are essentially a dependent variable of the content. So the knowledge file defines anchors as **ranges** (fragments about 1 per 4-7 sentences, one-sentence paragraphs about 1 per 6-10 paragraphs), and when assembling, prompt-crafter takes one set of "this chapter's rhythm parameters" from the ranges based on the chapter's emotional curve and scene weights, and writes them into the texture requirements. Three rules for taking values: (1) derive them from the emotional curve (mapping table: tense/outburst goes to the dense end of the range, gentle/setup goes to the sparse end), with no baseless randomness, since an LLM "randomizing" on its own converges to a middle point, while emotional curves differ from chapter to chapter, so entrusting variation to content is more reliable than entrusting it to dice; (2) stagger them against the previous chapter's prompt parameters (prompt-crafter reads the previous chapter's prompt file to check; prompts/ is already a readable product); (3) parameters only constrain the whole chapter's tendency, and when a local emotional passage speeds up or slows down in the opposite direction per the existing "alternating narrative rhythm", the emotional passage wins. The core of human flavor is rhythm following content; parameters are only a floor guard against uniformity, not a writing goal (the real sources of human flavor remain living-voice's three layers: something to do right now, details following the point of view, dialogue while doing things).

### D7: Source and license attribution

The asset pack README states "rules nineteen/twenty-six and other field-tested rules are personal accumulation; cite the source when quoting; ask the original author for permission before public or commercial use". The `statistical-anchor.md` file header MUST mark its rewritten source; the structural-heat added data comes from the same source, so marking "external single-book measurement" inside the laws is enough (that file already has the same annotation convention).

## Risks / Trade-offs

- [Quantitative anchors get executed mechanically by the model, and rhythm itself becomes a new template (telegram style within a chapter / same parameters across chapters)] → Triple protection: homed at the bottom in texture requirements, not in the hard-rules zone (D2); parameters instantiated per chapter, derived from the emotional curve, and staggered against the previous chapter (D6), so parameters differ across chapters; writing-execution Step 5 and anti-ai Gate D cleanup as a backstop. Residual risk: parameter values can be calibrated per book.
- [Token increment per chapter prompt] → The fixed injection channel adds about 300 words (4 statistical-anchor lines + 3 positive sections + the ornate-emptiness short-table row), about 400-600 tokens per chapter, below the per-chapter fluctuation of sparse scene-methodology injection. Acceptable.
- [Deployed product `anti-ai.md` grows in size] → About 4-6KB (under 10%), with the single-file merge mechanism unchanged, in exchange for closing the "no quantitative anchor for rhythm at generation time" gap.
- [New numbers trigger check-conflicts conflicts or out-of-bounds] → The new objects (fragments, commas, dialogue share) do not overlap with the authoritative source's existing threshold objects; the CI double gate exposes problems immediately, verified red-first-then-green during implementation.
- [test_platforms assertions too weak to catch a missed merge] → Following the existing "merged structural-heat law" assertion, add a merged-product content assertion for the statistical anchors (red first, then green).

## Migration Plan

1. Knowledge layer first (statistical-anchor.md as a new file + three files with additions), then run check-conflicts / check-agents.
2. Update the init.py merge list and add test_platforms.py assertions (red first, then green).
3. Update prompt-crafting.md injection scope and self-check table, then run check-agents.
4. E2E: `test_platforms.py` all green on seven platforms; old projects pull the new product via `sync-project.py`. Rollback is a revert of the commit, with no data migration.

## Open Questions

(None. All wording adjudications are settled in D5; remaining numeric calibration is per-book tuning during use and does not affect this change.)
