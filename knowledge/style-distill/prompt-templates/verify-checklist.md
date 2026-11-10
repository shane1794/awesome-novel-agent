# Case 2 Acceptance Check List (for anti-ai, replacing the old Gate G/distill-style.py check)

## Trigger
Run the instruction-following acceptance check on each chapter's text: read the same chapter's `prompts/vol-{N}-ch-{M}-prompt.md` for its
[Vocabulary] [Sentence Pattern] [Rhythm] [Rhetoric and Sensation] [Emotional Expression]
[Conversation Style] [Cohesion] [Perspective] [Hard Rules] [Overall Tone] [Style
Reference Examples] of the same chapter and compare them with the text one by one to
judge. Use and generate the same prompt word (cognate). (Two states: Undistilled state
prompt word has no quantified stanzas and contains text qualitative four fields → accept
"narrative identity/hard constraints/AI error prone/descriptive level" according to the
qualitative bar; distilled state → four categories of bars below + [style reference
example sentence] make style anchor point to compare the text sentence by sentence. The
rigid rules/tone/example sentences of the legacy jieba card (confidence>0 silent layer)
are according to §6.0b Go back and read the four qualitative fields of the text, and the
example sentences serve as descriptive level examples).

## Check items (four categories)
1. Value/proportion bar: "About 48% of the dialogue" → Whether the dialogue in this
   chapter deviates significantly (deviation is a violation, and the numerical accuracy
   is not required).
2. Rigid rules: Judgment one by one (such as "No 'like'" → check whether it appears; if
   it appears, it is violated).
3. Modeling rules: rhythm parameters (dialogue-intensive area must be monologue buffered
   after ≥4 rounds, pure narrative ≤3 sentences), dialogue mode (D-01~),
Anchor points (semantic closed loop at the beginning/end of the chapter) are determined
one by one.
4. Soft guide strip: Whether the overall tone is consistent.

## Violation report format (written in archives/*.anti-ai.md acceptance section)
| Article number | Original text requirements | Text performance | Violation or not | Suggestions |
Conclusion: PASS / FAIL (number of violations / total number of violations)

## Deterministic judgment caliber (this article is self-contained and does not rely on tools/*.py)
- **violated judgment** ("violated or not" column and conclusion count):
  `true/是/yes/1/违反/违反了` → violated; `false/否/空/other字符串` → not violated. Peel off the
  trailing punctuation and modal particles before matching (`是。`→`是`, `yes。`→`yes`,
  `违反了`→`违反`, `是；`→`是`); the string Boolean output by LLM will all converge according to
  this to prevent accidental card drawing.
- **verdict**: Any violation → FAIL; none of them are violated → PASS.
- **should_reroll (card draw)**: The current round is <3 and the number of violations in
  this round is >0 → rewrite (the violations report is fed back to the writer).
- **pick_best (pick the best after 3 rounds)**: Take the round with the fewest
  violations; take the latest round if there are ties.
- **format_report**: The above table item by item + conclusion line
  `Conclusion: FAIL/PASS (violations/total)`.
