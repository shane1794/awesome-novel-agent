# structural-heat Specification

## Purpose
Provide structure-level AI heat-source knowledge for the writer and anti-ai: external AI detectors' heat sources often sit in paragraph structure rather than word choice, and this capability lets agents avoid or identify high-risk structures using verifiable laws before writing and before editing, lowering detection rates from the source.

## Requirements

### Requirement: The structural-heat knowledge file must exist and be reachable at its deployment path

The knowledge file `knowledge/anti-ai/structural-heat.md` MUST exist in the repo; init MUST merge it into the anti-ai knowledge merge list and ship it with the deployed product `.claude/knowledge/anti-ai.md` (each platform's matching knowledge directory); references to it MUST point at that merged-product path, verified by `tools/check-agents.py`.

#### Scenario: Agent recall before writing
- **WHEN** the writer or anti-ai agent reads the deployed anti-ai knowledge
- **THEN** the merged product contains the structural-heat law content, and `check-agents.py` passes its reference-path check (exit 0)

#### Scenario: Repo static checks
- **WHEN** CI runs `check-agents.py` and `check-conflicts.py`
- **THEN** both exit 0, with no broken reference paths and no threshold conflicts

### Requirement: Knowledge content must be generalized and traceable

The file content MUST satisfy: (1) cover seven laws, question-answer chain density, positional heat value, slice-boundary stability, the character-padding iron rule, content-type switching, the particle-stretching method, and whole-chapter rewrite boundaries; (2) cover a high-risk structure list of at least 13 kinds: work-report style, evidence-closing style, operations-acceptance style, collaboration-demonstration style, advance-preparation style, numbers-explanation style, micro-closed-loop recursion, consecutive acceptance stacking, fixed-position reskinning, standard suspense staging, bridge-chain prefix style, private-memory proof chains, and fixed chapter-opening mini-plays; (3) contain no specific book titles, character names, or chapter numbers; (4) attach measured data as evidence to each law.

#### Scenario: Content completeness acceptance
- **WHEN** a human or script checks the file content
- **THEN** the seven laws and at least 13 high-risk structures are all present, the text has no proper nouns specific to a particular book, and law entries carry measured scores

#### Scenario: Threshold system does not conflict
- **WHEN** running `check-conflicts.py`
- **THEN** the numeric statements in the new laws do not conflict with existing anti-ai rule thresholds

### Requirement: Incremental merges from the human-writing rule pack must not overwrite the existing system

When merging entries from the human-writing rule pack, the merge MUST be additions only: do not change the existing thresholds or methodology framework of `common-rules.md` / `anti-ai-writing.md`, new entries MUST be traceable back to their source files one by one, and do not replace the repo's refactored versions wholesale with old fork files from the pack.

#### Scenario: Regression after merging
- **WHEN** the merge is done and anti-ai checks and tests run
- **THEN** existing rule entries and thresholds are unchanged (git diff shows only added lines), with no conflicting entries that redefine the same term

### Requirement: Scope and conflict-adjudication order must be stated

The knowledge file MUST state: (1) the measured source and scope (the experience comes from live tests on a single realistic-genre book; numeric thresholds are defaults, calibrated by style and genre); (2) the conflict-adjudication order: author settings and chapter outline > genre knowledge > structural defaults > detection optimization. Numeric statements MUST be labeled as defaults; when covering the same phenomenon as an existing rule, the file MUST state the relationship (a new scale running in parallel, or a reference to the existing rule) and MUST NOT redefine the same numeric wording (such as dialogue density or punctuation usage).

#### Scenario: Same topic as an existing rule
- **WHEN** a structural default and an existing rule (such as Gate E5 dialogue sentence counts or the common-rules dash ruling) cover a similar phenomenon
- **THEN** the file states clearly that they are different scales or directly references the existing wording, with no instructions pointing in opposite directions

#### Scenario: Priority written down
- **WHEN** the writer or anti-ai cites the file for a decision that conflicts with author settings or the chapter outline
- **THEN** it follows the stated adjudication order, and author settings and the chapter outline always win over detection optimization
