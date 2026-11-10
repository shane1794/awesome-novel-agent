# Writing style guide

> Guide writers in determining their writing style,the four-field anchoring system.
> After selecting the theme, match the default values of the four fields from
> `.claude/knowledge/genre-example.md`. The author can customize on this basis to
> override the default.

---

## The highest principle: the four fields are anchored to each other and each one is indispensable.

The four fields are anchored to each other. If you change any one, you must check
whether the other three are still consistent.

```
Narrative identity─────Hard constraints
      │                       │
      │ Mutual anchoring │
      │                       │
AI is prone to making mistakes──Description levels and techniques
```

**The design sequence is irreversible:** First determine the narrative identity → then
determine the hard constraints (what this narrative identity cannot do) → then determine
the description level and technique (what technique is most natural for this narrative
identity) → finally determine the AI’s tendency to make mistakes (review known
pitfalls).

**Adjustment Rules:** The default is just Qidian. At least one field must be discussed
and adjusted - all are the same as default indicating that this style has not been
selected.

---

## Part 1: Settings - Define the four fields one by one

### 1. Narrative Identity: Defining Narrative Identity

One sentence is qualitative, including narrative distance (close to the character or
overlooking the overall situation) and narrative attitude (neutrality/sarcasm/empathy).

This sentence is enough: **"What do you want readers to feel like when reading? - Like
someone sitting next to you and talking calmly, like getting into the protagonist's head
and feeling everything, or like watching movie footage?"**

The author's answer directly determines the role positioning.

```
✅ Qualified:
Narrative Identity: A limited-perspective narrator who stays close to the protagonist's mind - the reader only knows what the protagonist knows and feels the emotions the protagonist feels.
→ One sentence determines the narrative distance (close to the character) and narrative attitude (empathy but limited).

❌ Unsatisfactory:
Narrative Identity: Write a good story.
→ Too general. Any narrator can say this, there is no distinction between styles.
```

**Judgment criteria:** Does the narrative identity answer both "how far away" and "what
attitude"? Missing one → return to make up.

---

### 2. Hard constraints: enforceable hard rules

Every principle must be able to describe "what it would be like to violate it." 3-5
items, each of which is checkable.

Let’s talk about this sentence: **"What are the things that must not be done in this
style? - Write whatever comes to mind. You don’t have to think about it all at once. You
can change it later."**

The author may list items that need processing:

| The author said | What was written |
|---------|--------|
| "Don't be too wordy" | Each paragraph should not exceed 4 sentences, and the continuous description should not exceed 3 paragraphs |
| "Don't write too AI" | Mental activities should not start with "he felt" or "he realized" |
| "Pace it faster" | Each question and answer should not exceed three rounds, otherwise the scene will be changed |

```
✅ Qualified:
"Suddenly", "suddenly" and "instantaneously" are subject to the common-rules.md threshold (4 times/chapter, the red line paragraph is wider).
→ It can be inspected - if it exceeds, it is a violation.

❌ Unsatisfactory:
Don’t write too artificially.
→ Unenforceable - What counts as "AI flavor"?
```

**Judgment Criteria:** Can each principle be included in automated inspections? Cannot →
Change to actionable description.

---

### 3. AI is prone to mistakes: specific anti-patterns

Each item corresponds to a specific writing method ("Mental activities do not start with
'he feels'"), not a general warning ("Don't write too AI").

```
✅ Qualified:
Excessive use of facial expressions ("He frowned" "The corners of her mouth turned up")

❌ Unsatisfactory:
Don’t write like an AI, write naturally.
→ What is nature? There is no way to check.
```

**Judgment Criteria:** If you show someone a common mistake made by AI, can they
immediately tell whether they made it when writing it? Cannot → Not specific enough.

---

### 4. Description levels and techniques: give practice

Each technique is actionable ("pick your nails when nervous"), not abstract advice
("write more about actions and less about emotions"). Each method has implementation
examples.

```
✅ Qualified:
The environment is filtered through the character's attention: when the character is anxious, what he sees is not the whole room, but exits, windows, and things that can be used as weapons.

❌ Unsatisfactory:
Use detailed descriptions.
→ What details? What scene is it used for? have no idea.
```

**Judgment Criteria:** After reading the technique, can you immediately rewrite an
existing text to apply it? Cannot → Not specific enough.

---

### Write to File

```yaml
Narrative identity: <One sentence, including narrative distance and narrative attitude>

Hard constraints:
  - <Executable Principle 1>
  - <Executable Principle 2>
  - <Executable Principle 3>

AI is prone to making mistakes:
  - <Specific anti-pattern 1>
  - <Specific anti-pattern 2>
  - <Specific anti-pattern 3>

Description levels and techniques:
  - <Operation method 1 (including cases)>
  - <Operation method 2 (including cases)>
  - <Operation method 3 (including cases)>
```

---

## Part 2: Acceptance,Four-field self-inspection

### Quick Check on Judgment Criteria

| Field | How to calculate enough | How to calculate not enough | How to fix |
|------|---------|-----------|---------|
| Narrative identity | After reading, you will know "what identity am I writing in" | "write a good story" | ask "how far is the distance and what is the attitude" |
| Hard constraints | Each contract can be checked for violation | "Don't write too AI" | Change to a specific anti-pattern |
| AI is prone to making mistakes | Each item corresponds to a specific writing method | "Be natural" | Give actual sentence comparisons |
| Levels and techniques of description | Can be used to rewrite immediately after reading | "Write more details" | Techniques for specific scenes |

### Self-check list

- [ ] Do all four fields have values?
- [ ] At least one field differs from the default value (style is selected)?
- [ ] Narrative identity answers both narrative distance and narrative attitude?
- [ ] Can each hard constraint be quantitatively checked?
- [ ] AI is prone to making mistakes. Each article is written in a specific way, not an
      abstract concept?
- [ ] Are there implementation instructions for each description level and technique?
- [ ] After changing one field, have other fields self-checked for consistency?

---

## Case

### Case 1: Calm Narrative (xianxiaxuanhuan)

```yaml
Narrative Identity: A calm but not cold narrator - objectively describing the character's actions and environment without feeling for the character.
  Let dialogue and action convey emotion, no psychoanalytic narration.

Hard constraints:
  - There must be a hook at the end of each chapter, not a straightforward ending
  - Don’t insert narration into the dialogue to explain the character’s emotions - let the reader judge from tone and word choice
  - Focus on dialogue, supplemented by description. Return to the dialogue as soon as possible after a narrative.
  - "Suddenly", "Suddenly" and "Instantly" are subject to common-rules.md thresholds (4 times/chapter, the red line paragraphs are wider)
  - Don’t write meaningless daily routines - every scene must have conflict or information advancement

AI is prone to making mistakes:
  - Excessive use of facial expressions ("He frowned" "The corners of her mouth turned up")
  - Mental activities begin with "he felt", "he realized" and "he thought"
  - The battle scenes are written in slow motion, one move at a time.
  - The description of the environment is separated from the plot in separate paragraphs.
  - Each paragraph begins with "he/she" more than 3 times in a row

Description levels and techniques:
  - Emotions are expressed through actions: picking nails when nervous, speaking softly when angry
  - Environmental awareness is integrated into the character's actions: It's not "the street is noisy", it's "he has to scream at the other end to hear him"
  - Dialogue uses differences in tone and wording to differentiate between characters,not relying on "he said" or "she said" labels
  - The passage of time is suggested by environmental changes: sunlight angle, shadow length, temperature changes
  - The battle uses results and consequences to describe the process: "When the sound stopped, his left arm was hanging unnaturally by his side."
```

### Case 2: Close to the heart of the character (urban superpower)

```yaml
Narrative Identity: A limited-perspective narrator who stays close to the protagonist's mind - the reader only knows what the protagonist knows and feels the emotions the protagonist feels.
  Occasionally use inner monologue to close the distance, but do not provide an overall explanation from God's perspective.

Hard constraints:
  - Each chapter maintains the inner perspective of the protagonist and does not cut into the minds of other characters.
  - The inner monologue is in the character's own language style, not written language.
  - The dialogue is fast-paced,no more than three rounds of questions and answers, otherwise the scene will be changed.
  - There should be no more than 2 declarative sentences ending with the word "LE" in each paragraph.
  - Use blank lines for scene transitions instead of "at the same time" or "on the other hand" transitions.

AI is prone to making mistakes:
  - Write the inner monologue as "He thought", "He realized", "He suddenly discovered"
  - The narrator summarizes the character's emotions ("He felt sad")
  - Use "seems", "as if", "as if" to weaken certainty
  - The description of the environment is written as a running account ("He walked into the room, which had tables, chairs and windows")
  - The inner drama of the character is too long, and the reader forgets where the scene is

Description levels and techniques:
  - The inner monologue removes the guide tag and directly enters the narrative flow: "This was not a good idea. But he opened the door anyway."
  - Emotions are expressed through physiological reactions: heartbeat, breathing, trembling hands, dry mouth - no need for the word "nervous"
  - The environment is filtered through the character's attention: when the character is anxious, what he sees is not the whole room, but exits, windows, and things that can be used as weapons.
  - Dialogue uses dislocation to create tension: the character's hands are shaking when he says "It's okay"
  - Time jump is expressed through body sense: "I don't know how long it has passed" "It feels like a lifetime has passed"
```
