# detect-loop skill: External Detection Calibration Loop (author-triggered, optional)

## Responsibilities and Boundaries

When the author voluntarily sends a draft to an **external AI detection tool** (such as Zhuque) for verification, fix it with minimal intervention in a targeted way: only touch the highest-scoring segment, leave everything else unchanged at the character level, lock the version once it meets the bar, and bank the experience.

- **Compliance statement**: This step is for the author's voluntary quality calibration of their own draft. It is not packaged as "detector evasion" and does not bypass any platform risk control; the repository contains no automation scripts, interface reverse-engineering documents, keys, or browser fingerprinting schemes for any detection platform. Those belong to tools the author provides locally.
- **Offline by default**: It is not part of the default pipeline; it only starts when the author explicitly says "send it for checking / run it through external detection / check it". If no submission method exists, end gracefully (tell the author they need to provide their own detection route or submit it manually on a web page) without blocking the main flow.

## Trigger and Input

novel-agent writes `detect-loop-order.md` to call the anti-ai agent (this skill is a branch SOP of anti-ai). Order inputs:

```markdown
# detect-loop-order
status: pending
inputs:
  - Draft path (by default the main text of the current chapter's .anti-ai.md in archives/, or a file the author specifies)
  - Submission method: local tool command (author-provided, may be empty) / author submits manually
  - Result file path (the submission output; for manual submission, the result file the author pastes)
  - Pass bar (default 0.5, adjusted to the detection tool's scale)
outputs:
  - Revised draft path
  - sandbox/detect-battles.md (append this round's battle record)
```

The outputs do not include the detection tool itself.

## Submission Adapter (platform-independent)

The repository only agrees on three things; connecting to the specific detection tool is entirely local to the author:

1. **Submission entry point**: one local command (author-provided, such as a local script), or the author manually pasting the draft on the detection web page.
2. **Result file**: the segment-by-segment result file produced by the submission (JSON or a table), with the agreed fields:

```json
{
  "tool": "Example tool name",
  "threshold": 0.5,
  "overall": "Overall conclusion text (may be empty)",
  "segments": [
    {"start": 0, "end": 536, "score": 0.5123, "text": "Original text of this segment (for locating it)"},
    {"start": 536, "end": 1024, "score": 0.2301, "text": "…"}
  ]
}
```

   `start/end` are character offsets; `text` is used to locate the content substring in the draft (offsets may differ by scale, so text matching takes precedence).
3. **Pass bar**: all segments with `score` below `threshold` count as passing; a single numeric scale, without introducing any other rating from the detection tool.

## Repair Discipline (per round)

1. **Fix only the single highest-scoring segment**: take the segment with the highest score; if several tie, take the earliest. All other segments stay **unchanged at the character level** (verify by comparing a content hash of that segment before and after the edit).
2. **Stable boundaries**: the first and last sentences of the segment stay verbatim; prefer edits of equal length (within plus or minus 3%); locate the content substring in the draft using the segment text, never by guessing line numbers.
3. **Repair order**: first check the "structural heat source law" in `.claude/knowledge/anti-ai.md` to judge the structure type. Change structure first (swap content type / cut the Q&A beats / split a micro-loop / delete the meaning confirmation), and do sentence-level cleanup after.
4. **Decision order**: author settings and chapter outline > genre knowledge > structural defaults > detection optimization. A score-lowering edit **must not** rewrite locked lines, chapter outline landing points, or other core expressions on the author side; on conflict, keep the author-side expression and mark the report "settings take priority, residual score accepted" or submit it to the author for a ruling.
5. **Damage control**: if the same segment improves by less than 0.05 for two consecutive rounds, or its score rises instead, stop using that kind of edit, switch content type in the next round, or roll back to the previous version (if the author says "worse than before / backfired", roll back immediately).
6. **Before and after each round**: after editing, re-run `check-chapter.py` in the same round (only submit for checking when exit code is 0); append each round's result to `sandbox/detect-battles.md` (round number / changes / segment-by-segment results / conclusion).

## Locking the Version and Banking Experience

- **Passing**: all segments below the pass bar means generating a locked snapshot (at the location the author specifies, by default `archives/`), recording the SHA256 in the battle record; once locked, do not change it further unless the author explicitly unlocks it.
- **Banking experience**: the battle record banks the patterns from this round (which structures run hot, which repairs work); a failed original sentence is added to `sandbox/prose-regressions.txt` only after **the author confirms it** (no entry without the author's nod).
- **Re-run**: before banking, re-run `check-chapter.py` to confirm the hard defects are zero.

## Report (for the author, in everyday language)

- This round's detection: split into X segments; the segment that reads most machine-written is at the beginning / middle / end
- What changed: a one-sentence plain-language description ("this Q&A ran too smoothly, so two beats were cut"), with no internal terms such as segment or threshold
- Result: the score before and after the change, pass or fail; once it passes, it is locked and backed up
