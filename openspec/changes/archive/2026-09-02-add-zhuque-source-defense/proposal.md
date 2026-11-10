## Why

This project's anti-ai pipeline is open-loop: after the rules remove the AI flavor, the text is delivered directly, missing two capabilities: (1) structure-level heat-source knowledge (text with clean wording is still judged AI by external detectors, because the heat source is in the structure: question-answer chain density, positional heat value, micro closed loops, and more); (2) chapter-delivery-level deterministic checks (hard defects the model eye misses, such as sandwich quotes, nested quotes, and word-count expression mismatches). A live-tested external project (attack-and-defense lessons from 6 chapters in a row at 100% human characteristics) has verified both layers work, and they can be generalized to lower AI detection rates from the source.

## What Changes

- Add `knowledge/anti-ai/structural-heat.md`: seven measured laws (question-answer chain density, positional heat value, slice-boundary stability, the character-padding iron rule, content-type switching, the particle-stretching method, whole-chapter rewrite boundaries) + 13 high-risk structures, all rewritten in generic terms with book names removed, keeping measured scores as evidence.
- Incrementally merge missing entries from the human-writing rule pack (MIT) into `knowledge/anti-ai/common-rules.md` / `anti-ai-writing.md`, without file-level overwrites.
- Add `tools/check-chapter.py`: chapter-delivery defect checks (general regex items + platform-convention word counting), with the book-specific regression pattern library and whitelist kept outside in project files.
- Add the `tools/test_check_chapter.py` tests.
- init/sync deploy the new tool to `<platform root>/tools/` (same mechanism as check-prose.py).

## Capabilities

### New Capabilities

- `structural-heat`: structural-heat-source knowledge, structure-level AI heat-source laws and a high-risk structure list that anti-ai and the writer can recall before writing.
- `chapter-check`: a chapter-delivery deterministic check tool, regex defect scanning, word-for-word reconciliation, a project-level regression library and whitelist kept outside, plus deployment and exit-code contracts.

### Modified Capabilities

(None. This change does not alter existing spec-level behavior; the common-rules.md merge is an incremental knowledge-content addition, not a behavior-contract change.)

## Impact

- Added: `knowledge/anti-ai/structural-heat.md`, `tools/check-chapter.py`, `tools/test_check_chapter.py`.
- Changed: `knowledge/anti-ai/common-rules.md`, `knowledge/anti-ai/anti-ai-writing.md` (incremental entries), `tools/init.py`, `tools/sync-project.py` (deployment manifest), `tools/test_platforms.py` (E2E assertions).
- Dependencies: none new (Python standard library only); no CI changes needed (the existing static.yml automatically covers the new tests).
- Unchanged: `tools/check-prose.py` existing thresholds and behavior; `skills/` (pipeline wiring belongs to a later change).
