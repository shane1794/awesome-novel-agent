# short-write SOP: Main Text Writing in Batches

> Executed by short-writer. Produce the main text in batches under the frozen contract, 2-3 sections per batch.

## Step 1: Preparation

- Read the order: this batch's section numbers plus the **re-injected contract hard-rules zone** (written into the order by the coordinator; if not received, return the order instead of tracing the contract back yourself)
- Read the `outline.md` rows for this batch's sections plus the last 300-500 words of `manuscript.md` (for continuity)
- Read the general base plus the format standard plus the de-AI standard

## Step 2: Two Questions Before Writing (per section)

1. What is the target emotion of this scene?
2. Which technique entry in the contract applies here, and in which paragraph is it used?

If either cannot be answered, go back and read the contract; do not force the writing.

## Step 3: Writing Section by Section

- **Weave the three dimensions in**: happening / perception / reaction woven into the same continuous main text; splitting them into three stacked paragraphs is forbidden; break paragraphs on a new action / object / piece of information / line of dialogue / shift of gaze
- **Enter the scene late, leave early**: the first sentence is already inside conflict or tension; getting up / traveling / small talk / setting up is not expanded
- **Write emotion directly, with a concrete follow-through**: after an emotion word comes an action or object specific to this scene; write each emotion once
- **Clear out possessives**: do not write "my heart / my soul / my eye sockets" (我的心 / 我的灵魂 / 我的眼眶); do not write small clauses led by "I know / I feel / I see myself" (我知道 / 我感到 / 我看到自己)
- **Dialogue, four functions**: every line completes at least one of advancing the plot / revealing character / creating conflict / planting foreshadowing (for power games and subtext techniques see `.claude/knowledge/short-craft/dialogue-mastery.md`; for the hook type library see `.claude/knowledge/short-craft/hooks-chapter.md` / `.claude/knowledge/short-craft/hooks-paragraph.md` / for suspense design see `.claude/knowledge/short-craft/hooks-suspense.md`; for cross-genre techniques see `.claude/knowledge/short-craft/genre-writing-techniques.md`)
- **Reversal section**: complete the reveal within one section; when revealing, use looking back / monologue / physical evidence to **string the thread instantly** (bring all earlier clues back before the reader's eyes at once); the impact is stronger than in every earlier section
- **Throughline prop**: its third appearance (revealing the truth) lands in the reversal or ending section
- **Every section ends with a hook**; the emotional intensity within a section follows its outline row

## Step 4: Machine Verification (after each batch)

```bash
for PYBIN in python3 python py; do "$PYBIN" -c "" 2>/dev/null && break; done
"$PYBIN" -c "from pathlib import Path; import re; t=Path('stories/{slug}/manuscript.md').read_text(encoding='utf-8'); import sys; print('总字数', len(re.sub(r'\s','',t)))"
```

- **Word count per section**: at least 800 (at least 500 for high-information-density genres); falling short means the section is unfinished, so add sub-events / dialogue / flashback memories / environmental objects (brought in through action); padding is forbidden, and "add a perception layer" style stacking is forbidden
- **Total word count**: at least 8000 once everything is complete
- **Section count conserved**: the main text's section count equals the outline's planned section count; if a section turns out not to deserve standing alone, return to adjust the outline instead of quietly cutting it during writing
- Do not let the model estimate word counts; do not use `wc -c` (byte count); without Bash/Python access, declare "machine word count verification not completed" and estimate quickly by lines (about 15 words per line)

## Step 5: Completion Threshold (once the whole story is written; do not proceed to polishing until it passes)

- [ ] Total word count at least 8000 (machine measured)
- [ ] Every section meets its word count target
- [ ] Section count equals the outline's section count
- [ ] Format self-check: section markers uniform / single line break between paragraphs / no indentation / no Markdown / dialogue on its own line / quotes in the platform style / banned punctuation zero / no meta-information words
- [ ] Self-check while writing: AI stock phrases zero / degree adverbs at most 3 per thousand words / metaphors not in clusters / self-check records are not written into the main text

## Constraints

- Rule conflicts follow the contract's conflict ruling table; do not rule on them yourself
- Additions beyond the contract are marked with `[AI addition: ...]`
- Resuming after an interruption: read how many sections of the manuscript are already written, and continue from the interrupted section
