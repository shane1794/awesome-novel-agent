# Reference Gathering Skill

Prepare reference material for chapter outline planning. This is not a chapter outline or an outline. It is material for the author to slam the table over.

## Process

Input gathering → character expectation simulation → character collision → output reference material → multi-dimensional suggestions

## 1. Input Gathering

Read all four groups of information below before starting. If any group is missing, stop. Do not invent from impression.

### 1. Volume Outline Positioning

Read this chapter's summary in `volumes/volume-{N}.md#chapters_summary`. This is the story's skeleton: what step this chapter must advance to within the volume.

**Record:** One sentence. No added interpretation, no added speculation.

### 2. Character Knowledge Reconstruction

Only after reading the following three things can you say "I understand this character's state right now":

- **Character profile files** (settings/character-setting/): core personality, motives, ability limits. Read the full text only for this chapter's key characters; for other appearing characters, read only "Basic Information" plus the most recent state-change section under "State History", not the whole file
- **knowledge_state tracking**: each chapter's end-of-chapter role_information_state records what a character knew / did not know at the time. Read backward from the most recent chapter, accumulating each character's knowledge stock "up to before this chapter"

**Summarize each appearing character's state with this template:**

```
{Character Name}
  Just went through: {summary of events related to them in the last few chapters}
  Knows now: {knowledge stock accumulated from knowledge_state, listed in full regardless of weight}
  Does not know: {information they have not yet encountered, based on knowledge_state}
  Current motive: {what they most want to push forward right now / the contradiction they care most about / what they most want to avoid}
```

### 3. Previous Chapter Threads

Read the chapter outlines of the last few chapters (at least the previous 3 chapters; except for the first chapter), reading only their **end-of-chapter summaries** (do not read the full main text, to control the context budget). Extract mainly:

- **required_changes**: what the previous chapter's ending changed. This is this chapter's starting point
- **emotional_hook**: the emotional gap left at the previous chapter's end. What emotion the reader carries into this chapter
- **reader_expectation**: if the previous chapter's reader expectation is not answered in this chapter, what the reader will be waiting for

**Read only the end-of-chapter summaries**: for the previous chapters' main text, read only the outline's `summary` / `emotional_design` and the closing scene, not the whole chapter. When a prior detail is needed, check the most recent state section of the matching character's `settings/character-setting/{id}.md` instead of re-reading the full text.

### 4. Hook Ledger

The source of truth for hooks is each chapter outline's `payoff_plan` and the hooks field in the character settings files. Do not rely on memory; read them chapter by chapter.

Take stock by category:

```
Can close (must_resolve candidates):
  An old hook that has reached the time to close. Hooks of this kind usually appear in a character's
  pending section and have had enough planting.
  Criterion: the reader has already been expecting a follow-up to this for more than 1-2 chapters.
  · {hook description} → planted at: vol-{N}-ch-{M}.payoff_plan.partial_advance

Can advance (partial_advance candidates):
  Can be pushed forward but not fully closed. After the push, its state changes from "hanging" to "hanging worse"
  or "has a new direction".
  · {hook description} → current state: {pending / partial_advance}

Absolutely do not touch (must_hold candidates):
  A hook that would reveal the trump card if closed. Once touched, the design of later chapters falls apart.
  Hooks of this kind are usually tied to the story's core suspense or a character's ultimate motive.
  · {hook description} → reason: {why it cannot be touched}
```

### 5. Chapter Memory

Read the entries in `.claude/memory/chapter-memory.md` that apply to this chapter's planning (scene breakdown / emotional design / hook arrangement) and apply them; after citing them, increment use_count following skills/memory-recording.md Section 4.1.

> The author's feedback is banked in memory. If you do not read it, you cannot use it, and if use_count never rises, it will never be promoted to permanent memory.

## 2. Character Expectation Simulation

After input gathering is done, answer the following questions character by character.

**Rules:**
- Do it for every appearing character, including ones who have not formally appeared yet but may be active in the background
- Every answer must cite its basis (which step of the input gathering it comes from)
- An "intuition" with no basis does not count; go back and check the files

### Question Template

```
From {character name}'s point of view:

1. What does the character think the situation is now?
   Based on: {cite the "Character Knowledge Reconstruction" result}
   → The character's understanding of the current situation (note: this understanding may differ from the real situation;
      what a character does not know simply does not exist for them)

2. What does the character want to happen this chapter?
   Based on: {cite "Current motive"}
   → The concrete thing the character most wants to push forward. Not "investigate the case" but "go through the rented room"
     or "ask 方岩 about the inside story".

3. How would the character act?
   Based on: {cite ability preferences / behavior habits in the profile}
   → What they do first, what they do second. The more concrete the action chain, the better.
      陆征 is a former criminal police officer, so he looks for traces at the scene first, not the surveillance footage.
      苏沫 is an ordinary person's younger sister, so she asks someone she trusts for help instead of investigating herself.

4. What is the character's bottom line for this chapter (the thing that absolutely must not happen)?
   Based on: {cite the character's fears / avoidance tendencies in the cognitive model}
   → "If X appeared in this chapter, the character would feel it is wrong."
      陆征 does not want 方岩 to know he is still investigating the old case.
      苏沫 does not want her parents to know her sister is missing.

5. If what the character expects does not happen this chapter, how would the character react?
   Based on: {cite the character's flexibility in the profile}
   → Would they step back and switch plans? Or persist stubbornly? What loose end would they leave for later chapters?
```

### Inference Requirements

A character expectation is not pulled from one sentence in the profile file; it needs to be "reasoned out":

```
The profile file says "陆征 is highly observant"
→ You cannot directly output "陆征 will observe this chapter"
→ You must reason it out to something concrete:
   "Last chapter he touched a charging plug and it was still warm (source: ch-2 key_point 3),
    so this chapter when he enters the room he will first touch the cup / touch the bedsheet to confirm how long the person has been gone"
```

**Mark anything that cannot be inferred as "to be decided"**; do not invent it, leave it for the author to fill in.

### Character Collision

After every character's expectations are simulated, cross them once:

- **Points of agreement**: two characters both want the same thing to happen in the same scene. This is this chapter's anchor
- **Points of conflict**: one character wants to do X, another does not want X to happen. This is this chapter's dramatic fuel
- **Blind spots**: something no character has noticed. A new hook may be planted here

### Special Handling: First Chapter / New Character Appearance

- **First chapter**: there is no knowledge stock from a previous chapter, but the character profile files state how they were living when the story began. Reason from "the day before this moment": how does the protagonist normally spend this day? What breaks the routine?
- **New character appearance**: there is no accumulation from previous chapters, but the profile file states "what the character is doing right now". Cut in from their own world line: what are they busy with right now? What information would pull them into the main line?

## 3. Output Reference Material

Organize the analysis above into the following format and show it to the author.

### Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Volume {N} Chapter {M}: Reference Material
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Volume outline positioning:
{One sentence from chapters_summary, no added interpretation}

───────────────────────────────────────────────────
Character Expectations
───────────────────────────────────────────────────

{Character Name}
  Just went through: {event summary}
  Knows now: {knowledge stock}
  Does not know: {information blind spot}
  Current motive: {what they most want to push forward}

  What the character wants to happen this chapter:
  · {concrete expectation 1} ← basis: {source citation}
  · {concrete expectation 2} ← basis: {source citation}

  The character's bottom line:
  · {thing that absolutely must not happen} ← basis: {source citation}

  How the character would act (action chain):
  · {first step}
  · {second step}
  · {third step}

{Next character, same format}

───────────────────────────────────────────────────
Relationships Between Characters
───────────────────────────────────────────────────

Points of agreement:
· {scene/event}: {Character A} and {Character B}'s goals meet here

Points of conflict:
· {conflict event}: {Character A} wants {X}, {Character B} wants {Y}

Blind spots:
· {something no character noticed}: a new hook may be planted here

───────────────────────────────────────────────────
Hooks This Chapter Can Touch
───────────────────────────────────────────────────

Can close:
· {hook name} → planted at: vol-{N}-ch-{M} | enough planting, can close this chapter

Can advance:
· {hook name} → current state: {partial_advance} | give it a push

Absolutely do not touch:
· {hook name} → reason: {reveals the trump card / breaks the suspense / the character is not yet supposed to know}

───────────────────────────────────────────────────
Author Feedback
───────────────────────────────────────────────────

□ Is the volume outline positioning accurate?        Describe / change:
□ Is Character A's expectation right?       Describe / change:
□ Is Character B's expectation right?       Describe / change:
□ Is the hook judgment reasonable?        Describe / change:
□ Any character or hook left out?   Describe / change:

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Presentation Notes

**Do not dump all the information at once.** If there are many characters and a large amount of information, present it in batches:

1. First show the volume outline positioning and the hook ledger (these two are objective information; the author does not need to judge whether they are "right")
2. Then show one character's expectation, wait for the author's feedback, then the next
3. Finally show the relationships between characters and the complete hook classification

**During the author's calibration**, every time an item changes, update the citations of the related items at the same time. For example, if the author says "陆征 should not find out who the sticky note belongs to this chapter", also move "sticky note ownership" in the hook ledger from "can close" to "absolutely do not touch".

**If the author says "more or less", "you decide", or "whatever"**: do not let it pass. Ask concretely: "'More or less' means the character expectations are all right, or all wrong? Which character is most accurate? Which one is uncertain?"

## 4. Multi-Dimensional Suggestions

After the reference material is produced, do one round of multi-dimensional analysis before showing it to the author for calibration. The goal is to help the author locate problems faster.

### Analysis Dimensions

- **Plot continuity:** Does the previous chapter's ending (required_changes) connect directly to this chapter's starting point? What transition is missing? Is there a jump?
- **Character setup:** Are the existing characters enough to support this chapter? Is a key character missing to push the plot? Is there a character who should not appear this chapter?
- **Rhythm forecast:** Does the scene sequence the reference material produces have a reasonable rhythm? Is the climax too early or too late? Is a buffer transition needed?
- **Information gaps:** How much of the previous chapter's reader emotion (emotional_hook) does this chapter answer? What is the reader still waiting for that is not covered?

### Output Format

One sentence of judgment per dimension plus one concrete suggestion (1-2 items); do not push hard. Show it together with the reference material to the author.

## 5. Calibration Standard

The standard for judging whether the reference material has passed calibration: **the author can point at each character's expectation and say "Yes, the character would indeed think this way" or "No, the character would not think this way"**.

No character adjusted at all is a danger signal. It means the material is not concrete enough for the author to judge.
All characters answered with "more or less" means it did not pass. Ask about one most concrete point.
At least one character adjusted is normal. It shows the material is concrete enough to get a reaction from the author.
Multiple characters adjusted is good. The calibrated material is the real starting point.
