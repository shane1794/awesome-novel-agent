# generation-prompt-antiai Delta

## Purpose

Give prompt-crafter anti-AI injection increments for assembling generation prompts: inject statistical distribution anchors, ornate-emptiness protection, the emotion-list ban and deviant expression, the description-visibility test, and dialogue-position density knowledge into pre-writing prompts, so the main text carries human statistical characteristics from the generation stage instead of relying on post-writing cleanup. Injection follows the existing channels and sparse principles, and generation/cleanup separation stays unchanged.

## ADDED Requirements

### Requirement: The statistical rhythm anchor knowledge file must exist and be generalized

The knowledge file `knowledge/anti-ai/statistical-anchor.md` MUST exist in the repo and MUST be added to the anti-ai merge list in `tools/init.py` so it ships with the deployed product. Its content MUST satisfy: (1) cover five anchor categories, all stated as **ranges**: sentence-length rhythm (about 1 fragment of 5 words or fewer per 4-7 sentences), paragraph rhythm (about 1 one-sentence paragraph per 6-10 paragraphs), comma density (0-4 per paragraph, varying), sentence-opening types (no repeat of the same type for 3 paragraphs in a row), and key nouns keeping one wording (synonym rotation banned); (2) state the parameter-instantiation principle: rhythm anchors are a floor guard against uniformity, not a writing goal, and concrete parameters are a dependent variable of this chapter's emotional curve (tense scenes have dense fragments, gentle scenes have slow long sentences), with a reference mapping table from emotional passages to rhythm tendencies; (3) use no hard-quota wording such as "must / must not fall below / share must not fall below", no share floor, and no global fixed point values (aligned with the prompt-audit dimension F warmth-balance wording); (4) contain no specific book titles, character names, detector platform names, or chapter numbers; (5) contain no suggestions that conflict with the repo's current punctuation wording (no suggesting inserting ellipses or dashes); (6) contain no point-of-view mixing entries (point of view is decided by the chapter outline's POV); (7) state at the top that the measured source is single-book attack-and-defense experience, with the ranges as defaults calibrated per book and genre.

#### Scenario: Reachable after deployment
- **WHEN** reading the deployed product `.claude/knowledge/anti-ai.md` after `python tools/init.py` initializes a project
- **THEN** the merged product contains the statistical rhythm anchor content, and `tools/check-agents.py` passes its check (exit 0)

#### Scenario: Content generalization acceptance
- **WHEN** a human or script checks `knowledge/anti-ai/statistical-anchor.md`
- **THEN** all five anchor categories are present, the text has no book titles, detector platform names, or chapter numbers, no ellipsis/dash suggestions, and no point-of-view mixing entries, and the top carries the single-book measured source and per-book calibration statement

### Requirement: Rhythm parameters must be instantiated per chapter; identical parameters across chapters are banned

When prompt-crafter assembles a prompt, it MUST take one concrete parameter set from the knowledge file's anchor ranges for **this chapter** and write it into the "texture requirements" sub-section (this chapter's rhythm parameters). The values MUST satisfy: (1) they are derived from this chapter's emotional curve and scene weights (per the mapping table: tense/outburst passages take the dense end of the fragment range, gentle/setup passages take the sparse end), not fixed constants or baseless random numbers; (2) they differ from the previous chapter's prompt rhythm parameters (read the previous chapter's prompt file to check; identical parameters in two consecutive chapters are a violation); (3) they constrain the whole chapter's tendency, not a per-passage quota: when a local emotional passage speeds up or slows down in the opposite direction per the writing-methodology "alternating narrative rhythm", the emotional passage wins, and rhythm parameters must not suppress emotional speed changes. "Key nouns keep one wording" is still injected into "output: writing standards" as a hard constraint, with objects limited to core nouns, terms, and personal names. Rhythm-parameter entries MUST state the lowest concession position (yield first when conflicting with red lines, word-count compression, T1 words, cognitive verbs, or senses; low-weight compression passages are exempt) and their execution status (a tendency, not a hard rule), with no self-reference.

#### Scenario: Prompts contain this chapter's parameters, and parameters differ chapter to chapter
- **WHEN** prompt-crafter assembles prompts for two chapters in sequence
- **THEN** each prompt's texture-requirements sub-section contains one set of this chapter's rhythm parameters (concrete values within the ranges), the two sets are not fully identical, and each set's values match that chapter's emotional-curve direction (tense chapters have denser fragments than gentle chapters)

#### Scenario: Prompts contain all five anchors, homed correctly
- **WHEN** prompt-crafter finishes assembling `prompts/vol-{N}-ch-{M}-prompt.md`
- **THEN** the texture-requirements sub-section contains this chapter's parameters for the four categories of sentence length, paragraph, commas, and sentence openings (with the concession statement and no share floor), the writing-standards section contains "key nouns keep one wording" (with object limits), and the parameters do not appear in the rules-that-must-not-be-violated list

#### Scenario: No cross-source repetition with existing rhythm rules
- **WHEN** reading through the assembled prompt
- **THEN** paragraph-alternation semantics are defined exactly once by the existing "alternating narrative rhythm", and rhythm parameters only add the three distribution objects of sentence length, commas, and sentence openings, without repeating existing semantics such as "no uniform paragraph lengths throughout" (aligned with the prompt-audit dimension H deduplication hard gate)

#### Scenario: Emotional speed changes take priority over parameters
- **WHEN** a high-weight scene in this chapter is an outburst passage whose emotional rhythm demands short sentences throughout
- **THEN** the scene is written per the emotional passage, and rhythm parameters do not act as a hard constraint (parameters are a whole-chapter tendency; local passages follow the emotional passage)

### Requirement: Ornate-emptiness protection must share one source on the generation and cleanup sides

`knowledge/anti-ai/common-rules.md` MUST add the ornate-emptiness family to T1: (1) adjective stacking in a single sentence (split the sentence when there are more than 3); (2) piling consecutive environment/appearance descriptions at the opening (cut to two or three strokes); (3) ornate imagery that is physically impossible (imagery must be something that can really happen). prompt-crafter's T1 short-table injection channel MUST cover this family. New quantitative statements MUST pass `tools/check-conflicts.py` with no conflicts.

#### Scenario: Scannable on the cleanup side
- **WHEN** the anti-ai agent clears items one by one per common-rules T1
- **THEN** the ornate-emptiness family entries are in the T1 table, carrying "why it is banned + what to change it to", with no conflicts against existing thresholds (check-conflicts.py exit 0)

#### Scenario: Injectable on the generation side
- **WHEN** prompt-crafter injects the T1 most-toxic sentence-pattern short table per Step 1.6
- **THEN** the short table includes the opening-description cap and the imagery-realism constraint, without moving the whole table over

### Requirement: The emotion-list ban, deviant expression, and description visibility must enter the positive methodology

`knowledge/anti-ai/living-voice.md` MUST add three sections of positive principles (additions only, defining no new thresholds): (1) the emotion-list ban: do not list complex emotions as a list; write only one action or one detail; (2) deviant expression: a character's reaction must belong to "this person" (identity, body habits, what they need to do right now), and different people facing the same kind of situation must not react the same way; (3) the description-visibility test: after writing a description, check "delete it; does the character still hold up". A description that holds up makes the character visible; one that does not is piling no matter how ornate. The positive human-feel points prompt-crafter injects MUST cover all three (1-2 distilled sentences each).

#### Scenario: Positive methodology additions
- **WHEN** checking `living-voice.md` and the deployed product
- **THEN** all three sections are present, existing entries are untouched (git diff shows only added lines), and the anti-ai.md merged product contains the three sections

#### Scenario: Prompts contain the positive points
- **WHEN** prompt-crafter injects the positive human-feel points
- **THEN** the prompt contains distilled versions of the emotion-list ban, deviant expression, and description-visibility test, introducing no new thresholds

### Requirement: Dialogue-position density knowledge must be added, with the author side taking priority

`knowledge/anti-ai/structural-heat.md` MUST add measured data inside law 2 (dialogue density) and law 3 (positional heat value): when every line carries payload, a dialogue-line share of 50-70% is the passing zone; about 60-85% of mid-section content is immune to edits (floor 0.55-0.68); and placing pure-dialogue passages in the mid-section lets slices avoid narrative blocks. Additions MUST be embedded in the existing laws (no new law numbers), following the file's existing statements of "single-book measured defaults, calibrate by style and genre" and "author side takes priority over detection optimization". When prompt-crafter orders scenes, it MAY reference this knowledge and MUST NOT write it as a hard positional quota.

#### Scenario: Additions inside the laws
- **WHEN** checking `structural-heat.md`
- **THEN** the law count is unchanged (still seven), laws 2 and 3 contain the new measured data and calibration statement, and `tools/check-conflicts.py` exits 0

#### Scenario: Scene ordering is not a hard quota
- **WHEN** prompt-crafter marks scene weights and order
- **THEN** dialogue-position knowledge appears only as ordering reference (if at all), and when it conflicts with the author's chapter-outline order, the author side wins

### Requirement: Injection scope and generation/cleanup separation constraints stay unchanged

All additions in this change MUST land through the existing injection channels (positive human-feel points / T1 short table / writing standards / texture requirements) and MUST NOT change the existing boundaries: fatigue-word thresholds, T2/T3 tiers, and second-tier banned words are not injected; the writer does not write while checking a negative list; prompt-crafting's "post-assembly deduplication check" and the Step 4 acceptance self-check table's "anti-AI injection scope" check item MUST cover the new entries in sync (new rhythm anchors and the existing rhythm-alternation and sentence-pattern-alternation rules do not count as same-format repetition under the prompt-audit dimension H wording).

#### Scenario: Acceptance self-check covers the new entries
- **WHEN** prompt-crafter runs the Step 4 acceptance self-check
- **THEN** the self-check table's "anti-AI injection scope" item includes the statistical rhythm anchors and the new positive-point entries, and T2/T3 tiers and fatigue-word thresholds are still outside the injection scope

#### Scenario: Full-chain checks pass
- **WHEN** running `tools/check-agents.py`, `tools/check-conflicts.py`, and `tools/test_platforms.py`
- **THEN** all three exit 0, and E2E deployed-product assertions (if any) match the merged-product content
