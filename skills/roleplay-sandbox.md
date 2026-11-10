# Roleplay Sandbox

> An interactive character roleplay tool. When the author is stuck on the plot, set the "stage" and the "actors" and give the trigger conditions; the AI roleplays each character's actions / lines / expressions in series, and the author can change things each round, advancing over multiple rounds until the plot goal is reached. The roleplay record is a reference for the author when writing the chapter outline.

## Positioning

**When to use:** The author actively asks for a plot roleplay, or gets stuck on the plot while writing a new chapter: there is a core story but no idea how to develop it into concrete plot. The roleplay record gives character behavior material that helps write the chapter outline.

**When not to use:** The author is already clear about the plot direction and character behavior and needs no extra material.

**Relation to the existing flow:** The roleplay sandbox is an **interactive tool the author calls on their own**; it is not in novel-agent's automatic dispatch flow. It produces no order files and does not change `.agent/status.md`.

## Flow Overview

```
Step 1: Confirm the inputs
   → read the volume outline chapter direction + character settings (6-layer cognitive model) + the previous chapter's ending scene + hooks
   → output directory: sandbox/vol-{N}-ch-{M}/

Step 2: Set the stage (scene initialization)
   → ask the author for the scene settings: location / time / atmosphere / character positions / trigger event
   → assemble the initial scene state → confirm with the author

Step 3: Fix the appearance order
   → the author fixes the order in which characters are roleplayed

Step 4: Serial round roleplay
   ┌→ for each round:
   │    for each character:
   │      1. AI generates the character output (action + line + expression + scene change)
   │      2. Show it to the author
   │      3. The author chooses: accept / modify / redo / cut in / add information / stop
   │      4. Update the scene state → next character
   │    End of a round → check the stop conditions
   └→ until it stops

Step 5: Stop judgment → goal reached / scene closed / author calls a stop

Step 6: Produce the roleplay record
   → write to sandbox/vol-{N}-ch-{M}/推演{序号}.md
```

## Step 1: Confirm the Inputs

### Files that must be read

| File | Purpose |
|------|------|
| `volumes/vol-{N}.md` | Volume outline: this chapter's `chapters_summary` (who + did what + conflict + what changed) |
| `settings/character-setting/{character id}.md` | Each appearing character's 6-layer cognitive model + state history |

### Files that may be read

| File | Read if it exists |
|------|---------|
| `settings/foreshadowing.md` | List of active hooks |
| The previous chapter's `archives/vol-{N}-ch-{M-1}.md` ending scene | Scene initialization reference |

### Key information extracted from the volume outline

- `chapters_summary` → this chapter's one-sentence plot direction, as the roleplay's overall direction
- `情绪走向` (emotional direction) → this chapter's position on the volume's emotional arc, as the initial reference for the scene atmosphere
- `冲突阶梯` (conflict ladder) → the current conflict layer, as the boundary reference for conflict intensity during the roleplay

### Key information extracted from the character settings

- `认知6层模型` (6-layer cognitive model) → the detailed description of each layer, used to derive character behavior
- `状态历史` (state history) → the recent chapters' state changes, fixing the character's current position and emotion
- `情绪弧线` (emotional arc) → the recent trigger events and intensity
- `hooks` field → the character's unresolved hooks

## Step 2: Set the Stage (scene initialization)

### Ask the author

After the input reading is done, ask the author scene by scene:

```
We are about to roleplay the {scene name} of chapter {N}.

Please tell me:
1. **Scene settings**: where does it happen? When? What atmosphere?
2. **Appearing characters**: who is in this scene? Where are they positioned? What are they doing at the start?
3. **Trigger event**: what event starts this scene? (For example: "陆征 pushes the door open and finds 方岩 already waiting for him")
4. **Any extra information gap?**: what special information asymmetry exists between the characters right now?
5. **What do you want this round of roleplay to reach?**: for example, "confirm whether 方岩's reaction fits the character design" or "test the original dialogue rhythm"

If you are not sure, just say "follow the volume outline" and I will extract it from the volume outline's chapter direction.
```

### Assemble the initial scene state

From the author's answers + the files already read, assemble the initial scene state:

```markdown
### Scene Settings
- **Location**: {extracted or provided by the author}
- **Time**: {extracted or provided by the author}
- **Atmosphere**: {extracted or provided by the author}

### Characters' Initial States
#### {Character Name}
- **Position**: {physical position, may include posture}
- **Emotion**: {current emotion, extracted from the character's state history}
- **Knows**: {derived from the character's state history + the previous chapter's ending}
- **Does not know**: {derived from the information gap}
- **Current goal**: {derived from the character settings + the volume outline's chapter direction}
- **Micro-behavior pattern**: {habitual small actions extracted from the character settings}
```

### Confirm with the author

Show the initial scene state with these words:

```
This is the initial scene state. Take a look and see if anything needs adjusting.
→ No problem → go to Step 3
→ Change XX → update, then go to Step 3
```

## Step 3: Fix the Appearance Order

```
How should the appearance order of the characters go? By default, order by each character's importance in the current scene:
1. {Character A}: {one sentence on why they appear first, for example "they are the one who starts the dialogue"}
2. {Character B}: {explanation}
3. {Character C}: {explanation}

Do you want to change the order, or have a character stay silent at first and join later?
```

- The order is finally decided by the author
- Once fixed, it does not change within this round (unless the author asks for a cut-in during the roleplay)
- The order should stay consistent each round (unless the author explicitly asks to change it)

## Step 4: Serial Round Roleplay

### The logic for AI generating a character's output

For each character, run the following reasoning steps:

```
Inputs:
- Current scene state (the initial state + the accumulated changes from all previous character outputs)
- The target character's 6-layer cognitive model
- The target character's known state, emotion, and goal
- The current scene's conflict / information gap

Reasoning:
1. What did the character "see / hear / perceive" in the current scene? (based on the information boundary)
2. How does the character's cognitive layer 1 (worldview) interpret the current situation?
3. How does the character's cognitive layer 2 (self-positioning) require them to react?
4. What boundary does the character's cognitive layer 3 (values) set?
5. What details can the character's cognitive layer 4 (abilities) observe?
6. What can the character's cognitive layer 5 (skills) do?
7. Does the character's cognitive layer 6 (environment) affect how they behave?
8. What is the character's current goal? How do the factors above affect their choice?

Output (output only the result; do not show the reasoning process):
- Lines / actions / expressions: what the character said, did, and what expression they wore
- Scene state change: what the character's behavior changed
```

### Output format

```markdown
#### Round {N} · Character: {Character Name}

**Lines / Actions / Expressions:**
> {What the character said, what they did, what expression they wore}

**Scene State Change:**
- {dimension}: {concrete change}
```

### Handling author feedback

After each round's character output, pause and wait for the author's feedback. Use these words:

```
{Character Name}'s roleplay is above. You can:
- Accept: continue to the next character
- Modify: tell me what to change
- Redo: tell me the direction and I will rewrite this passage
- Cut in: let another character appear first
- Add information: add background the current character does not know but should know
- Stop: the roleplay ends here
```

#### Handling rules for each feedback type

| Feedback | AI action | Later effect |
|------|---------|---------|
| **Accept** | Apply the current change to the scene state and move to the next character | Normal |
| **Modify** | Modify the output per the author's request → update the scene state → move to the next character | Later characters in this round see the modified state |
| **Redo** | Roll the scene state back to before this character started → add the author's direction → regenerate | Does not affect previous characters' output |
| **Cut in** | Record the current character's state → roleplay the cut-in character first → return to the current character after finishing | The cut-in character's output becomes the current character's new input |
| **Add information** | Update the "Knows" field of that character in the scene state → the current character roleplays again | All later rounds see the updated information boundary |
| **Stop** | Freeze the scene state → go to Step 5 | none |

### Roleplay iron rules

1. **Based on the cognitive layers**: character behavior must be derivable from the character's 6-layer cognitive model. The cognitive layers decide behavior; do not go by empty feeling.
2. **No OOC**: a character cannot do something their layer 3 (values) refuses, and cannot hold a self-perception their layer 2 (self-positioning) does not accept.
3. **Transparent information gap**: the AI only uses the information that character currently knows. Information the character does not know cannot appear in their behavior or lines.
4. **Observable**: the output contains only behavior other characters can see / hear. Do not write inner monologue.
5. **Causal chain**: each character behavior must change at least one dimension of the scene state.
6. **One-way evolution**: the scene state only moves forward. The author's changes create new branches; they do not rewind other characters' behavior that already happened.

## Step 5: Stop Judgment

### Stop conditions (stop when any one is met)

1. **Goal reached**: the roleplay goal the author proposed has been shown
2. **Scene closed**: all characters are silent / have left, with no new behavior to roleplay
3. **Stall limit exceeded**: 3 consecutive rounds with no substantial advance; at that point ask the author "continue roleplaying or stop?"
4. **Author calls a stop**: the author picks "stop" at any feedback point

### After the stop is handled

```
The roleplay has ended, {N} rounds in total.

A summary of the roleplay results:
- Final scene state: {brief description}
- Key behavior nodes: {behavior 1 → behavior 2 → ...}
- Character relationship changes: {brief description of the changes}
- Material usable in the main text: {dialogue fragments, micro-behaviors, atmosphere words, and similar}

Should the roleplay record be written to a file?
```

## Step 6: Produce the Roleplay Record

Following the format in `.claude/knowledge/roleplay-sandbox-style.md`, write the complete roleplay process to:

`sandbox/vol-{N}-ch-{M}/推演{序号}.md`

### File naming

- First run: `sandbox/vol-{N}-ch-{M}/推演01.md`
- Roleplaying the same chapter again: `推演02.md`, `推演03.md`, and so on in order
- Ask the author to confirm the file name before writing

### Writing rules

- Before writing, show it to the author for confirmation: "This is the roleplay record to write. Take a look and see if anything needs adjusting?"
- Write it after the author confirms
- The file content includes: metadata, the initial scene state, the complete roleplay process (all rounds + author interventions), and the roleplay results

### File status

The roleplay record lives in the `sandbox/` directory, at the same level as `chapters/` and `volumes/`. It does not affect project state and does not appear in `.agent/status.md` or any order file path.

## Next Step

After the roleplay record is written, tell the author the path forward:

```
The roleplay record is written to sandbox/vol-{N}-ch-{M}/推演{序号}.md.
You can use the character behavior and dialogue material in the roleplay record to write the chapter outline, and the main text writing also has concrete behavior references.

Do you want to continue writing the chapter outline? Or do you want to change the roleplay record first?
```

## Boundaries and Constraints

### What the sandbox does not do

- Does not write order files
- Does not modify `.agent/status.md`
- Does not modify character settings files or foreshadowing.md
- Does not generate main text (that is writer's job)
- Does not automatically dispatch later steps (the author or novel-agent decides)

### Use boundaries for sandbox output

The roleplay record is reference material for the author, not a forced system input:
- The author writes the chapter outline and main text from the character behavior and dialogue in the roleplay record
- The roleplay record is not automatically injected into any later flow
