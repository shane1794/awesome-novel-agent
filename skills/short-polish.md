# short-polish SOP: De-AI Flavor and Fine Polishing

> Executed by short-editor. Change only the expression, not the plot; the short-story standard (`.claude/knowledge/short-anti-ai.md`) is the only basis for judgment.

## Step 1: Keep/Delete Comparison Table, Judged Paragraph by Paragraph

| Keep (selling point) | Delete |
|---|---|
| Direct emotion words (followed by a concrete follow-through) | Vague emotional summary sentences (a trace of X welled up in the heart, 一丝 X 涌上心头) |
| First-person judgment sentences / spoilers / "burn the bridge, then the reckoning" previews | Neutral author exposition (explanation unrelated to the character's emotion) |
| Judgment one-liners / "heart-dead" chapter endings | Hollow philosophical elevation |

Criterion: **Does this sentence carry the protagonist's subjective emotion right now?** Keep it if it does, delete it if it is neutral.

Delete first: if deleting loses no foreshadowing / hook / character / plot / necessary information, delete directly; only rewrite when something would be lost; prefer rewriting over regenerating.

## Step 2: Self-Check List, Item by Item (Section 11 of the standard)

Scan especially for:

- First-person possessives (my heart becomes heart, 我的心 → 心) and leading small clauses (I know / I feel / I see myself, 我知道 / 我感到 / 我看到自己)
- Degree adverb density: weakening (slightly / faintly / slowly / gently, 微微/淡淡/缓缓/轻轻) plus strengthening (just / in the middle of / very / extremely / increasingly / as expected / seemingly, 正/正在/非常/十分/极其/越来越/果然/好像) totaling at most 3 per thousand words
- AI stock phrases zero (met the eye / said to oneself in the heart / said in a deep voice / it is not hard to see / and so on, 映入眼帘 / 心中暗道 / 沉声道 / 不难看出 / 于是乎…)
- Metaphors not in clusters (functional metaphors, such as the throughline prop's imagery, are kept)
- Chapter endings not neatly tied off for the sake of tidiness (no forced parallelism / lists / rhyme)
- (Historical / alternate-world genres) modern vocabulary table scan with zero hits
- Names consistent with the record in setting.md

## Step 3: Six-Category Polishing Checklist

| Category | Check Items |
|----|--------|
| Opening | First 3 sentences grab the reader / no background setup / an opening hook exists / the scene enters mid-conflict |
| Emotion | The curve has a direction / enough planting before the reversal / enough impact after the reversal (peak held for one section) |
| Reversal | Surprising yet reasonable / the reveal completes the instant thread-stringing (clues linked back) / position matches the contract |
| Rhythm | No dragging / every sentence has value / density varies (dense at satisfying beats, sparse at transitions) |
| Hooks | A hook every 2-3 sections / a hook at each section's end (suspense or heart-dead lingering resonance) |
| Technique | A concrete reaction follows each emotion / the prop's three semantic steps complete / one movement and one stillness / opening event density at least 3 |

## Step 4: Format Compliance (grep, item by item)

- [ ] Section markers uniform throughout
- [ ] Single line break between paragraphs (no blank lines / `\n\n`)
- [ ] No indentation; main text paragraphs have no Markdown
- [ ] Dialogue on its own line, quotes match the platform
- [ ] Banned punctuation (ellipsis, double em dash, em dash, double hyphen) zero; pauses are rewritten at the semantic level (short sentences / action / line break), not mechanically replaced
- [ ] No meta-information words (this chapter / earlier text / foreshadowing / reader...)

## Step 5: Wrap-Up

- Sandbox assets: a hit in `sandbox/prose-regressions.txt` means failure; a hit in `sandbox/locked-lines.txt` means that line skips the ruling
- Word count re-measured and still on target (dropping below the floor means rolling back this round of deletions and switching to de-AI rewriting instead)
- **Clean delivery**: no self-check records, no check-mark comments, and no engineering terms at the end of the main text
- The finished draft is re-checked item by item against `.claude/knowledge/short-craft/quality-checklist.md` (chapter structure / opening / information delivery / scene / chapter ending / language)
- **Revision mode extra**: only touch the sections the author asked for; the difference list does not overreach (no changing the direction / deleting conflict / adding characters / changing character design / changing point of view); plot-level problems found are only marked and reported upward, not fixed on the spot
- The plot-level problem list (things this agent has no authority to fix) goes in the order notes and is returned to the coordinator
