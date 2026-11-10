# v4.22.0 Release Notes

> **Keywords:** The structural-heat-source law + deterministic chapter checks: knowledge and tools for avoiding AI detection from the source (generalizing lessons from Zhuque live tests)

---

## In One Sentence

A set of structure-level writing laws verified by live tests on an external AI detector (multiple chapters in a row judged "human characteristics" on every segment) is generalized into the knowledge base: new structural-heat-source knowledge (merged into the deployed anti-ai.md) and a deterministic chapter-delivery check tool (check-chapter.py, deployed to each platform by the same mechanism as check-prose.py), so AI heat sources are avoided before writing and caught by machine before delivery.

## What Changed in This Release

| Change | Description |
|------|------|
| **Structural-heat-source knowledge** | `knowledge/anti-ai/structural-heat.md`: seven measured laws (question-answer chain density, dialogue density as a positive signal, positional heat value, slice-boundary stability, the character-padding iron rule, content-type switching, whole-chapter rewrite boundaries) + 13 high-risk structures (work-report style, micro-closed-loop recursion, bridge-chain prefix style, private-memory proof chains, and others) + a pre-writing self-check card and fix discipline. Fully rewritten in generic terms with book names removed, values marked as defaults, with an adjudication order: author settings and chapter outline > genre knowledge > structural defaults > detection optimization |
| **Knowledge merge deployment** | `init.py` merges structural-heat.md into the anti-ai knowledge merge list, deploying it with `.claude/knowledge/anti-ai.md` (and each platform's matching knowledge directory) |
| **Deterministic chapter checks** | Added `tools/check-chapter.py`: hard items (quote-sandwich with label style, nested double quotes, half-width quotes, "X words" verbatim word-count mismatch, regression-string hits) + warning items (dense dashes/ellipses within a paragraph, broad quote sandwiches, multi-round question-answer in one paragraph, weak-adverb density, narrow trailing-label sets, and others, for human adjudication) + platform-convention word counting (reports only, sets no threshold). Punctuation conventions align with common-rules.md and add no book-level hard bans |
| **Project-level evolution assets moved out** | The regression pattern library (`sandbox/prose-regressions.txt`) and the locked-lines whitelist (`sandbox/locked-lines.txt`) are read from project files and skipped when missing, so each book accumulates its own library of failure strings and exemption list |
| **Deployment and sync** | init deployment, sync fingerprinting, and recovery all cover check-chapter.py (same mechanism as check-prose.py); E2E adds seven-platform assertions |
| **Incremental knowledge merge** | Incrementally merged rules from the human-writing rule pack into anti-ai-writing.md (synonym cycling, uniform subject completion, written filler, copula avoidance, over-qualification stacking, scene-tiered rewrite-strength table) and common-rules.md (adding "perhaps" to judgment-type lines), additions only, no deletions |

## Compatibility

- Purely incremental: the existing tool (check-prose.py) keeps its thresholds and behavior; the anti-ai Phase flows are unchanged (wiring structural scanning and the dual-script pre-screen into the pipeline comes in a later release).
- Existing projects get the new check script and updated merged knowledge after running `sync-project`, with no manual action needed.
- `check-chapter.py` is deployed in this release but the pipeline does not call it yet (it is wired into the writing/anti-ai flow in the next release). It can be used directly by hand: `python3 tools/check-chapter.py <chapter file>`.

## Tests

- `tools/test_check_chapter.py` adds 19 assertions (positive and negative cases per check, exit-code contract, regression library/whitelist, CRLF, directory input).
- `tools/test_platforms.py` 272 assertions all green (including new tool deployment and knowledge-merge assertions).
- check-agents / check-conflicts / py_compile all green.
