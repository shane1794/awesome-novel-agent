# Author-communication

> Unified language rules for all agents that talk to the author. Internal field names
> and self-created terms only appear in the exchange between files and agents; all
> dialogues, questions, presentations, and confirmations facing the author are all in
> plain language.

## 1. Iron law (common to all agents, with the highest priority)

1. **Dialogue, questions, presentations, and confirmation of copywriting for the author
   should all be done in everyday vernacular. ** The author is not a user of the writing
   system and does not need to understand any internal mechanisms.
2. **English internal field names are not allowed**: mood_progression, current_task,
   reader_expectation, payoff_plan, micro_payoffs, downtime_functions, key_choices,
   knowledge_state, required_changes, scene_cards, intensity_peak, i ntensity_level,
   emotional_hook, prohibitions, must_resolve, must_hold, partial_advance,
   outline.key_points, immersion_type, gold_finger, confidence, override, locked,
   inherits, use_count, skip_count Wait.
3. **Internal process words are not allowed**: order, phase, step, DONE, dispatch,
   archive, distillation, re-distillation, card/main card/scene card, template baseline,
   lore-keeping, setting change notification, circuit breaker, reassignment, idempotent,
   snapshot, upgrade and downgrade (memory), sweep.
4. **When showing the structure to the author, use the readable summary template (see
   §2). For the complete structure, only the file will be written and the original
   structure will not be displayed. ** "Show the complete xxx file" will always be
   changed to "Show the key points in summary format".
5. Common words in the Internet literary circle should be reserved without translation
   (see § 3). Do not over-translate and make your speech stilted.

## 2. Display template requirements - "Abstract to the author, complete structure into the document"

Each output that requires author confirmation has a corresponding author-friendly
display format; **The complete file (including English field names) is only placed on
the disk and not posted to the author**:

| Scene | Display method |
|------|---------|
| Chapter Outline Confirmation | `.claude/knowledge/chapter-setting-style.md` §Acceptance of step 1’s 📋 Summary format (Chapter Positioning/Connection/Main Content/Key Scenes/Key Dialogue/Conflict Progress/Word Count Target) |
| Volume plan confirmation | Author-friendly template for volume-planner STEP 3 (Chinese subtitle: What is this volume about / How readers’ emotions go / How conflicts escalate / Who knows what and what they don’t know / Chapter list) |
| Confirmation of writing style learning results | Style-distill's author portrait ("Your writing characteristics" "Your rules" "The quantitative feeling learned by AI" "Your typical sentences") |
| Reference material calibration | Chapter-reference reference material format (character expectations/now known/unknown/motivation/bottom line) |
| Memory/Feedback Confirmation | Use the author's original words or a one-sentence summary to display the entry content, and do not display the entry fields |

General rules for the rest of the confirmation scenarios: **Chinese subtitle + specific
content**, no English identifiers are used as subtitles; field names only appear in
parentheses for the agent to see, and are separated from the speech in the form of
"(internal field name)".

## 3. Terminology comparison list,internal nouns → author’s terms

Check this table when in doubt. Don’t use anything the author doesn’t understand. Use
the words listed on the right:

| Internal nouns | Author's terms |
|---------|---------|
| Information gap / Information gap relationship / Information gap changes | Who knows what, who doesn't know what ("Who doesn't know what at the beginning, what is revealed in the middle, and what new questions are left at the end") |
| Emotional anchor point / Emotional trend / Emotional arc / Micro-arc / mood_progression | How does the reader feel in this chapter (this volume) |
| Conflict Ladder/Level/Small Staircase within the Chapter | How does the conflict escalate level by level and which level is this chapter stuck on |
| Scene card | This scene (what the protagonist wants to do / what is stopping him / why the reader wants to continue reading - the three elements themselves are human words) |
| Reader gains / micro_payoffs | What readers can take away after reading |
| Cash-out plan / payoff_plan / Hook operation | How to fill in old pits and whether to bury new pits (retracting/burying wires) |
| Transition functions / downtime_functions | What else does this paragraph do besides adjusting the rhythm |
| Key choices / key_choices | Why did the character make this decision? Does it fit the character? Will the reader find it abrupt |
| Current task / current_task | What should be promoted in this chapter (one sentence) |
| Reader Expectation / reader_expectation | What are readers waiting for now and how to respond to this chapter |
| End-of-Chapter Changes / required_changes | What changed at the end of this chapter (from what to what) |
| Hard constraints / prohibitions | What must not be touched in this chapter |
| Intensity peak / intensity_peak | Which paragraph has the highest emotion (specifically which paragraph, not the "end") |
| Intensity level / intensity_level | Is it stronger or weaker than the previous chapter |
| Emotional hook / emotional_hook | The suspense left in the reader's mind at the end of the chapter (specifically who/what) |
| Dominant driving force | Reasons why readers want to continue reading (want to know the truth/worry about the protagonist/want to see the outcome/want to see how the relationship develops) |
| AI flavor / tired words / meta-narrative / forbidden words | machine-written tone / overused words / summary preaching |
| Anti-AI (modification/rules/acceptance) | Routines to avoid (when clarification is needed: make the text not like written by a machine) |
| Archive / lore-keeping / Volume completion determination | Archive, update settings and memory |
| Distillation / Master Card / Scene Card (Style) / Confidence / Template Baseline | Learn Your Writing Style / Your Style Profile |
| Version snapshot /.style-versions | Backup (old style files) |
| Deduction Sandbox | Plot Deduction ("Let the characters act out the core story again") |
| Memory promotion / downgrade / use_count / sweep | Rules for writing down: transfer to long-term memory if you use it too much, if it is no longer useful, ask the author if you want to delete it |
| Structural heat source / high-risk structure / anti-closed-loop card / receipt | At first glance, the paragraph structure looks like machine writing (such as work report-style paragraphs, question-and-answer paragraphs) / Five things to think clearly before writing this scene / This matter has a clear result in the book |
| Regression pattern library / Locked line whitelist | List of original sentences that have been turned over in this book (automatically prevent recurrence) / Exemption list of original sentences that you decided to keep |

## 4. Retain without translation - a common word in the Internet literary circle

The authors of these online articles all know these words and use them directly. Don’t
translate them into more convoluted terms:

Satisfying payoff, face-slapping, hook (burying the hook/retracting the thread),
foreshadowing, suspense, golden finger, CP, copy, sense of substitution, sense of
expectation, rhythm, character design, volume, volume outline, chapter outline, starting
point and ending.

## 5. Maintenance Agreement

- Add internal nouns → Synchronous addition § 3. Comparison table, don’t let the author
  be the first person to see it.
- Modify the author's visible words → Check § 3 first; if you are not sure, use
  "specific events + human descriptions" instead of terms.
- This specification itself is an authoritative constraint on the visible text of the
  author; the agent definition, skills, and display format in the knowledge base shall
  prevail. In case of conflict, this specification shall prevail.
