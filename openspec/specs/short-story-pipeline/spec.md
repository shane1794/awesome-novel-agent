# short-story-pipeline Specification

## Purpose
Give short stories a complete writing pipeline from "what feeling do I want to write" to "a submittable finished draft": seven stages, two author confirmation gates, two structural hard validations, one verifiable writing contract, hard floors for word count and section count, a revision path after delivery, and independent breakpoint resume. Authors who know short stories can go straight through in one sentence; authors who do not are guided item by item, and both paths produce the same finished structure.

## Requirements

### Requirement: D0 The dispatch contract must be independent and the single authoritative source

Short stories MUST have an independent dispatch contract file as the single authoritative source for the short-story order type list, author confirmation gates, and breakpoint resume semantics; the short-story commander agent's flow tree MUST state that it follows that file. Short stories MUST follow the order-file protocol (to-do files carry a status field, and the executor overwrites the status when done without deleting the file), and only the commander writes orders, dispatching one sub-agent at a time.

#### Scenario: D0.1 The contract is the single authority
- **WHEN** reading through the short-story commander agent definition and the short-story dispatch contract
- **THEN** the two agree on order types and breakpoint semantics, and the agent definition explicitly states it follows the contract

#### Scenario: D0.2 Order protocol matches
- **WHEN** checking a short-story project's to-do file directory
- **THEN** order files contain only input paths, output paths, and a status field, with no execution steps or methodology

#### Scenario: D0.3 The commander does not overreach
- **WHEN** the short-story commander completes one dispatch
- **THEN** it only wrote order files and status files, and did not directly write `setting.md`, `outline.md`, `prompt.md`, or `manuscript.md`

### Requirement: D1 Set the emotion and direction

The pipeline MUST start by **setting the emotion first, then the story**: before writing, the target emotion MUST be fixed, and all content serves that emotion. The commander MUST support two entry paths: straight through when the author already has a clear idea, guided selection when the idea is only vague. This stage MUST produce `setting.md` in the story directory and stop after producing it to wait for author confirmation.

`setting.md` MUST contain: basic info (working title / target word count / target platform), a one-sentence premise, the core reversal (type / content / at least 3 setup clues), a four-part emotion design (opening / middle / reversal / ending, each with a 1-10 intensity value), and quick character sketches. The emotion design MUST note the requirement that the reversal climax does not drop sharply.

#### Scenario: D1.1 Pick one of six emotion goals
- **WHEN** the author has only a vague idea
- **THEN** the commander offers emotion options (lingering regret / shocking reversal / payoff release / healing warmth / chilling realization / resonant emotion), each with fitting scenarios, difficulty, and commonly paired genres, and recommends a genre direction once the author picks one

#### Scenario: D1.2 Submission platform tone
- **WHEN** the genre direction is fixed
- **THEN** the commander confirms the submission platform (Zhihu Yanxuan / mini-programs / Tomato Short Stories) and continues with that platform's tone for point of view, conflict intensity, chapter-end hooks, and ending texture

#### Scenario: D1.3 A clear request goes straight through
- **WHEN** the author gives all elements in one sentence (such as "wife-chasing crematorium, lingering regret, submit to Yanxuan, eight thousand words")
- **THEN** the commander skips item-by-item guidance and goes directly to framework output, asking follow-up questions only for missing items

#### Scenario: D1.4 The framework is structurally complete
- **WHEN** this stage produces `setting.md`
- **THEN** the file contains basic info, a one-sentence premise, the core reversal (with reversal type and at least 3 setup clues), four emotion intensity values, and character sketches, and the selected genre techniques for this story are written in from the genre style pack

#### Scenario: D1.5 Author confirmation gate one
- **WHEN** the concept sub-agent's order is marked complete
- **THEN** the commander shows the framework summary in everyday language (what feeling the reader is left with / what happened / where the reversal is / who is who) and stops to wait for author confirmation; a vague author reply counts as unconfirmed and prompts a follow-up question; before confirmation, it MUST NOT lay out the outline

### Requirement: D2 Concept and outline

This stage MUST complete the design work in a fixed order, produce `outline.md` in the story directory, then pass two hard validations, and finally stop to wait for author confirmation. If any validation fails, it MUST return to the outline stage to fix it and MUST NOT enter contract assembly with defects.

This stage MUST first pick one **emotion chain** as the emotional skeleton of the whole story and then build the outline from it. An emotion chain is a numbered, named sequence of emotional progression (4-6 stages, each with a name, such as "Prey Enters the Cage, Lured Into the Trap, Logic Closes In, Public Execution, Treated as Nothing"). Once picked, its stages MUST cover every section of the whole story; no section MUST fall outside the chain.

The emotion chain's stages and the five parts (opening / setup / escalation / reversal / ending) are two independent descriptions and MUST NOT be forced into a one-to-one match: a four-stage chain may have two stages carried by the same one of the five parts.

`outline.md` MUST give one line per section, containing: structure part and function, main event, sub-events (3-5, joined with connectors and each carrying a function tag), emotion, character-relationship change, **causal chain**, new information the reader learns, the ending handoff or hook, foreshadowing objects, motion/stillness markers, dialogue density, and target word count.

**The causal-chain field MUST be written in a fixed shape** and MUST NOT be written as a generic causal description:

```
[Handoff Point]→[Motivation and Action]→[Core Event]→[Direct Consequence]→[Ending Hook]
```

Here "handoff point" states what this section inherits from the previous section, and "direct consequence" states what this section's events cause. These two connection points are the key to preventing the plot from drifting section by section, and MUST NOT be omitted.

`outline.md` MUST also contain an **emotion-chain landing** and a **technique landing table**: the emotion-chain landing marks the chain name and which section numbers each stage covers; the technique landing table marks, for each core technique selected for this story, its **carrying section** and its **payoff section**. Carrying and payoff sections MUST leave setup distance between them; a technique MUST NOT be carried and paid off in the same breath.

Every section MUST take on at least one of the following functions: advancing a core technique, adding pressure (humiliation / misunderstanding / escalating cost), planting or paying off foreshadowing, changing a character relationship, delivering emotion, or **developing a supporting-character subplot**. There MUST NOT be a section with no function at all: isolated sections of pure transition, pure emotion, or pure everyday routine MUST be merged with neighboring sections or given a function.

The relationship between the number of selected core techniques and the section count MUST be visible in the landing table: when the sections covered by technique carrying and payoff fall short of the total section count, the remaining sections MUST be carried by the five other function types (adding pressure, foreshadowing, relationship change, emotion delivery, supporting-character subplot) and MUST NOT be left empty. A supporting character who drives a subplot MUST have a memorable hook, and the subplot MUST affect the main plot (creating conflict or providing key help); it MUST NOT be a decorative character who appears without effect.

Every wrongdoing by the villain (or harming party) MUST have prior setup; it MUST NOT happen suddenly with no warning. The setup MUST let readers already sense danger or malice accumulating before the wrongdoing happens: the payoff comes from "retaliation after enough setup", and MUST NOT rely on evil arriving suddenly.

**The three appearances of a throughline prop MUST each carry a different semantic state** and MUST NOT repeat the same meaning three times:

| Order | Semantic state | Requirement |
|---|---|---|
| First | **Harmless** | Presented as an everyday detail the reader does not find important, carrying no emphasis |
| Second | **Draws attention** | Appears again, and the reader starts to notice, but its meaning is still unrevealed |
| Third | **Reveals the truth** | Its meaning is overturned, recovering the setup of the first two appearances |

A prop MUST NOT be limited to a physical keepsake: a habit, a sentence, or a number can carry the function. Its test is "ordinary on the surface, fatal underneath": on first read it looks like idle writing, and only on third read does it turn out to be the fuse.

**Before the reversal, there MUST be one "catalytic breakdown"**: at the 60-75% point of the full text, introduce a contradictory element the current explanatory framework cannot explain (such as a message from someone already dead, or physical evidence contradicting known facts). Its role is not to reveal the truth but to **force readers to abandon their old assumptions and upgrade their guesses**. It MUST NOT be replaced with "more information of the same kind": same-kind information only strengthens old assumptions and never pushes readers to rejudge. Genres where the reversal type does not apply (such as pure sweet pampering or pure healing) may mark it not applicable with a stated reason.

#### Scenario: D2.1 Design work runs in order
- **WHEN** the concept sub-agent runs this stage
- **THEN** it completes in order: fix the submission-platform tone and load the genre style pack, **pick one emotion chain as the whole story's skeleton**, pick 2-3 core techniques from the technique library, design the villain, fix the reveal method, write the section outline, and run the two validations; items that do not apply may be skipped after marking the reason

#### Scenario: D2.2 Each outline section is one line with complete fields
- **WHEN** reading any section line in `outline.md`
- **THEN** the line contains structure part and function, main event, 3-5 sub-events (each a concrete plot description plus a function tag, not a bare tag), emotion, relationship change, causal chain, new information learned, hook, foreshadowing, motion/stillness, dialogue density, and target word count

#### Scenario: D2.8 The causal chain follows the fixed shape
- **WHEN** checking any section's causal-chain field
- **THEN** the field contains five parts (handoff point, motivation and action, core event, direct consequence, ending hook), with the handoff point and direct consequence both written out, not written as a generic causal description and with no connection point omitted

#### Scenario: D2.9 The emotion chain covers the whole story
- **WHEN** checking the emotion-chain landing in `outline.md`
- **THEN** the chain name and the section numbers each stage covers are marked; every section of the whole story is covered by some stage, with no section outside the chain; the chain's stages and the five parts are not forced into a one-to-one match

#### Scenario: D2.3 Reversal reveal position validation
- **WHEN** computing the reveal section number against the total section count after the outline is done
- **THEN** a ratio below 50% is invalid and returns to outline adjustment; 50-60% is a gray zone that re-checks whether the misleading clues are sufficient; only above 60% passes

#### Scenario: D2.4 Foreshadowing re-check
- **WHEN** running the foreshadowing re-check after the outline is done
- **THEN** every key element of the ending (object / information / character / relationship change) has at least 1 setup earlier in the text; the throughline prop's three appearances (setup section / reversal section / ending section) are all present; the gap between the setup section and the reveal section is at least 3 sections; missing items must be fixed by adding setup and re-verified

#### Scenario: D2.12 The throughline prop's three appearances progress semantically
- **WHEN** checking the throughline prop's three appearances
- **THEN** the three semantic states are harmless, draws attention, and reveals the truth, with no same-meaning repetition; the first carries no emphasis and reads like idle writing, and the third recovers the first two appearances' setup; the prop type is not limited to a physical keepsake (a habit, a sentence, or a number all work)

#### Scenario: D2.5 Author confirmation gate two
- **WHEN** the outline and both validations have passed
- **THEN** the commander shows the outline summary in everyday language (what each section is about / how the emotion moves / where the breakpoints fall) and stops to wait for author confirmation; before confirmation, it MUST NOT assemble the contract

#### Scenario: D2.6 The technique landing table is complete
- **WHEN** checking the technique landing table in `outline.md`
- **THEN** every core technique is marked with a carrying section and a payoff section, with setup distance between the two; no entry carries and pays off at once

#### Scenario: D2.7 No functionless sections
- **WHEN** checking the outline section by section
- **THEN** every section takes on at least one of advancing a technique / adding pressure / foreshadowing / relationship change / emotion delivery / developing a supporting-character subplot; there are no isolated pure-transition or pure-emotion sections; sections not covered by techniques are carried by the other five function types

#### Scenario: D2.10 Technique entries pair formula with example
- **WHEN** checking the technique entries picked from the genre style pack into this story
- **THEN** each entry contains an applicable formula and one concrete example, and MUST NOT list only the technique name; the formula and example both match this story's genre

#### Scenario: D2.11 Villain wrongdoing has prior setup
- **WHEN** reading through the outline and the finished draft to locate each wrongdoing by the villain (or harming party)
- **THEN** every wrongdoing has setup that accumulates danger beforehand, and readers can already sense malice accumulating before it happens; there is no node where wrongdoing happens with no warning; the retaliation payoff comes from enough setup, not from evil arriving suddenly

#### Scenario: D2.13 The catalytic breakdown is set
- **WHEN** checking the 60-75% point of the full text
- **THEN** there is a contradictory element the current explanatory framework cannot explain, whose role is to force readers to abandon old assumptions; it MUST NOT be replaced by adding same-kind information; genres where the reversal type does not apply are marked not applicable with a stated reason

### Requirement: D3 The writing contract must be assembled as an executable, checkable product

After the outline is confirmed and before writing starts, each story MUST have one **per-story writing contract** assembled and saved as a readable product. The contract MUST use a six-element structure: persona / task instructions / background / input / examples / output. The output section MUST use a flat structure: merge writing standards, narrative rules, and constraint red lines into a single "rules that must not be violated" list to reduce nesting and priority-judgment cost; suggestive techniques MUST NOT enter the hard-rules zone.

The contract MUST NOT be a stitching of reference files and the outline. Assembly MUST complete three things:

1. **Transform**: the genre pack's general techniques MUST be transformed into this story's writing: anchor them to this story's protagonist, anchor them to this story's information-gap relationships, and anchor them to the emotional rhythm of the passage, forming directly executable writing rather than copying the general methodology text
2. **Order**: hard rules MUST be sorted in descending priority (constraint red lines > word counts > banned items > narrative rules > other same-level writing-standards rules)
3. **Deduplicate**: after assembly, it MUST self-check that the same meaning appears only once, and that quantity lines or bans for the same object (section length / word count / punctuation / dialogue density, and so on) MUST be defined in only one place

Every rule written into the contract's hard-rules zone MUST be checkable against the text (mechanically decidable, or with a clear criterion); abstract wording that cannot be checked MUST NOT enter the hard-rules zone.

The contract MUST inline the short story's own **conflict adjudication table**, covering two kinds of conflict:

- **Numeric conflicts**: the per-section length floor, whole-story total word count, five-part word-count shares, reversal reveal position, and paragraph line-shape, with the concession order when the five conflict with each other
- **Qualitative conflicts**: **logical consistency takes priority over payoffs and gut-punches**. When a payoff or gut-punch needs a character to act against their motivation or contradict an established setting, logical consistency MUST win, and the payoff design is adjusted instead of letting character behavior lose its basis. Every key action by a character MUST have a motivation source and stay consistent throughout; it MUST NOT change character behavior logic on the spot to manufacture an effect

The adjudication table MUST state the basis for each trade-off, so the writing side only executes and makes no priority decisions.

#### Scenario: D3.1 The contract is structurally complete
- **WHEN** checking the assembled writing contract
- **THEN** all six elements exist with values and no placeholder residue; the output section is a flat structure, with suggestive techniques in a separate sub-section rather than in the hard-rules zone

#### Scenario: D3.2 General techniques are transformed into this story's writing
- **WHEN** spot-checking the technique entries in the contract that came from the genre pack
- **THEN** each entry contains a concrete character name and information-gap relationship, shows how the passage's emotional rhythm affects the writing, and forms one directly executable instruction, not three parallel general explanations or a copy of the genre-pack text

#### Scenario: D3.3 Hard rules are in descending priority
- **WHEN** reading through the contract's rules-that-must-not-be-violated list
- **THEN** the order is constraint red lines > word counts > banned items > narrative rules > other same-level writing-standards rules, with no priority inversions, and suggestive techniques are not mixed into the hard-rules zone

#### Scenario: D3.4 Deduplicated after assembly
- **WHEN** reading through the whole contract
- **THEN** the same object in the same format is defined only once (no exact duplicate of the same quantity line or ban); equivalently worded constraints with different emphases may be kept

#### Scenario: D3.5 Contract entries are checkable
- **WHEN** examining each constraint in the contract's hard-rules zone one by one
- **THEN** each one can be checked against the finalized main text (with a decidable standard or a clear criterion), with no wording that can only be judged by feel

#### Scenario: D3.6 The conflict adjudication table is inlined
- **WHEN** checking the conflict adjudication content in the contract
- **THEN** it contains the concession order and trade-off basis when the five items (section-length floor / total word count / five-part shares / reversal reveal position / paragraph line-shape) conflict with each other, and the adjudication table can be picked up directly by the writing side in the hard-rules zone

#### Scenario: D3.7 The logic-first clause is inlined
- **WHEN** checking the qualitative-conflict part of the contract's conflict adjudication table
- **THEN** it explicitly states that logical consistency takes priority over payoffs and gut-punches, with the requirement that "a character's key actions must have a motivation source and stay consistent throughout"; when the writing side meets a payoff-versus-logic conflict, it follows this and does not adjudicate on its own

### Requirement: D4 The contract must pass independent audit before writing

After the contract is assembled, it MUST pass an independent audit, and the auditor MUST NOT be the assembler. The audit MUST cover at least five items: whether general techniques are transformed into this story's writing, whether hard-rule priority is descending, whether rules repeat, whether emotion and structure constraints contradict each other, and whether entries are checkable. If the audit fails, it MUST return to assembly for fixes and re-audit, and MUST NOT enter writing with defects.

#### Scenario: D4.1 Audit independence
- **WHEN** tracing the contract's assembler and auditor
- **THEN** the two are not the same executor

#### Scenario: D4.2 All five audit items present
- **WHEN** reading the audit output
- **THEN** it covers transformation quality, priority order, rule deduplication, consistency between constraints, and entry checkability, five items, each with quoted source evidence

#### Scenario: D4.3 Failed audit rolls back
- **WHEN** the audit judges a failure
- **THEN** the contract returns to assembly for fixes and re-audit, and writing MUST NOT start

#### Scenario: D4.4 The contract is frozen
- **WHEN** the audit passes
- **THEN** the contract is frozen as the baseline for this writing, and the main-text writing and later acceptance both follow that version

### Requirement: D5 Main text must be written in batches under hard floors

The main text MUST be produced by the writing sub-agent in batches (2-3 sections per batch), and each batch MUST be verified by the commander before advancing. Each section MUST meet the section-length floor, the whole story MUST meet the total word-count floor, and both MUST be measured with an executable counting method.

Word counting MUST use a cross-platform reliable method and MUST NOT be model estimation and MUST NOT use byte counts. When word or section counts fall short, the text MUST be expanded further rather than wrapped up; the section count MUST equal the outline's planned section count.

**Paragraphs and sections are two orthogonal descriptions and MUST NOT be mapped one-to-one.** The five parts (opening / setup / escalation / reversal / ending) are **functional segments**, described by shares; sections are the **writing and acceptance unit**, described by word-count floors. One section can span two functional segments (such as the first section carrying both the opening part and the start of the setup part), and one functional segment can span multiple sections. A functional segment MUST NOT be cancelled, sections merged, or a section exempted from its floor just because the word count from its share conversion falls below the per-section floor.

**Before each batch of writing, the contract's hard-rules zone MUST be re-injected into the writing context**; the writing side MUST NOT be relied on to look the contract up itself. The reason is that the contract is the story's single copy while the main text is produced in batches, so the distance between the writing side and the rules grows with each batch: by the last batch, the full written text already sits between it and the contract. Re-injection MUST cover **all entries** of the contract's hard-rules zone (constraint red lines, word counts, banned items, narrative rules, and other same-level writing-standards rules); wording may be compressed for length, but no hard constraint MUST be dropped; it MUST NOT inject only the subset relevant to this batch's scenes.

**Scenes MUST enter mid-conflict and MUST NOT enter from the start of the process** (late in, early out): cut into a scene already in progress and put the reader directly into something happening; lead-in routines such as a character waking up, traveling, exchanging greetings, or setting up MUST NOT be expanded, and necessary information is carried in one sentence or brought out in later dialogue. The test: whether the scene's first sentence is already inside conflict or tension.

**A reversal reveal MUST complete the reader-side "instant threading"** and MUST NOT only state the truth: when revealing, use a look-back, a monologue, or physical evidence to bring all the clues planted earlier back before the reader's eyes at once, so readers immediately recall "so that's what those places meant". Stating only the truth without reconnecting the clues leaves the reversal's impact undelivered: readers say "I see" instead of "so that's how it is".

#### Scenario: D5.1 Two questions before writing
- **WHEN** the writing sub-agent starts any section
- **THEN** it first fixes the scene's target emotion, the matching technique entry in the contract, and which paragraph to use it in; if any cannot be answered, it re-reads the contract before writing

#### Scenario: D5.2 Three dimensions kneaded in, plus anti-patterns
- **WHEN** checking any section's scene writing
- **THEN** the happening, perceiving, and reacting dimensions are kneaded into the same stretch of continuous main text, not split into three paragraphs laid out in sequence; paragraphs break on a new action / new object / new information / new dialogue / a shift of gaze

#### Scenario: D5.12 Scenes enter late and leave early
- **WHEN** checking any scene's entry point
- **THEN** the first sentence is already inside conflict or tension; lead-in routines such as waking up, traveling, greetings, and setup are not expanded; necessary information is carried in one sentence or brought out in later dialogue

#### Scenario: D5.3 Section-length hard floor
- **WHEN** any section is finished
- **THEN** the measured word count is at least 800 words; for high-information-density genres (payoff stories / face-slapping / system-flow), it may drop to 500 words but not below 500; if short, the section counts as unfinished and must add sub-events or dialogue and be re-measured, and MUST NOT move on to the next section carrying an under-standard section

#### Scenario: D5.4 Total word-count hard floor
- **WHEN** all sections are finished
- **THEN** the measured total word count is at least 8000 words, counted by cross-platform executable character counting, and MUST NOT use model estimation or byte counts

#### Scenario: D5.5 Section-count conservation
- **WHEN** checking the finished draft against `outline.md`
- **THEN** the main text's section count equals the outline's planned section count, with none merged or omitted; if writing reveals a section should not stand alone, it must return to the outline stage to adjust rather than quietly cutting it during writing

#### Scenario: D5.6 Five-part structure lands
- **WHEN** reading through the finished draft
- **THEN** the structure is opening (first 300-500 words, at least 3 event-dense items in the first 100 words, no event-free environment description in the first 3 sentences), setup (about 30-40%, with at least 3 reversal clues planted), escalation (about 20-30%, with conflict escalating on at least one dimension), reversal (about 10-15%, the reveal completed within one section with impact stronger than all previous sections), ending (about 5-10%, closing on a quiet detail)

#### Scenario: D5.13 The reversal completes reader-side instant threading
- **WHEN** reading the reversal reveal
- **THEN** the reveal uses a look-back, monologue, or physical evidence to bring the earlier clues back before the reader's eyes at once, so readers can immediately recall exactly which places they were; it MUST NOT only state the truth without recovering the clues

#### Scenario: D5.7 The writing side does not adjudicate beyond its authority
- **WHEN** two hard constraints in the contract conflict with each other during writing
- **THEN** follow the contract's inlined conflict adjudication table; the writing side does not decide the concession order itself

#### Scenario: D5.8 Paragraphs and sections are not one-to-one
- **WHEN** checking functional segments' start and end against section boundaries in the outline and finished draft
- **THEN** the two stand independently and are not forced to align; the opening and ending parts are not cancelled or merged because their share-converted word counts fall below the section floor

#### Scenario: D5.9 No exemption from the per-section floor
- **WHEN** counting the words of any section
- **THEN** all sections meet the section-length floor, including sections carrying the opening or ending part; no case of exempting the floor by functional segment exists

#### Scenario: D5.10 Re-inject the contract hard rules each batch
- **WHEN** starting a new round of batched writing
- **THEN** that batch's writing context contains the complete content of the contract's hard-rules zone (or an equivalent complete excerpt), without relying on the writing side to look the contract up itself

#### Scenario: D5.11 Re-injection drops no entries
- **WHEN** comparing a batch's injected hard rules against this story's contract hard-rules zone
- **THEN** entries correspond one-to-one with none missing; wording may be compressed but no hard constraint is deleted, and only the subset relevant to this batch's scenes was not injected alone

### Requirement: D6 De-AI pass and polish

The polish stage MUST follow the short-story-specific criteria and MUST NOT apply any other genre's de-AI rules. Polish MUST cover five aspects (opening hook, emotional curve, reversal setup, the value of every sentence, format compliance) and MUST pass the format compliance check.

#### Scenario: D6.1 Short-story criteria take priority
- **WHEN** the editor sub-agent runs the de-AI pass
- **THEN** it judges by the short-story keep-or-cut table: direct emotion words carrying the protagonist's subjective emotion, first-person judgment sentences, crematorium previews, and heart-death chapter endings are kept; vague emotional summary sentences with no concrete reaction following them, and neutral author explanations unrelated to the characters' emotions, are deleted

#### Scenario: D6.2 Polish checklist item by item
- **WHEN** polish is complete
- **THEN** opening (first 3 sentences hook the reader / no background setup / an opening hook exists), emotion (the curve has direction / enough setup before the reversal / enough impact after the reversal), reversal (unexpected / reasonable / well-timed), pacing (no dragging / every sentence has value / word count in range), hooks (a hook every 2-3 sections / a hook at the chapter end), and technique (a concrete reaction follows emotion / the keepsake's meaning flips completely / one movement and one stillness / opening event density) have each passed

#### Scenario: D6.3 Format compliance
- **WHEN** checking the finished draft's format
- **THEN** section markers are uniform throughout; exactly one line break sits between adjacent paragraphs, with no blank lines; no indentation; main-text paragraphs carry no Markdown markers; dialogue stands on its own lines with quote style matching the target platform; neither main text nor dialogue contains banned pause punctuation; the main text contains no chapter numbers or writing-engineering words

#### Scenario: D6.4 Punctuation and word-count finish
- **WHEN** polish is complete
- **THEN** pauses, choking up, trailing off, interruptions, and blank space are all done with short sentences, actions, or line breaks, with no banned punctuation used; word count still meets the total word-count floor after polish; self-check records are not saved into the main-text file

#### Scenario: D6.5 Clean delivery
- **WHEN** checking the finished main-text file
- **THEN** the end of the file has no self-check records, no check-marker comments, and no writing-engineering words

### Requirement: D7 The final draft must check payoff against the contract and pass independent experience acceptance

After the final draft, an independent executor who **did not take part in contract assembly, writing, or cleanup** MUST first check the main text's payoff item by item against the frozen contract, and only then does experience acceptance begin. The two acceptances' outputs MUST be kept separate, and experience acceptance MUST NOT be contaminated by the payoff checklist.

The payoff check MUST cover at least: whether each contract hard rule was followed, whether every outline sub-event landed, whether the emotion goal was met, whether the reversal reveal position matches the contract, whether the throughline prop's three appearances are complete (including the three semantic progressions), whether the catalytic breakdown is in place, **whether character behavior is consistent throughout** (no action contradicting the character's setting or motivation), **whether each line of dialogue carries a function**, whether word and section counts meet the standard, and whether banned pause punctuation is at zero.

The **criterion for the dialogue-function check** is: every line of dialogue must complete at least one of advancing the plot, revealing character, creating conflict, or planting foreshadowing; several consecutive lines that only carry greetings, repeat known information, or merely connect must be judged unqualified. The check MUST scan line by line and MUST NOT judge by sampling only.

Any hard item not delivered MUST be judged a failure and return to the matching stage for fixes; failing items MUST carry quoted main-text evidence.

#### Scenario: D7.1 Payoff check independence
- **WHEN** tracing the payoff check's executor
- **THEN** they did not take part in contract assembly, main-text writing, or de-AI cleanup

#### Scenario: D7.2 Payoff conclusions item by item
- **WHEN** reading the payoff-check output
- **THEN** contract hard rules, outline sub-events, emotion goal, reversal position, throughline prop (including semantic progression), catalytic breakdown, character consistency throughout, dialogue line-by-line function, word and section counts, and the punctuation ban each have a conclusion, and undelivered items carry quoted main-text evidence

#### Scenario: D7.7 Dialogue line-by-line function check
- **WHEN** running the dialogue-function check
- **THEN** it scans line by line rather than sampling; every dialogue line is marked with the function it completes (advancing the plot / revealing character / creating conflict / planting foreshadowing); several consecutive lines that only greet, repeat known information, or merely connect are judged unqualified, with positions given

#### Scenario: D7.3 Failure rolls back
- **WHEN** the payoff check judges a hard item undelivered
- **THEN** it returns to the matching stage for fixes and re-checks, and MUST NOT deliver directly

#### Scenario: D7.4 Experience acceptance runs independently
- **WHEN** the payoff check passes
- **THEN** experience acceptance reads immersively first and then evaluates item by item, with feedback aimed at "was it satisfying to read", and evaluation metric names do not appear in author-visible text

#### Scenario: D7.5 Delivery summary
- **WHEN** both acceptances pass
- **THEN** the commander shows an author-readable delivery summary: what this story wrote / whether the target emotion was met / what could still be improved / where the finished files are; it does not show internal structure or field names

#### Scenario: D7.6 Advancing, revising, and the next story
- **WHEN** the author confirms delivery
- **THEN** the story status advances to delivered, and the author then has two paths: ask for changes to this story (take the revision path) or start the next story. The next story reuses the same genre style pack, takes an independent story directory with independent settings and contract, and this story's files stay byte-for-byte unchanged

### Requirement: D8 Author revisions must return to the matching stage and re-run the affected gates

After delivery, when the author asks for changes, they MUST be supported, and the author MUST NOT be asked to walk the whole flow again or rewrite the full text. Revisions MUST first have the commander **locate the author's natural-language feedback to a specific stage and specific sections**, and only then roll back the affected parts.

The locating rule: feedback touching emotion goals, the core reversal, or characters MUST return to concept; feedback touching structure adjustments, foreshadowing, or techniques MUST return to the outline (and carry re-assembly and re-audit of the contract with it); feedback touching specific writing, pacing, or wording MUST return to rewriting the matching sections.

After revision, the affected gates MUST be re-run and MUST NOT be skipped: if the contract was re-assembled, it MUST be re-audited; if sections were rewritten, the de-AI pass and format compliance for those sections MUST be re-run; after any change lands, the payoff check MUST be re-run. The state machine MUST support rolling back to the matching stage while keeping the rest of the progress, and MUST NOT clear the whole story's progress.

**Revisions MUST change only what was asked for and MUST NOT smuggle in extras.** The following changes MUST NOT happen unless the author explicitly asks for them; if any occurs, the revision counts as failed and rolls back for a redo:

- Changing the story's core direction or ending
- Deleting or weakening key conflict scenes
- Adding new plot lines or new characters
- Changing character personality settings
- Changing the narrative point of view
- Changing sections not asked to be rewritten

Smuggling is the most common accident form in the revision stage: while rewriting one section, the model helpfully "fixes" neighboring content along the way, so the change scope runs out of control and the author loses control of the finished draft. So when a revision finishes, the diff list before and after the change MUST be compared to confirm it falls within the requested scope.

#### Scenario: D8.1 Feedback is located to a stage
- **WHEN** the author asks for a change
- **THEN** the commander first gives a locating conclusion (return to concept / return to outline / rewrite certain sections) and rolls back from there, and MUST NOT rewrite the full text directly

#### Scenario: D8.2 Minimal revision rollback
- **WHEN** the author's feedback touches only the writing of certain sections
- **THEN** only those sections are rewritten, and the rest stay as they are; it MUST NOT rewrite the full text and MUST NOT re-assemble the contract

#### Scenario: D8.3 Structure changes carry the contract with them
- **WHEN** the author's feedback touches structure adjustments or technique changes
- **THEN** it returns to the outline stage to fix them, carrying re-assembly and re-audit of the contract with it, and MUST NOT continue writing with a contract that was not re-audited

#### Scenario: D8.4 Gates re-run after revision
- **WHEN** any change is written
- **THEN** all affected gates are re-run (rewritten sections' de-AI pass and format compliance, plus the payoff check), and it MUST NOT deliver directly

#### Scenario: D8.5 The state machine supports partial rollback
- **WHEN** a revision rolls back to a stage
- **THEN** the state machine keeps the progress of unaffected parts and MUST NOT clear the whole story's progress

#### Scenario: D8.6 Revisions smuggle nothing in
- **WHEN** one revision finishes
- **THEN** the change diff list falls entirely within what the author asked for: the core direction or ending was not changed, key conflict scenes were not deleted or weakened, no new plot lines or characters were added, character personalities were not changed, the narrative point of view was not changed, and sections not asked to be rewritten were not changed. If any smuggled change appears, the revision counts as failed and rolls back for a redo

### Requirement: D9 Short stories must have an independent state machine and breakpoint resume semantics

A short-story project's progress MUST be recorded by an independent status file containing the current phase, the current story identifier, and the story status. After an interrupted restart, it MUST be recoverable from the status file and MUST NOT depend on a full scan. Judging completed stages MUST use strict greater-than semantics, with equal value treated as that stage unfinished and needing re-dispatch.

#### Scenario: D9.1 Status fields are short-story-specific
- **WHEN** reading a short-story project's status file
- **THEN** it contains phase, the current story identifier, story status, and the most recent word-count downgrade record, with no volume-or-chapter fields

#### Scenario: D9.2 Interrupted recovery
- **WHEN** restarting after an interruption during batched main-text writing
- **THEN** the commander reads the status file to find the breakpoint and continues from the current story's unfinished phase, without re-running completed phases

#### Scenario: D9.3 Equal value means unfinished
- **WHEN** the story status equals a stage and that stage's order is not marked complete
- **THEN** it is judged unfinished for that stage and re-dispatched, and MUST NOT be skipped
