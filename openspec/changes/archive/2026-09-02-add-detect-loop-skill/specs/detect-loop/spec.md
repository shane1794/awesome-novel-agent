## Purpose

Provide an optional external-detection calibration loop: when the author voluntarily sends their own manuscript to an external AI detector for verification, the agent fixes with minimal intervention (only the highest-scoring segment moves; everything else stays character-for-character untouched), locks the version once it passes, and distills the lessons into project assets.

## ADDED Requirements

### Requirement: Author-triggered only, offline by default

detect-loop MUST be an optional phase: it starts only when the author explicitly asks for submission or verification; the default pipeline (draft→anti-ai→review→archive) MUST NOT enter this stage automatically; when no local submission tool exists or the author has not provided a detection route, it MUST end gracefully with an explanation and not block the main flow.

#### Scenario: Not triggered, does not start
- **WHEN** the anti-ai phase finishes normally
- **THEN** dispatch produces no detect-loop order and goes directly to review

#### Scenario: Author triggers it
- **WHEN** the author says "submit it / run it through an external detector"
- **THEN** dispatch produces a detect-loop order and the flow runs per the SOP

#### Scenario: No tool, degrade
- **WHEN** no usable submission tool exists locally
- **THEN** the stage ends and tells the author they need to prepare a detection route themselves; the main flow can continue

### Requirement: Minimal-intervention fix contract

Fixes MUST follow: each round fixes only one highest-scoring segment; all other segments stay character-for-character untouched (verified by content-substring hashing); the first and last sentences of a segment stay word-for-word; equal-length edits are preferred; when improvement over two consecutive rounds is under 0.05 or the score rises instead, the agent MUST stop using the same kind of edit (switch content type or roll back to the previous version); segment decision thresholds (such as 0.5) are parameters, not hard-coded values. Detection-feedback-driven edits MUST follow the same adjudication order as the writing side (author settings and chapter outline > genre knowledge > structural defaults > detection optimization): they MUST NOT rewrite locked lines, chapter-outline landing points, or other author-side core expressions to lower a score, and when they conflict with style, style wins.

#### Scenario: Targeted fix
- **WHEN** detection returns multi-segment results with only one segment over the threshold
- **THEN** only that segment is changed, and the other segments' hashes are identical before and after

#### Scenario: Detection optimization does not overreach
- **WHEN** a score-lowering edit conflicts with author settings or a chapter-outline landing point
- **THEN** the author-side expression is kept, and the report marks that segment as "settings take priority, residual score accepted" or submits it to the author for adjudication

#### Scenario: Stop-loss
- **WHEN** the same segment improves by under 0.05 for two consecutive rounds or its score rises
- **THEN** stop using the same kind of edit and offer two options in the report: switch content type or roll back

### Requirement: Pass-and-lock plus lessons learned

Once all segments are below the threshold, the draft MUST be locked: generate a snapshot and record the content hash, and make no further changes after locking; the rounds, edits, and per-segment results of this round MUST be appended to the project `sandbox/detect-battles.md`; failure sentences MUST be added to `sandbox/prose-regressions.txt` only after author confirmation; before distilling lessons, `check-chapter.py` MUST be re-run to confirm hard defects are at zero.

#### Scenario: Locking
- **WHEN** all detection segments are below the threshold
- **THEN** generate a locked snapshot with a hash record, and reject later changes until the author explicitly unlocks it

#### Scenario: Lessons enter the library
- **WHEN** a battle round ends
- **THEN** the battle log gains the complete round table, newly added regression strings have an author-confirmation record, and the `check-chapter.py` re-run exits 0

### Requirement: Compliance boundary and asset isolation

The skill text MUST state: this stage serves the author's voluntary quality calibration of their own manuscript; the repo MUST NOT contain any automation scripts, interface-reversing docs, keys, or browser-fingerprint schemes for any detection platform; the connection to a local tool is described only as an adapter interface of "input manuscript path / output per-segment result file".

#### Scenario: Repo content review
- **WHEN** checking this change's output and the repo contents
- **THEN** there are no detection-platform automation scripts, no reverse-engineered protocol docs, and no key files; the adapter interface only describes the input/output file conventions
