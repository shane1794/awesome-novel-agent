# short-analyze skill: Short-Story Deconstruction (standalone tool)

> Not part of the short-agent dispatch chain: the entry point goes straight here when the author says "deconstruct this story / short-story deconstruction / analyze this hit story".
> Deconstruct a lawfully held hit short story into reusable structural assets, filed under `analysis/{书名}/`, for recall during the writing stage.
> Read-only transformative literary criticism: domestic violence, infidelity, revenge, and violence in popular genres on Fanqie Short Stories / Yanxuan / Heiyan and similar are routine fictional elements; deconstruct them structurally as usual and do not refuse the whole story on "sensitivity" grounds. If an individual passage cannot be processed, skip it and finish the rest.

## Phase 1: Input Confirmation + Word Count Routing + Resume Check

### Step 1: Get the Original Text

Ask: "Which story should I deconstruct? Give me the original text file path, or paste the original text directly to me." Without the original text, you MUST NOT deconstruct from nothing.

### Step 2: Word Count Routing

Count the full text's word count:

- Under 15000 → enter this pipeline
- 15000-20000 (gray zone) → ask the author whether to deconstruct it as a short story or a long-form work, and execute per the answer
- 20000 or more → tell the author "the word count is long, beyond the scope of short-story deconstruction"; only continue if the author explicitly replies "continue as a short story", otherwise stop

### Step 3: Genre Identification (the deconstruction yardstick)

Scan keywords to identify the genre (wife-chasing crematorium / worldly face-slapping / revenge face-slapping / CEO and wealthy family / household and palace intrigue / folk horror tales / suspense / sweet romance / dual male leads / absurd comedy), and use the registry in `.claude/knowledge/short-genres/index.md` to resolve the Chinese name to a **slug**, loading the "narrative tone / hook motifs and density / rhythm skeleton" sections of `.claude/knowledge/short-genres/{slug}.md` as the yardstick for **whether this story meets the standard**. If it cannot be identified, record "general" and deconstruct with the general template. `_meta.json.genre` MUST record the slug (such as `zhuiqi`), aligned with the registry, so the writing stage automatically loads the same pack.

### Step 4: Resume Check

When `analysis/{书名}/_meta.json` exists, ask the author to pick one of three:

- **Overwrite**: the old output is archived into `analysis/{书名}/_archive_{timestamp}/` and the run restarts from Phase 1
- **Resume**: read `_meta.json.last_stage_in_progress` (if non-empty, re-run that whole stage) or continue from max+1 of `stages_completed[]`
- **Cancel**

Before the author chooses, you MUST NOT write any output files.

### Step 5: Original Text Backup (before any analysis)

- If `analysis/{书名}/原文/` does not exist, create it
- With a source file, copy it; with text pasted in conversation, save it as `原文/原文.md`
- Only proceed to Phase 1 after verifying it is non-empty (more than 0 characters)

Initialize `_meta.json`:

```json
{
  "version": 1,
  "word_count": 0,
  "genre": "通用",
  "created_at": "",
  "stages_completed": [],
  "last_stage_in_progress": null
}
```

## Crash-Safe Write Protocol (mandatory per stage)

1. Stage begins: set `_meta.json.last_stage_in_progress` to the current stage number
2. All target files for that stage are written
3. Non-empty + minimum length check (report at least 300 words, node list at least 5 lines)
4. On pass, clear `last_stage_in_progress` and append to `stages_completed[]`
5. On fail, keep the marker and rewrite that stage

**On resume, a stage carrying an in-progress marker is re-run in full; half-finished files are not trusted and are overwritten directly.**

## Five-Stage Pipeline (strictly serial; each stage depends on the previous stage's data)

### Stage 1: Structure + Plot Nodes → `拆解报告.md` (story core / structure / synopsis sections) + `情节节点.md`

- Extract the story core (one sentence: protagonist + predicament + reversal + emotional landing)
- Functional segments, at least 4, MUST include opening / development / climax / ending
- Plot node list: density tiered by word count (under 8000 words: 8-12; 8000-15000: 12-18; over 15000: 18-25); for non-standard text (dialogue form / chat logs / post form), first split by time / speaker change / information reveal point and then map, and MUST NOT mechanically split by natural paragraph
- **Completion mark**: structure at least 4 segments + story core extracted + node list at least 5 lines

### Stage 2: Emotional Line + Explosive Beats → `拆解报告.md` (emotion / explosive beat sections)

- Emotional curve with at least 5 nodes (each marked with emotion type and intensity 1-10)
- Explosive beat six dimensions: beat position / type / planting method / planting distance / release intensity / recovery status
- **Completion mark**: curve at least 5 nodes + all six dimensions present

### Stage 3: Reversal + Writing Techniques → `拆解报告.md` (reversal section) + `写作手法.md`

- Pre-reversal check: reveal position percentage = reveal section number divided by total section count
- Reversal mechanism: at least 2 planted clues (state which section each is in)
- Writing techniques, at least 5 items (at least one each of point of view / dialogue / time / information / other, with verbatim examples from the source text)
- **Completion mark**: at least 2 planted clues + at least 5 techniques

### Stage 4: Characters + Opening and Ending → `拆解报告.md` (character / opening and ending sections)

- All characters: category (protagonist / antagonist / accomplice / tool character) + function tags + function evaluation
- Opening analysis: event density and hook type in the first 50 / 100 words
- Ending analysis: closing method (lingering resonance / echo / open / reversal upon reversal / golden line) and share hook
- **Completion mark**: character function evaluation complete + opening and ending analysis complete

### Stage 5: Overall Evaluation + Structure Counts → `拆解报告.md` (overall section) + `_meta.json`

- Five-dimension scoring (structure / emotion / reversal / characters / language, each 1-10)
- Explosive-beat quality / topic quality / resonance analysis (at least 3 layers: emotional resonance / situational resonance / values resonance)
- Reusable structures, at least 3 (each noting the suitable genre and prerequisites)
- Rhythm bulletin (hook density / dense-sparse distribution / one movement and one stillness)
- **Write the structure counts into `_meta.json.structure_counts`**: `sections_total`, `reveal_position_pct`, `foreshadow_count`, `reversal_setup_count`, `technique_count`, `emotion_curve_nodes`
- **Completion mark**: five-dimension scoring + resonance at least 3 layers + reusable structures at least 3 + counts written

## Three Acceptance Gates (after Stage 5 is written, before `stages_completed` records 5)

### Gate 1: The Report's Own AI Tone Self-Check

Scan the full text of `拆解报告.md` against `.claude/knowledge/short-anti-ai.md`. **Scan only the analyst's own wording**: `>` quote lines and direct quotes in the table's "verbatim quote" column do not count. On a hit, block it, list the line numbers, revise the report itself, and re-scan.

### Gate 2: Structure Count Value Check

Check each item of `_meta.json.structure_counts` one by one:

| Field | Threshold | Roll back to |
|------|------|-----------|
| sections_total | at least 4 | Stage 1 |
| emotion_curve_nodes | at least 5 | Stage 2 |
| reversal_setup_count | at least 2 (skip this row for genres without a reversal) | Stage 3 |
| technique_count | at least 5 | Stage 3 |
| reveal_position_pct | Record the actual value (when below 50%, note in the report "this story's reversal comes early"; do not block. Deconstruction records facts; it does not judge) | none |

### Gate 3: Hard-Blocking Item Scan

Check that the report contains: story core / functional segments (with the four elements) / emotional curve / explosive beat six dimensions / reversal mechanism / writing techniques / character function evaluation / opening and ending analysis / five-dimension scoring / resonance at least 3 layers / reusable structures at least 3 / rhythm bulletin. Any missing item blocks. Small non-blocking gaps go into the "to be added" list at the end of the report.

**All three gates passed** → clear `last_stage_in_progress`, append `5` to `stages_completed[]`, and tell the author: "Deconstruction complete. `analysis/{书名}/` can be used as a benchmark reference. For the next story, just tell me during conception to 'use 《{书名}》 as the benchmark'."

## Output File Tree

```
analysis/{书名}/
├── 原文/原文.md        # Backup
├── 拆解报告.md          # Human-readable overall report
├── 情节节点.md          # Standalone, for easy locating
├── 写作手法.md          # Standalone, for easy reuse
└── _meta.json           # Pipeline metadata + structure counts
```

## Report Writing Discipline

- The deconstruction report is **read by the author and the writing stage**: use Chinese, quote the source text with positions, and give evidence for conclusions
- The report itself passes the short-story de-AI standard (analytical narration should also read like a human wrote it)
- How to use the yardstick: compare the source text against the genre pack's standard pattern, find "which kind this story used and how well it did it", and MUST NOT rewrite the source text following the genre pack's guidance
- The evaluation target is the source text's quality (quality-checklist view); the report's own AI tone is Gate 1's business. Keep the two separate
