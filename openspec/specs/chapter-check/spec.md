# chapter-check Specification

## Purpose
Chapter-delivery-level deterministic checks: beyond the anti-ai statistical detection (check-prose.py), catch delivery defects the model eye misses (quote sandwiches, nested quotes, half-width quotes, word-count expression mismatches, and more), and provide a regression pattern library and locked-lines whitelist mechanism that grows with the project.

## Requirements

### Requirement: Check tool command contract

The tool MUST be invoked as `python3 check-chapter.py <manuscript path...>` and accept one or more file paths or directories; exit codes MUST satisfy: 0 means all passed (warnings needing human adjudication may exist), 1 means a hard hit exists, 2 means file reading failed. Output MUST give each item as `[check name] line number: context excerpt`.

#### Scenario: Hard hit
- **WHEN** the manuscript contains a hard hit (label-style quote sandwich, nested double quotes, half-width quotes, dashes/ellipses, word-count expression mismatch)
- **THEN** the exit code is 1, and the output lists each check name, line number, and context excerpt

#### Scenario: All pass
- **WHEN** the manuscript has no hard hits
- **THEN** the exit code is 0, and it still outputs the platform-convention word count (Chinese characters, full-width punctuation, quotes, and digits as separate items) and warning items

#### Scenario: File unreadable
- **WHEN** any input path does not exist or cannot be decoded
- **THEN** the exit code is 2, and it is not misreported as a check failure

### Requirement: Check coverage and grading

The tool MUST cover the following general checks, split into two grades: hard (a hit means exit 1) and warning (reported only, for human adjudication).
Hard: label-style quote sandwich, nested double quotes, half-width quotes, word-count expressions that do not match the quoted content word for word, exact-string hits in the regression library.
Warning: dashes/ellipses (when 3 or more appear in a paragraph, prompt judging each one against the `common-rules.md` usage, with no hard ban), broad quote sandwiches, multi-round question-answer in one paragraph, weak-adverb density over the limit, "X words" awaiting manual word-for-word verification, trailing labels (a narrow set of pronoun plus say/ask).
The tool MUST output the platform-convention word count but MUST NOT set a hard threshold on word count (word-count requirements are book-level settings); punctuation conventions MUST match `common-rules.md`, and book-level hard bans (such as "zero dashes") MUST NOT be default behavior.

#### Scenario: Grading behavior
- **WHEN** the manuscript only hits warning-level checks
- **THEN** the exit code is 0, and warning items are listed one by one and marked "needs adjudication"

### Requirement: Project-level regression library and whitelist kept outside the tool

The regression pattern library (exact strings that failed before) and the locked-lines whitelist MUST be read from project files (agreed paths `sandbox/prose-regressions.txt` and `sandbox/locked-lines.txt`, one entry per line, UTF-8); when a file is missing, the corresponding check MUST be skipped without affecting the exit code; a whitelist-hit line MUST skip family-type checks and be marked with its reason in the output.

#### Scenario: New project has no regression library
- **WHEN** the project has no `sandbox/prose-regressions.txt`
- **THEN** the regression-library check is skipped, and the tool exits normally on the remaining checks

#### Scenario: Regression string recurs
- **WHEN** the manuscript hits any exact string in the regression library
- **THEN** the hit is hard, exit code 1

#### Scenario: Whitelist exemption
- **WHEN** a line in the manuscript fully matches an entry in the whitelist
- **THEN** the line skips sentence-pattern family checks, and the output marks the whitelist skip

### Requirement: Deployment and testing

init MUST deploy the tool to each platform root `tools/` (same mechanism as check-prose.py), and sync's update detection MUST cover the tool; tests MUST cover positive and negative cases for each check, the exit-code contract, and missing/hit scenarios for the external files.

#### Scenario: Platform deployment
- **WHEN** running `python tools/init.py <project path> --platform claude`
- **THEN** the deployed project contains `.claude/tools/check-chapter.py`, and the seven-platform E2E tests (`test_platforms.py`) pass

#### Scenario: Check regression
- **WHEN** running `python tools/test_check_chapter.py`
- **THEN** all assertions pass (stdout prints ok, exit code 0)
