# Text acceptance criteria

> **Responsibility Statement:** This document is an acceptance checklist (diagnostic
> probe set). For objects that overlap with `common-rules.md`, the threshold value is
> subject to common-rules.md, and only non-duplicate definitions are quoted here;
> diagnostic items not covered by common-rules.md (fatigue word/sentence probes
> exclusive to this file) are allowed to be defined by yourself, but they must not
> conflict with common-rules.md.

**Positioning:** Subagent's text traceability diagnostic tool set - when the text does
not meet the author's expectations, locate the link (prompt/chapter outline/style
reference) where the problem lies, so that targeted corrections can be made. All
acceptance items are not the final judge, they are diagnostic probes.

After the subagent generates the text, the main agent checks the text item by item. But
these checks are not to "stop unqualified text" - the author has the final say whether
the text is qualified or not. ** The purpose of the inspection is to quickly locate the
source of the problem when the author says "wrong".

---

## Highest Principle

> **There is only one criterion for evaluating the text: whether it meets the author's
> expectations. **

All rules below are tools to aid judgment and are not the final judge. All the rules are
passed but the author feels it is wrong → The author’s judgment shall prevail. The rules
part has not been passed but the author thinks it is okay → respect the author’s
judgment.

The value of rules is to provide structured inspection dimensions and reduce omissions.
But the final arbiter of each chapter is the author himself, not the rules themselves.

---

## Global conflict resolution table

When rules conflict, this priority will be used to decide. This table has been preloaded
into prompt's task instructions and writing specifications during the prompt-crafter
stage, and writers and auditors refer to it here without duplication of rulings.

### Priority hierarchy (from high to low)

| Priority | Rules | Description | Implementation requirements | Conflict examples |
|--------|------|------|---------|--------|
| 1 (highest) | Constrained red lines | Plot red lines, character restricted areas, boundary prohibitions | Red line content may not be deleted or modified at any time. Word count compression cannot result in missing red lines. The sensory exception is limited to sound cues that are key information in the red line | When the word count exceeds the limit, the red line plot may not be deleted to make up the word count |
| 2 | Word count | Subject to the target word count of the chapter outline memo (±10%) | When the word count exceeds, priority will be given to compressing low-weight scenes (scene 1/2 transition/medium-weight paragraph), and the compression must not touch the red line. The core conflict segment of high-weighted scenes does not move. The order of compression is determined by the quality layer (within the writing standard level: writing style/emotion first) - cut the environment/passers-by/transition description first, and retain the emotional paragraphs and paragraphs requiring writing style | When sensory refinement requirements inflate the number of words, reduce the weight of non-core descriptions of scenes first |
| 3 | T1 words (modification category) | As if, a trace, can't help, can't help but etc. (suddenly/suddenly/suddenly belongs to the context-sensitive category, ≤4 times/chapter, the red line paragraph is wider) | When the threshold is exceeded, priority is given to retaining narrative functions, and non-functional redundant words are deleted. Be lenient when the red line paragraph appears (retaining the rhythm function) | When the narrative rules require "vivid dialogue" and the T1 word threshold conflicts, the T1 word takes precedence |
| 4 | Cognitive verbs | Realize, discover, understand, feel, feel, think | Replace with external action or direct perception description; key emotional nodes can be used briefly (≤2 times/chapter, see narrative-rules.md rule 2), and the rest will not be compromised | When the number of words is not enough, "he feels" cannot be retained to save word count |
| 5 | Senses/X | It is recommended to have ≤2 types per scene, and can be up to 3 types; I checked the structure | Sound clues are not counted if they are red line key information. Other senses are streamlined when they are suprathreshold. X can be retained if there is a rhythm function | When the sensory quota is full but the red line requires sound description, the sound exception will not occupy the quota. |
| 6 (minimum) | Writing standards | All other writing standards and technical guidelines (including narrative rules, basic iron rules) | Automatic concessions when conflicting with items 1-5 above | When the narrative rules require "short sentences for dialogue" and the word count requirement conflict, the word count takes precedence |

### Scenario exception (inherited from the original rule priority, the priority is not higher than the above ruling table)

The above six levels of priority always take precedence. On the premise that priorities
are met, the following scenarios can be executed leniently:

- **Dense dialogue paragraphs**: The rules for dialogue tags are relaxed (moderate
  adverb modifications are allowed), the paragraph length rules are suspended, and the
  sentence threshold is relaxed (the naturalness of the dialogue is prioritized)
- **Climax Conflict Paragraph**: The fatigue word threshold is relaxed (moderate
  emotional direct expression is allowed), the sentence structure constraints are
  relaxed (dashes/negative sentence structures are not included in the threshold), and
  the paragraph can be relaxed to ≤2000 words
- **Minimalist white paragraphs**: The threshold for tired words is relaxed (deliberate
  repetition is allowed to create rhythm), paragraphs can be relaxed to ≤150 words, and
  the proportion of single paragraphs is not limited

The rest of the daily narrative and emotional foreshadowing sections - all rules are
strictly followed.

---

## [Conflict Determination] Check Item 1, Word Count Check

**Positioning:** Check whether the number of main words meets the target word number of
the chapter memo (±10%), and whether the compression strategy is implemented according
to priority. This check verifies whether the compression strategy injected by
prompt-crafter is correctly executed by the writer.

**Check steps:**
1. Statistics of the total number of words in the text
2. If it is within ±10% of the target word count of the chapter outline memo → ✅ Passed
3. If the upper limit is exceeded (> target ×1.1) → Check the execution of the
   compression strategy:
   - Have low-weight scenes (especially the transition section of scene 1/2) been
     streamlined?
   - Are non-core passages of medium-weight scenes condensed?
   - Are the core conflict passages of high-weight scenes retained?
   - Are plot redlines preserved? If deleted → ❌
4. If it is lower than the lower limit (< target ×0.9) → Check whether there are missing
   scene details:
   - Have high-weighted scenes been sufficiently detailed?
   - Is the emotional turning point in place?
   - Was the redline content accidentally deleted for compression?

**Judgment:**
| Situation | Judgment |
|------|------|
| The word count reaches the standard (outline memo target ±10%) | ✅ |
| The word count exceeds the limit but the compression strategy is executed correctly (low weight has been compressed, red lines are not deleted) | ⚠️ The word count exceeds the limit, it is recommended to further compress low-weight scenarios |
| The word count exceeds the limit and the redline content is deleted | ❌ Priority 1 is violated, the redline content needs to be restored and low-weighted scenes need to be recompressed |
| The number of words is insufficient and high-weight scenes are full of details | ⚠️ The number of words is insufficient, it is recommended to check whether there are missing scenes |
| Insufficient word count and sloppy high-weighted scenes | ❌ Need to add details of high-weighted scenes |

**Root cause tracing:** Word count problem → Check whether the prompt task instructions
and the compression strategy of the target word number field are clear → Check whether
the writer operates according to the strategy when executing.

---

## [Conflict Determination] Inspection Item 2,Sensory Inspection

**Positioning:** Check whether the number of sensory refinements per scene is reasonable
(recommended ≤ 2 types, up to 3 types), and whether sound exceptions are used correctly.
This check verifies whether the sensory layering strategy injected by prompt-crafter is
correctly implemented by the writer.

**Check steps:**
1. Scene-by-scene statistics of detailed sensory categories (which of the senses of
   vision, hearing, smell, touch, and taste are detailed descriptions)
2. If ≤ 2 types per scene → ✅ Passed
3. If a scene > 2 types → check if there are sound exceptions:
   - Are the extra senses considered sound cues (auditory detailed description)?
   - Is this sound clue key to the chapter's plot line (gunshot = battle signal,
     footsteps = danger sign, etc.)?
   - Yes → Allow not counting, marked 🎵 Sound exceptions
   - No → ❌ Sensory overload, need to be streamlined
4. If there are audio cues in the scene but are kept only as brief sketches:
   - Confirm whether it is red line key information (not environmental decoration sound
     such as "bird chirping")
   - Make sure it is a "short description" (no more than 1-2 sentences) rather than a
     long description of the environment

**Judgment:**
| Situation | Judgment |
|------|------|
| ≤ 2 sensory refinements per scene | ✅ |
| Exceed but all legal sound exceptions (red line key sounds + short white description) | ✅ and mark 🎵 Exceptions in the report |
| Exceeds and has non-exceptional senses (decorative ambient sounds, redundant touch, etc.) | ❌ Need to be streamlined to ≤2 types, with priority to retain red line related senses |

**Ambiguous coverage example:**
| Scene | Sound type | Exception | Reason |
|------|---------|-----------|------|
| Battle / gunshots | "Gunshots fired" 1 sentence line drawing | ✅ Exceptions | Red line key information (combat trigger sign) |
| Environment / Birdsong | "There are birds chirping outside the window" in 1 sentence | ❌ Not an exception, counted in the sensory quota | Environmental decoration sound, not red line information |
| Pursuit / Footsteps are approaching | "Footsteps are getting closer and closer" 2 sentences | ✅ Exceptions | Red line key information (pursuit danger upgrade) |
| Everyday hawking in the distance | "The sound of hawking from a distance is heard" 3 sentences | ❌ Not an exception, counted in the sensory quota | The realism of the environment, not the red line of the plot |

**Root cause tracing:** Sensory exceedance → Check whether prompt writing methodology /
sensory hierarchical selection has injected sound exceptions → Check whether exception
conditions are abused during writer execution.

---

## [Conflict Determination] Check Item 3 - Priority Execution Consistency

**Positioning:** Check whether there are violations of the priority hierarchy in the
text - low-priority rules override high-priority rules.

**Check steps:**
1. Scan the text for all paragraphs that exhibit "rule violations" (a rule is followed
   but a higher-priority rule is violated)
2. Confirm whether the conflict direction is consistent with the priority table

**Ambiguous coverage example (how to determine when the rule boundary is not clear):**
| Conflict Scenario | Phenomenon | Global Ruling Table Ruling | Correct Practice |
|---------|------|---------------|---------|
| Number of words vs senses | The number of words is not enough, so I refined the senses to only 1 type | Word count priority 2 > Sensory priority 5 | ✅ Correct. The word count is higher than the senses, and the senses are streamlined |
| Word Count vs Red Line | The word count exceeded, and a section of the red line plot was deleted | Red Line Priority 1 > Word Count Priority 2 | ❌ Error. Any time redline > word count. Low weight scenes should be compressed |
| Sound exception vs. senses | The scene has 3 sensory refinements: vision + touch + hearing (sound exception declaration) | Sound exception needs to meet: red line key information + short white description | Check whether the sound is red line information. Yes→✅Exception established; No→❌Sensory limit |
| Writing standards vs red lines | Writing standards require "short sentences for dialogue", but red line paragraphs require long sentences to convey information | Red line priority 1 > Writing standards priority 6 | ✅ Correct. Redline paragraphs can break the limits of writing standards |
| T1 words vs writing standards | The T1 word "suddenly" appears 3 times in the redline paragraph, and the writing standards require all replacements | T1 words should be used more broadly in the redline paragraph (retaining the rhythm function) | ✅ Correct. T1 words in redline paragraphs can be retained |
| Cognitive verbs vs word count | Replacing cognitive verbs will increase the word count, resulting in an overrun | Cognitive verb priority 4 > Word count priority 2 | ❌ Error. Cognitive verbs must be replaced (except for key emotional nodes ≤2 times/chapter), and the word count is controlled by compressing low-weight scenes |

**Root cause tracing:** Priority execution exception → Check whether the constraint red
line of prompt declares the highest priority → Check whether there are old statements in
the prompt writing specification that are inconsistent with the global ruling.

---

## 1. AI taste detection-fatigue words

The word fatigue itself is not a wrong word, but when certain words appear frequently
(more than 3 times) in a chapter, they form "AI accent". Thresholds and alternative
policies are listed below by category.

### 1. Adverb class

> **Threshold source:** The following fatigue word thresholds are based on
> `common-rules.md` (suddenly/suddenly/suddenly 4 times/chapter,
> unexpectedly/unexpectedly 3 times/chapter, the red line paragraph is wider). This
> table only retains alternative strategies.

| Fatigue Words | Single Chapter Threshold | Alternative Strategies |
|--------|---------|---------|
| Sudden, sudden | See common-rules.md | Most "sudden" is redundant - the unexpectedness of the event itself already conveys "sudden". Delete "suddenly" and write the event directly |
| As expected, unexpectedly | See common-rules.md | Let the readers judge "actually" by themselves, don't be surprised for the readers. Delete "even", the fact itself is surprising enough |
| Momo, Weiwei | See common-rules.md (T1 context-sensitive category, if it is not in the vocabulary, it will be treated as T1) | Replace with specific actions. "Stand up silently" → "He stood up, the legs of his chair scraping the ground, his voice softer than usual" |
| Gradually, gradually | 2 times | Delete the adverb and use changing details to reflect gradualness. "The sky is getting dark" → "The shadow of the sycamore tree outside the window climbed from the ground to the wall" |
| Still, still | 2 times | Replace with status description. "He's still sitting there" → "His posture is exactly the same as an hour ago" |

### 2. Verb class

| Fatigue Words | Single Chapter Threshold | Alternative Strategies |
|--------|---------|---------|
| Show (smile/expression) | 3 times | "Show a smile" → Write the specific way to smile. "She smiled" or "The corners of her mouth moved" |
| Remind (memory/corner of mouth) | 2 times | Write the specific thing that triggered the memory, not the action of "reminding" |
| Emerge (ripples/warmth/sourness) | 2 times | Replace with physical feelings. "He felt warm in his heart" → "He pushed the bowl of porridge back and added another spoonful of sugar" |
| Emergence (picture/memory) | 2 times | Directly write the memory content or trigger details, without writing the intermediate layer of "emergence" |
| Fall into (silence/contemplation/memory) | 2 times | Write about the specific behavior or state after silence |
| Welling (emotion/memory) | 2 times | Replace with physical reaction. "A surge of anger" → "His fingers dug hard into his palms" |
| Flooded | 1 time | Can almost always be deleted or replaced with a specific description |

### 3. Adjective/abstract part of speech

| Fatigue Words | Single Chapter Threshold | Alternative Strategies |
|--------|---------|---------|
| Complex, subtle | 3 times each | Write specific contradictions. "Mixed emotions" → Write about the simultaneous existence of two opposing impulses |
| Indescribable, inexplicable | 1 time each | Since it is "indescribable", don't use this word to escape - write the specific expression of that indescribable thing |
| Strange and strong | 2 times each | Write down the specific differences and what is strong |

### 4. Connect parts of speech

| Fatigue Words | Single Chapter Threshold | Alternative Strategies |
|--------|---------|---------|
| However, however | 4 times | Most transitions do not require "however" - the content of the preceding and following sentences is the transition itself. Remove the connectives and let the sentences collide directly |
| So | 3 times | "So" is the conditioned reflex of LLM - two things before and after have cause and effect, and "So" is the extra glue. Cause and effect becomes more natural after deletion |
| Immediately, immediately afterwards | 2 times | Delete. The natural sequence of actions does not require temporal adverb annotation |
| Meanwhile | 1 time | "At the same time" = I can't write transitions. Directly use the scene at the beginning of the new scene to transition |

### 5. Physical reaction category (fatigue template)

| Fatigue Words | Single Chapter Threshold | Alternative Strategies |
|--------|---------|---------|
| Pupils shrink and body freezes | 2 times | These two are LLM's most stubborn habits - fear causes pupils to shrink, and shock causes body to freeze. Let’s put it into a specific scenario: Fear can be that your hands are shaking so much that you can’t press the lighter, shock can be that you forgot to hold the cup when it fell over |
| Take a breath | 1 time | The frequency of online articles is too high, and readers have become numb. Change to specific breathing changes or other body responses |
| Stagnation of breathing | 1 time | Same as above - a physiological response that has been overused |

### 6. Metanarrative and academic accent

| Fatigue words/sentence patterns | Treatment methods |
|-------------|---------|
| This chapter tells, next, in this chapter, the story continues | **Delete all**. These are positioning sentences in the chapter outline and are copied into the text by the subagent. The fastest AI flavor detection: "This chapter", "next chapter", "story" and "reader" are not allowed in the text |
| To sum up, in summary, in a sense, undeniable, obvious | Delete. The text is not an argumentative essay |
| Seem, maybe, probably, as if | See common-rules.md (3 times/500 words). Replace vague words with definite descriptions - not "He seemed angry", but "He put out his cigarette and rubbed his fingers three times" |

### 7. High-risk fatigue words in English

English themes (LitRPG / Progression Fantasy, etc.) Extra checks: `delve` / `tapestry` /
`testament` / `embodiment` / `harbinger` / `veritable` / `inexorable` / `nonetheless` /
`furthermore` / `however` / `seemed to` / `as if`. You can skip this item for Chinese
themes.

### Fatigue word scanning method

1. Paste the text into a plain text editor
2. Ctrl+F Search the above fatigue words one by one
3. Record line number for each hit
4. Total times by category
5. Words that exceed the threshold → replace one by one (not deleted in batches - each
   word must be judged whether it has narrative function)

---

## 2. AI flavor detection - sentence pattern violations

8 structural sentence quirks and 6 sentence rules. Item-by-item scanning,
super-threshold flagging.

### 1. Structural sentence patterns (8 types)

Refer to the definition of `tic-patterns.yaml`. Each mode has a single chapter
threshold, exceeding which triggers a warning.

#### 1.1 "It's not...but" sentence pattern

```
Single chapter threshold: 3 times | Severity: high
Instructions: Check the contrastive structure of "not...but" in the text. The narrative function is retained (distinguish between representation and motivation), but the negative clauses without narrative function are directly deleted.
```

#### 1.2 "No...just/only" sentence pattern

```
Single chapter threshold: 3 times | Severity: medium
Description: Variation of "not but". When the threshold is exceeded, the "without" clause is deleted and the content after "just" is retained.
```

#### 1.3 Negation-Correction Sentence Pattern

```
Single chapter threshold: 2 times | Severity: high
Hit Pattern: "No, that's not it" "It's not that" "More accurately"
Explanation: The narrative function is retained (the character discovers the facts in two steps), but the negative clauses without narrative function are deleted.
```

#### 1.4 Dashes explain sentence patterns

> **Threshold reference common-rules.md:** Dashes are determined by usage (allow
> pauses/pacing, dialogue interruptions; remove punctual redundancy), and there is no
> number line. This item is only a diagnostic tip - if there are too many dashes
> followed by pronoun expansion explanations ("--he/she/it/this/that"), it means that
> it has fallen into indirect redundancy and will be handled according to the
> common-rules.md usage judgment. Judgment principle: If you delete the dash and the
> content on both sides, will the meaning become blurred? If not, delete it.

#### 1.5 Formulaic adverbs

> **Threshold reference common-rules.md:** Formulaic adverbs are processed as soon as
> they appear in T1 (common-rules.md is the most poisonous sentence
> pattern/first-level banned word level), and there is no loose threshold. This item
> is for diagnostic purposes only.

```
Hit mode: "can't help it", "can't help it", "can't help it", "involuntarily", "subconsciously", "by some strange coincidence"
Instructions: Delete the adverb and let the action speak for itself. "He couldn't help but take a step back" → "He took a step back".
```

#### 1.6 "On one side... on the other side" sentence pattern

```
Single chapter threshold: 2 times | Severity: medium
Note: When the threshold is exceeded, split it into independent actions or highlight a main action. Within 2 times and the narrative function is retained.
```

#### 1.7 "At this moment/at this moment/suddenly" sentence pattern

```
Single chapter threshold: 5 times | Severity: medium

This is a common transition technique with a high threshold, but it appears more than 2 times every 500 words to expose the sense of template.
Fix: Delete transition words and write events directly. "Just then, the door opened" → "The door opened."
```

#### 1.8 Body Part Emotion Template

```
Single chapter threshold: 6 times | Severity: high
Hit pattern: "eyes/eyes/pupils/heart/heart/heart/bottom of heart/palms/fingertips/throat" + "a/slight/dark/heavy/tight/trembling/trembling/shrinking/warm/cold/cool/hot/sour"
Explanation: Emotions are externalized with specific actions, without formulas. "My heart felt warm" → "She put an extra piece of meat into his bowl".
```

### 2. Other sentence rules

#### 2.1 Beginning with "With"

"As the footsteps approached, his heartbeat accelerated." → "As the footsteps
approached. His heartbeat accelerated." Delete "as", split the two things into two
sentences, and the cause and effect will appear.

#### 2.2 "Let/order/make" sentence pattern

"This scene reminded him of yesterday" → "He remembered yesterday." Delete "let" and let
the subject act directly. "Let" means that the author is controlling the character, and
the character will act on its own.

#### 2.3 "Dang" sentence pattern

"When he walked into the room, everyone looked at him" → "When he walked into the room.
Everyone looked at him." Delete "when..." and turn the clause into an independent action
sentence.

#### 2.4 Abuse of "LE"

| Rules | Thresholds |
|------|------|
| The number of "LE" in each paragraph | ≤ 3 |

Overuse: ↓
> "He put down the cup, walked to the window, opened the window, looked at the street
> outside, and then sighed." ← 5 "了" in a row

Repair: Delete half of the "er" and replace it with a short sentence - "He put down the
cup. The bottom of the cup hit the table. He got up and walked to the window."

#### 2.5 Perceptual word masking

```
Rule: "see/hear/smell/feel" followed by an abstract description = perception word masking. Delete the sensory words and write sensory content directly.
Example: "He saw that the room was in a mess" → "The room was in a mess"
```

#### 2.6 Continuous with the same structure at the beginning

```
Rule: Avoid more than 5 sentences in a row starting with the same subject or conjunction
Key points to check: he/she/at this time/then/then/so/then/just/but/but
Repair: Change the subject or sentence structure - "He walked to the window. He looked outside." → "It was quiet outside the window. When he turned around, his knees hit the coffee table."
```

### Sentence scanning method

Unlike fatigue words, you can Ctrl+F (some of them can) for sentence violation.
Suggestions:

1. Print the text or change the font to read (changing the font can break
   desensitization)
2. Use a pen to mark the beginning of the sentence paragraph by paragraph (circle 5
   consecutive sentences with the same subject)
3. Search regular rules: `不是.*(而是|是)`, `没有.*(只是|而是)`, `不由得|不禁|忍不住|不由自主|下意识`
4. "了" scan: The number of "了" in each paragraph exceeds 3 marks

> **Scenario exceptions:** Sentence thresholds for intensive dialogue sections and
> climactic conflict sections are relaxed (dash/negative sentence patterns are not
> counted in the single chapter threshold, and priority is given to ensuring the
> naturalness of dialogue and emotional tension). See the top Global Conflict
> Determination Table / Scenario Exceptions for details.

---

## 3. AI flavor detection - duplicate content

Large repetitions are a common problem with AI generation. Detection is divided into 5
categories:

### 3.1 Repetition at the beginning of a paragraph

```
Rule: Avoid 4 consecutive paragraphs starting with the same subject/scene word
Detection: Extract the first 5 words of the first sentence of each paragraph and search for 4 consecutive identical patterns
Repair: Change the subject at the beginning of the paragraph (he → her → outside the window → transition → start with an action)
```

### 3.2 Sentence repetition

```
Rule: Avoid 6 sentences in a row with the same sentence pattern
Detection: Statistical sentence structure (declarative sentence/short sentence/dialogue/exclamation sentence), 6 consecutive tags of the same type
Repair: statement → short sentence → dialogue appears alternately
```

### 3.3 Duplication of description objects

```
Rules: It is prohibited to describe different attributes of the same item/person in two consecutive paragraphs.
Detection: Extract the core object described in each paragraph, and the same object mark appears in 2 consecutive paragraphs
Repair: Change the scene to an object, or use actions instead of descriptions
```

### 3.4 Repetition of emotional words

```
Rules: Nervous/happy/sad/angry/fearful and other emotional words should be used ≤3 times in a single chapter
Detection: Emotional word list search, super-threshold tagging
Fix: Use physical reactions/actions instead of direct emotional words
```

### 3.5 Image/metaphor repetition

```
Rules: Used metaphors/imagery are no longer used in this chapter
Detection: Record the metaphors that appear in the text, and repeat the marks
Fix: Updated sensory descriptions
```

**Scan method:**
1. Beginning of paragraph: Extract the first 5 words of each paragraph and search for 4
   consecutive same prefixes
2. Sentence pattern: separate sentences according to periods, count the proportion of
   sentence patterns, 5 consecutive marks of the same type
3. Description object: extract the core nouns of each paragraph, and mark the same noun
   in 2 consecutive paragraphs
4. Emotional words: Search for emotional words such as "nervous, happy, sad, angry,
   scared, excited, excited, disappointed"
5. Imagery: record figurative sentences (such as "like X", "like X"), repeated
   occurrence of marks

---

## 3. Dialogue rules

### 1. Conversation tags

```
Rules: Dialogue tags are mainly "say/dao/ask", accounting for more than 80%; adverbs are prohibited from modifying dialogue tags
Example: "Lu Zheng said seriously" → "Lu Zheng said. Fang Yan stopped in front of the cabinet, his hand hanging in the air"
```

### 2. Conversation interval

```
Rules: There must be action/environment/inner activities as rhythm intervals between dialogues, 8 consecutive sentences of pure dialogue = violation
Exception: Threshold for dialogue-heavy passages (paragraphs deliberately advanced with dialogue) is relaxed to 12 sentences
Evaluation: When distilled, the proportion of dialogues rendered by prompt words (dialogue_pct) is evaluated first, rather than the number of hard-coded sentences.
```

### 3. Exclamation marks and ellipses

```
Rules: Do not use "!" instead of emotional description; maximum 1 exclamation point per paragraph
```

### 4. Instructional dialogue

```
Rules: Characters cannot tell each other known information. Check to see if there are characters in the text who are filling in the background for the reader.
```

### 5. Dialogue intention

```
Rules: Every conversation has at least one intention - to persuade, to test, to hide, to refuse, to change the subject, to obtain information, to apply pressure

Unintentional dialogue (small talk, greetings) = filler, should be deleted or changed to narrative
```

> **Scenario exceptions:** Dialogue labeling rules for dense dialogue segments are
> relaxed (moderate adverb modification is allowed), and the continuous pure dialogue
> threshold is relaxed to 12 sentences. See the top Global Conflict Determination
> Table / Scenario Exceptions for details.

---

## 4. Set compliance verification

**Reference Baseline:** `settings/world-setting.md`, character design documents, genre
rules (genre-taboos)

**Judgment Rules:** Any violation → §5 is disqualified. All items passed → ✅. Violations
need to be marked with root causes (missing setting reference/prompt not injected/seed
missing).

### 1. Observe worldview rules
- Ability Boundary: The character's cultivation/magic/technological abilities do not
  exceed the set range
- Rule consistency: the basic rules of the world (social hierarchy, physical laws, power
  systems) are not violated
- Time and space logic: geography, timeline and setting are consistent, no contradiction

### 2. Role consistency (OOC detection)
- Core character: The character performance in this chapter is consistent with the
  character (introvert will not suddenly take the initiative to strike up a
  conversation). Violation ≥ 1 → ❌
- Ability Boundaries: The character does not do anything beyond the set capabilities.
  Violation ≥ 1 → ❌
- Knowledge Boundary: The character does not say/know information that he or she cannot
  possibly know. Violation ≥ 1 → ❌
- Relationship status: The relationship between the characters is consistent with the
  personality. Violation ≥ 1 → ❌

### 3. Taboo subject matter
Check the taboos list one by one. 1 offense → ❌

### 4. Information continuity
- Objects/buildings that were destroyed in the previous chapter were not restored
  without reason. Contradiction ≥ 1 → ❌
- The character status at the end of the previous chapter connects well with this
  chapter. Contradiction ≥ 1 → ❌

### 5. Set version alignment (additional to novels)
Exclusively for novels. When a new setting element is introduced in the body section,
check for version consistency with setting-change-log.md:
- The newly introduced organization/location/ability names and characteristics do not
  conflict with existing settings. Conflict → ❌
- The settings that have been changed in this volume will not be described in the old
  version in subsequent chapters. Drift → ❌
- Significant setting deviations are documented in setting-change-log.md. Should be
  filed but not filed → ❌

---

## 5. Verification of Chapter Outline Fulfillment

Did the main text of the chapter achieve what the memo promised?

### 1. required_changes Check Item by Item

`required_changes` of the chapter outline memo is the core commitment of this chapter.
After writing the main text, go through it one by one:

| Check items | Methods |
|--------|------|
| Did each "what became what" actually happen in the text? | Find the corresponding paragraph in the text. Can't find = not honored |
| Does the changed type match? | The outline of the chapter is about "information changes", and the main text cannot just be "He knows a lot" |
| Can readers feel the change? | It’s not the author who knows what’s changed - it’s what’s written on paper that lets readers know what’s changed |

```
Rules: required_changes Each item must have a corresponding body paragraph and cannot be included in a summary sentence. Find specific passages in the text to confirm fulfillment.
```

### 2. Check payoff_plan item by item

| Check items | Methods |
|--------|------|
| must_resolve Is every hook resolved in the text? | Find the specific passage that concludes. Not found = missing |
| must_hold each hook is not accidentally leaked? | The text does not disclose suppressed information |
| partial_advance Is each hook advanced in place? | Compare the advance description of the chapter outline with the degree of advancement of the main text - insufficient advancement or excessive advancement are deviations |

### 3. micro_payoffs Redemption

At least 1 of the chapter's micro_payoffs must be honored. Confirm in the text:
- Fulfilled: There is a specific scene (not a narrative summary) in the right place, and
  the reader can perceive "something gained"
- Unfulfilled: only mentioned in one sentence or the corresponding position cannot be
  found in the text → ❌

### 4. key_choices Redemption

Chapter outline key_choices ≥ 1 No corresponding paragraph found in the text (including
motivation inconsistent with the chapter outline) → ❌

### 5. Prohibitions Not Violated

Check the prohibitions one by one to confirm that the text does not violate them. If
there is any violation → modify it immediately.

---

## 6. Hook redemption check

Hook management is not in settings/foreshadowing.md - the source of truth is in the
hooks field of each chapter's chapter.md and memo.payoff_plan (foreshadowing.md is only
for cross-volume foreshadowing). Confirm during text check:

- [ ] **The new hook in this chapter** does appear in the main text (there is a specific
      scene, not a hint) → No scene ❌
- [ ] **The closing hook of this chapter** The closed loop is completed in the main text
      (there is a complete paragraph, the reader will not miss it) → The closed loop
      paragraph cannot be found ❌
- [ ] **payoff_plan is not missing**, It is listed but the corresponding content cannot
      be found in the text → ❌
- [ ] **Long foreshadowing and hook closing are important**: Foreshadowing ≥ 2 chapters,
      the number of words for hook closing is ≥ 100 words and there are specific scenes
      → ❌ Only one sentence or only inner monologue
- [ ] **Missing foreshadowing across volumes (additional to full-length novel)**: Scan
      foreshadowing.md for active foreshadowing from previous volumes to confirm that
      this chapter has not forgotten to mention old foreshadowing that should be
      advanced → Foreshadowing from previous volumes can be mentioned in this chapter
      but not touched ❌

---

## 7. Reading experience verification

**Reference Baseline:** Chapter outline satisfying payoff design, emotion curve, hook
planning

**Judgment Rules:** ≥ 2 out of 3 items in each section are passed → this section ✅. ≥ 3
out of 4 sessions ✅ → §8 ✅.

### 1. The implementation of satisfying payoff
- [ ] There are specific implementation scenarios (non-general description) → only
      summary without scenarios ❌
- [ ] Emotional release is consistent with the positioning of the chapter → deviation ❌
- [ ] Readers can feel the satisfying payoff (not "I wrote it but didn't feel it") →
      There is no sense of satisfaction after reading ❌

### 2. Emotion curve matching
- [ ] The three paragraphs of Decrease→Ascending→Conclusion are aligned with the outline
      of the chapter (the depressing paragraphs are not written too loosely)
- [ ] The emotions at the turning points are well rendered (be nervous when you should
      be nervous, be warm when you should be warm)
- [ ] No unexpected deviations (the "depressive ending" in the chapter outline was not
      written as "sunny ending") → deviations ❌

### 3. End-of-chapter traction
- [ ] There is an emotional gap (unresolved/unclarified/unclosed threads) → all the
      threads are closed ❌
- [ ] There is no "safe landing" (all conflicts are perfectly resolved within this
      chapter)
- [ ] Readers will have a feeling of "What next?" after reading → There will be no
      suspense after reading ❌

### 4. Sense of gain from reading
Readers get at least one:
- New information (plot advancement)
- Emotional experience (laughing/nervous/touched)
- Relationship progress (changes or changes in role relationships)

---

## 8. Technical quality

### 1. Consistent perspective

```
Rules: Use a single perspective throughout the chapter (unless the chapter outline indicates dual perspective)
Detection: The third-person limited perspective can only write about what the perspective character sees and hears, but cannot jump into other people's hearts. Search for cross-perspective signal words such as "thinking", "he/she realizes", "he/she feels", etc.
```

### 2. Tense/person agreement

```
Rules: The tense and person should be consistent throughout the chapter. You cannot jump back and forth within the same scene.
```

### 3. Paragraph length

```
Rules:
- It is recommended that a single paragraph should be ≤ 250 words (the climax section can be relaxed), ≥ 20 words (except for single paragraphs)
- The recommended proportion of a single segment is 15%-35%, used for rhythm emphasis
- It is recommended to consider splitting if there are more than 4 commas, but it is not mandatory.
```
> **Scenario exceptions:** Climactic conflict paragraph ≤ 2000 words; rules for dense
> dialogue paragraphs are suspended; minimalist white description paragraphs ≤ 150
> words and the proportion of single sentences is not limited. See the top Global
> Conflict Determination Table / Scenario Exceptions for details.

---

## 9. Content quality

### 1. God’s perspective summary and meta-narrative

```
Rules: Meta-narrative statements such as "this chapter tells it", "the story continues", "in this chapter", etc. are not allowed in the text; no voice-over summary comments are allowed
Detection: Search for meta-narrative signal words such as "this chapter", "story", and "reader". ≥ 1 place → ❌
```

### 2. Define reader responses

```
Rule: The text should not tell the reader how to feel. It is forbidden to "make people feel", "cannot help", "readers see this..."
Detection: Search for preset signal words such as "人人", "人人", and "reader". ≥ 1 place → ❌
```

### 3. No inclusion of non-text content

Check for content that should not be in the text (≥ 1 → ❌):
- [ ] Introduction ("Start writing the text below" "Chapter X officially begins")
- [ ] Summary at the end of the article ("The above is the content of Chapter X" "This
      chapter is mainly written")
- [ ] Bracket comments ("(This can be written better)""(This paragraph can be deleted)")
- [ ] Subagent's self-evaluation ("I think this description is good" "This echoes the
      previous one")

### 4. Information is accurate

- [ ] The character names must be spelled the same (Lu Zheng/Lu Zheng/Lu Zheng cannot be
      mixed)
- [ ] The timeline is not inconsistent (the "one week ago" mentioned yesterday cannot
      become "three days ago" today)
- [ ] **story_date Continuity (Novel Plus)**: This chapter `story_date` is reasonably
      spaced from the previous chapter (no jump breaks or time lapses). Tracked in
      timeline.md → No records ❌
- [ ] The status of the items is not inconsistent (the broken vase in the previous
      chapter cannot be left intact on the table in this chapter)
- [ ] The relationship between the characters is not contradictory ("first meeting" in
      the previous chapter cannot be "met many years ago" in this chapter - unless this
      is a well-designed foreshadowing)

---

## 10. Style consistency

### 1. Align with writing style

Compare the four fields of `.claude/knowledge/writing-style.md`:

| Field | Judgment Criteria |
|------|---------|
| Narrative identity | The text reflects the writing identity. Identity=Restraint from long and sensational paragraphs in line drawing → ❌ |
| Hard constraints | Check item by item. Violation ≥ 1 → ❌ |
| AI is prone to mistakes | Check each item one by one. Hit ≥ 1 → Mark modified, 3+ → ❌ |
| Levels and techniques of description | At least 1 recommended technique can be identified in the text |

### 2. The flavor of the subject matter

If the project is configured with `genre-setting.md`, check whether the text conveys the
core flavor of the theme:
- At least 1 item of the core flavor of the subject matter can be perceived
  (corresponding from "The driving force to know the truth/Details of the power
  system/Daily reality/Avoiding modern time travel")
- Taboos (genre_taboos): 0 violated

**Judgment:** Core taste 0 items → ❌; Taboo ≥ 1 violation → ❌

### 3. Rhythm of writing

- [ ] Narrative segment/scenario segment alternation. 1000 words in a row without
      dialogue ∪ 500 words in a row with dialogue → ❌
- [ ] Strong mood swings: at least 1 alternation of strong and weak emotions in the same
      chapter. High energy throughout or calm throughout → ❌
- [ ] The highest emotional point is not at the end of the chapter (the climax is around
      1/4 before the end of the chapter, and the end of the chapter is the hook)

---

## General form of text acceptance (7 items)

### L1 surface text
- [ ] **Fatigue words**, each of the six categories does not exceed the threshold (see §
      1 for details)
- [ ] **Sentence pattern violation**, All sentence pattern rules do not trigger warnings
      (see §2 for details)
- [ ] **Duplicate content**, The beginning of the paragraph/sentence structure/object of
      description/emotional words/imagery do not exceed the threshold (see §3 for
      details)
- [ ] **Dialogue Rules**, Tags/intervals/intentions/exclamation points are all compliant
      (see §4 for details)

### L2 content compliance
- [ ] **Setting Compliance**, Worldview/OOC/Taboo/Continuity All passed (see §5 for
      details)
- [ ] **Chapter Outline Cashing**, required_changes/payoff/prohibitions All cashing out
      (see §6 for details)
- [ ] **Hook cashing**, New burial/contraction/weight are all in place (see § 7 for
      details)

### L3 + base quality
- [ ] **Reading retention**, satisfying payoff + curve + end-of-chapter traction + sense
      of gain Total ≥ 3 sub-items passed (see §8 for details)
- [ ] **Basic Quality**, Perspective/Tense/Paragraph/Content Quality/Style/Word Count
      are all qualified (see §9~§11 for details)

---

### Execution method

**Priority: Agent Teams > subAgent > Self-Test**

1. **Agent Teams (optimal)**: Open an independent reviewer agent and pass in the text of
   this chapter + this chapter's outline (chapter.md) +
   `.claude/knowledge/writing-style.md` + `anti-ai.md` (if it exists) + this list. The
   reviewer agent checks each item item by item and gives "pass/fail + evidence (quote
   from the original text)" for each item. The agent automatically performs fatigue word
   scanning and sentence pattern scanning (regular matching), while manual verification
   only takes place.
2. **subAgent (suboptimal)**: Same as above, using a subagent to perform the review. The
   subagent's judgment of "content quality" and "style consistency" is weaker than that
   of the complete agent. It is recommended to use a subagent for AI flavor detection
   (fatigued word/sentence rules), and the content quality part should be handled by the
   agent himself.
3. **Main Agent self-inspection (double check)**: Strictly follow this list item by
   item. Pay special attention to three high-risk blind spots:
   - **Fatigue word desensitization**: The main agent has just finished reading the
     generated text and has been desensitized to fatigue words. It does not rely on the
     "feeling of reading" - you must run a keyword search and check the threshold word
     by word.
   - **memo Commitment Self-deception**: It is easiest to say to yourself "Although it
     is not written explicitly, it is implied." The check method is: point to a specific
     paragraph in the text and answer "Which promise of the chapter outline does this
     sentence fulfill?" If you can't point it out, you haven't fulfilled it.
   - **Dialogue rhythm blind spot**: A long continuous dialogue reads "quite quickly"
     but can easily be skipped and checked. Pure dialogue lines are extracted
     separately, with several action/environment descriptions interspersed in the
     number. 8 consecutive sentences of pure dialogue without gaps → mark.

**What to do after getting the conclusion:** The diagnosis result points to the problem
link - AI is heavy → check whether the constraints of prompt output and writing specs
are in place; memo is not fulfilled → check whether the seed core event is covered;
perspective jump → check the prompt perspective lock field. Regenerate after completing
the corresponding link. **But whether the final text is archived or not is determined by
the author, not by the list. **

---

## Acceptance report format

After the inspection is completed, a hierarchical report will be output in this format:

```markdown
## Text Acceptance Report: Chapter X

### General comments
✅ Passed / ⚠️ Conditionally passed / ❌ Needs modification

### Stratified results
| Tier | Pass Rate | Key Findings |
|------|--------|---------|
| L1 surface text (§1~§4) | n/4 | |
| L2 content compliance (§5~§7) | n/3 | |
| L3+Basic Quality (§8~§11) | n/2 | |

### Details of failed items
| Check items | Result | Text citation | Root cause tracing |
|--------|------|---------|---------|
| (item name) | ❌ | (original text paragraph) | output and writing specs / seed core events / chapter outline memo / setting reference |
| ... | ... | ... | ... |

### Handling suggestions
- ✅ All passed → Remove -draft archive
- ⚠️ Minor problem → Archive after targeted modifications
- ❌ Major problem → Repair the corresponding link and regenerate it
```
