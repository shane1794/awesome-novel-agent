# Chapter Setting Guide

> The second step of the third stage - fill in the content of the selected chapter.
> The chapter outline allows the author to see clearly: what happens in this chapter,
> which characters are involved, how the paragraphs are divided, what is written in
> each paragraph, which hooks are fulfilled/buried, and the total word count. The
> output is written to `chapters/vol-{N}-ch-{M}.md`.

**Precondition:** Direction input confirmed (3.1 hard node passed). The chapters_summary
of volume-N.md already has this chapter positioned.

---

**Table of Contents**
1. [The highest principle](#the-highest-principle-the-chapter-outline-makes-the-author-feel-that-it-meets-expectations)
2. [Formal layer - "What to write in this chapter"](#formal-layer-what-to-write-in-this-chapter)
   - 1. Direction input
   - 2. From direction to outline
   - 3. List of chapter contents
   - 4. Emotional design
3. [Feng Gu Layer, "What cannot be written into the outline of the
   chapter"](#feng-gu-layer-what-cannot-be-written-into-the-outline-of-the-chapter)
4. [What not to do,hard constraint red line](#what-not-to-do-hard-red-line)
5. [After completion - acceptance process](#after-completion-acceptance-process)
6. [Complete chapter outline example](#5-example-of-complete-chapter-outline)

---

## The highest principle: the chapter outline makes the author feel that it meets expectations

> After reading the chapter outline, the author can say, "Yes, this is the chapter I
> want to write." It's not "I understand it but I don't think it's what I want", it's
> not "I don't mind if you write it" - it's "Yes, that's it".

The chapter outline is given to the author. After he nodded and said "right", it was
used as input for prompt word generation. After reading it, the author felt that "the
direction was similar but not what I wanted", so he returned to the adjustment and did
not proceed with prompt word generation.

**Judgment Criteria:**
- **Expected Test:** The author can say "Yes, that's it" after reading it. If you don't
  say "right", it doesn't count as passing.
- **Clarity Test:** The author can point to key points and say "this paragraph is about
  this scene" and "that hook should be closed in this chapter". If you can't point it
  out, it means it's not in place.
- **Completeness Test:** The author can answer after reading it - what is the total
  number of words in this chapter, what is written in each paragraph, who are the
  characters, which step of the main plot is advanced, what old hooks are fulfilled,
  what new hooks are buried, and what changes at the end

**Two bottom lines** (if either one fails, prompt word generation is prohibited):
1. **The chapter outline must be understandable to the author** - not the data
   structure, not the writing instructions. If the author cannot understand it, then he
   is not qualified.
2. **Chapter synopsis does not include God's perspective deconstruction** - "This
   chapter tells", "The protagonist experiences", "Y is shown through X" are not
   allowed. Once these are mixed into the chapter outline, the prompt words will be
   copied into the text as they are, and the entire chapter will be scrapped.

---

## Formal layer - "What to write in this chapter"

The formal layer determines the content of the chapter outline: how to set the
direction, how to write each paragraph, and how to design the mood. Three steps to
complete: input direction → expand outline points → fill in the content list.

### 1. Direction input (Chapter N+1)

The first chapter starts directly from chapters_summary. Chapter N+1 (not the first
chapter) needs to first analyze "where the reader and the characters were at the end of
the previous chapter" in order to push the direction of this chapter.

**Principle: Instead of the agent guessing the direction, the context is spread out and
let the author judge. **

#### 1. Collect four sets of inputs

| Input | Source | Purpose |
|------|------|------|
| Reader Gap | Previous Chapter `emotional_design.emotional_hook` + `reader_expectation` | What are the readers waiting for - do you want to respond to this chapter or continue to read |
| Character status | The status history added when the previous chapter was archived + the current motivation of the active character | What the character wants to do now, what he knows, and what he is driven by |
| Hook inventory | The hooks field in each role setting file - pending / partial_advance | Which hooks should be closed, which ones still have to be suppressed, and which ones can be pushed |
| Volume positioning | `volumes/volume-{N}.md#chapters_summary` Chapter summary | This chapter's positioning in the volume - which step to advance the conflict |

#### 2. Composite direction

Cross the four groups of inputs, push 1-3 direction options, and sort them by
credibility:

```
Reader is waiting for {X} → Character {Y} wants to push {Z} → The outline says this chapter wants {W}
↓
Direction A: {Specific events} - Respond to readers’ expectations, advance character motivations, and match the syllabus positioning
Direction B: {Different directions} - Deflect readers' expectations and give surprises, but still within the scope of the volume.
```

#### 3. Show to author

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Volume {N} Chapter {M}, Directional Input
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Outline positioning: {chapters_summary one sentence}

Reader Gap: The previous chapter ended with {emotional_hook} - the reader is waiting for {specific expectations}

Character movements:
  / {Character A}: {What does he want to do now/what does he know}
  / {Character B}: {their position/motive}

Active hook:
  / pending: {which are pending and untouched}
  / What can be pushed: {What can be pushed forward in this chapter}

Direction suggestions: {1-2 specific directions, each with a sentence of reasoning}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Choose a direction, or say "I'll do it myself"
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**After the author confirms the direction, go to "From Direction to Outline Points" to
expand it into specific paragraphs. **

---

### 2. From direction to outline

**How to chat:** Read the chapters_summary of this chapter in volume-N.md and ask the
author:

> "The goal of this chapter is 2,500 words. We have divided it into 5 stories, each of
> ~500 words. Starting from the summary, for example, 'knocked on the door and opened
> the door → first impression after entering the door → inspected the bed → checked
> the refrigerator → found sticky notes → locked the door and came out → was stared
> at'. Do you think this will work? Use two sentences for each story to explain
> clearly what to write."

Write the passages spoken by the author into the key points of the outline
(outline.key_points). Each key_point corresponds to a paragraph. **The key points must
be written in 2-3 sentences, not one sentence. **

Reason: One key point 1 sentence → The agent needs to expand 800-900 words by himself,
almost all based on his brain. 2-3 sentences give the scene anchor point, action anchor
point and judgment anchor point, and the expansion space of agent is constrained to a
reasonable supplementary range.

**Writing method - three-paragraph anchor point method:**

Each key_point covers three anchor points, not necessarily three sentences, but three
pieces of information must be present:

> 1. **Sensory Anchor** - where the camera cuts. Light, sound, smell, sense of space.
> It's not "what kind of room is this", but "what do you feel as soon as you open the
> door". 2. **Action Anchor** - What exactly the character did. It's not "checking the
> room", it's "opening the drawers, lifting the quilt, and running fingers across the
> table". The more specific the action chain, the more stable the agent's rhythm. 3.
> **Judgment Anchor** - What the character draws from this. It's not "he felt
> something was wrong" (abstract psychology), but "he straightened up and scanned the
> room again" (behavioral response).

**Key: key_point is a note style, not a narrative style. ** It is a paragraph planning
note written by the author to himself, not a mini version of the text. Don't write "At
two o'clock in the afternoon, Lu Zheng opened the door, and the sunlight cut a bright
area on the floor" - this is the first draft of the text. It should be written as "Lu
Zheng comes to the door→No one knocks on the door→Gets the key→The door is not locked.
Pay attention to the sense of space when the sunlight cuts through the window" - this is
the planning notes. Difference: Narrative style fills the senses for the writer, while
notebook style leaves the sensory filling to the writer.

**Correspondence to the three elements of the outline scene card:**

The underlying logic of the three-paragraph anchor point method is consistent with the
outline scene card (what the protagonist wants to do + what is stopping him + what
suspense makes the reader want to read more), but the granularity is finer:

```
Outline Scene Card (Chapter Level) Chapter Outline Key Points (Paragraph Level)
  What the protagonist wants to do → Action anchor (what the character is doing, what to advance)
  What is blocking him → Judgment anchor point (what obstacles are encountered, what contradictions are found)
  Is there any suspense that makes readers want to read on → Full text emotional hook + information gap (each paragraph contributes part of the suspense)
```

The three-section anchor point method breaks down each "stop him" line in the scene card
into a specific beat sequence of "action → discovery → judgment". In turn, each key
point should be able to answer: **"What is the protagonist doing in this paragraph? What
obstacles are encountered? Why does the reader want to know what happens next?"**

**Conversation key points - a variation of the three-paragraph anchor method:**

There are key points in dialogue, and the focus of the three anchor points changes from
"sensory → action → judgment" to "scene → dialogue → power":

> 1. **Scene Anchor** - Who is talking in what environment, in what position, and in
> what posture. It wasn't "They were talking in the teahouse", it was "Fang Yan chose
> a corner seat and waited for Lu Zheng to sit down before speaking." 2.
> **Conversation anchor** - the core content and tone intention of the conversation.
> It wasn't "Fang Yan asked him what case he was investigating", it was "Fang Yan
> didn't ask about the case directly, but chatted a few words about the current
> situation. His tone sounded casual but his eyes were observing." 3. **Power Anchor**
> - Who has the upper hand at the end of the conversation, who is on the defensive,
> and any subtle changes in the relationship. It's not "they're done talking", it's
> "Fang Yan put down the teacup and lowered his voice by half a degree: 'Don't touch
> this case' - it's not a suggestion, it's a warning."

Key points in the dialogue must be marked `[dialogue]`.

For positive and negative examples, see §6 / Few-Shot examples (key points in dialogue).

**The number of words is calculated backwards - the number of pieces to be divided is
determined by the number of words:**

The number of key points to split is not a pat on the head, but a backward calculation
based on the target word count.

> **Default word count:** If the author does not specify the word count for a single
> chapter, it will be calculated as **2500 words** - this is the default word count
> for a single chapter in the book. If overall adjustment is required, change it here
> and synchronize the example numbers below; you can still confirm the actual goal for
> each chapter with the author (see "Two final questions"). **Target number of words ÷
> Expected number of words per article = Number of articles that should be split**
> 2500 word goal (default): 2500 ÷ 500 = 5 articles (each agent expands ~500 words)
> 4000 word goal: 4000 ÷ 500 = 8 articles 6000 word goal: 6000 ÷ 500 = 12 articles

Why 500 words/article? A key point 2-3 sentence anchor point ≈ 80-120 words, and the
agent needs to be expanded to 500 words to add scene details and transitions - this
ratio is just right. If each entry is expected to exceed 800 words (for example, 3
entries total 2,500 words), the agent can only write inner monologues and environment
renderings to fill the word count.

**After getting the word count target, count the number of articles first, and then
split the scenes:**

> The author said "4000 words" → 4000 ÷ 500 ≈ 8 items. The author said "6000 words" →
> 6000 ÷ 500 = 12 items. The author said "you watch and write" → 5 items based on the
> default value of 2500.

**How to dismantle it specifically-scene decomposition method:**

What the author calls "a scene" often contains multiple narrative beats. Each beat is a
key point. How to find the beat: **Follow the character's action chain, and make a cut
every time a complete cycle of "action→discovery→judgment" occurs. **

> Survey the scene → Knock on the door (action) and no one answers → Use the key to
> open the door (action) → The door is not locked (discovery) → Push the door and take
> a quick look at the whole place (judgment) → **Article 1** → Lift the quilt (action)
> → Wrinkle the sheets + charger (discovery) → Touch the charger and there is residual
> heat (judgment) → **Article 2** → Open the refrigerator (action) → Leftovers are not
> poured + the sides of the bowl are dry (discovery) → The toilet toothpaste lid is
> open + the towel is wet (discovery) → It does not look like leaving (judgment) →
> **Article 3** → Post-it notes on the bedside table (action) → Phone only (discovery)
> → Taking photos (judgment) → **Article 4** → Lock the door and leave (action) →
> Shadows in the corridor, silhouettes in the carport (discovery) → A man in gray
> short-sleeves left the community (discovery) → Keep walking without looking back
> (judgment) → **Article 5**

**Verify whether the number of entries is enough:**

Divide the number of articles into 500 words and see if you can reach the word count
target:

> 5 items × 500 = 2500 ✅ 3 items × 500 = 1500 ✗ → The difference is 1000 words, the
> agent must add water

If the number of items is not enough → Look back to see which scenes can be continued.
Each "action→discovery→judgment" cycle is one, and there is no omission.

**Pros and cons cases:**

✅ **Positive: The author said "survey site", word count 2500**

> Before demolition: The author said "just survey a rental house" After disassembly: 5
> steps along the chain of "Action → Discovery → Judgment" → 5 items Verification: 5 ×
> 500 = 2500 ✅ Just right Each article has 2-3 sentence anchor points, and the agent
> should be expanded to ~500 words. There will be no shortage of information or forced
> filling of water.

❌ **Converse①: The author said "survey the site", so I will break it down regardless of
the word count**

> Agent closes his eyes and reveals 3 items: bed/bathroom/being followed 3 × 500 =
> 1500 ✗ 1000 words away from 2500 Halfway through the writing, the agent will realize
> that the number of words is not enough, and start adding large paragraphs of
> environmental renderings and inner monologues of the characters to make it up - the
> text is full of water-filled paragraphs such as "He looked out the window and
> thought for a long time." Root cause: missing the beats of "knock on the door and
> enter → check the refrigerator → sticky notes → lock the door and go downstairs"

❌ **Reverse side ②: The scene is not dismantled, one piece carries the entire section**

> The "Inspection Site" only wrote one key point: "Lu Zheng entered the rental house
> and found that the bed was unmade, the charger was there, and there were leftovers
> in the refrigerator." 1 article requires 2500 words → agent can only edit Root
> cause: The author did not break down the "scene" into beats and directly used the
> scene title as the key point.

❌ **Converse ③: Lack of transitional beats, plot interruption**

> The author said, "Write about investigation first, then write about being followed."
> He broke down 2 items: being photographed at the entrance of the investigation
> room/community. Skip the 4 transition beats of "lock the door→corridor→go
> downstairs→exit the community" Write the main text: Lu Zheng was still looking
> through the drawers in the house, and the next part was filmed at the entrance of
> the community. Readers dance. Root cause: Transition scenes also have a cycle of
> "action→discovery→judgment", not "nothing to write about"

**How to talk:** After the author talks about a paragraph, convert it into 2-3 sentences
on the spot and show it to the author.

> "The section about 'surveying the room' you mentioned, I wrote it roughly like this
> - listen to it, right? 'The afternoon sun shines in through the window, and dust
> floats in the beam of light. Lu Zheng opened the drawer, lifted the quilt, and ran
> his fingers across the table - everything said that she would come back, but she was
> gone.' Which sentence do you think needs to be adjusted?"

**If the author says:**
- "One or two sentences are enough for me, no need to be so detailed" → Explain the
  reason: "I know that one sentence can tell the plot clearly, but when the agent writes
  the text, the information in one sentence is not enough and it will make up the
  details of the scene by itself. We don't decide for the agent what the room looks like
  - decide it in advance so that the text can meet the author's expectations."
- "Then just write it into 2-3 sentences for me." → Write a version first and let the
  author change it: "I will give you a first version, and you can look at the tone. This
  is the anchor point, not the final copy."
- Only the main points of the plot are given, but the details of the scene cannot be
  told → Follow-up question: "Is the first scene indoors or outdoors? Day or night? What
  does the protagonist see first when he walks in?"

**After talking about segmentation, ask about paragraph distribution:**

> "How are these paragraphs distributed? - Which paragraphs advance the plot, which
> paragraphs are transitional buffers, and which paragraphs are foreshadowing/creating
> suspense?"

Record the function type of each segment. The distribution is clear, and the rhythm and
function of the paragraph are determined.

**Ask readers again to get:**

> "What will the reader take away from this chapter?,a new piece of information, a
> relationship advancement, or an emotional release? Which paragraph should I put it
> in?"

Reader acquisition is the "what to give the reader" dimension of the chapter outline. At
least one for each chapter, and one for transitional chapters.

**Two final questions:**

> "What is the total number of words in this chapter? The default is 2500. Do you
> think it is enough? Does it need to be adjusted?"

> "What new hooks are there to bury in this chapter? In addition to fulfilling the old
> hooks, are there any new clues/suspense to be put in? In which paragraph?"

**Frequently asked questions and solutions:**

| What the author says | Questions | How to connect |
|--------|------|------|
| "Just one scene, survey site" | Too rough, a big scene contains multiple narrative beats | "How many beats are there in the survey site itself? First glance after entering the door → bed → refrigerator → bathroom → sticky notes, each beat is divided into a story strip, about 5 strips" |
| "Write about the survey first and then get targeted" | There are only two steps, and there is no transition in the middle | "How did you leave after the survey? Was there anything unusual when you left?" |
| "About 3-4 paragraphs" | Too short, one paragraph corresponds to 3-5 minutes | "The default limit for this chapter is 2,500 words. Each paragraph of 3-4 paragraphs requires six to seven hundred words, which is too thick. Let's break it down a little more - for example, the 'inspection site' paragraph you mentioned can be broken down into knocking → entering the door → bed → refrigerator → bathroom → sticky notes, 5-6 story strips" |
| "The number of words is not important" | Without a goal, writing is boundless | "I don't want to be precise, the approximate amount is about 2500, if it is too long or too short, I will adjust it next time" |
| "Just help me plan it" | Leave it all to AI and lose the author's intention | "I will give you a suggested version first, and then you adjust it - this is your outline, not mine" |

**Output:** Outline summary (outline.summary, 1 sentence summary) + outline key points
(outline.key_points, the number of items is calculated backwards by word count - default
2500 words ≈ 5 items, each covering 2-3 minutes of story time + function type) + outline
appearance characters (outline.characters) + outline scene location (outline.location) +
outline time (outline.time) + Outline perspective (outline.pov, POV character of this
chapter - select within the perspective type settings/writing-style.md
narrative.perspective, the default first protagonist is limited POV) + reader
acquisition (micro_payoffs, at least 1 per chapter) + word count target + character
information status (knowledge_state).

> Key points are marked with `[function-type]` (promoting the plot/creating
> suspense/transition), and if there is dialogue, add `[dialogue]`: `[advance-plot / dialogue]`, `[build-suspense]`,
> `[transition]`.

For positive and negative examples, see §6 / Few-Shot examples (exploring key points,
dialogue embedding).

---

### 3. List of chapter contents

The content of the chapter outline is the core of the second step - record the
information of different dimensions of this chapter in 8 paragraphs. Together they are
the complete input for prompt word generation. Each paragraph answers a different
"What's in this chapter?"

**General Judgment:** After writing each paragraph, ask questions - "Is this information
complete? Can the prompt word generation be used directly?"

---

#### 1. Current task (current_task)

Record the "goal of this chapter" - not the theme feelings, but the advancement actions
that should be completed.

**What to write:** One sentence: The specific actions to be promoted in this chapter +
what relationship it has to which story line.

**How to talk:** Extract from the outline. The outline breaks down the paragraphs, and
the current task is the common goal of these paragraphs.

> "After a few paragraphs of this chapter, what is the core pushing forward? Say it in
> one sentence."

If the author says "build suspense" or "advance the main plot", follow up with:

> "What specific things are used to build suspense/advance the main line? Write the
> things into the current task (current_task), and leave the feelings to the reader's
> expectation (reader_expectation)."

```
✅ Qualified:
"Establish Lu Zheng's character image and daily work status, and introduce the main case through Su Mo's entrustment"
→ Main line Qidian: daily + commission + case introduction

"Through on-site investigation, we are advancing the investigation of the case, and clues gradually point to the fact that Su Tang did not leave on his own initiative."
→ Plot direction: Investigation → Overturning the police conclusion

❌ Unsatisfactory:
"This chapter builds suspense"
→ What suspense is built? Through what? Incomplete information

"The protagonist continues to investigate the case"
→ What does "continue" mean? Investigate what? What was found? It’s as if I didn’t write it
```

---

#### 2. Reader expectations (reader_expectation)

Record the reader's current emotional state and how this chapter responds to that state.
This is the core of the chapter outline - it determines the emotional direction of the
chapter.

**What to write:** Three sub-fields - emotional state (state, the reader's current
mood), strategy (strategy, the processing strategy for this chapter), and detail
(detail, what the reader is waiting for).

**How to chat:** Read the previous chapter of the chapter outline document on emotional
design (emotional_design). Look at the emotional hook of the previous chapter and the
emotional gap that readers enter this chapter with.

> "What mood did the reader feel at the end of the previous chapter? For example,
> 'curious where Su Tang went', 'nervous that Lu Zheng was being targeted'."

> "Then how should we deal with this emotion in this chapter? - Give some progress and
> be satisfied, should we suppress it and not give it, or should we give it a little
> first and then create bigger doubts?"

> "Specifically, what are readers waiting for? Who is waiting for, waiting for a
> certain truth, waiting for a confrontation? Name specific people/things/things."

**If the author says:**
- "Readers are looking forward to the content of the next chapter" → Taixu, Zhui: "Which
  reader has which specific expectations? Specific to people/things/things"
- "Whatever, you decide" → Unable to decide on your behalf: "I'll suggest a version
  first, you see if it's right - if not, we'll adjust it"

```
✅ Qualified:
state: "Curiosity - the end of the previous chapter left a suspense, the reader wants to know where Su Tang went"
strategy: "Create a new gap"
detail: "Readers expect progress in the investigation - the first half of the chapter gives progress (details of conflicts in the room), and the second half creates new questions (who is the man downstairs?)"
→ Emotional rhythm: the first part satisfies expectations and the second part creates new suspense

❌ Unsatisfactory:
state: "Looking forward to"
strategy: "Maintain suspense"
detail: "Readers are looking forward to the content of the next chapter"
→ Three rows are all empty - what to expect? What suspense is maintained? It’s as if I didn’t write it
```

---

#### 3. Payoff plan (payoff_plan, news/hook management)

Record the treatment of hooks in this chapter - which old hooks are fulfilled, which new
hooks are buried, which suspense must be suppressed and cannot be touched, and which
clues are pushed but not closed.

**What to write:** Three lists - must be resolved (must_resolve, the old hook that is
fulfilled in this chapter), must be suppressed (must_hold, the suspense that must not be
touched), advance without closure (partial_advance, the old clue that is advanced + the
new hook that is laid). No need to number, just describe it in plain English.

**How to talk:** Read the outlines of the previous chapters - which old hooks are still
hanging, which ones should be closed, and which trump cards are too early to be
revealed. Let’s ask about the new hook of this chapter.

> "What threads have been buried in the past that have not yet been confiscated? Is
> there anything that should be collected in this chapter? - Write these into
> must_resolve."

> "What things must not be touched now,things that can't be taken back once they're
> revealed?,Write these into must_hold."

> "Which old clues can be pushed but not fully illuminated? How much? - 'Let the
> reader know there is a connection' or 'Let the protagonist feel vaguely wrong'?"

> "Are there any new hooks to bury in this chapter?,New clues, new suspense, hints of
> new characters' appearances? These are written in partial_advance (advance but not
> end)."

**If the author says:**
- "Just make your arrangements" → Don't lay the hook: "I'll list a few candidates first
  and see which ones meet your expectations."
- "No old hooks, this chapter is brand new" → verify: "Are you sure there aren't any old
  clues to advance? Leave it blank for now."
- must_resolve and must_hold write about the same thing → Contradiction: "These two
  conflict - should we accept or hold?"

```
✅ Qualified:
must_resolve: [] # Chapter 1, no old things to collect
must_hold: ["Cannot reveal the reason why Lu Zheng left the police force"]
partial_advance:
  - "Planting the suspense of the main plot - Su Tang disappeared, the police determined that he left voluntarily, but the details are contradictory"
→ The status of the hook is clear: press what should be pressed, and plant what should be planted.

❌ Unsatisfactory:
partial_advance:
  - "Advance the main line"
→ "Push" is too vague - pushing by a millimeter is also pushing, and directly closing is also pushing.

must_resolve: ["Reveal the truth"]
must_hold: ["Reveal the truth"]
→ The same thing needs to be both collected and suppressed - logical contradiction
```

---

#### 4. Transition functions (downtime_functions)

Non-conflict passages are not "rests" - each transitional scene must have a clear
narrative function. Paragraphs that do not function should not exist.

**What to write:** Each `[paragraph-position / scene] → [function]`. Functions must be specific actions.

**How to talk:** Pick out the non-conflicting paragraphs from the outline and ask
questions paragraph by paragraph:

> "What will be the impact of removing this section?"

Delete it if it doesn't affect it. If the author says "adjust the rhythm" or "make a
transition", follow up with:

> "While adjusting the pacing, can we do other things in this paragraph - such as
> foreshadowing, showing the character's personality, and supplementing information?"

**If the author says:**
- "It has no function, it just adjusts the rhythm." → Reply: "Paragraphs that purely
  adjust the rhythm for more than one paragraph are just watering down. Add a function
  to it - even if it just allows readers to see one side of the character."
- "This paragraph is about showing daily life" → Chasing: "Which aspect of daily life? -
  work status, character background, or relationship atmosphere?"

```
✅ Qualified:
- "The opening office scene → establish Lu Zheng's daily status and character background"
- "Description of the environment on the road → The contrast between Nan'an New District and the old city hints at the two sides of the city"

❌ Unsatisfactory:
- "Transition Paragraph" → No functional mapping, this paragraph has no reason to exist
- "Daily description" → too vague, you can write a page about daily life and also advance the plot
```

---

#### 5. Key choices (key_choices)

The character's important choices in this chapter must be examined,why they were made,
do they fit the character, and will they feel jarring to the reader.

**What to write:** Each entry includes what choice the character made + why + why it
fits the character + verification of readers’ feelings.

**How to chat:** Read the character file (world view/self-positioning/values) and
determine whether the choice grows naturally from the setting.

> "This chapter xxx has to make the decision YYY. Why? Is it profit-driven or
> emotion-driven?"

> "Does this fit with his previous character design? - If the author says 'in line
> with', ask 'Which specific setting supports this choice?'"

> "What will readers think when they see this choice? Do they think 'of course he
> would do that' or 'why did he suddenly change'?"

**If the author says:**
- "Plot necessity" → Reply: "Plot necessity is not a reason. Why does the character make
  this decision? Look for his inner motivation, not the plot's motivation."
- "This is his personality" → Chase: "Which specific personality? Please quote me the
  description in the character file."
- "The reader will not find it abrupt" → Verification: "Is it because the previous
  foreshadowing is enough, or is it because the chapter itself explains it?"

```
✅ Qualified:
- "Why did Lu Zheng take the case? - Partly because he needed income to keep the office running, and partly because the address Su Mo said was not found, which made him feel that the police were sloppy. In line with his character: not rush to judge, trust the details."
→ It’s not passion or sympathy, it’s professional vigilance + practical needs

- "Why did Fang Yan warn Lu Zheng privately? - He feels guilty for Lu Zheng, but he doesn't want Lu Zheng to cause trouble and harm himself. The contradictory choice is in line with the character."
→ There is guilt and self-protection, not just "good people helping"

❌ Unsatisfactory:
- "The protagonist chose to investigate"
→ Why investigate? What driver? Does it fit the personality? No answer at all - it means no writing
```

---

#### 6. Role information status (knowledge_state)

Record what the characters in this chapter know and what they don’t know. The
information gap is the fuel for suspense and conflict - who has more information and who
is kept in the dark directly determines the power structure of this chapter.

**What to write:** List of "know/don't know" for each character who appears +
**Information Gap Relationship** (information asymmetry between characters/character and
reader) + **Information Gap Change** (what the information gap changes to in this
chapter).

**How to chat:**

> "Who are the characters in this chapter? - What does Lu Zheng know now and what
> doesn't he know? What does the man in gray short sleeves know?"

> "Is the information between the reader and Lu Zheng equal? What the reader knows but
> Lu Zheng doesn't know? Or is it the other way around?"

> "How do the information gaps change in this chapter?,What information gaps are
> largest at the beginning? What new information gaps appear at the end?"

> "Is there any dialogue in this chapter? Which paragraphs are there? Who are the two
> parties involved in the dialogue? What information is advanced by the dialogue?"

**If the author says:**
- "Everyone knows" → red flag. Full knowledge = zero information gap = no conflict fuel
  in this chapter. Follow-up: "Think again, is there something that at least one of the
  characters doesn't know?"
- "The reader knows as much as the protagonist does" → OK. But make sure the reader is
  brought into the protagonist’s perspective

**Output:** List of what the characters know/don't know + information gap relationship +
**Information gap change** (opening→end) + dialogue markers (marked with `[dialogue]` in key
points)

```
✅ Qualified:
Checklist:
  Lu Zheng: I know that Su Tang is missing and did not leave voluntarily / I don’t know whose phone number the sticky note belongs to, and I don’t know the identity of the man in gray short sleeves
  Man with gray short sleeves: I know Lu Zheng is investigating the case/I don’t know what Lu Zheng found out

Information gap relationship:
  / The man in gray short sleeves knows that Lu Zheng is investigating Su Tang’s case ↦ Lu Zheng does not know the identity of the other party ⬅ The source of suspense in this chapter
  / The reader saw the man in gray short-sleeves following him ↦ Lu Zheng didn’t notice ⬅ Create tension

Information gap changes:
  Opening: The protagonist doesn’t know where Su Tang has gone ↦ The reader is the same as the protagonist
  Middle section: The protagonist discovers contradictory details ↦ The information gap is narrowing
  Ending: The villain knows that the protagonist is investigating ↦ The protagonist does not know the identity of the opponent ⬅ The new information is poor, driving the next chapter

Dialogue: None (One-man Show Exploration Chapter)

❌ Unsatisfactory:
"The characters all know what to do"
→ It’s not information status, it’s plot judgment
```

---

#### 7. Chapter end changes (required_changes)

Something must change by the end of this chapter. Nothing changes at the end of the
chapter → This chapter shouldn't exist.

**What to write:** 1-3 specific changes, each marked with the type of change
(information/relationship/physical/power) + what it changed from.

**How to chat:** Push from the current task (current_task).

> "This chapter is to complete the task of XXX. At the end, what is different from the
> beginning? - Who knows what? Who's relationship with whom has changed? In what ways
> is the protagonist different?"

If the author says "the investigation progressed" or "the relationship changed", follow
up with:

> "What does 'advance' specifically mean? From 'not knowing' to 'knowing' something?
> From 'trust' to 'suspiciousness' or from 'strangeness' to 'cooperation'? Explain
> 'what becomes what'."

```
✅ Qualified:
- "Information changed: Lu Zheng (and the reader) knew the basic facts and several doubts about Su Tang's disappearance"
- "Threat introduction: The man downstairs is staring at Lu Zheng - the investigation is being targeted."

❌ Unsatisfactory:
- "There is progress in the investigation" → What progress? What do you know? No new information = no changes
- "Relationship changes" → Who and whom? From what to what? All empty
```

---

#### 8. Scene cards (scene_cards)

Scene breakdown of this chapter - each chapter is composed of **2-5 scene cards** (the
chapter level of the scene cards is separated from the volume outline), and each scene
card has three pieces of information (three elements):

| Field | Meaning | Description |
|------|------|------|
| **What the protagonist wants to do** | Goal - what the protagonist wants to achieve in this scene | Even passive scenes have a purpose ("survive", "figure it out") |
| **What's blocking him** | Obstacle - what is the obstacle | People to people, things to things, heart to heart |
| **Is there any suspense that makes readers want to keep reading** | Hook - why readers care about this paragraph | From emotional anchor point + information gap |

**How to talk:** Merge the scenes from the key points (outline.key_points) and confirm
the three elements scene by scene.

> "This chapter has N scenes? - In each scene, what does the protagonist want to do,
> what stops him, and why does the reader want to read on?"

**The corresponding relationship with outline.key_points (the caliber is the same as the
scene card in skills/chapter-outline.md): ** Each key point corresponds to a scene card,
and the underlying logic is consistent with the outline - the three elements of the
scene card are mapped to the three anchor points of the key point:

```
Three elements of scene card → reflected in key points
  What does the protagonist want to do → Action anchor (what exactly does the character do)
  What's blocking him → Judgment anchor point (what obstacles the character encounters/what contradictions he finds)
  Is there any suspense that makes readers want to read on → Emotional hook + information gap in the full text
```

**Consumer:** When prompt-crafter assembles "Input / Scene Raw Materials", the core
events (external event chain) are extracted using the three elements of the scene card,
and are not extracted directly from outline.key_points.

**If the author says:**
- "Just one scene" → Ask and break it down: "Are there any changes of location/time
  jump/emotional transition in this scene? If so, just break it up. There are 2-5 scene
  cards in one chapter."
- "No need to separate scenes, just write directly" → Reply: "The scene card determines
  the scene raw materials of the prompt words. Without splitting the prompt-crafter, it
  is impossible to inject weights and techniques according to the scene."

```
✅ Qualified:
Scene 1 (Inspection / Inside the House): What does the protagonist want to do - find out the doubts about Su Tang’s departure;
  Stop him - the door is not locked, the room does not look like he left the room voluntarily (conflicting details);
  Suspense - what clues are hidden in this room?
Scenario 2 (Leaving / Being Targeted): What does the protagonist want to do - leave normally without being noticed;
  Stopping him - the figure in the carport, the man in gray short sleeves; the suspense - who sent the person targeting Lu Zheng

❌ Unsatisfactory:
Scene 1: Investigation site → only the event without the three elements
```

---

### 4. Emotional design (emotional_design)

Record the emotional parameters of this chapter. The emotional design is divided into
two levels: **The position of this chapter in the emotional trend of the volume** +
**The internal emotional trend of this chapter**.

**How to chat:** Chat in two steps - first decide the location, then decide the content.

**Step 1: The emotional trend of the inheritance volume**

The outline of the volume determines the emotional direction of the entire volume (such
as "depression → suppression → promotion → face-slapping → pretentiousness"). First
confirm which step of the arc this chapter is in:

> "Where is Juan's emotional direction now? - Is this chapter in the middle of the
> repression stage, or is it in the face-slapping release stage?"

The emotional tone of the chapter is determined by the arc position of the volume:
- The first part of the depressive stage → the tone is "building a dilemma" and the mood
  falls into depression/uneasiness
- The second stage of the repression stage → the tone is "escalation of oppression", and
  the mood falls into more depression/angry
- Turning point → The tone is "discovering a turning point", and the mood falls on
  expectation/shock
- Release stage → The tone is "anti-kill/show", and the mood falls on
  refreshment/satisfaction

> "The main emotional color of this chapter is called {primary_mood}. Follow this
> tone, right?"

**Step 2: Design the emotional trend within the chapter**

After the position is determined, the chapter cannot have one emotion going to the end -
there must also be a slight arc within the chapter:

> "How does the reader's emotion change from beginning to end of this chapter? - What
> emotion does it start with, what happens in the middle, and what emotion does it end
> with? At least three steps."

Chapter direction = a microcosm of volume direction. The depressive stage does not mean
that the entire chapter is depressed - there can be a micro-arc of "calm → uneasiness →
confirmation of dilemma" within the depressive chapter.

```
Curl direction: Depressed → Depressed → Enhanced → Face-slapping → Pretentious
               ↑
Position in this chapter: The second "depression"

Internal micro-arcs in this chapter:
  Calm (beginning with daily life) → uneasy (finding an abnormality) → depressed (confirming the dilemma)
  → Anger (escalation of oppression) → Powerlessness (end of chapter)
```

**Step 3: Verify consistency**

Check whether the directions of the two layers are self-consistent:

> "Does the end of the micro-arc inside this chapter support the next step in the
> direction of the volume?" - At the end of the depressive chapter, the reader should
> be "more depressed/angry", and then have the motivation to follow and enter the
> improvement stage of the next chapter., If the reader is "happy" at the end of the
> depressive chapter, the direction of the volume is broken.

#### Field filling guide

| Fields | How to Chat | Filling Standards | Common Errors |
|------|--------|---------|---------|
| Main mood (primary_mood) | "What is the main mood of this chapter? - Choose the most precise word" | A precise mood word (curious/nervous/depressed/refreshing/warmth/sad/angry/relieved) | "Complex" or "mixed" - means no choice |
| Emotional trend (mood_progression) | "How does the micro-arc in this chapter go? - What emotion does it start with, why does it turn in the middle, and what emotion does it end with? At least three steps, each step is followed by a specific event" | The current section of the volume trend → Micro-arc within the chapter (A → Event → B → Event → C), the ending point of the chapter supports the next step of the volume | "Suppress first and then advance" - there are only two nodes with no intermediate transition; or there is a conflict between the ending point at the end of the chapter and the next step in the direction of the volume (for example, the reader is no longer depressed at the end of the depressing chapter) |
| Intensity peak (intensity_peak) | "Which paragraph has the strongest emotion? - Not the 'end', but which moment in which paragraph" | Specific to the key point or scene | "End" - no specific paragraph |
| Intensity level (intensity_level) | "Compared with the previous chapter, is the intensity of this chapter higher or lower? The difference between adjacent chapters does not exceed 2" | 1-10 number, the difference from adjacent chapters is ≤ 2 | Fill in 7 for each chapter or 3 for each chapter - no change |
| Emotional hook (emotional_hook) | "What is the emotion left in the reader's heart at the end of the chapter? - Not the type word, but the specific person/what kept the reader awake" | Emotional type + specific content | "Suspense" - what kind of suspense? What creates suspense for readers? |

**If the author says:**
- "The trend of emotion is to first suppress and then to increase." → There are only two
  steps, which is not enough: "There is a lack of transition in the middle. What
  transition happened from depression to elevation? Which specific event caused the
  emotion to turn?"
- "Let's fill in 5 for the strength level" → I fill in 5 every time because I don't
  think about it: "Compared with the previous chapter? Is it stronger or weaker than the
  previous chapter? How much worse?"

#### Readers get (micro_payoffs, formerly "micro payoffs")

At least 1 reader gain per chapter - what readers take away from reading the chapter.
There must also be at least 1 transition chapter.

**How to chat:** (Direction confirmation has been asked, just confirm the record here)

> "The reader just mentioned, please confirm the type and position - should it be
> placed in the front, middle or back paragraph?"

**If the author says:**
- "This chapter is mainly a transition, there is nothing to give." → Reply: "The
  transition chapter must be gained by the reader - otherwise the reader will feel that
  'nothing happened' after reading it. Even if it is just 'confirmation of a certain
  character trait of the protagonist', it is considered information gain."

| Field | Filling criteria |
|------|---------|
| Type (type) | Information (info, new clues/new information)/Relationship (relationship, relationship promotion)/Emotion (emotional release)/Clue (clue, foreshadowing recovery)/Ability (ability, ability display)/Resource (resource, obtain items)/Recognition (recognition, obtain recognition) |
| Description | Specific event: what the reader obtained, not "obtaining information" |
| Location (location) | Front/middle/back paragraph - don’t put it at the end of the chapter, don’t compete with the emotional hook (emotional_hook) for position |

---

### 5. Intra-Chapter Conflict Ladder

The conflict ladder and the emotional trend are in the same pattern - the first volume
determines the overall ladder, the chapters inherit the levels, and there are also small
ladders within the chapters**.

#### Design Method

**Step 1: Inherit the volume level**

Confirm this chapter's place in the volume conflict ladder:
- Level 1 / Introduction → The obstacles in this chapter are mainly about information
  acquisition/exploration, and do not involve life and death duels.
- Level 2 / Upgrade → The obstacles in this chapter are mainly external resistance, and
  the protagonist begins to bear the price
- Level 3 / Turning → The obstacles in this chapter are mainly losses/setbacks, and the
  situation has fundamentally changed.
- Level 4 / Ultimate → The obstacles in this chapter are mainly head-on confrontations,
  and all conflicts break out together.

**Step 2: Design small steps within the chapter**

A certain level of the volume cannot be completed with one obstacle - there must also be
progression within the chapter. Break a chapter into 2-3 ascending obstacles:

```
Volume Ladder→This chapter is on level 2 / Upgrade
Small steps within the chapter:
  Testing (Scene 1) → The protagonist tries to make contact and finds that the other party is defensive ← Getting Started
  Encounter (Scene 2) → Protagonist is warned/blocked, confirmation of resistance ← Upgrade
  Conflict escalates (scene 3) → The protagonist persists in the investigation, and the other party increases pressure ← Climax in the chapter
  Point at the end of the chapter: The protagonist's situation becomes more dangerous → The next step of the support volume (Level 3 Turning)
```

**Step 3: Verify the landing point at the end of the chapter**

> "Does the situation of the protagonist at the end of this chapter lead to a higher
> Qidian in the next chapter?", If the situation of the protagonist at the end of this
> chapter is similar to that at the beginning → There is no advancement in the ladder
> within the chapter, and there are not enough obstacles.

#### Correspondence between the ladder and key points in the chapter

Each step of the small ladder within the chapter corresponds to one or more key points
(outline.key_points). The "judgment anchor point" of each key point is the
information/situation changes brought about by the obstacles in this step:

```
Volume Conflict Ladder: Level 1 Getting Started → Level 2 Upgrading → Level 3 Transition → Level 4 Ultimate
                              ↑
Level of this chapter: Level 2 / Upgrade
                              ↓
Small ladder within the chapter: temptation → encounter → conflict escalation
                              ↓
Key point mapping: 1-2 → 3-4 → 5-6 (2 key points per step)
              Test scene, encounter scene, upgrade scene
```

#### Acceptance

- [ ] **The small staircase in the chapter has 2-3 steps** - not just one obstacle, nor
      is it divided into 5 steps to make up the number
- [ ] **Each step is more difficult than the previous step** - Scenario 2 is more
      confrontational than Scenario 1, and Scenario 3 is more severe than Scenario 2
- [ ] **The next step of the landing point support volume at the end of the chapter** -
      After the obstacle is upgraded, the protagonist's situation has changed, and there
      will be a higher Qidian in the next chapter
- [ ] **The judgment anchor point of the key point corresponds to the ladder step** -
      each obstacle has a specific "action → discovery → judgment" beat in the key point

---

## Feng Gu Layer - "What cannot be written into the outline of the chapter"

The character level decided that the chapter has no AI flavor. In the chapter outline,
if "this chapter is about", "the protagonist experienced", "Y is revealed through Here's
a quick look at deadly patterns and empty words.

### 6 Deadly Modes

| # | Pattern | Scan position | Hit examples | After correction |
|---|------|---------|---------|--------|
| 1 | God's Perspective Overview | Outline, Content List / Current Tasks | "This chapter tells the story of Lu Zheng entering the rental house to inspect" | "Lu Zheng entered the rental house to inspect. The moment he opened the door, he smelled the smell of leftover food" |
| 2 | Abstract psychological summary | Content list / Reader's expectations, key choices | "He felt uneasy" | "He closed his notebook and pushed the door open" |
| 3 | Analytical conclusion | Content list / Reader expectations, chapter end changes | "This shows that the case is more complicated than imagined" | Only write "what has changed", not "what does this mean" |
| 4 | Literary criticism | Content list / Current tasks, transitional functions | "The professional ability of the protagonist is demonstrated through meticulous observation" | "Lu Zheng noticed that the bed was unmade, the charger was still on the wall, and there were leftovers in the refrigerator" |
| 5 | "Not but" sentence pattern | Content list all fields | "He is not angry, but disappointed" | Just write "He is disappointed". If you must use contrast, break it into two sentences |
| 6 | Abstract tags | Content list / Current tasks, chapter end changes | "Relationship progression" "Conflict escalation" "Character growth" | "The relationship between Lu Zheng and Fang Yan changed from mutual distrust to exchange of information" |

### Empty adjective quick check

| Category | Hit word | Modification |
|------|--------|------|
| Empty adjectives | Wonderful, tense, interesting, good, shocking, touching, profound | Delete and change to a verifiable description - "nervous" → "He saw the man's hand in his pocket in the rearview mirror" |
| Abstract adverb | profoundly, fully, vividly, perfectly | Delete all |
| Words of degree | Sufficient, sufficient, appropriate, to a certain extent | Change the specific quantity or range |

---

## What not to do - hard red line

Record the things you absolutely cannot touch in this chapter. It's not "it's best not
to", it's "scrap it if you do it".

**What to write:** Specific prohibited scenes or actions, format: "Don't do Y thing in X
scene" or "Don't have X character do Y thing." Must be verifiable.

**How to talk:** Progressive accumulation of constraints from the outline to this
chapter.

> "What are the things that absolutely cannot be touched in this chapter? - Which
> settings cannot be revealed yet, which characters cannot appear yet, and which
> relationships cannot be revealed yet?"

**If the author says:** "Don't procrastinate" or "Keep it tight", type back:

> "Hard constraints (prohibitions) are 'not to do', not 'to do'. Be specific - who is
> not allowed to appear? What information is not revealed? What scenes are not allowed
> to happen?"

```
✅ Qualified:
- "Don't reveal the detailed reasons why Lu Zheng left the police force three years ago - just hint through the details that he was a criminal police officer before."
→ Verifiable: Scan keywords such as "three years ago" and "left the police force"

- "Don't let the man downstairs talk to Lu Zheng - just create pressure through your eyes and atmosphere."
→ The body can be written and the atmosphere can be written, but the dialogue is the red line

❌ Unsatisfactory:
- "Don't be too procrastinating" → How is procrastination considered? no judgment criteria
- "Keep the tension" → This is not a prohibition, it is an expectation
```

---

## After completion - acceptance process

After writing the chapter outline, follow the following steps for acceptance. Prompt
words will be generated only after all are passed.

### Step 1: Show it to the author

Arrange the main points of the chapter outline in the following format and give it to
the author. Don’t lose the original text, make the summary readable:

> 📋 **Chapter N Outline Feedback** **Book Location:** Volume N / Total? Volume /
> Chapter M / Total? Chapters **Positioning of this chapter:** The role of this
> chapter in this volume (one sentence) **Connection to the previous chapter:** Where
> did the last chapter end? → Where does this chapter start? **Main content:** What
> happened in this chapter (2-3 sentences) **Key Scenes:** - Scene One (Character:
> List of Appearing Characters) - Scene Two (Character: List of Appearing Characters)
> -... **Key Dialogue:** Yes/No. Others indicate who and whom and about what
> **Conflict Progress:** This chapter advances what conflicts are interpreted and what
> progress is accomplished **Word Count Goal:** NNNN words

After the author reads the feedback, he must be able to say "Yes, that's it" to be
considered qualified.

**If the author says:**
- "Almost", "Write as you see", "OK" → do not count as passing. Ask specific questions:
  "Which point do you think is OK? Which point are you not sure about?"
- "I want to adjust this section" → Let him adjust it, and confirm again after adjusting
  it.
- "Overall OK" → passed. Go to next step

**Passing conditions:** The author clearly says "yes" or "yes" or nods to confirm.

### Step 2: Go through the checklist yourself

Check the following list item by item. If any item is unqualified → return for
modification, otherwise you will not be able to proceed to the next step.

- [ ] **Word Count Target** Confirmed (default 2500, author can adjust), author’s
      informed consent
- [ ] **Paragraph distribution** Confirmed: which paragraphs advance the plot, which
      paragraphs are transitions, and which paragraphs are foreshadowing/creating
      suspense
- [ ] **Reader Earns (micro_payoffs)** At least 1, the author knows what the reader will
      take away after reading
- [ ] **Outline key points (outline.key_points)** Each item corresponds to a paragraph,
      and the author can say "what scene is written in this paragraph"
- [ ] **Scene cards (scene_cards)** 2-5 per chapter, each card has three elements (what
      the protagonist wants to do/what’s blocking him/what suspense) are complete,
      corresponding to the three anchor points of the key points
- [ ] **Old hooks cashed out** Recorded (must_resolve wrote which old hooks are resolved
      in this chapter)
- [ ] **New hook buried** Recorded (partial_advance contains newly buried suspense/clues
      in this chapter)
- [ ] **Current task (current_task)** Does not contain abstract labels, does not contain
      God's perspective overview, and is executable
- [ ] **Reader Expectation (reader_expectation)**’s emotional state/strategy/specific
      instructions are all valuable, and the specific instructions are specific to
      people/things/things
- [ ] **Cash-out plan (payoff_plan)** The three lists are complete (the empty list is
      explicit `[]`), and the specific advancement method is written if the advancement
      is not closed.
- [ ] **Transition functions (downtime_functions)** Each item has `[scene] → [function]` mapping
- [ ] **Key_choices** Each answer answers "Why do you do it + Does it fit the character
      + Does the reader find it awkward?"
- [ ] **Character information status (knowledge_state)** What each character
      knows/doesn’t know has been recorded
- [ ] **Information gap relationships** have been marked with the format "What {} knows
      ↦ {} doesn't know" - at least one pair of relationships
- [ ] **Changes in Information Difference** Marked - What information is different at
      the beginning, what new information is different at the end, and there is a
      dynamic process in the middle
- [ ] **Information gap changes serve the volume arc** - The new information gap at the
      end of this chapter is a step forward in the volume Qidian→end arc
- [ ] **Dialogue mark** Key points are marked `[dialogue]`, and those without dialogue are
      marked "No dialogue"
- [ ] **End of chapter changes (required_changes)** 1-3 items, each item has a change
      type + "from what to what"
- [ ] **Hard constraints (prohibitions)** Each item can be verified (can be checked
      after the text is written), and does not contain abstract taboos
- [ ] **The direction of the emotional inheritance volume in this chapter** - The tone
      of the chapter in the repression stage is depression/uneasiness, and the tone of
      the chapter in the release stage is excitement/satisfaction, which is not
      contradictory.
- [ ] **Intra-chapter micro-arc (mood_progression)** At least three nodes (A→B→C), with
      causal anchors between nodes
- [ ] **The landing point at the end of the chapter supports the next step in the
      direction of the volume** - At the end of the depressive chapter, the reader
      should be "more depressed/angry" so that he or she has the motivation to enter the
      next chapter.
- [ ] **This chapter’s level inheritance volume conflict ladder**, No life-and-death
      showdown at the entry level, no easy transition at the ultimate level
- [ ] **Intra-chapter 2-3 steps** - Not a single obstacle, nor too many steps to make up
      the number
- [ ] **Each step in the chapter is more difficult than the previous step** - The
      intensity of obstacles between scenes is progressive, not repeating the same
      confrontation
- [ ] **Intensity peak (intensity_peak)** Specific to the scene, not the "end"
- [ ] **Intensity level (intensity_level)** The difference from the adjacent chapter is
      no more than 2
- [ ] **Emotional_hook** has specific content (who/what/what suspense)
- [ ] **Micro_payoffs** At least 1, type/description/location all have values
- [ ] **The full text of the chapter outline contains no summary from God's perspective,
      no analytical conclusion, no literary criticism, no "not but" sentence structure,
      and no empty adjectives**

### Step 3: A quick sniff

Cover up the outline and see if you can tell from memory:
- How many stories are divided into and what scenes are written in each story?
- What each character knows and doesn’t know
- Which old hooks have been cashed in and which new hooks have been laid?

Can't tell → The outline of the chapter is not dense enough, please fill in the details.

### Step 4: AI flavor self-test

Use Feng Gu Layer's "Six Fatal Modes" and "Empty Adjective Quick Check" to scan the full
text. Hit any one → modify it before generating prompt words.

---

## 4. Fanqie decision-making Guidance

When filling in the chapter outline, take the initiative to ask the author these
questions. **The author is not asked to go to fanqie.md himself, but the AI actively
asks. **

### Question list

| Question | Trigger Timing | Output Field |
|------|---------|---------|
| "What kind of immersion method is used in this chapter? (Familiarity/label/conflict urgency/grounding)" | After the direction is confirmed | memo.immersion_type |
| "The emotional curve of this chapter: pressure→X→Y→explosion?" | emotional_design ago | mood_progression |
| "What type of satisfying payoff is this chapter? (face-slapping/growth/reversal/ambiguity/desperate comeback) where is the foreshadowing/release?" | memo filling | payoff_plan + micro_payoffs |
| "Is there a copy? What type and what are the core events?" | outline when split | outline.scene_type |
| "What is the conflict point between the two protagonists/CP in this chapter?" | Character status | key_choices |
| "What abilities does golden finger show in this chapter?" | When memo is filled | memo.gold_finger |
| "What is the 'reason why' the protagonist of this chapter cannot give in?" | Conflict design | key_choices.conflict_motivation |

### Guiding Principles

- **Cannot make decisions on your behalf**: "You say it first, I will say it" - the
  final decision rests with the author
- **Must be specific**: "Which paragraph is the slowest" rather than "Pay attention to
  the rhythm", "Which scene" rather than "Pay attention to the character"
- **Blank answer to return**: The author said "you watch and write" → "I list the
  candidates for you to see and you choose one"

### Description of the sense of substitution method (for the author’s reference)

| Method | Applicable scenarios |
|------|---------|
| Sense of familiarity | Scenes that readers have experienced (examination/graduation/workplace) → natural substitution |
| Tags | Personal tags + small flaws + memory points (birthmarks/mantras/habits) |
| The conflict is urgent | The sense of crisis is full, and the readers are pushed away |
| Down-to-earth | Character shortcomings + vernacular description, imperfections are more approachable |

---

## 5. Example of complete chapter outline

The following is a complete chapter outline, covering all fields, taking Volume 1
"Missing" Chapter 2 as an example:

```
Volume number: 1
Chapter: 2
Title: Rental House

── Outline ──

Summary: Lu Zheng entered Su Tang's rental house to investigate and found many things related to "voluntary departure"
Conflicting details: I was followed and photographed when I left.

Key points:
1. [Advance the plot] Lu Zheng went to the door of the rental house → No one knocked on the door → Get the spare key →
   The key is inserted but not locked → open the door and take a quick look at the whole thing. Sunlight cuts through the window,
   The air smells of leftover rice. Sensory emphasis: sight + smell.
2. [Advance plot / investigation] Lifting the quilt → wrinkled sheets and indentations on the pillow;
   The charger is plugged into the wall and the cable hangs down to the bedside → there is residual warmth in the charging head when touched.
   Action chain: lift → look → touch. Don't write about "uncertain" mentality.
3. [Advancing the plot / Investigation] There is a crack in the refrigerator door→The leftover rice is not poured out, and the edge of the bowl is dry;
   There is a cup of water in the microwave that has not been taken out. Bathroom → The toothpaste cap is open and the towel is hanging wet;
   The wardrobe door was open and the suitcase was dusty. Comparative clues: Unlike someone who leaves voluntarily.
   List only the facts, not conclusions.
4. [Creating suspense] The sticky note on the bedside table → only has a phone number and the back is blank.
   Lu Zheng turned over and looked → took pictures. Note the rolled edge of the sticky note.
5. [Transition → Create suspense] Lock the door → Hold the key in your hand for a moment. A voice-activated light in the corridor turns on →
   Corner shadow. Going downstairs neither quickly nor slowly→The figure in the carport moved for a moment and then stopped.
   Exiting the community → A man in gray short-sleeved shirts leaned on a telephone pole and held up his mobile phone; Lu Zheng stopped to tie his shoelaces →
   The man has turned away. Lu Zheng did not look back. Camera tip: Lu Zheng didn’t know he was being watched.
   The two have no direct interaction.

Appearing characters: Lu Zheng, gray short-sleeved man (new appearance)
Scene location: Su Tang’s rental house in a low-rent housing community in Nan’an New District
Time: 2pm

── Chapter outline ──

Current task: Promote case investigation through on-site investigation, clues gradually point to Su Tang
Didn't leave voluntarily

Readers can expect:
- Emotional state: Curiosity - the reader wants to know where Su Tang went.
- Strategy: Create new gaps
- Specific instructions: Readers expect progress in the investigation,the first half of the chapter gives evidence
  (Conflict details in the room), the second half of the chapter creates new questions (Who is the man downstairs?)

Redemption plan:
- Must be resolved: None (Chapter 2 of the first case, no old business to settle)
- Must be suppressed: The reason why Lu Zheng left the police force cannot be revealed
- Pushing forward without closing:
  / Planting the suspense of the main plot - Su Tang disappeared, the police determined that he left voluntarily, but the details
    There is a contradiction
  / New hook: Who does the phone number on the sticky note refer to? Who is the man with gray short sleeves?
    Sent?

Transition functions:
- "Pause in the corridor → Transition line of character state: switch from concentration during investigation to alertness of being targeted"
- "The figure in the carport going downstairs → creates an intermediate layer of pressure before entering direct conflict"

Key decisions:
- "Why did Lu Zheng notice the contradictions in details? - He used to be a criminal policeman, and he is used to
  Observe details. "In line with the personality"

Role information status:
- Lu Zheng: I knew Su Tang was missing and found out that he didn’t leave voluntarily / I didn’t know about the sticky note
  Whose phone is it? I don’t know the identity of the man in gray short sleeves.
- Man with gray short sleeves: I knew Lu Zheng was investigating Su Tang’s case / I didn’t know Lu Zheng was investigating
  to what extent
- Information gap relationship:
  / The man in gray short sleeves knows that Lu Zheng is investigating the case ↦ Lu Zheng does not know the other party’s identity
  / Readers saw the man in gray short-sleeves following him ↦ Lu Zheng didn’t realize he was being followed
- Dialogue: None (One-man Show Exploration Chapter)

Chapter end changes:
- Information change: Lu Zheng (and the reader) knows that Su Tang did not leave on his own initiative
- Threat introduction: The man in gray short-sleeves targeted Lu Zheng,the investigation was noticed

Hard constraints:
- Don’t let the man in gray short sleeves talk to Lu Zheng,just create it through his eyes and atmosphere
  pressure
- Do not reveal the ownership of phone numbers on post-it notes

Scene card:
- Scene 1 (Inspection / Inside the House): What does the protagonist want to do - find out the doubts about Su Tang’s departure;
  Stop him - the door is not locked, the room does not look like he left the room voluntarily (conflicting details);
  Suspense - what clues are hidden in this room?
- Scenario 2 (Leaving / Being Targeted): What does the protagonist want to do - leave normally without being noticed;
  Stopping him - the figure in the carport, the man in gray short sleeves;
  Suspense - Who sent the person targeting Lu Zheng?

── Ladder of Conflict ──

Volume ladder level: Level 1 / Entry
  → This chapter focuses on obtaining information and building awareness, and does not involve direct confrontation

Small steps within the chapter:
  Exploration (Article 1) → Enter the site and find anomalies in the environment ← Getting started / Acquisition of information
  Contradictions found (Article 2-4) → Many contradictory details were investigated ← Upgrade and confirm doubts
  Being targeted (Article 5) → Found being followed when leaving ← Turning point / Change of situation
  → The ending point of the chapter: the protagonist goes from "uncertain" to "sure that something is going on", supporting the next step of the volume (upgrade: external resistance appears)

── Emotional design ──

Volume direction position: Level 1 (entry level) - the first stage of the repression stage
  →The tone of this chapter is "establishing a dilemma", and the main mood is curiosity/uneasiness

Micro-arc in the chapter: Calm investigation → Discovering contradictory details → Alert → Being targeted
sense of oppression
  → From calm to uneasy, the end point is "the sense of oppression of being targeted" - the next step in the direction of the support volume (escalation of depression)

Intensity Peak: Article 5 (when tracked is detected)
Strength level: 5
Emotional Hook: Suspense - Who is the man in gray short sleeves? Whose post-it phone number is it?

Readers get:
- Type: information (info) - Confirm that Su Tang did not leave on his own initiative
- Position: front section - middle section (2nd and 3rd key points)

Word count goal: 2500 words
```

> This chapter is a one-man show with no dialogue. For how to write key points in the
> dialogue version, see §6 / Few-Shot example (Example 4).


## 6. Few-Shot Example

The following positive and negative examples are used to guide the note writing of
key_point. **❌ Narrative style** = Mini text that is sensory filled for the writer; **✅
Note style** = Only the planning anchors are written, and the sensory filling is left to
the writer.

### 1. Key points in the dialogue: Fang Yan’s interview

❌ Narrative:

```
[Advance the plot and dialogue] Fang Yan asked Lu Zheng to meet at the teahouse and chose a corner seat. He first chatted a few words about the current situation, his tone was casual but his eyes were always observing. When Lu Zheng talked about Su Tang's case, Fang Yan put down his tea cup and lowered his voice by half a degree: "Don't touch this case." - It was not a discussion, but a warning.
```

✅ Note style:

```
[Advance plot / dialogue] Fang Yan asked Lu Zheng to meet in the corner of the teahouse. First talk about the current situation to test the tone. When Lu Zheng talks about the case → Fang Yan's tone turns lower → "Don't touch this case." Pay attention to Fang Yan's eye observation throughout the whole process. The power of dialogue lies with Fang Yan.
```

→ The note type saves time, environment rendering, placing teacups, etc., and only
writes the scene location + conversation intention + power relationship.

### 2. Key points in the dialogue: Su Mo’s interview

❌ Narrative:

```
[Advance the plot and dialogue] Su Mo sat in the reception room, twisting his backpack strap with his fingers. Lu Zheng handed him a glass of water, but she didn't take it and said, "My sister won't leave on her own." The voice was quiet, but firm,not to ask for help, but to make sure someone believed her.
```

✅ Note style:

```
[Advance the plot / Dialogue] Su Mo was twisting her backpack strap in the reception room, and Lu Zheng handed her water but she didn't take it → "My sister won't leave on her own." The voice is not loud but firm, not asking for help but seeking recognition. Pay attention to Su Mo's finger movements (nervous but restrained).
```

### 3. Key points in surveying: 5 items for renting a house (a one-man show for surveying)

❌ Narrative (extract the first 3 items):

```
1. [Advance the plot] At two o'clock in the afternoon, Lu Zheng stood at the door of Su Tang's rental house. No one answered the knock on the door, so he took the spare key from Su Mo. The sound of metal clashing was particularly loud in the corridor. The key was inserted into the keyhole and turned around - it didn't lock. He opened the door, and the sunlight cut a bright area on the floor. The air was a bit stuffy, with the smell of leftover food and dust. He stood at the door and did not rush in. He glanced at the whole place first.
2. [Advance plot / investigation] Lu Zheng lifted the quilt, the sheets were wrinkled badly, and there were indentations on the pillow. The charger is plugged into the wall and the cord hangs down to the bedside. He reached out and touched the charging head - it was still warm.
3. [Advancing the Plot / Investigation] Lu Zheng opened the refrigerator door. He did not pour out the leftover rice, but worked around the edge of the bowl. He walked into the bathroom, with the toothpaste cap open and the towel hanging wet. The wardrobe door was open and the suitcase was dusty.
```

✅ Note style:

```
1. [Advance the plot] Lu Zheng arrived at the door of the rental house → No one knocked on the door → Take the spare key → Insert the key without locking it → Open the door and take a quick look at the whole room. Pay attention to the emptiness of the sound of metal clashing in the corridor; the sunlight cuts through the windows and the air smells of leftover food. Sensory emphasis: sight + smell.
2. [Advance plot / investigation] Lift the quilt → wrinkled sheets and indentations on the pillow; plug the charger into the wall and hang down to the bedside → there is residual warmth when touching the charging head. Action chain: lift → look → touch. Don't write about "uncertain" mentality.
3. [Advancing the plot and investigation] There is a crack in the refrigerator door → The leftover rice is not poured out, the edge of the bowl is dry; there is a cup of water in the microwave oven that has not been taken out. Bathroom → The toothpaste cap is open and the towel is hanging wet. Comparative clues: Unlike someone who leaves voluntarily. List only the facts, not conclusions.
```

→ The note type uses `→` to connect the action chain. It only marks the sensory focus
and does not provide sensory filling for the writer. The judgment anchor point uses
behavioral responses instead of abstract psychology.

### 4. Dialogue embedding (dialogue beats inserted into the exploration chapter)

> In the complete chapter outline example, item 1 is replaced by a dialogue beat, and
> other exploration beats remain unchanged:

❌ Narrative:

```
1. [Advance plot / dialogue] At two o'clock in the afternoon, Su Mo was sitting in the reception room of Lu Zheng's office, twisting his backpack strap with his fingers. Lu Zheng handed him a glass of water, but she didn't take it and said, "My sister won't leave on her own." The voice was quiet, but firm,not to ask for help, but to make sure someone believed her.
2. [Advance the plot] Lu Zheng placed the water glass in front of her and opened the notebook. He didn't say "I understand" or anything like that, but directly asked: "When was the last contact?" Su Mo was stunned for a moment and started to speak.
```

✅ Note style:

```
1. [Advance the plot and dialogue] Su Mo was in the reception room, twisting his backpack strap with his fingers. Lu Zheng handed her water but she didn't take it → "My sister won't leave on her own." The voice is not loud but firm, not asking for help but seeking recognition. Pay attention to Su Mo's finger movements (nervous but restrained).
2. [Advance the plot] Lu Zheng put the water glass on the table and opened his notebook. Without greetings, ask directly, "When was the last time we contacted you?" Su Mo was stunned for a moment and started to speak.
```

→ For a complete survey of key_points + dialogue embedding hybrid examples, see §5.
Complete chapter outline example.
