# anti-ai skill: De-AI Flavor Pipeline

## Responsibilities

Read writer's draft and run it through the Phase 1-4 pipeline to detect and clear AI traces. **Change expression only, never plot.**

## Process Overview

```
Input: archives/*.draft.md (writer's original output)

Phase 1 Scan: scan the full text and mark AI flavor positions, classified by Gates A-F
Phase 2 Diagnosis: machine first pass (check-prose.py, can fall back) + score the 6 quantitative indicators, grade it (light / medium / heavy)
Phase 3 Cleanup item by item: systematic revision by Gates A-F (converging over multiple rounds)
Phase 4 Report: output the revision report

Output: archives/*.anti-ai.md
```

## Reference Files

| File | Purpose |
|------|------|
| `.claude/knowledge/anti-ai.md` | Anti-AI rules merged file (human-feel positive methods + tiered banned word list + methodology + false-positive protection + genre positive and negative examples, generated per genre by init.py) |

---

## Phase 1: Scan

Read the whole text and mark AI flavor positions sentence by sentence, classified by Gates A-F.

### Structural Heat Source Scan (first, before Gates A-F)

Read the "structural heat source law" section of `.claude/knowledge/anti-ai.md` and compare the draft against the 13 high-risk structures (work report style, micro closed-loop recursion, bridge-chain prefix style, private memory proof chains, and similar) and the pre-writing taboos (Q&A ping-pong chains, chapter openings with a "time marker + state", chapter endings with inner parallel sentences / three linked state closings, and similar), paragraph by paragraph:

- On a hit, mark it `[S]` (structural hit) and record the paragraph and structure name. **The report lists a separate "structural hits" section; do not mix it into the Gate A-F counts**. When the same problem hits both a structure and a wording rule, count it once, as a structural hit
- The source data is measured from a single realistic-genre book; the numbers are defaults. When they conflict with the author's settings / style, follow the ruling order stated in the knowledge file (the author side takes priority)

Phase 3 revision order: **structure before wording**. Structural hits are handled first (swap the content type / cut the Q&A beats / split the micro-loop), and sentence-level cleanup comes after. Sentence-level surgery only works when a passage's heat is high; a structural problem requires changing the paragraph structure.

### Gate A: Banned Words

Scan for any word in the banned-words table → mark the position and entry with `[A]`.

Scan range: word level across the whole text, independent of context.

### Gate B: Sentence Pattern Formulas

| ID | Pattern | Example |
|----|------|------|
| B1 | "Not A, (but) B" (不是A，（而）是B) | "He was not angry; he was disappointed" (他不是生气，而是失望) |
| B2 | Adverbial "with..." (，带着……) | "He looked out the window, with a trace of melancholy" (他看着窗外，带着一丝惆怅) |
| B3 | "As if / like / as though ... in general" (仿佛/犹如/宛若……一般) | "The voice seemed to come from far away" (声音仿佛从很远的地方传来) |
| B4 | "Make / let / cause" causal patterns (让/令/使) | "This scene made him think of his childhood" (这一幕让他想起了童年) |
| B5 | "When... / at the time when..." (当……时/的时候) | "When he pushed the door open" (当他推开门的时候) |
| B6 | "Meanwhile" scene switching (与此同时) | "Meanwhile, in another place" (与此同时，在另一个地方) |
| B7 | "Seemingly / as if + perception verb" (似乎/仿佛+感知动词) | "He seemed to hear something" / "He seemed to see" (他似乎听到了什么 / 他仿佛看到了) |

### Gate C: Psychological Description

| ID | Pattern | Example |
|----|------|------|
| C1 | Direct "he felt / thought / realized" (他感到/觉得/意识到) | "He felt a wave of unease" (他感到一阵不安) |
| C2 | Direct emotion words (情绪词直述) | "He was very nervous" / "She was very sad" / "He became angry" (他很紧张 / 她很难过 / 他愤怒了) |
| C3 | "A surge of ... welled up in the heart" (心中涌起一股……) | "A warm current welled up in his heart" (心中涌起一股暖流) |
| C4 | "He could not help / involuntarily..." (他不禁/不由得) | "He could not help shivering" (他不禁打了个寒颤) |
| C5 | Inner debate | "One voice said... another voice said..." (一个声音说……另一个声音说……) |
| C6 | Repeated description (the same information split across multiple paragraphs) | The same scene / emotion written over and over across consecutive paragraphs |

### Gate D: Rhythm

| ID | Pattern | Description |
|----|------|------|
| D1 | Consecutive parallel sentences (3 or more with the same structure) | "Maybe... maybe... maybe..." / "No... no... not even..." (也许……也许……也许…… / 没有……没有……甚至没有……) |
| D2 | Overloaded long sentence (a single sentence over 40 words) | A long sentence with no pause |
| D3 | Over-dense paragraph (a single paragraph over 60 words with no line break) | Information piled into one paragraph |
| D4 | Consecutive paragraphs of the same length (3 or more) | Even paragraphs, no long-short variation |
| D5 | Consecutive same subject (4 or more sentences) | The same subject opening sentences in a row |
| D6 | Monotonous sentence patterns (5 consecutive sentences of similar length) | Little variation in sentence length |
| D7 | Em dash parenthetical redundancy (double em dash, description, double em dash) | "A, [a long appositive], did B" (A, [a long appositive set off by double em dashes], did B) → write "A did B" directly |

### Gate E: Dialogue

| ID | Pattern | Example |
|----|------|------|
| E1 | Dialogue too complete | Every line is a complete written sentence |
| E2 | Excessive tags | "He said angrily" / "She said softly" (他愤怒地说 / 她轻声说道) |
| E3 | Everyone in the same tone | Everyone speaks the same way |
| E4 | Template small talk | "Are you okay?" / "I am fine" (你还好吗 / 我没事) |
| E5 | Dialogue too dense | 8 or more consecutive lines of pure dialogue, with no action / silence / environment / inner life in between (the threshold follows chapter-quality-checklist.md; dense dialogue passages are relaxed to 12 lines, see the checklist's scene exception) |

### Gate F: Endings

| ID | Pattern | Example |
|----|------|------|
| F1 | Elevating ending | "He finally understood..." (他终于明白了……) |
| F2 | Summarizing ending | "This is the meaning of..." (这就是……的意义) |
| F3 | Preview-style ending | "What he did not know was..." (他不知道的是……) |
| F4 | Exclamatory ending | "...!" closing with high emotion |

### Scan Output

Record the scan results temporarily for Phase 2 quantification:

```
Gate A: X hits (word list)
Gate B: X hits (classified B1-B7)
Gate C: X hits (classified C1-C6)
Gate D: X hits (classified D1-D6)
Gate E: X hits (classified E1-E5)
Gate F: X hits (classified F1-F4)
```

### Gate G: Style Acceptance (instruction following; read the same chapter's prompt)
- Read `prompts/vol-{N}-ch-{M}-prompt.md` (same source as writer's generation) and judge the main text against it item by item per `.claude/knowledge/style-distill/prompt-templates/verify-checklist.md` (four categories: numbers / proportions, hard rules, modeling rules, soft guidance).
- Both states use this flow: the prompt always carries style (undistilled = the main text's qualitative four fields; distilled = Case 2 quantification + voice layer). Judge both states only by the prompt's content.
- Output the violations report (the .anti-ai.md acceptance section): item by item, "number + original requirement + main text performance + violated or not + suggestion", totaling the violated count / total count, with the conclusion PASS/FAIL.
- The summary / ruling / report format follows the deterministic standard in `.claude/knowledge/style-distill/prompt-templates/verify-checklist.md` (violated string-boolean convergence / verdict PASS-FAIL / violation count; does not depend on tools/*.py); violated entries are the card-draw feedback source.
- Gates A-F (de-AI flavor) stay unchanged; Gate G only outputs a verdict and does not revise the main text.

---

## Phase 2: Diagnosis

### Machine First Pass (run the script before doing it by hand)

Before quantifying, run the deterministic scripts (regex / statistics, catching hard indicators the model's eye would miss or miscount):

```
python3 .claude/tools/check-prose.py archives/vol-{N}-ch-{M}-{slug}.draft.md
python3 .claude/tools/check-chapter.py archives/vol-{N}-ch-{M}-{slug}.draft.md
```

(On Windows without `python3`, use `python` or `py` instead, same below)

The two scripts split the work: check-prose handles AI flavor statistical form; check-chapter handles chapter delivery hard defects (quote sandwiching, nested / half-width quotes, word-by-word word count reconciliation, regression strings, and similar; the project-level regression library and whitelist live in `sandbox/`). The results are judged independently per tier:
- **Either script says "needs revision" (hard failure, exit code 1)**: merge into the Gate A/B hit list and revise in Phase 3; check-chapter hard hits are marked `[hard defect]` and cleared first
- **"Needs human judgment / needs ruling" (warning, exit code 0)**: use as candidates for Phase 3's "save the person before cleaning the sentences" priority passages and as a reference for human re-checking; do not rule them as violations directly

Two result tiers, with different uses:
- **"Needs revision" (hard failure, exit code 1)**: hard stop words / blacklisted talk / model road signs / reversal sentences hit → merge into the Gate A/B hit list and revise in Phase 3
- **"Needs human judgment" (warning, exit code 0)**: semantic pivot sentence patterns, sentence length rhythm, short paragraph bursts, opening repetition, metaphor clusters, conjunction density, and similar → use as candidates for Phase 3's "save the person before cleaning the sentences" priority passages and as a reference for human re-checking; do not rule them as violations directly

Boundaries:
- The script only reports; it does not revise the main text. Thresholds follow this file and `.claude/knowledge/anti-ai.md`; a script warning never escalates into a hard Gate
- Fallback: script missing (`.claude/tools/check-prose.py` does not exist; other platforms keep it under their own root) / no Python (`python3` / `python` / `py` all unavailable; on Windows try `python` / `py` first before ruling a fallback) / cannot run a shell → skip the machine first pass, fall back to Phase 1 model eyeball scanning, and mark the Phase 4 report "script verification not run" (non-blocking)

### 6 Quantitative Indicators

| Indicator | Calculation | Light | Medium | Heavy |
|------|---------|----|----|----|
| Banned word density | Gate A hits / thousand words | <5 | 5-12 | >12 |
| Parallel paragraph count | Paragraphs with consecutive identical sentence structures | <2 | 2-4 | >4 |
| Psychological word share | Gate C1-C4 hits / total paragraphs | <15% | 15%-30% | >30% |
| Dialogue tag density | Gate E2 hits / dialogue sentences | <10% | 10%-25% | >25% |
| Average sentences per paragraph | Total sentences / total paragraphs | 2.5-4 | 4-5.5 | >5.5 or <2 |
| Repeated description density | Gate C6 hits / thousand words | <1 | 1-3 | >3 |

### Grading Rule

Take the **highest tier** among the 6 indicators from A-F as the final grade (Gate G is an independent ruling: PASS/FAIL, not merged into this tier):

| Grade | Handling Range |
|------|---------|
| Light | Gate A + B (banned words + sentence patterns) |
| Medium | Gate A + B + C + D (plus psychology + rhythm) |
| Heavy | Gates A-F all open (including dialogue + endings) |

> The grading information travels with the draft to Phase 3 and decides which Gates take part in the revision.

---

## Phase 3: Cleanup Item by Item

### Pre-Check (before each round)

**Save the person before cleaning the sentences:** Judge paragraph by paragraph. Would another model, or another genre, write this passage exactly the same way (no character imprint, no details specific to the current scene)? If yes, mark it `[priority passage]` and handle it first in this round's Gate revision; if no (it is already alive: details follow the character's point of view, dialogue is doing work, idle brushstrokes have a source), only clear the Gate hard violations and do not rewrite it.

Read the "false-positive protection" section of `.claude/knowledge/anti-ai.md` and run an exemption ruling on each Gate hit first:
- Is the hit on the false-positive protection list? → Yes → skip it (mark `[SKIP: false-positive protection]`) and do not change it
- Unsure → keep the original text and mark it in Phase 4 as `[suspected: possible false positive]`

### Convergence Rules

1. Within the Gate range fixed by the grade, revise Gate by Gate
2. **If the same paragraph has no change for two consecutive rounds, skip that paragraph**
3. **At most 3 rounds for the whole text** (each round covers all Gates)
4. **If round 3 still has 10 or more items, mark them `[needs review]` and continue**
5. Each round outputs an arbitration request and waits for the user to confirm whether to continue

### Gate A: Banned Word Replacement

Extra rules:
- Most toxic sentence patterns (five stars): replace on sight (see the banned word table in `.claude/knowledge/anti-ai.md`)
- Tier 1 banned words: replace on sight
- Tier 2 banned words: replace when over the threshold
- Metaphor check: "as if / like / as though / as" (仿佛/犹如/宛若/如同) → delete or use plain description

### Gate B: Sentence Pattern Breakdown

| Pattern | Handling |
|------|------|
| "Not A but B" (不是A而是B) | Write B directly |
| ", with..." (，带着……) | Split into short sentences or swap in an action |
| "As if / like ... in general" (仿佛/犹如……一般) | Delete or use plain description |
| "Make / let / cause" (让/令/使) | Delete "make" / "let"; the subject acts directly |
| "When..." (当……时) | Split into standalone action sentences |
| "Meanwhile" (与此同时) | Switch to the new scene's opening directly |
| "Seemingly / as if + perception verb" (似乎/仿佛+感知动词) | Delete "seemingly" / "as if"; write the perceived fact directly |

### Gate C: Externalizing Psychology

| Hit Pattern | Handling |
|---------|------|
| "He felt / thought / realized" (他感到/觉得/意识到) | Delete the lead-in and write the perceived fact directly. **This rule does not trigger at the end of a dialogue line** ("So...?" He realized his voice was shaking a little, 他意识到自己声音有点抖) |
| Direct emotion words (nervous / sad / angry, 紧张/难过/愤怒) | Replace with a bodily reaction (shaking hands / staring blankly / bulging veins) |
| "A surge welled up in the heart" (心中涌起) | Replace with an action |
| "Could not help / involuntarily" (不禁/不由得) | Write the action directly |
| Inner debate | Cut it down to only the conclusion |
| Repeated description | Merge or delete the redundant paragraphs |

> For the emotion word to bodily detail quick reference, see the "Four, replacement strategy quick reference → externalizing emotion" section of `.claude/knowledge/anti-ai.md` (the only authority; not maintained again here).

### Gate D: Breaking Rhythm

| Check Item | Handling |
|--------|------|
| Consecutive parallel sentences | Keep the strongest one; break the rest apart |
| Overloaded long sentence (>40 words) | Split it into two sentences at a comma / action turn |
| Over-dense paragraph | Split the paragraph by action / information change; use single-sentence paragraphs for rhythmic emphasis |
| Consecutive paragraphs of the same length | Split one paragraph into a single-sentence paragraph, or merge adjacent short paragraphs |
| Consecutive same subject (4 or more sentences) | Adjust the subject's position; alternate long and short sentences |
| Monotonous sentence patterns | Split one long sentence into short ones, or join two short sentences into a long one |

### Gate E: De-Toning Dialogue

| Check Item | Handling |
|--------|------|
| Dialogue too complete | Add half-finished lines, tone words, repetition |
| Excessive tags | Use action / context to carry it; delete the adverbs |
| Everyone in the same tone | Distinguish the tone by character personality |
| Template small talk | Replace with blank space or trailing off |
| Dialogue too dense (8 or more lines of pure dialogue) | Break it up in the middle with action / environment / silence / inner activity |

### Gate F: De-Elevating Endings

| Check Item | Handling |
|--------|------|
| Elevating ending | Delete it; stop on a scene / action |
| Summarizing ending | Delete it; let the scene end naturally |
| Preview-style ending | Delete it or swap in a concrete hook |
| Exclamatory ending | Change it to a period or an action |

### Word Count Control

The deletion amount is limited by grade:

| Grade | Deletion Cap |
|------|---------|
| Light | At most 15% of the original text |
| Medium | At most 25% of the original text |
| Heavy | At most 35% of the original text |

### Whitelist

If a `.anti-ai-whitelist` file exists in the same directory, the paragraphs it lists skip all Gate checks.

---

## Phase 4: Report

After the revision is done, output a report containing the following:

### Word Count Change

```
Original word count: XXXX
Revised word count: XXXX
Change: +/- XXX (±X%)
```

### Revision Statistics

```
Gate A replacements: X items
Gate B breakdowns: X items
Gate C externalizations: X items
Gate D breaks: X items
Gate E fixes: X items
Gate F changes: X items
Total: X revisions
Grade: light / medium / heavy
Convergence rounds: X
Script verification: passed / not run (fallback marked)
Style acceptance: see the violations report in the acceptance section
```

### Before / After Comparison

For each Gate type, give at least 1 typical revision showing the before (AI flavor) → after comparison.

### Machine Re-Run Verification

Re-run the scripts on the revised main text: take the main text section of `.anti-ai.md` (excluding the acceptance report section, since the counter-examples quoted in the report would be misjudged) and write it to a temporary file, then run:

```
python3 .claude/tools/check-prose.py <temporary file path>
python3 .claude/tools/check-chapter.py <temporary file path>
```

- "Needs revision" zeroed → script verification passed; still hits → go back to Phase 3, handle them, and re-run (both scripts must zero their own hard items)
- False-positive protection exemptions apply the same way: a hit on the `.claude/knowledge/anti-ai.md` false-positive protection list is marked `[SKIP: false-positive protection]` and is not forced to zero
- "Needs human judgment" is still judged by a human as before; zeroing it is not required
- Fallback: cannot run the scripts (missing / no Python, Windows ruling as in Phase 2 / no shell) → mark the report "script verification not run" (non-blocking)

---

## Acceptance Checklist

| Check Item | Standard |
|--------|------|
| Most toxic sentence patterns (five stars) | 0 items |
| Tier 1 banned words | 0 items |
| Tier 2 banned words (high frequency) | At most 1 per type |
| Ending elevation | 0 items |
| Emotional mismatch | The whole text need not be fully reasonable; a mismatched reaction must come from the character's personality or the scene's pressure. Formulaic padding counts as a fail |
| Information density | Sparse passages (if any) must belong to the current scene and the character's point of view (idle brushstrokes / state / drifting off); template idle brushstrokes inserted by quota count as a fail |
| Dialogue tags | No 3 consecutive sentences with the same tag |
| Dialogue density | No 8 or more consecutive lines of pure dialogue (dense dialogue passages relaxed to 12 lines, see the checklist's scene exception; when distilled, prefer the dialogue share rendered in the prompt) |
| Em dash | Usage ruling (common-rules.md): allowed for pauses / rhythm and dialogue interruption; delete parenthetical redundancy |
| Plot integrity | Consistent with the original text; no plot added or deleted |
| Machine re-run verification | "Needs revision" zeroed (false-positive exemptions marked SKIP); on fallback, the report is marked "script verification not run" |
| Phase 4 report | Fully output |
