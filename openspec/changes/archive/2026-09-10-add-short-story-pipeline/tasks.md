# Tasks: 2026-09-10-add-short-story-pipeline

> Organization: `## N.` = main flow / sub-flow; `- [ ] N.M` = leaf node.
> Each item's `[number]` maps one-to-one to the Scenario numbers under `specs/`, traceable in both directions.
>
> Scope (design D13): bounded by "the author says one sentence, write a short story, and gets a finished draft". List scanning, text teardown, and cross-genre check-tool porting are not in this change; see the proposal's "Later Changes".
>
> **Implementation pace (design migration plan step 0)**: do not wait until all 18 groups are done before the first end-to-end live test. By then, finding out whether the chain works costs the most rework. First run the chain through in the **first wave**: 1 genre pack (wife-chasing crematorium), 1 platform, knowledge files limited to the three essentials (format spec + de-AI criteria + writing base), length pressed to 3-4 sections. Once one `manuscript.md` exists, fill in by group (10 genres / 7 platforms / all reference files).

## 1. Main flow A, sub-flow A1: initialization entry point routes by length

- [ ] 1.1 [A1.1] The entry-point skill gains a short-story branch: recognize intents such as "write a short story / write a Yanxuan story / write a short tale", then ask, run `init.py` with `--length short`, and load the short-story commander after completion. Verify: say one sentence in a live test and confirm it takes the short-story branch
- [ ] 1.2 [A1.2] Existing projects route by the `length` marker in the project index: when marked short, load the short-story commander directly. Verify: hand-edit the marker and re-invoke, confirming it enters no non-short-story flow
- [ ] 1.3 [A1.3] Short stories are not the default: without `--length`, the project index contains no short-story marker. Verify: after `init.py <tmp>`, grep finds no length marker
- [ ] 1.4 [A1.4] `--length` value check: a value other than `short`/`long` prints the allowed values and exits non-zero, creating no files. Verify: `python tools/init.py /tmp/t --length medium; echo $?` is non-zero and the directory was not created

## 2. Main flow A, sub-flow A2: short-story skeleton is a complete set of its own

- [ ] 2.1 [A2.1] Create the `templates/short/` skeleton tree: project index (with length marker), story directories, sandbox, `.agent/task/`, `tools/`, genre settings, platform directories. Verify: after `--length short` initialization, the directory tree is complete and the index contains the marker
- [ ] 2.2 [A2.2] `create_skeleton` picks the template-tree root by length (design D10), and the skeleton contains only directories the short-story flow needs. Verify: top-level directories all belong to the short-story flow, with no extra directories
- [ ] 2.3 [A2.3] Short-story project-level instructions (`CLAUDE.md` / `AGENTS.md` / `AGENTS.codex.md`): agent composition, flow (emotion, concept, contract, writing, polish, payoff check, acceptance, revision), and directory map are all in short-story form. Verify: the three files match the short-story flow
- [ ] 2.4 [A2.4] Short-story state machine: `phase` covers setup/planning/contract/writing/polishing/verifying/delivered, with the current story identifier and story status. Verify: grep assertions, and no volume-or-chapter fields

## 3. Main flow A, sub-flow A3: genre system numbered independently

- [ ] 3.1 [A3.1] Build the short-story genre registry (10 entries: number + identifier + Chinese name), with numbers corresponding one-to-one to style-pack files. Verify: a script checks that every registry identifier has a matching file
- [ ] 3.2 [A3.2] With `--length short`, the genre numbering space switches to the short-story registry, and knowledge products take the short-story style packs. Verify: after `--length short --genre 1`, genre references come from the short-story style packs
- [ ] 3.3 [A3.3] Short-story out-of-range numbers error and prompt the short-story range. Verify: a number above 10 exits non-zero and prompts 1-10

## 4. Main flow A, sub-flow A4: short-story agent group with independent duties, deployable on all platforms

- [ ] 4.1 [A4.1] Write 5 short-story agent definitions (commander / concept / writer / editor / verifier), with frontmatter isomorphic to existing agents. Verify: `python tools/check-agents.py` exit code 0
- [ ] 4.2 [A4.2] Duty independence is traceable: contract audit and payoff checks belong to the verifier agent, contract assembly belongs to the concept agent, the two are not the same agent, and the verifier agent writes no content files. Verify: check each of the five definitions' input/output contracts item by item
- [ ] 4.3 [A4.3] Claude and OpenCode deploy to the agents directory. Verify: both platforms' short-story project agents directories contain the short-story group
- [ ] 4.4 [A4.4] Codex platform TOML products (name / description / inlined SOP). Verify: products parse and the SOP is inlined
- [ ] 4.5 [A4.5] Grok platform Markdown products, with sub-agents carrying the no-further-dispatch constraint. Verify: products contain the sub-agent list and the no-redispatch section
- [ ] 4.6 [A4.6] Reasonix / Zcode / DSH inlined skills, matching the short-story agent group in count, with the commander containing that platform's dispatch adapter section. Verify: initialize each of the three platforms once and assert SKILL.md counts and content
- [ ] 4.7 [A4.7] No non-short-story agents deployed. Verify: no non-short-story writing agent in any platform product of a short-story project

## 5. Main flow A, sub-flow A5: knowledge base deployed independently

- [ ] 5.1 [A5.1] `deploy_knowledge` gains a short-story branch: the short-story de-AI criteria merge into a standalone product. Verify: the short-story project knowledge directory has a standalone short-story anti-AI product whose content comes from the short-story criteria files
- [ ] 5.2 [A5.2] The three kinds (short-story format specs / writing references / genre style packs) land in place. Verify: all three are reachable through post-deployment paths
- [ ] 5.3 [A5.3] All reference paths resolve. Verify: `check-agents.py` exit code 0
- [ ] 5.4 [A5.4] Genre style-pack content is complete: each contains narrative voice / opening paradigm / hook motifs / emotional intensity / dialogue style / **emotion-chain library** / technique library / pacing skeleton / ending paradigm; the emotion-chain library gives several named emotional arcs (each with 4-6 stages, each stage named); each technique-library entry is a formula + concrete example, not just a name. Verify: check each pack for all nine sections; spot-check technique entries for formula and example

## 6. Main flow A, sub-flow A6: sync tools sync by length

- [ ] 6.1 [A6.1] The sync tool reads the project index's length marker, and a short-story project stays in short-story form after sync. Verify: short-story form assertions still hold after running sync on a short-story project
- [ ] 6.2 [A6.2] Change detection covers short-story assets. Verify: changing a repo-side short-story knowledge file makes the sync check exit non-zero

## 7. Main flow A, sub-flow A7: static check chain covers short stories

- [ ] 7.1 [A7.1] All short-story agent references resolve. Verify: `python tools/check-agents.py` exit code 0
- [ ] 7.2 [A7.2] Deployed-product simulation covers both long and short lengths (design D7), and short-story knowledge is not judged orphaned. Verify: every short-story knowledge file has a reference source or sits on an explicit exemption list
- [ ] 7.3 [A7.3] Run the rule-conflict check: short-story thresholds do not conflict with the existing threshold system; where the same object has different numbers, add an explicit exemption with its reason recorded. Verify: exit code 0 and exemption entries carry reasons
- [ ] 7.4 [A7.4] The platform test suite adds short-story E2E assertions (split by length). Verify: `python tools/test_platforms.py` all green

## 8. Main flow A, sub-flow A8: one directory per story, with story isolation

- [ ] 8.1 [A8.1] Story-directory isolation: two stories each occupy independent directories, each with settings / outline / contract / main text. Verify: after writing two stories in sequence, check file paths and content independence
- [ ] 8.2 [A8.2] Shared resources sit at project level (project-level instructions / status / genre knowledge) and are not copied into story directories. Verify: no shared-resource files under story directories
- [ ] 8.3 [A8.3] A new story does not affect old stories. Verify: after starting a second story, the first finished story's checksum is unchanged

## 9. Main flow B, sub-flow D0: independent dispatch contract

- [ ] 9.1 [D0.1] Write the short-story dispatch contract as the single authoritative source, with the commander definition stating it follows it. Verify: both state the same thing and the definition contains the statement
- [ ] 9.2 [D0.2] Order protocol matches (only input / output paths + status field). Verify: to-do directory files contain no execution steps or methodology
- [ ] 9.3 [D0.3] The commander does not overreach (only writes order and status files). Verify: after one dispatch, the content files' writer is not the commander

## 10. Main flow B, sub-flow D1: set the emotion and direction

- [ ] 10.1 [D1.1] Six emotion goals to pick from, each with fitting scenarios / difficulty / commonly paired genre packs. Verify: with no idea, the guided path picks an emotion and yields a genre recommendation
- [ ] 10.2 [D1.2] Submission-platform tone, three to pick from (Zhihu Yanxuan / mini-programs / Tomato Short Stories), switching point of view, intensity, chapter-end hooks, and ending texture by platform. Verify: after picking a platform, the framework's point of view and landing points match the template
- [ ] 10.3 [D1.3] A clear request goes straight through (no item-by-item guidance when one sentence gives all elements). Verify: with all elements given as input, the framework is produced directly, with follow-up questions only for missing items
- [ ] 10.4 [D1.4] `setting.md` is structurally complete (basic info / premise / core reversal with type and at least 3 setup clues / four emotion intensities / character sketches / genre techniques). Verify: check item by item
- [ ] 10.5 [D1.5] Confirmation gate one: after completion, show the framework summary and stop; vague replies count as unconfirmed; do not lay out the outline before confirmation. Verify: replying "more or less" does not advance

## 11. Main flow B, sub-flow D2: concept and outline

- [ ] 11.1 [D2.1] Design work runs in order (platform tone + genre pack, then pick 2-3 techniques, villain, reveal method, outline, two validations). Verify: non-applicable items carry a reason mark
- [ ] 11.2 [D2.2] `outline.md` gives one line per section with complete fields (structure part / main event / 3-5 sub-events with function tags / emotion / relationship change / causal chain / new information learned / hook / foreshadowing / motion-stillness / dialogue density / target word count). Verify: pick any line and check its fields
- [ ] 11.3 [D2.3] Reversal reveal position validation: below 50% rolls back, 50-60% is a gray zone for re-check, above 60% passes. Verify: construct an outline below 50% and confirm it is blocked
- [ ] 11.4 [D2.4] Foreshadowing re-check: ending elements have prior setup, the throughline prop appears three times, setup-to-reveal gap is at least 3 sections. Verify: deleting one setup makes the re-check report the missing item
- [ ] 11.5 [D2.5] Confirmation gate two: show the outline summary and stop; do not assemble the contract before confirmation. Verify: the contract file does not exist before confirmation
- [ ] 11.6 [D2.6] Technique landing table: each core technique is marked with a carrying section and a payoff section, with setup distance between the two and no carry-and-payoff-at-once entries. Verify: read the landing table entry by entry; construct one carry-and-payoff-at-once entry and confirm it is blocked
- [ ] 11.7 [D2.7] No functionless sections: every section takes on at least one of advancing a technique / adding pressure / foreshadowing / relationship change / emotion delivery / developing a supporting-character subplot; sections the techniques do not cover are carried by the other five types; supporting characters who drive subplots have a memorable hook and affect the main plot, and are not decorative characters. Verify: check section by section; construct a pure-transition section and confirm it is judged unqualified
- [ ] 11.8 [D2.8] The causal chain follows the fixed shape: handoff point, motivation and action, core event, direct consequence, ending hook; the handoff point and direct consequence are both written out, with no connection point omitted and no generic causal description. Verify: spot-check any section line
- [ ] 11.9 [D2.9] The emotion chain covers the whole story: the outline contains the chain name and the section numbers each stage covers; every section is covered by some stage, with no section outside the chain; the chain's stages and the five parts are not forced into a one-to-one match. Verify: reconcile section numbers one by one
- [ ] 11.10 [D2.10] Technique entries pair formula with example: every technique picked into this story contains an applicable formula and one concrete example, not just a name. Verify: spot-check technique entries
- [ ] 11.11 [D2.11] Villain wrongdoing has prior setup: before each wrongdoing there is setup where danger accumulates, and readers can already sense malice accumulating before it happens; there is no node with sudden wrongdoing and no warning. Verify: locate each villain wrongdoing and trace back its prior setup
- [ ] 11.12 [D2.12] The throughline prop's three appearances progress semantically: the three semantic states are harmless (like idle writing, carrying no emphasis), draws attention, and reveals the truth (recovering the first two); not limited to physical keepsakes (a habit / a sentence / a number all work). Verify: check each appearance's semantic state in turn
- [ ] 11.13 [D2.13] The catalytic breakdown is set: at the 60-75% point of the full text there is a contradictory element the current explanatory framework cannot explain, whose role is to force readers to abandon old assumptions; it is not replaced by adding same-kind information; genres where the reversal type does not apply are marked not applicable. Verify: locate the device and check its position

## 12. Main flow B, sub-flows D3 contract assembly / D4 independent contract audit

- [ ] 12.1 [D3.1] Contract assembly SOP: six-element structure, flattened output section, suggestive techniques in a separate sub-section outside the hard-rules zone. Verify: the produced contract has all six elements and no placeholder residue
- [ ] 12.2 [D3.2] Transforming general techniques into this story's writing (anchor the protagonist / anchor the information gap / anchor the emotional rhythm / merge into output). Verify: spot-check technique entries for concrete character names and information-gap relationships, not genre-pack text copies
- [ ] 12.3 [D3.3] Hard rules in descending priority (red lines > word counts > banned items > narrative rules > other same-level writing-standards rules). Verify: read through the contract with no priority inversions, and suggestive techniques not mixed into the hard-rules zone
- [ ] 12.4 [D3.4] Deduplication after assembly: the same object in the same format is defined only once. Verify: read through the contract with no exact duplicate of the same quantity line or ban
- [ ] 12.5 [D3.5] Contract entries are checkable: every hard-rules-zone entry can be checked against the finalized main text. Verify: examine entry by entry, with no "judge by feel" wording
- [ ] 12.6 [D3.6] The contract inlines the conflict adjudication table, numeric-conflict part (the concession order and trade-off basis when section-length floor / total word count / five-part shares / reversal reveal position / paragraph line-shape conflict). Verify: construct one numeric conflict and confirm the contract has an executable adjudication
- [ ] 12.11 [D3.7] The contract inlines the conflict adjudication table, qualitative-conflict part: logical consistency takes priority over payoffs and gut-punches, with the requirement that "a character's key actions must have a motivation source and stay consistent throughout"; when the writing side meets a conflict, it follows this and does not adjudicate on its own. Verify: construct a case where "a payoff needs a character to act against their motivation" and confirm the adjudication table says to change the payoff, not the logic
- [ ] 12.7 [D4.1] Contract audit SOP: the auditor is not the assembler (the verifier agent performs it). Verify: trace assembler and auditor as different agents
- [ ] 12.8 [D4.2] All five audit items present (transformation quality / priority order / rule deduplication / consistency between constraints / entry checkability), each with quoted source evidence. Verify: read the audit output item by item
- [ ] 12.9 [D4.3] Failed audit rolls back to assembly for fixes and re-audit, and writing does not start. Verify: deliberately create one priority inversion and confirm it is blocked
- [ ] 12.10 [D4.4] After the audit passes, the contract is frozen as this round's baseline. Verify: the contract version used by writing and the payoff check matches

## 13. Main flow B, sub-flow D5: main-text writing hard floors

- [ ] 13.1 [D5.1] Two questions before writing, now against the contract (target emotion / matching technique entry in the contract / which paragraph to use it in). Verify: when they cannot be answered, the contract is re-read before writing
- [ ] 13.2 [D5.2] Three dimensions kneaded in (happening / perceiving / reacting in the same paragraph), with paragraphs breaking on new action / object / information / dialogue / gaze. Verify: spot-check sections for no "three-paragraph stacking" writing
- [ ] 13.3 [D5.3] Section-length floor of at least 800 words (high-information-density genres at least 500), machine-measured; when short, expand before writing the next section. Verify: construct a 600-word section in an ordinary genre and confirm it is judged unfinished
- [ ] 13.4 [D5.4] Total word count of at least 8000, using cross-platform executable character counting (model estimation banned, byte counts banned). Verify: the counting command runs on macOS / Linux / Windows
- [ ] 13.5 [D5.5] Section-count conservation: main-text section count equals the outline's planned section count. Verify: construct a finished draft missing one section and confirm it is blocked
- [ ] 13.6 [D5.6] Five-part structure lands (shares + at least 3 event-dense items in the first 100 words + no event-free environment description in the first 3 sentences). Verify: spot-check the finished draft against spec `D5.6`
- [ ] 13.7 [D5.7] The writing side does not adjudicate beyond its authority: when contract hard constraints conflict, follow the contract's adjudication table. Verify: construct one conflict and confirm the writer did not decide the concession order itself
- [ ] 13.8 [D5.8] Paragraphs and sections are not one-to-one: functional segments' start and end stand independently of section boundaries, and the opening and ending parts are not cancelled or merged because their share-converted word counts fall below the section floor. Verify: check both sets of boundaries against the outline and finished draft
- [ ] 13.9 [D5.9] No exemption from the per-section floor: sections carrying the opening or ending part meet the section-length floor just the same. Verify: count all sections' words; no case of exemption by functional segment
- [ ] 13.10 [D5.10] Re-inject the contract hard rules each batch: when a new batch starts, the writing context contains the hard-rules zone's complete content, without relying on the writing side to look it up itself. Verify: check the writing input of the second and later batches
- [ ] 13.11 [D5.11] Re-injection drops no entries: batch-by-batch injected hard rules correspond one-to-one with the contract hard-rules zone, with none missing and no subset-only injection. Verify: compare the first and last batches' injected content against the contract text
- [ ] 13.12 [D5.12] Scenes enter late and leave early: every scene's first sentence is already inside conflict or tension; lead-in routines such as waking up / traveling / greetings / setup are not expanded. Verify: spot-check every scene's entry point
- [ ] 13.13 [D5.13] The reversal completes reader-side instant threading: at the reveal, a look-back / monologue / physical evidence brings the earlier clues back at once, and readers can name exactly which places they were; not just stating the truth. Verify: read the reversal section and check whether concrete clues were recovered

## 14. Main flow B, sub-flow D6: de-AI pass and polish

- [ ] 14.1 [D6.1] Run the de-AI pass by the short-story criteria (keep-or-cut table, see AR2). Verify: judgment sentences / crematorium previews / heart-death chapter endings were not wrongly deleted
- [ ] 14.2 [D6.2] Polish checklist, six categories item by item (opening / emotion / reversal / pacing / hooks / technique). Verify: each checklist item has a conclusion
- [ ] 14.3 [D6.3] Format compliance (uniform section markers / single line break between paragraphs with no blank lines / no indentation / no Markdown in main text / dialogue on its own lines / quote style / no chapter numbers or engineering words). Verify: item-by-item grep assertions
- [ ] 14.4 [D6.4] Punctuation and word-count finish: banned punctuation at zero, pauses done with short sentences / actions / line breaks; word count still meets the standard after polish. Verify: grep finds no banned punctuation + re-measure word count
- [ ] 14.5 [D6.5] Clean delivery: no self-check records, no check-marker comments, and no engineering words at the end. Verify: manually check the last 20 lines of the finished file

## 15. Main flow B, sub-flow D7: payoff check and acceptance delivery

- [ ] 15.1 [D7.1] Payoff-check SOP: performed by an executor who took part in neither assembly / writing / cleanup. Verify: trace the executor as having taken part in none of the three
- [ ] 15.2 [D7.2] Conclusions item by item (hard-rule compliance / outline sub-event landing / emotion goal / reversal position / throughline prop's three appearances including semantic progression / catalytic breakdown / character consistency throughout / dialogue line-by-line function / word and section counts / punctuation ban), with undelivered items carrying quoted main-text evidence. Verify: read the check output; no item has "conclusion only, no evidence"
- [ ] 15.3 [D7.3] Undelivered means rollback: when a hard item is undelivered, return to the matching stage for fixes and re-check; do not deliver directly. Verify: deliberately create one undelivered item (such as a shifted reversal position) and confirm it is blocked
- [ ] 15.4 [D7.4] Experience acceptance runs independently: immerse-read first, then evaluate item by item, with metric names absent from author-visible text. Verify: the acceptance output contains no internal metric names
- [ ] 15.5 [D7.5] Delivery summary (what was written / whether the emotion was met / what could still be improved / where the files are), without showing internal structure. Verify: the summary has no violating words per the author-communication spec
- [ ] 15.6 [D7.6] Two paths available after delivery: ask for changes to this story, or start the next story; the next story has an independent directory and independent contract, and this story's files stay byte-for-byte unchanged. Verify: walk both paths once
- [ ] 15.7 [D7.7] Dialogue line-by-line function check: scan line by line (no sampling), marking each line's function (advancing the plot / revealing character / creating conflict / planting foreshadowing); several consecutive lines that only greet, repeat known information, or merely connect are judged unqualified, with positions given. Verify: go through one section's main text line by line

## 16. Main flow B, sub-flow D8: author revisions

- [ ] 16.1 [D8.1] Locate the feedback: after the author asks for a change, first give a locating conclusion (return to concept / return to outline / rewrite certain sections) instead of rewriting the full text directly. Verify: give three kinds of feedback (emotion-goal type / structure type / writing type) and confirm they locate to different stages
- [ ] 16.2 [D8.2] Minimal rollback: feedback touching only certain sections' writing rewrites only those sections, keeping the rest as-is, without re-assembling the contract. Verify: after changing one section, the other sections' files are unchanged and the contract was not regenerated
- [ ] 16.3 [D8.3] Structure changes carry the contract with them: feedback touching structure adjustments or technique changes returns to the outline to fix, carrying re-assembly and re-audit of the contract with it. Verify: change one technique and confirm the contract was re-assembled and re-audited before writing continued
- [ ] 16.4 [D8.4] Re-run gates after revision: rewritten sections re-run the de-AI pass and format compliance, and the payoff check re-runs after changes land; do not deliver directly. Verify: after changing one section, the check output is updated
- [ ] 16.5 [D8.5] State machine partial rollback: rollback keeps the progress of unaffected parts and does not clear the whole story's progress. Verify: after changing section 2, confirm section 3 and later progress is still there
- [ ] 16.6 [D8.6] Revisions smuggle nothing in: the change diff list falls entirely within what the author asked for: core direction or ending unchanged, key conflict scenes not deleted or weakened, no new plot lines or characters added, character personalities unchanged, narrative point of view unchanged, sections not asked to be rewritten unchanged; if any appears, the revision counts as failed and rolls back for a redo. Verify: construct a "change one section and helpfully change the neighboring section" case and confirm it is blocked

## 17. Main flow B, sub-flow D9: state machine and breakpoint resume

- [ ] 17.1 [D9.1] Short-story-specific status fields (phase / current story identifier / story status / word-count downgrade record; no volume-or-chapter fields). Verify: grep assertions
- [ ] 17.2 [D9.2] Interrupted recovery: after an interruption midway through batched main-text writing, restart and continue from the unfinished phase, without re-running completed phases (including the contract stage). Verify: interrupt once manually and observe the restart
- [ ] 17.3 [D9.3] Equal value means unfinished: when the story status equals a stage and the order is not marked complete, judge it unfinished and re-dispatch. Verify: construct an equal-value case and confirm re-dispatch

## 18. Main flow C, short-story independent anti-AI track (AR1-AR7)

- [ ] 18.1 [AR1.1] Produce the short-story de-AI **check-item grading list**: each item marked reuse or independent with its reason (genre-independent / bound to genre wording); no blanket "reuse the whole tool" or "drop the whole tool" conclusions. Verify: every list item has an owner and a reason; check against design D2's grading table with nothing missing
- [ ] 18.2 [AR1.2] Genre-independent items are handled by existing tools: format and layout items, general AI-tone items. Verify: when a short-story project runs checks, these items come from existing tools, with no duplicate implementation of the same kind of check in the repo
- [ ] 18.3 [AR1.3] Genre-bound items use short-story calibration: lyrical word choice, reversal sentence patterns, paragraph shape, universal-metaphor thresholds. Verify: these four items' judgments come from the short story's own word lists and criteria, without directly adopting another party's calibrated output
- [ ] 18.4 [AR1.4] Build the short-story de-AI directory, with the criteria deployed as a standalone product file. Verify: knowledge directory location is correct and the deployed product is standalone
- [ ] 18.5 [AR2.1-2.3] Write the short-story keep-or-cut table (three keep categories / two cut categories / three-column structure) with the single criterion "does it carry the protagonist's subjective emotion right now". Verify: judging the same doubtful sentence produces no conflicting conclusions
- [ ] 18.6 [AR3.1-3.4] Land emotion writing in the short-story writing references: emotion words are followed by scene-specific concrete actions or objects; one emotion is written once; emotion words themselves are not in the deletion scope; **first-person possessives are cleared** ("my heart" becomes "heart", "my soul" becomes "soul"; leading mini-clauses such as "I know / I understand / I realize / I feel / I see myself" become statements, feelings, or actions). Verify: a regex scan of the finished draft finds zero hits for "my + body part"
- [ ] 18.7 [AR4.1-4.5] Write the short-story banned-word list (eight categories), containing no emotion words themselves; **the degree-adverb category covers both weak and strong ends** (weak: slightly / faintly / slowly / gently; strong: right / currently / very / extremely / increasingly / indeed / seemingly), constrained together by one per-thousand-word cap and trimmed by density rather than deleted indiscriminately. Verify: `check-conflicts.py` exit code 0 or exemption entries carry reasons; spot-check the list for both ends' words
- [ ] 18.8 [AR5.1-5.4] Write the short-story self-check list (emotion follow-through / present-tense narration kept / chapter ending with hook and judgment / anti-templating). Verify: all four items are mechanically decidable or have clear criteria
- [ ] 18.9 [AR6.1-6.3] The punctuation hard constraint is stated once each in the short-story format spec and the short-story criteria; pauses are rewritten at the semantic level (short sentences / actions / line breaks), not by mechanical replacement. Verify: both places carry the statement; the finished draft has no banned punctuation and its pauses read naturally
- [ ] 18.10 [AR7.1-7.3] Add the paragraph-shape floor and ceiling (design D12): the floor is the platform shape (a short-paragraph base color with one sentence per paragraph), the ceiling guards against telegram style (a decidable signal for consecutive fragments in sheets); state that short sentences are occasional beats landing on emotional peaks, not the base color throughout. Verify: both the format spec and the de-AI criteria contain the floor, ceiling, and positioning statement, and the ceiling signal is decidable
- [ ] 18.11 Move all short-story writing references and genre style-pack files, applying design D9's three rewrites (paths changed to the post-deployment base / external-system references removed / passed through the author-communication spec), with file headers marking the source and the "commercial use needs original author confirmation" note. Verify: `grep -r "story-architect\|narrative-writer\|character-designer\|consistency-checker\|\.story-deployed\|/story-"` finds nothing; `check-agents.py` exit code 0
- [ ] 18.12 [AR8.1-8.3] Character-naming constraint: give high-convergence full names and characters (including homophones) as a list that is machine-scannable, without using "random generation" as the mechanism; naming results are saved into the story settings (stable across passes, revisions do not change names); later stages follow the record and do not regenerate. Verify: scan a finished draft with the list and find zero hits; revise once and confirm names are unchanged
- [ ] 18.13 [AR9.1-9.4] Modern-concept firewall: one machine-scannable word list covering five categories (modern science and technology terms / internet slang / academic terms / modern institutions and job titles / modern time and measurement units), marked as **applying only to ancient- and fictional-world-setting genres**; main text must not bare reasoning-layer modern concepts (psychological trauma / family of origin / boundaries and similar); when translation fails, delete the concept and use senses and behavior instead, without bypassing with a generic metaphor. Verify: an ancient-genre sample draft scans the word list with zero hits; a modern-genre sample draft is confirmed not wrongly covered

## 19. Compatibility regression, end-to-end live test, and wrap-up

- [ ] 19.1 Compatibility regression: existing initialization and existing pipeline behavior do not change because of this change (design D13 compatibility statement). Verify: initialization products without `--length` match the pre-change items one by one; existing specs' requirements are unmodified
- [ ] 19.2 Full-chain regression: `python -m py_compile tools/*.py`, `python tools/test_platforms.py`, `python tools/check-agents.py`, and `python tools/check-conflicts.py` all exit 0. Verify: all four commands output no FAIL
- [ ] 19.3 Run short-story initialization once on each of the seven platforms and manually check the product shapes. Verify: the seven platforms' products match spec A4 / A5
- [ ] 19.4 End-to-end live test (required before repo submission): from "say one sentence, write a short story" to receiving the finished main text, covering both the expert straight-through path and the guided path for newcomers; deliberately construct one undelivered item to confirm the payoff check blocks it; deliberately raise one revision request to confirm it takes the D8 path. Verify: the live-test record is attached to the PR description
- [ ] 19.5 Documentation sync: `README.md` / `README-en.md` / `ARCHITECTURE.md` / `SKILL.md` gain short-story explanations and trigger words. Verify: all four documents contain short-story sections
- [ ] 19.6 Submit and open a PR (`feat: 短篇写作流水线`, linked to this change); after merging, bump `VERSION` and write release notes per the release flow. Verify: CI green, review passed
