# Prompt Production SOP

**Positioning:** Produce chapter outline + writing-style + genre-profile into subagent
executable prompt.md (`prompts/vol-{N}-ch-{M}-prompt.md`), and make a qualification
judgment on the product. Only responsible for prompts and not involved in text writing.

**Global constraints:**
- All four writing-style fields must be injected into prompt - narrative identity
  determines narrative distance and attitude, rigidly determines unbreakable writing
  creeds, AI is prone to mistakes and determines a specific anti-pattern list, and
  description levels and techniques determine operable description practices. If any
  subagent is missing, it will be let go at the most critical place.
- Execution parameters such as word count target and emotion target are read from
  `settings/writing-style.md` and `chapters/vol-{N}-ch-{M}.md` and are not repeatedly
  defined in prompts/ - modifications in one place take effect globally.

**Design principle: Single definition per semantic**
- "Emotion" is only defined in the input scene raw materials, and the character's
  initial state and texture do not repeatedly define emotions.
- "Scene" is only defined in the input scene raw material, and the previous context only
  refers to the scene name.
- "satisfying payoff" is only defined in mission instructions and narrative objectives,
  and does not appear repeatedly.


## 1. Prompt project structure

Organize according to prompt engineering standards: first define identity and tasks,
then provide background and cases, and finally give input and output definitions.

```
## Role

You are a {author novel subject} subject novel writer.


## Task instructions

Create the text of chapter ______ (role in the overall volume: ______).

## Word Count and Compression Strategy
- **Target word count**: Suggested ______ words (±10% acceptable, narrative integrity takes precedence over precise word count)
- **Compression strategy**: When the word count exceeds, priority is given to compressing low-weight scenes (scene 1/2 transitions/medium-weight paragraphs). It is recommended to compress to less than 100 words - retain 1 sentence of environment switching + 1 sentence of character action + 1 sentence of emotion/atmosphere blank; red line content shall not be deleted or the main emotional line destroyed due to compression.

Driving force for this chapter: ______
Information release rhythm: ______

Narrative goals:
1. Core suspense: ______ → End of chapter: ______ (resolved/deepened/transferred)
2. Reader sentiment: ______
3. Satisfying payoff design: ______, paved in the scene______, released in the scene______

Writing methodology:
1. Focus locking: For each scene, identify its unique "core conflict" or "character emotion" or "information gap" (choose one of the three, no superposition). Concentrate more than 70% of the text on this focus object, and briefly mention the secondary elements. High-weight scenes are refined to the level of action and perception, and the "sensory layering and trade-off" rules must be applied at the same time; low-weight scenes are allowed to transition quickly, but must not violate focus locking or sensory layering and trade-off rules.
2. Sensory layering selection: Focus on 2 senses for refinement, increase to 3 if the atmosphere allows (such as hearing + touch), and sketch the rest. Uniform stacking in all dimensions is prohibited. Sound exceptions: When sound clues are key information of the red line of the plot of this chapter and are presented in short white descriptions (1-2 sentences), they may not be counted in the sensory quota (such as gunshots = key signals of battle, approaching footsteps = danger signs); environmental decorative sounds (birdsong, hawking, etc.) are not exceptions
3. The narrative rhythm alternates: a dense action/dialogue + a short psychological blank + a light environment transition cycle. Long paragraphs such as continuous long descriptions, continuous dialogues, and entire articles are prohibited.
4. Information release control: Key foreshadowing and character secrets are brought out in fragments, rather than being fully explained at once. Allow blank space


## Background information

### Previous Context

Ending scene of the previous chapter: ______

Reader’s emotional residue: ______

The gap left by the previous chapter: ______

### Character initial state

______：
  Qidian: ______
  → Experience:______
  → End point: ______
  Mini habits/little actions in this chapter: ______

______：
  ...


## Case

[Reference examples for scenario writing, filled in after four steps of transformation from the scenario methodology]


## Input

### Scene raw materials

Scene N｜______｜______Tone｜Weight: ______
  Core event: ______
  Emotional meaning: ______
  Information gap: ______
  Emotional turning point: ______ (the transition from X to Y)
  → Connection: ______
  Focus of this scene: core conflict/character emotions/information gap (choose one from three)
  Weight of this scene: ______


## Don't break the rules

### Priority (high to low)
1. **Restraint Red Line**, plot red line, character restricted area, boundary prohibition
2. **Number of words**, Hard constraint on the target number of words (compression strategy is enabled if the limit is exceeded)
3. **T1 words/cognitive verbs/sensory**, Modification threshold, cognitive verb moderation, sensory stratification
4. **Narrative rules** (higher than other rules of the same level and writing standards)
5. **Other rules for writing standards at the same level**

### Red Line Constraint

Conflict Ladder: ______

Plot red line (cannot be deleted):
1. ______
2. ______

Border prohibitions (not covered):
1. ______
2. ______

Character restricted areas:
______ No ______
______ No ______

### Web writing style baseline (applicable to any chapter)
1. Full linear narrative
2. Reject perfect narrative - allow for blank spaces and jumping thoughts
3. Deliberate accumulation of techniques is prohibited
4. Prohibition of poetry
(Cognitive verb restraint, natural cause and effect, and narrative warmth are injected from the "Specific Narrative Rules" paragraph, and this baseline will not be repeated)

### Style suggestions (can be deviated) (only the undistilled state is injected; the distilled state is deleted in this section - the style is subject to the rendering section of Case 2, the strict matching deviation is ≤20%, and there is no deviating clause)
- **Perspective**: Defined according to `settings/writing-style.md` (undistilled = text "Narrative Identity" field; distilled = rendering [Perspective] section, setting stage definition, consistent throughout the book). This chapter's POV characters are by chapter outline `outline.pov`. **It is forbidden to redefine the perspective type in the prompt word** (such as third person written in the template).
- **Description**: Use motion perception to promote the narrative, and the senses serve the atmosphere.
- **Rhythm**: Paragraphs rise and fall naturally, and sentences alternate between long and short sentences. The above can be appropriately deviated if the mood or plot is served.

### Guidelines for scenario writing (injected after transformation from the four steps of scenario methodology)
This chapter involves {N} scene types ({type list}. Optional values: dialogue / fight / environment / inner-mono / transition / group-scene), each type injects 1-2 specific guidelines.

### Texture requirements

Useless details (trivial life-oriented details that do not serve the main line):
  1. ______
  2. ______

Dialogue rhythm: allow half-sentences, modal particles, meaningless pauses, and repeated mantras to fit the character's habits

Paragraph precision stratification (distribution of pen and ink according to weight):
  - High-weight scenes: full of details, at least 3 action/perception level details used to develop core conflicts/emotions/information gaps
  - Medium weight scene: normal narrative rhythm, character interaction drives the plot
  - Low-weight scenes: Optional transition template reference - Note: The following is a reference structure and can be fine-tuned according to the context. 1 sentence for environment switching + 1 sentence for character action + 1 sentence for emotion/atmosphere blank, the number of words should be controlled within 100 words

Additional constraints (specific to this chapter):
  1. ______

### Appendix: Demonstration Paragraph (Non-Binding Reference)

**Disclaimer:** The following examples are for style reference only. The writer can choose whether to follow them or not and should not replace any instructions above. The name of the demonstrated methodology is noted at the end of each case.
  2. ______
```

**Chapter 1 Special Rules (enabled when automatically detecting vol-x-ch-1):**
1. The pre-situation context is fixedly filled in with "no pre-chapter, the opening
   chapter directly cuts into the character's current actions", and large sections of
   world background introduction are disabled.
2. The first scene of the scene raw material must be marked with a high weight, and
   priority should be given to describing the protagonist's appearance, subconscious
   habits, and current predicament.
3. The writing specification is added: "The first three paragraphs start with the
   character's actions as the first sentence, and do not pile up multiple layers of
   description of the environment."


## 2. Core filling method

Each element has an independent filling method that defines the input source, filling
principle, and output requirements.

**Global Principle:** After filling in all the fields, read through them once. Mask the
field names to see if each item reads as a narrative screen (✅) or a writing instruction
(❌).


### Role

| Fields | Input Sources | Filling Principles |
|------|--------|---------|
| Theme of the author's novel | genre-setting.md | Copied, each chapter unchanged |


### Task instructions

| Fields | Input Sources | Filling Principles |
|------|--------|---------|
| Chapter number | Volume number + Chapter number | Chapter {M} |
| Role in the whole volume | Chapter outline memo | Foreshadowing/advancement/climax/conclusion |
| Target word count | Chapter outline memo | Take it directly and add flexible explanations (recommended value ±10% is acceptable, narrative integrity is priority). If the number of words in the chapter outline is missing (abnormal), use the default 2500 (see.claude/knowledge/chapter-setting-style.md for the word count backward method), and mark it in the completed report |
| Driving force of this chapter | Outline Dominant driving force + information gap relationship of chapter outline | Consistent with the outline |
| Information release rhythm | Chapter outline information gap relationship + driving force type | Suspense → leave a hook at the end of each chapter; threat → shorten the safety period; goal → phased advancement |
| Core suspense | Chapter synopsis memo | It is in the form of a question, not a plot summary |
| Suspense state | Chapter outline memo | Choose one of three: resolved/deepened/transferred |
| Reader’s feelings when leaving the scene | Chapter outline Point of emotional curve | An emotional word or picture description |
| satisfying payoff type | chapter outline memo | face-slapping/growth/ambiguity/reversal/puzzle/desperate comeback |
| Padding position/release position | Chapter outline memo | Scene number, consistent with the input scene raw material |

**Writing Methodology:** The four-step execution process directly copies the template
without making adjustments.


### Background information

#### Previous Context

| Fields | Input Sources | Filling Principles |
|------|--------|---------|
| The ending screen of the previous chapter | The emotional_design of the previous chapter outline `chapters/vol-{N}-ch-{M-1}.md` (emotional hook emotional_hook + end point of the chapter, take the last paragraph of mood_progression) + required_changes extraction | Sensory details (what you see/hear/feel), 30-50 words |
| The residual emotion of the reader from the previous chapter | The point of the emotional curve of the previous chapter | An emotional word (not analysis) |
| The gap left by the previous chapter | Chapter outline memo | Something the reader is looking forward to but has not yet happened, 1 sentence |

When the previous chapter is ch-1: Fixed filling in "No pre-chapter, the beginning of
the chapter directly cuts into the character's current actions", and large sections of
world background introduction are disabled.

#### Character initial state

| Fields | Input Sources | Filling Principles |
|------|--------|---------|
| Qidian | Character setting + previous chapter archive | Specific status (including micro-actions), not just emotional words |
| → Experience | Chapter Outline Character Status | 1-2 Key Turning Points |
| End point | Chapter outline Character status | Perceptible status changes |
| Mini habits/small actions | Chapter outline memo + character setting | Something unique to this chapter and related to the plot |

A key supporting role (such as an appearance) fills in an additional impression and one
thing that must be completed.


### Case

After four steps of transformation from the scenario methodology, fill in the writing
reference examples of the scenarios in this chapter. Select 1-2 methodologies for each
scene type (optional values: dialogue / fight / environment / inner-mono / transition /
group-scene), and inject them as cases after four steps of transformation.

**Fill source:** scene-craft methodology → four-step transformation (anchor role →
anchor information difference → anchor emotional rhythm → fusion output)

**Principle:** Each case is a demonstration of "how to write a specific character in a
specific scenario", not a copy of the general methodology.

**Case marking requirements:** At the end of each case, mark the methodological name of
the demonstration in parentheses, such as (Demonstration: Sensory Layered Choice /
Tactile + Hearing). Annotations help writers understand the correspondence between cases
and writing methodology. When there are multiple cases for the same methodology, only
the first one is marked.


### Input

#### Scene raw materials

Scene is the basic unit of narrative. Scene segmentation is based on the inflection
point of the emotional line:

**Boundary signal (segmentation if any one is met):**

| Signal | Decision | Example |
|------|------|----|
| Change location | Character walks to another place | Breakfast shop → Bookstore |
| Jump time | There is an invisible passage of time | Morning → Dusk |
| Emotional transition | Tone changed | Awkward → Natural |

**Seed field structure:**

| Fields | What to write | Control |
|------|--------|--------|
| Entrance emotion | How the reader feels when entering | One word |
| Core event | External event chain captured by camera. Use arrows to connect them in series ("A → B → C"). Prohibit character inner activities/cognitive verbs/emotional conclusions | Keep the plot from going astray |
| The emotional significance of the core event | What this event means to the reader | Not analysis, but feeling |
| **Information Gap** | **{Who knows what} ↦ {Who doesn’t know what}** | **Information asymmetry injected into this scenario - source of tension/expectation** |
| Emotional turning point | The moment when the emotion changes from X to Y | Turning point |
| Exporting emotions | How you feel when you leave | One word |
| → Connection to the next scene | Emotional transition method | No jumping |
| Weight of this scene | Marked based on the importance of core events | High = detailed action/psychology accounts for 70% of the text; medium = normal narrative; low = quick transition |

**Chapter 1 Special Rules:** The first scene must be marked with high weight, giving
priority to the protagonist's appearance, subconscious habits, and current dilemma.


### Output

#### Constraint red line

| Fields | Input Sources | Filling Principles |
|------|--------|---------|
| **Conflict ladder** | **Chapter outline memo** | **Levels 1-4, consistent with the outline conflict ladder. Determines the intensity of the pressure** |
| Plot red line (cannot be deleted) | Chapter synopsis memo | 2-4 key events/lines/actions, subagent's rails |
| Boundary prohibition (not involved) | Chapter outline memo | Write "what not to do" and not write "what to do" |
| Character restricted area | Chapter outline memo + author's supplement | Things each character will not do in this chapter |

**No substitutions allowed:**

| ❌ BANNED | ✅ ALTERNATIVE |
|---------|--------|
| State emotional conclusions directly | Externalize with actions/expression/environment |
| Sublimation summary at the end of the chapter | Stop on the scene/action |
| Adverbs modify dialogue | Remove adverbs and use actions to suggest |

#### Writing standards

| Source | File | Fill in fields |
|------|------|---------|
| Basic constraints | genre-example/{genre}.md#prompt_segment | Perspective/Description/Rhythm |
| Universal anti-AI |.claude/knowledge/anti-ai.md (merged file) | Positive points of living voice (living-voice) + T1 summary of the most poisonous sentence patterns + meta-narrative prohibition; fatigue word threshold / T2 / T3 no injection (return to anti-ai agent) |
| Theme anti-AI | anti-ai/{genre}.md (if it exists) | Theme positive and negative examples |

**Scene writing methodology injection:** According to the scene type identified by the
scene raw material (optional value: dialogue / fight / environment / inner-mono /
transition / group-scene), read the corresponding file from
`.claude/knowledge/scene-craft/`. **Must be contextually filtered** - Rewrite the
methodology based on the character status, information gaps, and emotional trends of
this chapter, and cannot apply it mechanically. **Only 1-2 items are extracted from each
scene type, and it is not required to cover them all. **

**Special treatment for Chapter 1:** Perspective/description added "The first three
paragraphs should start with the character's actions as the first sentence, and do not
pile up multiple layers of environment description"; the first scene is forced to have a
high weight.

#### Texture requirements

| Fields | Input Sources | Filling Principles |
|------|--------|---------|
| Useless details | Chapter outline memo + author's brainstorming | Trivial life-like details that do not serve the main line are allowed (if any, pinching the corners of clothes, rubbing fingertips on the table, wandering in a daze), they must belong to the current scene and character's perspective, and are not inserted according to quotas |
| Dialogue rhythm | writing-style.md | Allow half-sentences, modal particles, meaningless pauses, and repeated mantras to fit the character's habits |
| Paragraph precision stratification | Scene weight mapping | High-weighted scenes must have at least 3 action/perception level details; low-weighted scenes must be based on the transition template (1 sentence of environment + 1 sentence of action + 1 sentence of atmosphere, ≤100 words); to prevent the full text from being refined and unified |


## Input source mapping table

| Elements | Primary Sources | Secondary Sources |
|-----|---------|---------|
| role | genre-setting |, |
| Task instructions | writing-style, chapter outline memo, volume outline dominant driving force |, |
| Background information / Previous chapter context | Previous chapter outline emotional_design/required_changes (archives/ forbidden to read) | Volume outline previous chapter summary |
| Background information / Character initial state | Chapter outline Character state, character settings |, |
| Case | scene-craft methodology (four-step transformation) | role setting, information gap relationship |
| Input / Scene raw materials | Chapter outline Scenario card (three elements of the scene + information gap relationship) |, |
| Output / Constraint Red Line | Chapter Outline Memo, Author's Supplement, Chapter Outline Conflict Ladder |, |
| output and writing specs | genre-example.md, anti-ai.md,.claude/knowledge/scene-craft/ | scene type identification results |
| Output / Texture requirements | Chapter outline memo, author's supplement | writing-style.md |



## 3. Inspection (prompt-crafter quality access control)

> Note: The following check process is an operational check of prompt-crafter, **no
> prompt file is injected**.

### Quick Sniff

Read the **core event** of scene raw material Scene 1 - mask the field name. Does it
read "what happened" (✅) or "what to write" (❌)? The former is qualified, the latter is
a writing instruction and needs to be refilled.

### Integrity Check

Pass = prompt Pass:

| # | Element | Check item | Passing criteria |
|---|-----|-------|---------|
| 1 | Role | Clear identity | Fill in the subject matter, and the writer will know "who I am" after reading |
| 2 | Task instructions | Complete parameters | Chapter number/number of words/driving force/rhythm 4 fields all have values |
| 3 | Background information / previous context | Picture sense | The picture at the end of the previous chapter is sensory details (ch-1 marked without previous text) |
| 4 | Background information / Character initial state | There are changes | Each character has Qidian → Experience → End point, perceptible changes |
| 5 | Cases | Reference examples | At least 1 example of scenario writing after four-step conversion |
| 6 | Input / Scene raw materials | Weight + field | Each scene has a weight annotation, including entry emotion/core event/information difference/exit emotion |
| 7 | Output / Constrain red line | Hard constraint | Conflicting ladder layer + red line + restricted area |
| 8 | output and writing specs | Anti-AI + techniques | Contains anti-AI rules + 1-2 technique guidelines for each type |
| 9 | Output / Texture Requirements | Imperfect Constraints | Containing half-sentences/life-oriented details/paragraph accuracy layering |

**Judgment:** All 9 items ✅ → Passed. Item 1-2 ❌ → Targeted modifications. 3 items or
more ❌ → Refill in entirety.

### Conflict Detection

After filling in, read through and check the reference consistency of each element:

| Check items | Consistency ✅ |
|--------|---------|
| Background information / Emotional residue of the previous context = Background information / Character initial state Qidian of the first character |, |
| Character state turning point = Input / Scene raw material Emotional turning point of a certain scene |, |
| Task instructions / narrative goal suspense state = input / scene raw materials exit emotion of the last scene |, |
| The satisfying payoff release position exists in the input scene raw material |, |

### Check section by section

| Element | Qualification Criteria | Failure Signal |
|-----|---------|-----------|
| Character | You can know the author's identity and tone from the first reading | Template-level empty words |
| Task instructions | Clear parameters, know what chapter to write and how many words | Missing number of words or driving force |
| Background information / Previous context | Like normal memories, with a sense of picture (ch-1 marked without previous text) | Written as a plot summary |
| Background information / Character initial state | It says "What changes has TA experienced in this chapter?" | The character encyclopedia has been copied, or only the state has not changed |
| Case | There are specific reference examples of scenario writing, non-universal methodology | Leave blank or copy the general methodology |
| Input / Scene raw materials | Each scene has a weight annotation, and the seed is the narrative picture | The seed is the "write this scene..." writing instruction |
| Output / Constraint red line | Red line + restricted area complete | Constraint is empty ("no deviation") |
| output and writing specs | Contains anti-AI + sparse techniques | Full coverage without anti-AI rules or techniques |
| Output / Texture requirements | Contains "imperfect" constraints (half-cut/life-oriented/accuracy layered) | Leave empty or just write "none" |

All passed → Enter text generation. If any of them fails → take the exam first and then
write.
