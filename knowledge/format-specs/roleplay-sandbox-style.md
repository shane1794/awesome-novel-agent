# Role play record format specification

> The deduction record is the product of the character deduction sandbox, which
> records the behavior/lines/expression and scene state changes of each character in
> each round. As optional reference material for prompt-crafter to read.

## File Path

`sandbox/vol-{N}-ch-{M}/deduction-{n}.md`

## Overall Structure

```
# Role play record

## Metadata
...

## Initial scene state
...

## Deduction Process
### Round 1
#### Round 1 / Character: {Character Name}
...
### Round 2
...

## Deduction results
...
```

## Field specification

### Metadata

```markdown
## Metadata
- **Volume Number**: 1
- **Chapter Number**: 3
- **Trigger scenario**: {One sentence describing the deduced Qidian scenario, extracted from chapters_summary or provided by the author in Step 2}
- **Characters**: {Character 1, Character 2, Character 3}
- **Deduction round**: {N}
- **Deduction Goal**: {The deduction goal set by the author in Step 2}
```

- `trigger-scene` is quoted from `chapters_summary` of `volumes/vol-{N}.md`, or provided by the
  author when setting up the stage in Step 2
- `deduction-goal` is set by the author when setting up the stage in Step 2 as a basis for judging
  the conclusion of the deduction.

### Initial scene state

```markdown
## Initial scene state

### Scene setting
- **Location**: {Specific location}
- **Time**: {specific time}
- **Ambience**: {Ambience description}

### Character initial state
#### {Character name}
- **Location**: {physical location}
- **Mood**: {Current Mood}
- **Known**: {Information known to the character}
- **Don't know**: {Information that the character does not know}
- **Current Goal**: {What the character wants to achieve in this scene}
- **Microbehavioral Patterns**: {Habitual small actions when tense/relaxed}

### Active Hook/Foreshadowing
- {Hook 1}
- {Hook 2}
```

- `character-initial-state` must be extracted from the following fields of
  `settings/character-setting/{id}.md`:
  - Cognitive 6-layer model → Derivation of possible response patterns of characters
  - Status history → Current mood and location
  - Emotional arc → recent triggering event and intensity
- `micro-behavior-pattern` is extracted from the language characteristics and habit descriptions in the
  character settings (not a hard field, if it does not exist, write "No information")
- `active-hooks` is extracted from `settings/foreshadowing.md`

### Round Output (Core)

Each round of output includes two parts: **"AI deduction output"** and **"author
intervention record"**:

```markdown
### Round {N}

#### Round {N} / Role: {Character name}

**Line/Action/Appearance:**
> {What words did the character say, what actions did it take, and what expressions did it have}

**Scene status changes:**
- {Dimension of change}: {Specific changes}
```

#### Output requirements

Only three items are output, without additional reasoning process:
1. **Lines/Actions/Appearance**, What the character said, did, and expressed after a
   paragraph
2. **Scene State Change**, What changes the character's behavior
3. Remove internal reasoning content such as cognitive layer analysis, behavioral
   derivation, and conclusions.

- Text content **Strictly character-based information boundaries** - information unknown
  to the character does not appear in its behavior
- No inner monologue, no character’s unexpressed hidden motivations

#### Scene state change rules

Each character's behavior must change at least one dimension of the scene state:

| Dimensions of change | Description | Example |
|---------|------|------|
| **Atmosphere** | Overall atmosphere change | "From small talk to mutual testing" |
| **Relationship** | Changes in the power/closeness relationship between characters | "Fang Yan takes the initiative to draw clear boundaries" |
| **Information** | Changes in information gap | "Lu Zheng confirmed that Fang Yan knew the inside story" |
| **Position** | Changes in character's physical position | "Wang Wu moved his stool toward the door" |
| **Item** | Scene object state changes | "The tea cup was rubbed repeatedly, and the rim of the cup was stained" |
| **Conflict** | Conflict escalation/de-escalation | "The confrontation between the two sides has formed" |

#### Cognitive layer reference rules

Each output comes with a cognitive layer reference in the format `{character-name} layer {n} ({layer-name}): {derivation}`:

```markdown
**Involving the cognitive layer:**
- Lu Zheng Layer 4 (Ability): Observed Fang Yan’s scanning movements and judged that he was on guard.
- Lu Zheng Level 2 (self-positioning): "I am a patient person" - choose not to ask directly, let the other person relax first
```

- The level number (layer 1-layer 6) and layer name (world
  view/self-positioning/values/ability/skills/environment) must be consistent with the
  cognitive 6-layer model of `character-setting-style.md`
- Multiple layers can be referenced
- If a layer is empty in the character settings, it will not be referenced.

#### Record of author intervention

After each author's intervention, the intervention record is appended below the round
output:

```markdown
---

**Author intervention:** Modify/Restart/Jump in line/Add information/Terminate

{Description of intervention content}

**Intervention impact:**
- {Changes in scene status after modification}
```

- `modify`: The author has changed some of the output of the current character → affecting
  the deduction of subsequent characters in this round
- `redo`: The author overturns the output regeneration of the current character → keeps
  the previous state unchanged
- `jump-queue`: The author requires a certain character to appear first → adjust the order and
  continue
- `add-info`: The author adds information that the current character does not know but should
  know → Updates the character’s knowledge status
- `stop`: The deduction is over and the results are sorted.

### Deduction results

```markdown
## Deduction results

### Scene Final State
- **Location**: {Same as above or changes}
- **Time**: {time after the deduction is advanced}
- **Ambience**: {Final Ambience}

### Character Final State
#### {Character name}
- **Emotion**: {Emotion at the end}
- **New knowledge**: {New information obtained during the deduction}
- **Next step**: {The character’s subsequent action tendency under the current goal}
- **Behavioral Consistency**: {Conform to character / deviate from character + explanation}

### Writing materials that can be refined
1. **{Material type}**, {Specific description}
2. **{Material type}**, {Specific description}

### Compare with deduction goal
- **Goal Completion**: {Part/Full/Excess}
- **Deviation Description**: {The difference between the deduction results and the expected goal}
```

- `character-final-state` is extracted from the last scene state during the deduction process
- `extractable-writing-material` is for prompt-crafter to use: dialogue fragments, micro-behavior patterns,
  scene atmosphere words, character relationship change nodes
- `compare-with-deduction-goal` Verifies whether the deduction has achieved the goals set in Step 2

## Validation rules

- Does not contain inner monologue or hidden motives (only visible behaviors are
  recorded in the deduction)
- The output of each round includes: lines/actions/expression + scene state changes
- Internal reasoning processes such as cognitive layer analysis and behavioral
  derivation do not appear in the output.
- Before the first deduction, the initial scene status must be confirmed by the author
