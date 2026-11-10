# Structural Heat: Avoiding AI Detection at the Source

> **Scope of application and source of evidence:** The experience of this document
> comes from the actual measured attack and defense of external AI detection in a
> single book with realistic themes (the "artificial feature" determination of all
> detector fragments has been achieved in multiple consecutive chapters, with a
> maximum of 44 rounds of iterations in a single chapter). The laws and numbers are
> the **default values**, calibrated according to the writing style and subject
> matter; the evidence score is the actual measured value of the single book, which is
> used to illustrate the direction and is not a universal constant. **Conflict
> resolution order:** Author settings and outline > Subject matter knowledge > Default
> value of this file structure > Detection optimization. When conflicting with the
> author's side, the author's side takes priority, and detection optimization must not
> cover the author's core expressions such as locked lines and chapter outlines.
> **Division of labor with common-rules.md:** common-rules manages the word and
> sentence level (banned words, sentence patterns, punctuation), and this file manages
> the paragraph/scene/position level structure. The numerical definitions for the same
> phenomenon are not repeated; see common-rules for word and sentence hits, and this
> document for structure hits.

---

## 1. Seven Laws of Actual Measurement

### Law 1: Question Chain Density Law

**Conversation is not a human signal, the ping-pong chain of questions and answers is an
AI signal. ** Questions and answers exceeding about 8 beats within 300 words in a single
window are high risks (actual measurement: 8-13 beat window 0.68-0.74, action narrative
window 0.22-0.49).

The only way to fix it is to cut the number of beats, change the pre-positioning of
naked lines to actions, and insert action shots between questions and answers. If you
add more shots to the window, it will rise.

### Law 2: Law of Conversation Density (Forward)

**A high proportion of dialogue is a cold signal, and pure narrative density is an AI
signal. ** Actual measurement: Chapters with about 85% dialogue density are 0.09-0.11
piece by piece; pure narrative sections are still 0.63-0.86 after repeated word changes.

Correction: Reduce the narrative to only factual sentences, and break the information
into dialogue. The paraphrase sequence ("He asked me how I was doing. I said I didn't
ask.") is equally hot within the isolation window, and immediately drops into two lines
of attributable dialogue.

### Law 3: Positional Heating Value Law

Testing proportional slices, **about 9-17% of slices at the beginning of the chapter and
about 10% at the end of the chapter are immune to wording surgery** - the score is
determined by "position × content type", not by wording. Actual measurement: Three
completely different contents at the beginning of the same chapter for three consecutive
rounds: 0.59→0.68→0.69.

- The default cold opening at the beginning of the chapter: dialogue or action is the
  first line, and the "time mark + scene state" type opening is prohibited.
- At the end of the chapter, inner comparisons, lists of three consecutive states,
  symmetrical reactions of two people, and still life lists are prohibited; the chapter
  stops at actions, objects, complete lines, or unresolved consequences.

### Law 4: Slice Boundary Stability Law

The detection slices follow semantic boundaries (actually measured about 250-540
words/slice). **Any modification may redraw the boundaries and cause hot spots to
jump**. When repairing the window: the first and last sentences of the window should be
kept as they are word by word, and changes of equal length will be given priority; the
character levels of other windows should remain unchanged, and modifications are
prohibited.

### Law 5: The Iron Law of Complementing Words

New sentences, new paragraphs, and new information will inevitably heat up their
location or redraw the slice. The only safe way to make up for the word count gap is
**inline stretching at the same position**: lines complement modal particles, narratives
and synonymous retellings - the number of lines, paragraphs, and periods remain
unchanged, and the slice boundaries remain unchanged (actual measurement: after
stretching line by line to make up for the number of words, the score does not rise but
decreases by 0.04; if the same number of words is filled in with ready-made sentences, 3
hot windows will be re-drawn).

### Law 6: The Law of Content Type Switching

If the improvement is less than 0.05 in two consecutive rounds in the same window or the
score increases instead, **the third round of similar modifications is prohibited**
(continuing to change words, objects, and action sequences are all the same). First
write down the existing content types (controversy field, proof field, process field,
suspense field, life chatter), and the type must be changed in the next round; the fixed
position block that still rises after changing the type, and the compression is
extremely simplified so that the slice boundary falls into the known cold area.

### Law 7: Rewrite boundaries throughout the chapter

Compressing, moving, and merging **does not count** rewriting the entire chapter (the
actual test is invalid); only changing the content type + changing the attribution
method + rearranging the order of the scenes will count. Before rewriting, save
snapshots and make a "list of fixed issues" to compare them one by one - the structures
that have been repaired in history (parallel shooting, interlayering, and paraphrasing)
are written back by hand. This is the main reason for the failure of rewriting.

---

## 2. Thirteen high-risk structures

The heat source lies in the structure and shape, not the words. If any of the following
shapes appears, first change the structure and then clarify the sentence (corresponding
to the self-check card in Sili). The common principle of demolition methods: ** Let the
characters only do the current step. The results will be unsatisfactory, the receipts
will be incomplete, and the evidence will not be arranged. **

| # | Structure | Heat source shape | Disassembly method |
|---|------|---------|------|
| 1 | Work report body | Assign tasks → execute them one by one → report all → confirm → arrange the next step | Let the characters face the interface/site and only find the current gap, do not write "all completed" |
| 2 | Evidence collection and case closure | Discover clues → Record → Verify → Supplement sources → Judge significance → Lock | Only write the traces you see at the moment, if there is insufficient evidence, clearly stop at "don't know" |
| 3 | Business Acceptance Body | Quotation → Accounting → Accounting → Rules → Contract Status → Summary Learning | Let money get stuck in a specific choice and only deal with one amount of money at a time |
| 4 | Collaboration demonstration | Teaching method → Failure → Correction → Proficiency → Summary of tacit understanding | Keep a misreading and correct it on the spot, delete "The cooperation was very good later" |
| 5 | Preparation body | Answer the phone → Review → Prepare materials → Division of work → Departure → Arrive on time | Directly enter the main scene, and materials will be replenished when needed on site |
| 6 | Number explanation | What is the concept of this number → Conversion → Supporting role evaluation → Narration and summary | The same number is only settled once: it falls on an action or decision |
| 7 | Micro-closed loop recursion | The small window independently completes "appear → confirm → execute → feedback" | Scan recursively according to 300/200/150 words, and any window can reduce all four items to a maximum of three items |
| 8 | Continuous acceptance superposition | Multiple sets of receipts at the same site: signature to take effect + arrival of account + authorization + verification of full cashing | At most one result in the same site will receive a clear receipt (single receipt exemption at the satisfying payoff site) |
| 9 | Changing the skin body at a fixed position | Continuously changing the content at the same position at the beginning/end of the chapter is still hot (the position is collecting taxes) | Stop inventing the fourth trick, simplify and push the slice boundary into the cold area |
| 10 | Standard suspense setting body | Abnormal objects → Source → Familiarity → Memories → Denial → Pointing to pictures → Questions in the last sentence, all sentences serve as hooks | Insert personal digressions that do not serve hooks and will go astray to interrupt the setting (default depth item, used only when hook strength gives way to chapter outline) |
| 11 | Bridge chain prefix | Old information arrives → Confirm unknown → Point out who knows → Immediate approval (permission is a receipt, execution has not happened yet) | Scan the first permission/decision/transition from the new information node, remove a layer of clear cause and effect, and the permission appears independently after irrelevant events |
| 12 | Private memory proof chain | Object trigger→Multiple evidences in a row→Confirm "Someone actually loves me" at the end of the paragraph | Only one complete emotional chain is left in the same memory window, and the rest will be modified by memory errors, disputes, and interruptions; when filling the number of words, it is forbidden to add a warm proof paragraph |
| 13 | A complete short play at the beginning of the fixed chapter | The beginning of the chapter is independently responsible for the complete play with inheritance and transition, cut out into a piece | The beginning of the chapter is minimalist (default is 100 words, up and down), and the main character level of the low score is locked |

---

## 3. Repair discipline (after testing feedback)

1. Only one window with the highest score is modified in each round, and the character
   level of the other windows is unchanged (hash verification).
2. The first and last sentences of the window are kept verbatim, and changes of equal
   length are given priority; first restore the modified paragraphs in the window, and
   then move the only non-locked paragraph.
3. If the improvement in the same window is less than 0.05 in two consecutive rounds or
   rises instead → change the type or roll back according to Law 6, and do not make the
   third round of similar improvements.
4. All fragments below the threshold are locked (snapshot + hash) and are not edited
   word for word.
5. The rounds, changes, and piece-by-piece results of each round are recorded in the
   project `sandbox/detect-battles.md`; the original sentence of the rollover is added
   to `sandbox/prose-regressions.txt` after confirmation by the author - this is the
   generation mechanism of all laws in this document.

---

## 4. Self-check card before writing

**Five Elements Anti-Closed Loop Card for each game** (if you can’t answer items 3-5,
don’t start writing):

1. What does the character just want to accomplish at this moment?
2. From whose immediate response does resistance arise?
3. At what point does this performance stop?
4. Which results are not explained and are left to the readers to see for themselves?
5. Which piece of information is left to the next session and not accepted here?

**Eight questions about the structure after placement** (for any "yes", change the
structure first, and then check the words):

1. Is there a paragraph that can be summarized as "Complete A, record B, verify C,
   confirm D"?
2. Is there a scene that explains all the origin, action, result, and meaning?
3. Is there a sentence explaining the effect or attitude after the action?
4. Is the same number counted more than twice?
5. Have unconfirmed things been written down as results?
6. Is it just replacing the old interpretation with new objects, leaving the structure
   unchanged?
7. Does the end of the chapter summarize what the character has learned?
8. Is there still an independent micro-closed loop of "appear → confirm → execute →
   feedback" in the small window?

> Idle stroke details warning: AI is best at writing idle strokes and scene
> arrangements such as "the shade of the tree moved its position" and "the red light
> slid into the end of the queue" (actually measured when adding idle stroke details
> to the hot window, it increased from 0.71 to 0.86). The details must be focused on
> action, friction, and relationships, not on the passage of time and the setting up
> of the environment.
