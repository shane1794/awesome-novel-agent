# style-distill skill: Three-Stage 13-Template LLM Distillation (style-distill-order)

## 1. Main Card Distillation
1. Collect samples: the author's documents (`.md`/`.txt`, placed by the author) in the project root `novel-samples/` directory, `.agent/task/style-sample.md` (pasted in chat), or archived chapters. **If there are fewer than 6000 words (about 3 chapters' worth), tell novel-agent the quality is insufficient and it may be suspended.** With a 1500-word sample, sentence-length distribution and five-layer proportion statistics are noisy and scene card sub-samples are insufficient (each type needs at least 800 words or many will be skipped); only 6000-10000 words cover multiple scene types and give stable statistics.
2. Read `.claude/knowledge/style-distill/prompt-templates/feature-extract.md` (the methodology is the 13-template definition).
3. Stage one, decomposition (templates 1-4): annotate the sample paragraph by paragraph, sentence by sentence, and emotion by emotion (LLM internal reasoning, no files written).
4. Stage two, quantification (templates 5-8): frequencies, five-layer proportions, emotion channels, vocabulary, turned into a quantification table.
5. Stage three, modeling (templates 9-13): sentence pattern card, behavior tree, dialogue pattern, rhythm model, anchors, turned into modeling rules.
6. Converge:
   - Quantification table goes to the card's quantitative dimensions (case 1 has nine dimensions; schema in check-agents)
   - Modeling rules go to the card's voice layer (hard_constraints / soft_guidance / few_shot_examples)
7. Write `settings/writing-style.md` (the converged card) plus `settings/style-profiles/analysis/general.md` (the full quantification table and modeling rules).
8. Back up the old card to `settings/.style-versions/v{N}_{YYYY-MM-DD}.md` (N is the current maximum plus 1; card and analysis draft share the version).
9. confidence: the LLM gives **1-100 (must be >0)** based on sample quality and consistency. 0 is only for undistilled or manual cards (which take the qualitative injection branch, see prompt-crafting Step 1.1); setting a distilled card to 0 silently falls back to qualitative injection and loses the quantitative rendering. Write `last_updated` as the current date.
10. **Generate an author portrait** (for the author to confirm, written in the "Author Portrait" section at the top of `settings/style-profiles/analysis/general.md` plus in the handover report):
    - Open by stating the positioning: **"This is how the AI understands your writing style. It is not a literary review; the AI will write following this. Say directly wherever it is wrong."**
    - **The whole text uses the author's language, with no internal terms at all** (card / main card / scene card / confidence / dimension / override / distill / quantify / feature, and similar). Do not use anything the author would not understand:
      - "Your writing characteristics" (the narrative identity, restated in plain language, not copied from section names)
      - "The rules you set" (the hard constraints, restated in plain language, 2-4 items)
      - "3-5 quantified feelings the AI learned": "mostly short sentences (mostly within 20 words)", "dialogue is about half", "mostly plain description, restrained rhetoric", "words you love to use: ..."
      - "Your typical sentences", 2-3 items (verbatim from few_shot_examples)
    - End with a confirmation question: "Does this read like your writing? If not, just say 'not like me' and I will learn it again."

## 2. Scene Card Distillation (inside style-distill-order)
1. Classify the sample by paragraph into scenes (dialogue/fight/environment/inner-mono/transition/group-scene).
2. Aggregate a sub-sample per type (only distill when it is at least 800 words; skip a scene card when it falls short).
3. Run that scene's sub-sample through the same three stages as step 5 for the main card; in stage three, focus on rules that differ by scene.
4. Converge into an override (only the dimensions that differ from the main card) plus a scene voice layer.
5. Write `settings/style-profiles/{scene_type}.md` (inherits: writing-style.md plus override)
   plus `settings/style-profiles/analysis/{scene_type}.md` (that scene's quantification table and modeling rules).

## 3. Write Whitelist (the Only Exception)
| Tool | May write | Forbidden |
|------|--------|------|
| Write/Edit | settings/writing-style.md, settings/style-profiles/*, settings/style-profiles/analysis/*, settings/.style-versions/*, .agent/task/*-order.md (status only) | Do not write any other settings, chapters, or archives |
| Read | archives/, chapters/, settings/, sample files | Never read outside the project |
| Bash | No script calls (pure LLM extraction); explain other commands to novel-agent | Do not call retired tools |

## 4. Conflict Prevention / Self-Check
- Merge and deduplicate banned_words with the anti-ai banned words.
- A scene card override must not sit alongside the same dimension in the main card (an override replaces it).
- Self-check: frontmatter passes the check-agents validation (9 dimension keys / enums / distribution sums); the backup exists; idempotent (re-running on the same sample produces no extra backup).
- Card freeze: this skill performs no updates. Machine-generated chapters never write back to the card; re-distillation happens only when the author triggers it.
