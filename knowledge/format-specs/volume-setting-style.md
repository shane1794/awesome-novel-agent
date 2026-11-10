# Outline Setting Guide

> Phase 2 - Fill the selected volume with content. Including setting the direction,
> defining the core conflict, breaking down the chapter list, and adding new
> characters/settings. Outputs `chapters_summary` written to `volume-{N}.md`.

**Prerequisites:** story.md already has the story_arc positioning of this volume (which
step of the main line + one sentence of the core conflict). See
`.claude/knowledge/story-arc-style.md` - what is determined there is "which step in the
main line is this volume", and what is determined here is "how to go in this volume".

---

**Table of Contents**

- [Core Principles](#core-principle-the-outline-serves-the-writing-cycle)
- [1. Determining the volume direction](#1-determining-the-volume-direction)
- [2. Core Conflict](#2-core-conflict)
- [3. Emotional trend](#3-emotional-trend-the-emotional-arc-of-the-entire-volume)
- [4. Conflict Ladder](#4-conflict-ladder-the-escalation-of-conflict-layer-by-layer)
- [5. Information difference](#5-information-gap-the-engine-of-driving-force)
- [6. Scene card](#6-scene-card-scene-decomposition-of-chapters)
- [7. Chapter List](#7-chapter-list-chapters_summary)
- [8. New characters and settings added](#8-new-characters-and-settings-added)
- [Output Template](#output-template)
- [How each field is used downstream](#how-each-field-is-used-downstream)
- [Acceptance](#acceptance)

---

---

## Core Principle: The outline serves the writing cycle

> Before all the rules below, let me ask: **"With this outline, can I directly write
> out the direction proposal for each chapter?"**

The outline is not a summary for readers, not notes for authors - it is a directional
instruction for the writing cycle. Its only purpose is: when the Agent opens
`chapter-planner agent` and reads the chapters_summary of `volume-{N}.md`, it can
immediately deduce the plot direction proposal of this chapter.

**Judgment Criteria:**
- Each summary of chapters_summary is not a summary of "what happened", but an
  instruction of "what conflicts are promoted and what states are changed"
- Each chapter can be countered by asking: "Which step in the core conflict does this
  chapter serve?"
- After reading the outline, even without turning to `chapters/vol-{N}-ch-{M}.md`, you
  will know what the main line of this volume is and what each chapter does.

**Allowed:**

| Behavior | Description |
|------|------|
| Leave the chapter outline blank (when it is not the first volume, only the title and one sentence of direction are written in subsequent chapters) | The first volume must all have conflict carriers, volume N+1 allows 3 detailed chapters at the near end, and the far end is left blank, but the blank chapter must write a sentence of conflict direction |
| The volume direction adjusts the presentation of the core conflict as the writing progresses | but does not overturn the factual basis of the archived chapters |

**Prohibited:**

| Behavior | Consequences |
|------|------|
| Write a "thematic" chapter outline (such as "This chapter is about trust") - no specific conflict events | There is no way to start the writing cycle, and the direction proposal becomes a guessing game |
| One chapter carries multiple unrelated main line conflicts | The chapter is divided and the main text is rambling |
| In the first volume, I skipped the direction determination (whether it was a template or the character's voice) and wrote the chapter outline directly | Structural collapse - after writing 3 chapters, I found that the direction was wrong, and all the previous chapters were useless |
| Volume N+1 does not have a character voice, and directly uses the template of the first volume | The character status is ignored, and subsequent actions are disconnected from history |

---

## 1. Determining the volume direction

The first step in the outline is not to write the outline, but to set the direction. The
direction is wrong, and all the rest is written in vain.

**First determine whether this volume is the first volume:**

### 1. Volume One: Using the Story Structure Template

**What to write:** Choose a structure template and clearly allocate the functions and
number of chapters in each stage.

**How to Chat:** Read settings/genre-setting.md for selected types. If there is a value,
go to `.claude/knowledge/genre-example.md` to find the corresponding type of
`story_arc_templates`; if there is no value, use the following general template. Agent
directly outputs the proposal (**without asking "which one do you want"**):

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Volume 1 Structural Suggestions: Three Acts
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Recommended number of chapters: 10-12 chapters

Overview of each stage:
1. setup (about 3-4 chapters) → Establish the protagonist’s situation and core suspense
2. confrontation (about 4-5 chapters) → the conflict escalates and the protagonist takes the initiative
3. resolution (approximately 2-3 chapters) → The conflict ends, leaving the suspense at the end of the volume

Can be replaced by: starting point, suspense progression, character arc
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Universal story structure template (theme is not timed):**

| Template | Suitable | Default volume |
|------|------|---------|
| **Three Acts** (setup→confrontation→resolution) | Conflict-driven story with clear opponent or goal | setup Chapter 3-4 / confrontation Chapter 4-5 / resolution Chapter 2-3 |
| **Qi Cheng Yu Jie** (Qi → Cheng → Fu → Knot) | Oriental narrative structure, suitable for slow and delicate stories | Starting with Chapters 2-3 / Cheng with Chapters 3-4 / Cheng with Chapters 2-3 / Ending with Chapters 1-2 |
| **Suspense progression** (question → clue → reversal → answer → aftertaste) | Puzzle-oriented, story with information gaps | Questions Chapter 1-2 / Clues Chapters 2-3 / Reversal Chapter 2 / Answer Chapter 1 / Aftertaste Chapter 1 |
| **Character Arc** (Daily → Turn → Struggle → Transformation → New Normal) | Character-driven, growth-oriented story | Daily Chapter 2 / Turn Chapter 2 / Struggle Chapter 2-3 / Transformation Chapter 1-2 / New Normal Chapter 1 |

**Filling standards for each stage:**

| Fields | Filling Standards | Frequently Asked Questions |
|------|---------|---------|
| Structural template selection | There must be a clear division of stages, not "just write" | Just saying "write a few chapters first and take a look" - is equivalent to having no direction |
| Functions of each stage | Each stage has a clear one-sentence function (such as "setup: establishing the protagonist's situation and core suspense"). Empty words such as "development" and "expansion" cannot be used | "Second stage: story unfolding" - what to unfold? What happened to who and whom? |
| Chapter number allocation | Each stage is assigned a specific number of chapters, and the total number matches the expected volume length. The author is allowed to adjust, but there must be a number | "About 10-15 chapters" - there is no distribution, it is impossible to judge whether the proportion is reasonable |
| Match the subject type | If the subject type is selected, the template should match the type (suspense type uses suspense progression, and immortality type uses upgrade arc) | The urban love theme uses a three-act style, but the first act has 8 chapters - the reader leaves without waiting for the conflict |

**Example (starting with the knot, suspense theme): **

```
✅ Qualified:
Introduction (Chapter 2): Establishing suspense about the disappearance case + demonstrating the protagonist’s investigative abilities. Chapter 1 receives the case, Chapter 2 investigates the scene and discovers contradictions.
Development (Chapter 3): Expansion of clues + first reversal. Chapter 3 discovers the connection between old cases, Chapter 4 encounters obstacles, and Chapter 5 achieves a key breakthrough.
Turn (Chapter 2): The truth is approaching + the protagonist’s personal crisis emerges. In Chapter 6, a bigger conspiracy is discovered, and in Chapter 7, the protagonist is forced to make a choice.
Conclusion (Chapter 1): The small case is closed and the big picture is revealed. A missing person is found, but the protagonist knows there is something bigger behind it.
```

```
❌ Unsatisfactory:
Introduction (Chapter 3): Introducing the world view and character relationships.
Development (Chapter 4): The story gradually unfolds and the conflict gradually escalates.
Turn (Chapter 2): The story takes a turn.
Conclusion (Chapter 1): The story ends.
```

> Reason for failure: All empty words - "expand", "upgrade", "turn" and "end". I can’t
> write a direction proposal.

**Possible author options:**
- "That's it" → Use the confirmed template as the outline for discussion
- "Change {variant}" → Display the selected variant and reconfirm
- "I'll do it myself" → Skip the template and go straight to the core conflict
  discussion
- "I'll change it" → follow the author's adjusted structure

### 2. Volume N+1: Let the characters speak

There is a previous volume archive (`archives/` is not empty) → **Start directly from
character-driven analysis**, no template is pushed. Existing characters have their own
status and intentions, and they tell the author what to write in the next volume.

**How to chat:**

**Operation process:**
1. Read the latest `status-history` of each character `settings/character-setting/<id>.md` - where
   they were at the end of the previous volume, what they experienced, and what
   information they had
3. For each active role (including antagonist/important supporting role), generate the
   role "voice":

**Character voice format:**

```
[{Character Name}'s Situation] The end of the volume is at hand - who is he with, what information he has, and what situation he is currently in.
[{Character name}'s unfinished business] The obsessions/goals/fear left behind in the previous volume - what has not yet been resolved
[{Character name}Thinking between volumes] In the gap between volumes, what does he think about repeatedly?
[What {character name} wants to do now] Based on the current situation, what is he most likely to promote in the next volume?
```

4. Show to author. **The more sounds, the more natural the direction of the scroll** -
   the conflict of wills of several characters will naturally form the main line
5. The author determines the direction of the volume based on the character's voice.

**Filling standards for each field:**

| Fields | Filling Standards | Frequently Asked Questions |
|------|---------|---------|
| Active character filtering | Read the status history of each character `settings/character-setting/<id>.md` to find characters with unfinished goals/status changes. Not all characters speak, only those who have roles in the next volume | All 12 characters are listed to speak - the author can't see it at all |
| Character situation description | It must be specific to the "end of the paper": where it is, who it is with, and what information it has. It can't be "I experienced a lot in the previous volume" | "Lu Zheng continues to investigate" - not in place and didn't say what he knew |
| Conflict of character wills | The voices of multiple characters should naturally conflict or overlap. "A wants to find out the truth + B wants to cover up the truth + C wants to win over A" is better than "A wants to find out the truth + B also wants to find out the truth" | All characters have the same direction - without conflict, there is no main line |
| Author Confirmation | After the character's voice presentation, the author must clearly confirm the volume direction. Do not jump directly from speaking out to writing an outline | Agent thinks that "the author should agree" and starts working directly |

**Example:**

```
✅ Qualified:
[Lu Zheng’s situation] At the end of the volume, he was in the office and found that it had been turned over. Three things were known: Su Tang voluntarily hid, the case was suppressed three years ago, and the man in gray short sleeves was following him. I have photos of old case files given by Fang Yan.
[What Lu Zheng wants to do now] Find out what happened three years ago - who suppressed the case and why. Su Tang's disappearance is just the introduction, and what lies behind is the real goal.
[Fang Yan’s situation] Within the police force, someone knew that someone was watching Lu Zheng. He gave the dossier to Lu Zheng but was warned by his superiors.
[What Fang Yan wants to do now] Help Lu Zheng secretly but cannot be exposed. He wants to know why the case from three years ago was suppressed - it has something to do with his professional dignity.
```

```
❌ Unsatisfactory:
[Lu Zheng’s situation] Experienced the adventure in the first volume and solved the disappearance case.
[What Lu Zheng wants to do now] Continue to be a detective and take on the next case.
```

> Reasons for failure: no placement information, no specific known/unknown, and no
> residual motivation. "Continuing to be a detective" means having no direction.

**Back to the bottom:** The author still has no direction after the character speaks →
Return to the structure template above to help find the structure.

### 3. From voicing to chapter unfolding (exclusive to Volume N+1)

The completion of the character's voice does not mean that the direction has been
determined. Voicing collects the state and intent of each character, and the next step
is to see where those intents intersect.

**The main line emerges from the intersection of character states. ** This is not made
up, it is detected from the "things I want to do now" of multiple characters.

**Step one: Check whether the main line appears**

Lay out the "What I want to do now" of all active roles:

- ✅ At least two characters’ action directions point to **the same conflicting point** →
  the main line naturally emerges
- ✅ The character directions are not all confrontational - some provide help, some
  provide information, but they all converge on the same thread
- ❌ All characters go their separate ways without any intersection → Either a key role
  is missing, or the protagonist lacks a clear action goal

If the intersection is not obvious, ask the author:

> "These characters are all trying to push for different things now - which pair's
> conflict do you think is at the heart of this volume?"

**Example:**

```
[What Lu Zheng wants to do now] Find out what happened three years ago - who suppressed the case and why
[What Fang Yan wants to do now] Help Lu Zheng secretly but cannot be exposed
[What someone in the police force wants to do now] Stop Lu Zheng from settling an old score

Intersection → "Investigating old cases vs. suppressing the truth" → Main line: "Lu Zheng touches the internal protective umbrella of the police force"
```

**Step 2: Check whether the number of chapters can be deduced**

Each character's "what they want to do now" takes approximately a few chapters to
complete. It’s not about guessing, but looking at how many conflict scenes this volume
involves and how many chapters each scene requires to advance.

> "3 chapters of Lu Zheng investigating old cases + 2 chapters of Fang Yan's line
> interspersed + 2 chapters of pressure from the forces suppressing the case + 2
> chapters of the climax = about 9-10 chapters"

❌ The source of the chapter number is unclear → The voice only talks about the status of
the characters, not what they will do next. Go back and make up.

**Step 3: Check whether the chapter outline has direction to follow**

The direction of advancement of each stage can be detached from the main line. It's not
about breaking things out of thin air, it's about "what needs to be done first and what
needs to be done next to resolve this conflict."

- ✅ "First check old cases → then encounter warnings → then find a breakthrough → and
  finally the conflict escalates"
- ❌ "Just write a few chapters first and see" → The main line is not clear enough to
  deduce the stage

**Step 4: Template optional but not required**

If the main line is clear, the template is just an auxiliary skeleton. Chapter
directions can be derived from character actions without using templates. Templates are
structure confirmation, not structure discovery.

---

## 2. Core Conflict

One line governs the entire volume.

**What to write:** One sentence for the core conflict of this volume - consistent with
the definition in the story.md sub-volume list, but here it can be refined to **the
antagonistic relationship within this volume**.

**How to talk:** Inherit a sentence from story.md and ask the author, "The main line of
this volume is this sentence, right? Is there anything that needs to be adjusted?"

✅ Passed: "Lu Zheng wants to find out who suppressed the case three years ago, but
someone within the police force wants to stop him from settling old scores." - Who (Lu
Zheng), what does he want to do (find out the truth about the case three years ago),
what is hindering him (forces within the police force prevent him)

❌ Unqualified: "Lu Zheng investigated various cases in the city while facing the shadow
of his past." - "Various cases" is not a main line. "Shadows of the Past" has no
specific counter force.

### Fill in the criteria

| Fields | Filling Standards | Frequently Asked Questions |
|------|---------|---------|
| Conflict expression | In one sentence: "Who + wants to do + what is hindered by what". There must be a countervailing force, it cannot be a one-way wish | "The protagonist wants to become stronger" - there is no blocking party, and there is no conflict |
| Opposing force | The obstacle must be a specific role/power/situation, not an abstract concept | "Fighting fate" and "Fighting society" - too imaginary to write a specific plot |
| Retroactive relationship with chapters | The summary of each chapter contains at least one verb pointing to the advancement of the core conflict (discovery/encounter/choice/failure/advance/obstacle) | The summary of Chapter 3 is "The protagonist goes to the market to buy things" - it has nothing to do with the main conflict, it is a filler chapter |
| Single line vs multi-line | There can only be one main line conflict in a volume. If there is a conflict between branch lines, the relationship between the branch lines and the main line must be clearly stated in 2 sentences | The three lines in a volume are independent of each other, and each chapter jumps between the three lines - the reader cannot follow, and the chapter outline will inevitably split |

### Two bottom lines (if you fail either one, you are prohibited from entering Phase 3)

1. **The core conflict can be stated in one sentence** - The main conflict of the volume
   must be expressed in one sentence, without the need for "because", "at the same
   time", "on the other hand". I can't say clearly, I just didn't think clearly. A reel
   can have branch lines, but there can only be one main line.
2. **Writable conflict carrier for each chapter** - Each summary of chapters_summary
   must contain a writable event conflict. Chapter outlines that only include "character
   establishment", "world view display", "transition foreshadowing" and "relationship
   progression" without specific conflict events are not written. The carrier of
   conflict is "what changes after the reader reads this chapter."

---

## 3. Emotional trend - the emotional arc of the entire volume

Conflict answers "what happens in the plot", and emotional direction answers "how does
the reader's emotions change when reading this volume from beginning to end". The same
set of conflicts, different emotional trends, and completely different reader
experiences.

### Determine the emotional direction

Don't first ask "what is the reader's mood?" - a volume is not a mood, but a series of
progressive moods. Ask the author first:

> **"How does the reader's emotions go from the beginning to the end of this volume? -
> For example, the cool volume is pressing and pressing → turning over → face-slapping
> → showing off; the suspenseful volume is approaching layer by layer → sudden
> reversal → aftertaste."**

The answer is not a single emotional word, but an arc:

| ✅ Qualified (arc) | ❌ Unqualified (single word) |
|----------------|-------------------|
| "Depressed → Depressed → More depressed → Improved → Face-slapping → Pretentious" | "Cool" |
| "Tense→Approaching→Shocked→Relieved" | "Tense" |
| "Warmth → Conflict → Sadness → Hope → Warmth" | "Warmth" |
| "Angry→depressed→gathering momentum→excited→satisfied" | "cool" |

### Quick check on types of emotional trends (divided by arc mode)

| Arc mode | Typical trend | Suitable for subject matter |
|---------|---------|---------|
| **Suppress first and then enjoy** | Depressed→depressed→more depressed→enhancement→face-slapping→pretending to be awesome | feel-good fiction, upgrade flow, revenge |
| **Approaching layers** | Tension → Tension ↑ → Approaching → Shock → Soothing | Suspense, detective, thriller |
| **Tension opening and closing** | Warmth → Conflict → Sadness → Hope → Warmth | Romance, emotion, family |
| **Preparing to explode** | Suppression → Expectation → Preparing for momentum → Excitement → Satisfaction | Competition, growth, counterattack |
| **Spiral Progression** | Anger→Small Feeling→Depression→Medium Feeling→Depression→Great Feeling | Long feel-good fiction (to prevent fatigue) |

### Volume-level emotional arc design

Emotional trend = an arc, with a Qidian, a middle turning, and an end point. Each step
in the arc corresponds to a stage in a volume (a stage of the template/a level of the
conflict ladder):

```
✅ Press first and then curl (suitable for curling):
  Depressed (dilemma established) → Depressed ↑ (Oppression escalated) → More depressed (desperate situation)
  → Improve (get a turn) → face-slapping (counter-attack) → show off (show results)
  → The reader has been suppressed and finally released in a concentrated manner

✅ Approaching the arc layer by layer (suitable for suspense volumes):
  Tension (building suspense) → Tension ↑ (Crisis approaching) → Shock (reversal of revelation)
  → Anticipation (building up momentum for climax) → Soothing (ending the aftertaste)

❌ Unsatisfactory:
  "Cool" → No arc, just a one-time emotion. How to progress? From where to where?
  "Tense → Tension → Tension" → No change, the reader is numb in Chapter 3
```

### Chapter emotional anchor point design

After the emotional direction of the volume is determined, **each chapter is a point on
the arc**. When setting the summary of each chapter, mark the position of this chapter
on the arc:

```
### 1-3: Survey site
- **Conflict incident**: Lu Zheng discovered a conflict at the scene
- **Emotional Anchor**: Depression↑, The protagonist discovers that someone is obstructing him and the situation becomes more difficult.
- **Arc position**: Chapter 3/Total 10 chapters - the latter part of the repression stage, approaching the turning point
```

---

## 4. Conflict ladder - the escalation of conflict layer by layer

The core conflict defines "who versus whom," but the core conflict of a volume needs to
be broken down into a series of escalating obstacles. Not an obstacle, but a ladder,each
level higher and more dangerous than the previous one.

### Ladder design principles

1. **Each level of obstacle is a direct result of the previous level** - the protagonist
   passes the first level before triggering the second level, not because "it's time to
   do the next thing"
2. **Each level is more difficult than the previous level** - the opponent is stronger,
   the cost is greater, and the choice is more painful
3. **There is a turning point between layers** - not "the same thing is harder", but
   "the situation has fundamentally changed"

### Conflict Ladder Structure

```
Visualization example (suspense volume):
  Level 1 (1-1~1-2): Taking the case → Investigation and finding contradictions ← Barrier to entry: Obtaining information
       ↓ Turning point: It is discovered that an old case has been suppressed
  Level 2 (1-3~1-5): In-depth investigation → Encounter warning ← Obstacles to upgrade: External resistance
       ↓ Turning point: Umbrella reveals its true face
  Level 3 (1-6~1-7): The key witness is missing → the evidence chain is broken ← Major obstacles: losses and setbacks
       ↓ Turning point: The protagonist is forced to choose
  Level 4 (1-8~1-10): Head-on conflict → The truth emerges ← The ultimate obstacle: Showdown
```

### Key Turning Point Design

A reel must have **2-4 key turning points**. The turning point is "the moment when the
situation fundamentally changes", and the turning points are the "advance stages".

| Twist types | Examples | Effects |
|---------|------|------|
| **Information Turn** | "The protagonist discovers that an old case has been suppressed" | What we know has changed, and the target has changed |
| **Relationship turning point** | "Cooperators are actually enemies" | The camps have changed, and the confrontation pattern has changed |
| **Status Transition** | "The protagonist loses the support of the police force" | Resources have changed, difficulty has changed |
| **Turn of events** | "The key witness was killed" | The situation has changed and is irreversible |

> **Judgment Criteria:** Without this turning point, would the rest of the story still
> follow the original path?, Can walk → Explain that it is not a turning point, just a
> normal advancement, increase the difficulty or delete it., Can’t walk → This is the
> real turning point.

### Conflict Ladder Acceptance

- [ ] **Each level of obstacles is more difficult than the previous level** - not
      repeating the same confrontation (each level is equal if "encounter the gangster →
      win")
- [ ] **There is a clear turning point between each layer** - the situation has
      fundamentally changed and is not a continuation of the same thing
- [ ] **No obstacles "just for the sake of obstacles" - each layer serves the
      advancement of the core conflict
- [ ] **The number of turning points is between 2-4** - too few straightforward
      narratives, too many breathless

---

## 5. Information gap, the engine of driving force

Driving force answers "why readers want to read on", and **information gap** is the core
engine of driving force. Readers turn pages not because of conflict, but because they
want to know "what will happen next" - this "want to know" comes from **who knows what
and who doesn't know what**.

### Four subjects with poor information

The information gap is always a relationship in which "one party knows something and the
other party does not." Four subjects are involved:

| Subject | Representative | Description |
|------|------|------|
| **Protagonist** | Protagonist/Core Team | Reader’s Perspective Subject |
| **Supporting Characters** | Allies, neutral characters, informants | Information may be asymmetrical between the protagonist and other characters |
| **Villains** | Opponents, hostile forces, environmental traps | Information may be asymmetric between the protagonist and the antagonist |
| **Reader** | Reader | The reader may know something that the character does not know and vice versa |

### Three types of relationships with information gaps (divided by informed parties)

| Relationships | Patterns | Examples | Reader Psychology |
|------|------|------|---------|
| **The protagonist knows ↦ Others don't know** | The protagonist knows a certain key information, but the villain/supporting character does not | The protagonist has a golden finger, and the protagonist knows the conspiracy in advance | Expectation - "Let's see how he uses this information" |
| **The villain/supporting character knows ↦the protagonist does not know** | The villain or supporting character has secrets/traps that the protagonist does not know | The villain sets up an ambush for the protagonist, and the readers/villains know that only the protagonist does not know | Nervous - "Don't step in!" |
| **The reader knows ↦ the protagonist does not know** | The reader knows something through the narrative, but the protagonist is still kept in the dark | The reader knows it is a misunderstanding but the character is still angry | Anxiety - "Speak clearly!" |

> **Note:** The point of information gap is to clarify "who knows what and who doesn't
> know what", not to judge "whose disadvantage is this". Which party knows and which
> party does not know the same information gap is fixed - after the information is
> revealed, the relationship reverses and becomes a new information gap.

### Marking of information gaps in the syllabus

After the summary of each chapter, the active information gaps of the chapter are
marked. Use arrows to express "who knows ↦ who doesn't know":

```
### 1-4: Trap
- **Conflict Event**: Lu Zheng went to the warehouse based on the informant's information, but the information was false - the other party had set up an ambush waiting for him.
- **Emotional Anchor**: Tension
- **Information gap**: The villain knows it’s a trap ↦ The protagonist doesn’t know ⬅ The source of suspense in the whole chapter

### 1-5: Counterattack
- **Conflict incident**: Lu Zheng was actually prepared - he used the trick to fish out the person behind the informant
- **Emotional Anchor**: Cool
- **Information gap**: The protagonist has a back-up plan ↦ The villain doesn’t know ✅ The information gap in the previous chapter is reversed
```

### Types of driving forces for poor information

The distribution of information gaps determines the type of driving force, and the
driving force determines the rhythm design of the entire volume:

| Dominant driving force | Core mechanism | Information gap model | Chapter rhythm design |
|-----------|---------|-----------|------------|
| **Suspense driven** | "Want to know what the truth is" | The unknown truth of the protagonist ↦ is gradually revealed | Information hooks are left at the end of each chapter to release a layer of new information |
| **Threat driven** | "Worried about whether the protagonist will die" | The villain knows the trap ↦ The protagonist does not know | The crisis spirals and the safety period becomes shorter and shorter |
| **Goal driven** | "I want to see if the protagonist can achieve it" | The protagonist knows the goal ↦ The villain does not know the trump card | Phased results + new obstacles, cyclical advancement |
| **Relationship-driven** | "How will the relationship develop?" | The reader knows the truth↦The character still misunderstands | The tension accumulates to reveal, and the opening and closing are moderate |
| **Information gap driven** (pure) | "Let's see when it will be revealed" | Readers know everything ↦ Characters don't know | Countdown to reveal, taking advantage of readers' anxiety |

**Combination use:** A volume can have 1 dominant drive + 1 auxiliary drive. When suspense
drive is the main focus, threat drive can be used partially to create tension.

### Volume level information difference arc

The syllabus does not define "how the information gap changes in each chapter" - that is
a matter for the chapter syllabus. The outline of the volume only defines **Qidian and
the end point**: What does the protagonist know and does not know at the beginning of
this volume, and what does the villain know and do not know? Who learns new information
by the end? The middle arc is played out step by step from chapter to chapter.

**Step 1: Information difference at the beginning of the fixed volume**

> "At the beginning of this volume, what does the protagonist know and doesn't know?
> What does the villain know? What does the reader know?"

```
At the beginning of the volume:
  ⬆ The protagonist knows: Su Tang disappeared and the police determined that he left voluntarily
  ⬇ The villain knows: the inside story of the case three years ago and where Su Tang is
  👁 Readers know: as much as the protagonist (insert perspective)
  → The biggest information gap is "the villain knows the inside story ↦ the protagonist does not know", this is the Qidian pull of this volume
```

**Step 2: Information difference at the end of fixed volume**

> "At the end of this volume, who has the information? - What did the protagonist know
> that he didn't know before? What information advantage did the villain lose?"

```
At the end of the volume:
  ⬆ The protagonist learns something new: the fact that the old case was suppressed, the existence of a protective umbrella, and that he is being watched
  ⬇ New villain knowledge: The protagonist is investigating and is more difficult to deal with than expected
  👁 Readers know: Same as the protagonist
  → The protagonist’s information has advanced, but the gap with the villain still exists. This is the next volume of Qidian
```

**Step 3: Qidian→Arc direction of the end point**

What is the changing trend of the information gap from Qidian to the end point? It’s not
the details of each chapter, it’s the volume-level direction:

```
✅ Qualified:
  Qidian: The villain knows the inside story ↦ The protagonist doesn’t know
  End point: The protagonist knows the existence of the inside story, but does not know everything
  Arc: Information gap changes from "complete asymmetry" to "partial balance",
        The protagonist catches up one step, but it is not enough → Support the next volume to continue the pursuit

❌ Unsatisfactory:
  Qidian: The protagonist knows nothing
  End point: The protagonist knows everything
  → One volume fills all the information gaps, and the next volume has no information driving force.
```

### Information gap acceptance

- [ ] **Information gaps are marked in each chapter** - Write clearly "who knows what ↦
      who doesn't know what"
- [ ] **The information gap in the volume has a complete cycle of "setting → suspension
      → revealing"** - setting it up but not revealing it means setting it up in vain,
      revealing it too early means there is no setting up
- [ ] **There is an inheritance relationship between information gaps** - the latter
      information gap arises from the revelation of the previous one, not a new secret
      emerging out of thin air
- [ ] **The information gap does not mean leaning towards the same side throughout the
      entire process** - The protagonist knows the key information throughout the
      process but the villain does not → there is no sense of tension; the villain knows
      the inside story throughout the process but the protagonist does not → too
      depressing. need for alternation

---

## 6. Scene card - scene decomposition of chapters

> Outline → Chapter (including conflict points + emotional anchor points + information
> gaps) Chapter Outline → Scene Cards (3 information per card)

Scene cards are a refinement tool at the chapter level. A chapter consists of 2-5 scene
cards, each scene card records three pieces of information:

| Fields | Answered Questions | Description |
|------|-----------|------|
| **What the protagonist wants to do** | Goal - what the protagonist wants to achieve in this scene | Even in a passive scene, the protagonist has a purpose ("survive", "figure out the situation") |
| **What's blocking him** | Obstacle - what is the obstacle | It can be people (opponents), things (insufficient conditions), heart (fear/hesitation) |
| **Is there any suspense that makes readers want to keep reading** | Hook - What unanswered questions make readers want to know "What then?" | Corresponding to emotional anchor + information gap, readers care about "What then?" |

### Scene card example

```
## Chapter Outline: 1-3 Old Files

### Scene 1: Fang Yan’s office
- **What does the protagonist want to do**: Lu Zheng wants to get the inside information from Fang Yan about the case three years ago.
- **What's stopping him**: Fang Yan didn't dare to say - there was someone else in the office, hinting to Lu Zheng that "someone is watching this case"
- **Is there any suspense that makes the reader want to read on**: The reader feels that Fang Yan knows the inside story but dare not tell it, and is even more curious about who is behind the case.

### Scene 2: Archives Room
- **What does the protagonist want to do**: Lu Zheng retrieved the files from three years ago and found the record of the crime
- **What's stopping him**: The file information is incomplete and a few key pages have been taken away.
- **Is there any suspense that makes readers want to keep reading**: Who took it away? What information is written in the file that cannot be seen by others?

### Scene 3: Parking lot
- **What the protagonist wants to do**: Confirm whether you are being followed when leaving the police station
- **What's stopping him**: Someone is indeed following him - the man in gray short-sleeves is sitting in the car
- **Is there any suspense that makes readers want to keep reading**: Who is the other party? Lu Zheng has been targeted, what will happen next?
```

### The three-element principle of scene cards

Each card has three elements that are **indispensable**:

| Missing | Consequences | Correction |
|------|------|------|
| There is no "what the protagonist wants to do" | Running account - the protagonist is pushed by the plot and has no initiative | Give the protagonist a purpose, even if it is just to "figure out where he is" |
| There is no "something holding him back" | No conflict - the protagonist does whatever he wants and the reader is not nervous | Add an obstacle, big or small |
| No "is there any suspense that makes the reader want to keep reading" | Straightforward narrative - written but the reader doesn't care | Add an unanswered question: the reader wants to know "What's next?" |

### Scene card acceptance

- [ ] **Each card has all three elements** - no missing fields
- [ ] **There is a progression of cause and effect between scenes** - Scene one is the
      cause of scene two, and scene two is the premise of scene three.
- [ ] **The sum of the emotional anchor points of the scene card = the emotional anchor
      point of the chapter** - the scenes within a chapter may have ups and downs, but
      the overall serves the mood of the chapter
- [ ] **The information gap of the scene card has changed** - the whole chapter is "the
      protagonist doesn't know" which will make you tired. In the middle, you can switch
      to "the reader knows that the protagonist doesn't know" to increase the tension.

## 7. Chapter list (chapters_summary)

chapters_summary is the core output of the volume outline - it directly determines
whether the outline of each chapter can be written.

### 1. Chapter structure

**What to write:** The id, title, and summary of each chapter.

**How to chat:** Each stage of the template confirmed in the previous step is the
skeleton (or the direction of the character's voice derivation), which is filled in
chapter by chapter. The first volume starts with the chapters from the first stage of
the template, and Volume N+1 starts with the natural Qidian derived from the character's
vocalizations.

| Fields | Filling Standards | Frequently Asked Questions |
|------|---------|---------|
| id | Format "volume number-chapter number" (such as 1-1, 1-2). Continuous numbers without skipping | 1-1, 1-3 (skipping 1-2) - the writing cycle will be broken |
| title | Provides information. No "Chapter X" or purely functional names are used. The title itself should allow the reader (or Agent) to guess the core events of this chapter | "Chapter 1" (equal to not being written), "Transitional Chapter" (revealing the unclear content) |
| summary | One sentence, containing three elements: **who did what + what happened (conflict) + what changed at the end of the chapter**. If one element is missing, the person is unqualified | "The protagonist continues to investigate" - who investigates? Investigate what? What was found? Nothing has changed? |

### 2. Conflict carrier (must be checked in every chapter)

Each chapter summary must contain a writable event conflict. The following are four
types of unqualified chapters and corresponding modification methods:

| Unqualified types | Typical sentence patterns | Why can’t I write | Modification direction |
|-----------|---------|-------------|---------|
| Thematic | "This chapter talks about trust" and "discussing freedom and responsibility" | There are no events, only concepts. Agent cannot deduce plot | Turn concepts into concrete events: Who trusted whom about what? turn out? |
| Functional style | "Establish character relationships" and "show world view" | Functions are not stories. Establishing a character relationship can be written as "two characters disagree on something" | Fold the function into the conflict event: show/establish through something |
| Summary style | "The protagonist goes through a day of adventure" | No specific points of conflict. There are countless things in a day - Agent doesn't know which one to write about | Identify the most important thing in this day |
| Result formula | "The protagonist won the game" | There is only the result and no conflict process. Who won? How did you win? What obstacles did you encounter along the way? | Write obstacles and confrontations: "The protagonist faces XXX in the finals and wins the game through YYY" |

**Causal chain between chapters:**

```
✅ Qualified (clear causal chain):
1-1 Receive the case → 1-2 Contradictions are found in the investigation (the investigation was carried out because the case was accepted) → 1-3 In-depth investigation encounters obstacles (the old case was investigated because of the contradictions)
Each chapter is the result of the previous chapter and the cause of the next chapter.

❌ Unqualified (each chapter is independent):
1-1 The protagonist goes to location A → 1-2 The protagonist meets character B → 1-3 The protagonist obtains item C
There is no causal progression between the three events - it's just that the protagonist went to different places and did different things, not that the story progressed.
```

---

## 8. New characters and settings added

During the outline discussion, it may be discovered that new characters or worldview
settings need to be added. These additions must be implemented before entering the
writing cycle.

### 1. New roles

| Check items | Standards |
|--------|------|
| The role file has been created | `settings/character-setting/<id>.md` exists, and the completeness of the field filling is not lower than the set stage standard |
| Story role has been assigned | Cannot be left blank or written "To Be Determined" |
| Required fields have values | World view / Self-positioning / Values / Abilities / Skills / Environment At least the fields related to the role function are filled in |
| Character diagnosis (if this volume has > 1 chapter) | Angry expression + shortcomings + own purpose (refer to the character diagnosis standards in the setting stage) |
| The supporting role has a clear purpose | If the supporting role only serves one scene (sending information/leading the way/being rescued), it must be marked as a "one-time role" or expanded into a multi-scene role |

### 2. New settings added

| Check items | Standards |
|--------|------|
| New settings have been written to `settings/world-setting.md` | Additional content under relevant fields, do not forget after verbal discussion |
| The new setting asks questions through "perceivable" | "Will readers feel this setting in the text?" - If you can't answer, don't add it |
| The new settings do not affect the consistency of existing chapters | If the added settings conflict with the archived chapters, the conflict must be marked and a solution must be given (modify the archived / limit the effective scope of the new settings / abandon the addition) |

**Example:**

```
✅ Qualified:
During the outline discussion, it was decided that "this case requires a forensic role to provide professional clues" →
  Create fa-yi-li-ming.md
    - **Story Character**: Supporting Role
    - **Ability**: Forensic medicine major, able to discover autopsy details that ordinary people ignore
    - **Environment**: Forensic Medicine Department of the Municipal Bureau, working with Fang Yan
  Role purpose: Provide key clues + serve as Fang Yan's "internal information source"

❌ Unsatisfactory:
During the outline discussion, I felt that "the world needs an underground trading market" →
  Confirmed verbally but not written `settings/world-setting.md`
  Three days later, I started writing Chapter 5. The Agent did not know the rules of the underground market and made up his own
  → Conflicts with author’s intent, Chapter 5 rewritten
```

---

## Output Template

After confirmation, write `volume-{N}.md` in the following format:

```markdown
# Volume 1: {title}

## Volume information

- **Emotional trend**: The arc of emotional changes of readers in this volume (depressed→depressed→more depressed→upgraded→face-slapping→pretentious)
- **Core Conflict**: Who + what + what + hindered by
- **Leading driving force**: suspense drive/threat drive/goal drive/relationship drive/information gap drive
- **Ladder of Conflict**: Level 1 (Entry) → Level 2 (Upgrade) → Level 3 (Transition) → Level 4 (Ultimate)
- **Estimated Chapter**: N

## Chapter list

### 1-1: {Informative title}

- **Conflict Event**: Who did what + Conflict Event + What changed at the end
- **Emotional Anchor**: The reader’s mood while reading this chapter
- **Information gap**: {Who knows what} ↦ {Who doesn’t know what}
```

## How each field is used downstream

| Field | Who uses it | How to use it |
|------|------|--------|
| chapters_summary | Phase 3.1 Direction Proposal | The direction proposal for each chapter is based on the summary reasoning of chapters_summary - "What conflict will this chapter advance" |
| chapters_summary | Phase 3.2 Chapter outline | As the skeleton of the chapter outline, expand the memo seven paragraphs in detail |
| core_conflict | Phase 3 All | Each chapter asks "Which step of the core conflict does this chapter serve?" - Make sure the chapter does not go off track |
| **Emotional Trend** | Phase 3.2 Chapter Outline + Writer Text | Determine the position of each chapter on the arc - write short sentences with a fast pace during the depression stage, and write long sentences with a delicate feel during the release stage. The emotional anchor point of each chapter is a point in the trend |
| **Leading driving force** | Phase 3.2 Chapter outline + writer text | Determine the information release rhythm and information gap design of each chapter |
| **Conflict Ladder** | Phase 3.2 Chapter Outline | Make sure the obstacles in each scene card are at the corresponding level - do not use high-level conflicts prematurely |
| **Chapter Emotional Anchor** | Writer text | Directly guides the emotional rendering direction of the text - this chapter is to make readers nervous, so the writing style focuses on short sentences and a sense of unknown |
| **Chapter Information Gap** | writer text + prompt-crafter prompt word | Information gap design is injected into the prompt word - "the reader knows the trap but the protagonist does not" drives the reader to turn the page |
| New character file | Phase 3 text | Additional character settings will be added with prompt words when writing |

---

## Acceptance

### Volume Level Verification 1: The sum of the chapters’ stories = the volume is finished

Point to chapters_summary, read all the summaries chapter by chapter, and ask:

> **"Have these chapters taken together completed the core conflict of this volume? Is
> there any story missing?"**

- ✅ All the chapters together are the complete story of this volume, no more, no less
- ❌ A key turning point is missing → Add a chapter or adjust an existing chapter
- ❌ There is an extra chapter that has nothing to do with the main plot → delete or
  merge it into other chapters

This is the volume-level principle of "each volume is a subset of the main plot" mapped
to chapters - **just like 2.0's "the main plot cannot be completed without this volume",
here it corresponds to "the story of this volume is incomplete without this chapter"**.

### Volume level verification 2: Each chapter can be traced back to conflicts in the volume

Pointing to the core conflict of the volume, ask chapter by chapter:

> **"Where does the story in this chapter advance the conflict of the volume?"**

- ✅ "Chapter 1 takes over the case and builds suspense → Qidian of Conflict"
- ✅ "Chapter 3: Old case discovered → Conflict escalates"
- ❌ "This chapter is about the protagonist eating → has nothing to do with the conflict
  between Juan"

Occasionally, deviations between one chapter and two chapters are allowed (for example,
setting aside the writing, adjusting the rhythm), but most of the chapters do not match
up → either the conflict of the volume is not clearly defined, or the chapters are
written out of order.

### Volume Level Verification 3: The resolution of the conflict in each chapter advances the story of the volume

Point to the changes at the end of each chapter and ask:

> **"After the end of this chapter, has Juan's story taken a step forward?"**

- ✅ Key clues found → The next step can be traced (the story advances)
- ✅ Encountered an obstacle → The protagonist was forced to change direction (story
  turning point)
- ✅ The role relationship has changed → the subsequent conflict has a new basis (status
  change)
- ❌ A clue was discovered but it did not affect the follow-up → It means that it was not
  discovered
- ❌ If you have a fight, winning or losing will not affect the follow-up → It means
  there is no fight.
- ❌ The protagonist has figured something out but his behavior has not changed → It
  means he has not figured it out

**Core Difference:** The second verification question is "Is this chapter related to the
conflict in the volume?" The third verification question is "Did the volume's driving force
carry forward after the end of this chapter?" Relevant does not mean useful.

### Volume Level Verification 4: The name of the chapter matches the story of the chapter

Just look at the title, not the summary, and ask:

> **"Just by looking at the title, can you guess what is going on in this chapter?"**

- ✅ "Client" → You can guess: Someone is looking for the protagonist, and it is most
  likely a commissioned case
- ✅ "Rental House" → Guess: The protagonist went to a certain place and something
  happened there
- ❌ "Chapter 1", "New Beginning", "Turning" → The amount of information is zero and can
  be used in any story
- ❌ "Mist" "Abyss" → Too virtual, can't guess what exactly happened

The title is the first signal to the reader (and Agent). A qualified title will make
people think "that's what it means" after reading the summary, rather than "the title
and the content are two different things".

### Quick sniff (15 seconds)

If you pass all three, you have a high probability of passing:

1. **Can you say one sentence about the core conflict without looking at the document?
   ** → Can’t tell → Didn’t think clearly
2. **Just point to a summary of a chapter. Can you tell me "what changed after the end
   of this chapter"? ** → Can’t tell → There is no conflict carrier in the chapter
   outline
3. ** Just point to two chapters at random. Can you tell me "Why is it that Chapter 1 is
   followed by Chapter 2 instead of jumping directly to Chapter 3?" ** → Can’t tell → No
   causal chain

### Check item by item

- [ ] **The core conflict can be said in one sentence** (who + what + what is hindered
      by what), you can speak without speaking to yaml.
- [ ] **The direction of the volume has been determined** (the first volume has a
      structure template, volume N+1 has character voices + the author confirms the
      direction)
- [ ] **First volume: Structural template selected + stage functions written clearly +
      number of chapters assigned**
- [ ] **Volume N+1: Active characters have been screened, the end of the volume is
      detailed, characters have conflicting wills, and the author has confirmed the
      direction**
- [ ] **The emotional direction has been established** - it is an arc
      (suppression→face-slapping→pretending), not a single emotional word
- [ ] **The emotional direction is progressive** - the arc has Qidian, turning point,
      and end point, and each step is more advanced than the previous step.
- [ ] **Conflict ladder designed** - 2-4 levels of obstacles, each level is more
      difficult than the previous one, with clear turning points
- [ ] **Key turning points have been marked** - Each turning point is a "fundamental
      change in the situation", not an ordinary advancement
- [ ] **Information gaps have been marked** - Write clearly "who knows what ↦ who
      doesn't know what" in each chapter
- [ ] **The dominant driving force has been determined** - one of the
      suspense/threat/target/relationship/information gap drivers, with primary and
      secondary
- [ ] **chapters_summary Each chapter has id (continuous), title (with information), and
      summary (all three elements are complete)**
- [ ] **Each chapter has a writable conflict carrier**, You can directly deduce the plot
      direction proposal from the summary
- [ ] **Each chapter can be traced back to the core conflict** - Ask one by one, "Which
      step in the main conflict does this chapter serve?"
- [ ] **There is a progression of cause and effect between chapters** - the change at
      the end of the previous chapter is the Qidian or motivation of the next chapter
- [ ] **No unqualified chapter outlines for "topic type", "functional type", "summary
      type" and "result type" were found**
- [ ] **All new character files have been created** and story roles have been assigned
- [ ] **All new settings have been written to `settings/world-setting.md`**, ask through
      "perceivable"
- [ ] **There is no conflict between the new settings and the archived chapters** (if
      there is any conflict, there will be a solution)

### Verify execution

Execute according to the SKILL.md self-test protocol (Priority Agent Teams → subAgent →
Self-test). After getting the conclusion, first change the fail item before entering
Phase 3.
