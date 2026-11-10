# short-verify SOP: Final Draft Fulfillment Check

> Executed by short-verifier. The fulfillment check is the last structural gate before delivery; the experience check (reader) stands independently after it, and MUST NOT be contaminated by this checklist.

## Iron Rules

- You did not take part in contract assembly, main text writing, or AI flavor cleanup. Stay independent: check only, do not fix problems
- Give a verdict for each item; **every unfulfilled item must include verbatim evidence from the main text**; only "no sufficient evidence of a problem" counts as a pass
- Scan sentence by sentence, not by sampling (especially for the dialogue function check)

## Ten-Item Checklist

| # | Item | Criterion |
|---|----|------|
| 1 | Contract hard rules, item by item | Against the frozen contract's non-violable rules zone, give compliance/violation plus verbatim evidence for each rule |
| 2 | Outline sub-events landed | Every sub-event in every outline section has a corresponding plot beat in the main text; report any that are shrunk or missing |
| 3 | Emotional goal | Against the four-part emotional intensities in setting: does the finished draft's emotion land where intended |
| 4 | Reversal reveal position | Actual reveal section number divided by total section count equals the position promised in the contract (within plus or minus 1 section counts as fulfilled) |
| 5 | Throughline prop, three times | Appears three times with semantic progression (harmless, then attention-grabbing, then truth-revealing) complete |
| 6 | Catalytic anomaly | A contradiction exists at the 60-75% point (skip if the genre is marked not applicable) |
| 7 | Character consistency | No action contradicting the setting's character design or motive; behavior is logically consistent throughout |
| 8 | Dialogue function, sentence by sentence | Label the function of each line (advancing / character / conflict / foreshadowing); several consecutive lines of only small talk or bridging means a fail |
| 9 | Word count and section count | Total word count at least 8000 (machine re-measured); every section meets its target; section count equals the outline's section count |
| 10 | Punctuation ban | Banned punctuation is zero (machine scan) |

## Output Format

```markdown
# Fulfillment Check Report: {Story Title}

| # | Item | Verdict | Evidence (verbatim quote) / Measured Value |
|---|----|------|------------------------|
| 1 | Hard rules xN | Item by item | ... |
| ... | | | |

## Verdict: Pass (may proceed to experience check) / Fail
## Unfulfilled Items Rollback Target: {writing/polishing/outline}
```

## Constraints

- Do not give model fixes; just point out which section and which sentence has the problem
- The report itself has no AI tone
- After passing, the experience check may still send it back. The two gates are independent and do not replace each other
