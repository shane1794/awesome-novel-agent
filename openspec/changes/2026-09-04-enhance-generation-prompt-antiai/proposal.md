# Proposal: 2026-09-04-enhance-generation-prompt-antiai

## Why

The de-AI asset pack (gifted 2026-09-03, at `~/Downloads/去AI味资产包_20260903/`) shares the same origin as this repo's anti-AI system. Comparing it item by item confirms: the cleanup side (the anti-ai pipeline) and the structural-heat knowledge already have equivalent implementations for about 70% of it, but **the generation side (prompt-crafting assembling prompts) has five real increments**. The existing generation prompts state all pacing constraints qualitatively ("alternate long and short sentence patterns", "no uniform paragraph lengths throughout"), with no statistical distribution anchors; synonym cycling is already identified as an AI fingerprint in anti-ai-writing.md (section 1.4), but the generation side has no positive solution for it; description density and physical realism have no constraint lines; emotion lists and generic reactions have no bans; and scene ordering lacks dialogue-position density knowledge. This change only brings in the parts that directly improve generation prompts; the cleanup-side wordlist increments are out of scope for this change.

## What Changes

- `skills/prompt-crafting.md` expands the anti-AI injection scope by 5 categories, with the injection channels (positive human-feel points + T1 short table + meta-narration ban + genre positive/negative examples) and the sparse-injection principle and generation/cleanup separation principle unchanged:
  1. **Statistical rhythm anchors (instantiated per chapter)**: anchors are defined as ranges: short fragments about 1 per 4-7 sentences, one-sentence paragraphs about 1 per 6-10 paragraphs, commas 0-4 and not fixed, sentence-opening types not repeated for 3 paragraphs in a row. prompt-crafter takes one set of "this chapter's rhythm parameters" from the ranges based on the chapter's emotional curve and injects them; the parameters differ from chapter to chapter (tense chapters have dense fragments, gentle chapters have slow long sentences), and the same parameters must not repeat across chapters
  2. **Key nouns keep one wording**: core nouns and terms always reuse the same wording; synonym rotation is banned
  3. **Ornate-emptiness protection**: opening environment and appearance descriptions cut to two or three strokes, imagery must be something that can really happen, and the combination of delicate writing plus a basic common-sense error is ironclad proof of AI
  4. **Emotion-list ban + deviant expression**: complex emotions must not be listed as a list; reactions must belong to "this person" (deviant expression, not safe expression)
  5. **Description must make the character visible**: the test is "delete this description; does the character still hold up"
- `knowledge/anti-ai/` adds `statistical-anchor.md` (generalized rewrite: book names, detector proper names, ellipsis/dash suggestions, and point-of-view mixing entries removed; marked with its single-book measured source and a per-book calibration statement)
- `knowledge/anti-ai/common-rules.md` T1 adds the ornate-emptiness family (adjective stacking / opening-description piling / physically impossible imagery), so the cleanup side and the injection side share one source
- `knowledge/anti-ai/living-voice.md` adds the emotion-list ban, the deviant-expression principle, and the description-visibility test (positive principles that define no new thresholds)
- `knowledge/anti-ai/structural-heat.md` laws 2 and 3 gain the dialogue-density line passing zone (when every line carries payload, a dialogue-line share of 50-70% is the passing zone) and mid-section measured data (60-85% of content is immune, floor 0.55-0.68), following the existing "single-book measured defaults, calibrate per book" framework
- `tools/init.py` adds `statistical-anchor.md` to the anti-ai merge list

## Capabilities

### New Capabilities

- `generation-prompt-antiai`: anti-AI injection increments for prompt-crafter's generated prompts: statistical distribution anchors, key nouns keeping one wording, ornate-emptiness protection, the emotion-list ban and deviant expression, the description-visibility test, dialogue-position ordering reference, plus injection-scope constraints (statistical anchors stated as distribution tendencies, not quotas; negative lists only enter through the T1 short-table channel; generation and cleanup stay separated)

### Modified Capabilities

(None. structural-heat.md gains data inside its laws, adding no new laws and changing no existing requirement, so no spec delta is listed.)

## Impact

- **Code/docs**: `skills/prompt-crafting.md` (Step 1.6 injection scope + the Step 4 acceptance self-check table's "anti-AI injection scope" check item), `knowledge/anti-ai/` (1 new file + 3 files with additions + the README directory), `tools/init.py` (merge list)
- **Deployment products**: `.claude/knowledge/anti-ai.md` grows by about 4-6KB, with no new failure paths (still a single-file merged product); each chapter's generated prompt gains a fixed injection increment of about 300 words (4 statistical-anchor lines + 3 positive sections + the ornate-emptiness short-table row)
- **Check chain**: `check-agents.py` (prompt-crafting reference-path checks), `check-conflicts.py` (new quantitative statements do not conflict with the existing threshold system), `test_platforms.py` (E2E assertions on merged-product content, synced if needed)
- **No** new third-party dependencies, no platform-adapter (platforms.py) changes, no breaking changes
