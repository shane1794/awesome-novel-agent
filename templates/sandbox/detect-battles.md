# Detection Battle Log

> Purpose: when the author voluntarily sends a manuscript to an external AI detector (such as Zhuque) for verification, record each round of "what changed and how the scores moved", and once the target is met, distill the patterns. This log itself is a source of writing rules: re-read it before starting the next chapter.
> How to use: the agent appends one row per round when submitting for detection; when the author submits manually, the agent can record it on their behalf. When showing it to the author, only say "which round, what changed, and how the scores moved from X to Y".

## Detection Criteria for This Book

- Detection tool: <!-- e.g. Zhuque web version (per-segment AIGC values, pass line = all segments below 0.5) -->
- Submission method: <!-- e.g. local tool auto-submission / author manually pastes on the website -->
- Pass line: <!-- e.g. all segments < 0.5 -->

## Battle Log

<!-- One section per chapter; append round by round, only edit the highest-scoring segment, leave everything else character-for-character unchanged -->

### Chapter X (date)

| Round | What Changed | Per-Segment Results | Conclusion |
|----|---------|---------|------|
| 1 | (first draft submitted) | Segment 1 0.xx / Segment 2 0.xx / ... | Highest-scoring window: segment N |
| 2 | (only fix segment N: specific change) | ... | ... |

**Locked version**: after passing, record the date and the manuscript hash (SHA256); after that, do not polish a single word; store the snapshot in `archives/`.

## Distilled Patterns

<!-- After each battle ends, write new patterns here: which structures run hot, which fixes work, which changes backfire.
     Verified failure lines confirmed by the author are also added to sandbox/prose-regressions.txt to block recurrence. -->

- (Example format) Measured in one chapter: a window with more than 8 straight beats of question-and-answer always runs hot; cutting beats and inserting action between questions passed within two rounds.
