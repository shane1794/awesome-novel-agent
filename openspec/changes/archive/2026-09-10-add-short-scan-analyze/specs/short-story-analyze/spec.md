# short-story-analyze Delta

## Purpose

The benchmarking teardown pipeline for short stories: break a hit story into reusable structural assets (story core, structural segments, plot nodes, emotional curve, reversal mechanism, writing techniques, structure counts) and save them as reference material the writing stage can recall directly.

## ADDED Requirements

### Requirement: A1 Input confirmation and word-count routing

Teardown MUST first obtain the original text (a file path or text pasted by the author); without the original, it MUST guide the author to provide it and MUST NOT tear down from nothing. After obtaining it, it MUST count the words: within the short-story range, enter the pipeline directly; in the gray zone, ask the author; over the limit, note that it does not apply and continue only when the author explicitly asks.

#### Scenario: A1.1 No original text is blocked
- **WHEN** the author has not provided the original text
- **THEN** guide them to provide it; MUST NOT tear down from nothing

#### Scenario: A1.2 Word-count routing
- **WHEN** counting the words
- **THEN** within range, enter the pipeline; in the gray zone, ask; over the limit, note it does not apply and continue only if the author insists

### Requirement: A2 Genre yardstick and resume checks

The genre MUST be identified and the matching short-story genre style pack loaded as the teardown yardstick; if no genre is identified, mark it as general. When teardown output already exists, the agent MUST ask whether to overwrite, resume, or cancel, and MUST NOT silently overwrite; resuming continues from the breakpoint using the output metadata's stage markers.

#### Scenario: A2.1 Existing output must prompt a question
- **WHEN** teardown output already exists for this story
- **THEN** ask the three-way choice; before a choice is made, MUST NOT write any output files

### Requirement: A3 Original-text backup comes before analysis

Before entering the pipeline, the original text MUST be backed up into the output directory (copy the source file or save the conversation text), and the backup must be verified non-empty afterward.

#### Scenario: A3.1 Backup first
- **WHEN** teardown starts
- **THEN** the original-text backup exists and is non-empty, before any analysis is written to disk

### Requirement: A4 Five-stage serial pipeline, each stage with a completion marker

Teardown MUST run in five serial stages and MUST NOT skip stages: (1) structure + plot nodes (at least 4 structural segments including beginning, development, climax, and ending; node density tiered by word count, with non-standard texts reordered first by time, speaker, or information-reveal points); (2) emotional curve (at least 5 nodes) + the six dimensions of the high point; (3) reversal mechanism (at least 2 setups) + writing techniques (at least 5 items); (4) character functions + opening and ending; (5) overall assessment + structure counts written into metadata.

#### Scenario: A4.1 Per-stage completion markers
- **WHEN** a stage ends
- **THEN** it advances to the next stage only when all completion markers are met

### Requirement: A5 Writes must be crash-safe

Before each stage starts, its in-progress state MUST be marked in the metadata; the marker is cleared and the stage recorded as complete only after all target files are written and pass non-empty plus minimum-length checks; on resume, an incomplete stage is re-run in full, and half-finished work is not trusted.

#### Scenario: A5.1 Half-finished work is not trusted
- **WHEN** resuming after an interruption
- **THEN** the stage marked in-progress is re-run in full

### Requirement: A6 Fixed output file tree, consumable by writing

The output directory MUST contain: the original-text backup, the teardown report, plot nodes, writing techniques, and `_meta.json` (genre identification + structure counts). Each file must be independently readable; the metadata lets the writing stage automatically load the matching genre style pack.

#### Scenario: A6.1 File tree complete
- **WHEN** teardown finishes
- **THEN** all five outputs are present and independently readable

### Requirement: A7 Three acceptance gates before counting as complete

After the last stage is written, three checks MUST pass: (1) the report's own AI-tone self-check (per the short-story de-AI criteria, scanning only the analyst's wording and skipping quoted source text; hits block and list line numbers); (2) structure counts verified item by item against thresholds (a miss names the stage to roll back to); (3) a strong-blocking item scan of the template (missing items block; missing non-strong-blocking items go on a to-add list). Only when all pass are the markers cleared, completion recorded, and the author told they can move on to writing.

#### Scenario: A7.1 The report itself has no AI tone
- **WHEN** scanning the teardown report
- **THEN** only the analyst's wording is scanned; a hit blocks and lists line numbers

#### Scenario: A7.2 Count checks name the rollback
- **WHEN** a count is below its threshold
- **THEN** it blocks and names which stage to roll back to
