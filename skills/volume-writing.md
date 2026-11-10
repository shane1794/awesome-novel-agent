# Volume Outline Discussion Skill

> One volume has only one main line; all chapters together tell that main line. If any chapter is missing, the story is incomplete.

## Process

Read the volume memory → set the emotional direction → fix the core conflict → set the conflict ladder → build the information gap → break into scene cards → append new characters / settings → write the output → accept

## 0. Read the Volume Memory

Before planning starts, read the entries in `.claude/memory/volume-memory.md` that apply to this volume's planning (volume direction / conflict design / rhythm distribution) and apply them; after citing them, increment use_count following skills/memory-recording.md Section 4.1.

> The author's feedback is banked in memory. If you do not read it, you cannot use it, and if use_count never rises, it will never be promoted to permanent memory.

## 1. Fix the Core Conflict

Inherit this volume's core conflict from story.md and ask the author, "Is there anything to adjust?"

**Bottom line (if any item fails, do not proceed to breaking into chapters):**
1. **The core conflict can be said in one sentence**: "who + wants to do what + is blocked by what", with no need for "at the same time" or "on the other hand"
2. **The opposing force is concrete**: the obstacle must be a concrete character / force / situation, not hollow words such as "fighting fate" or "fighting society"
3. **Both sides of the conflict have a reason they cannot back down**: derive it from the characters' layer 3 values in their settings; if it cannot be derived, ask the author to add it.

> Ask the author about the non-negotiable reasons of both sides of the conflict (ask only about plot):
> "The core of the conflict between the protagonist and {opponent} is {X}. What does each side stand to lose if they back down? What happens if {Character A} backs down? What happens if {Character B} backs down?"
>
> After the author answers, judge against `.claude/knowledge/plot-craft/conflict-motivation.md` whether it is concrete enough:
> - Both sides have concrete motives (survival threat / identity / obsessive trauma, and similar) and they are mutually exclusive → pass
> - Either side has an invalid motive (born evil / needed by the plot / abstract concept) → ask: "If {character} backed down, what exactly would they lose?"
> - Both sides' motives can be reconciled (a Plan Z exists that lets each side step back) → warn: "This conflict can currently be reconciled. Should it be hardened? See the hardening methods in conflict-motivation.md"
>
> If the characters' layer 3 values are too abstract for even the author to answer, append a setting-change notice as a reminder to add them.

## 2. Set the Emotional Direction

> Conflict defines "what happens"; the emotional direction defines "how the reader's emotion changes from the start of this volume to the end".

After inheriting this volume's core conflict from story.md, the agent first designs the emotional direction on its own; do not rush to break it into chapters, and do not ask the author first.

### How the Emotional Direction Is Set

**Step 1: Fix the arc mode**

Based on the core conflict type and genre, the agent picks the most suitable emotional arc mode on its own. The basis for the choice:

| Conflict Type | Recommended Arc Mode | Description |
|---------|-------------|------|
| Revenge / comeback | Repress first, then satisfy | repression → repression → rise → face-slap → showing off |
| Investigation / puzzle | Closing in layer by layer | tension → closing in → shock → relief |
| Growth / trial | Tension opening and closing | tension → relief → tension, higher → relief → climax |
| Confrontation / war | Building up to an eruption | repression building up → repression building up → eruption → lingering resonance |

If unsure, default to "closing in layer by layer" (the most general investigation-type narration).

**Step 2: Assign it to each layer of the conflict ladder**

Each step of the arc maps to one layer of the conflict ladder:

```
Conflict ladder                    Emotional direction
Layer 1: predicament set up     ↔   repression (oppression at the volume's start)
Layer 2: pressure escalates     ↔   repression, higher (even more painful)
Layer 3: desperate straits / turning point   ↔   more repression / shock (the lowest point)
Layer 4: counterattack / climax   ↔   rise → face-slap → showing off (release)
```

**Step 3: Verify the arc is perceptible**

The agent checks on its own: if the repression layer is written as the protagonist drinking tea in everyday life, the conflict design has a problem; go back and change it.
No need to ask the author. Let the author judge it in one go when the plan is shown.

### Bottom line

- **The emotional direction must be an arc, not a point**: "satisfying" is not a direction; "repression → repression → rise → face-slap → showing off" is
- **Each step of the arc maps to one layer of the conflict ladder**: emotion cannot be designed separately from conflict
- **The arc must progress**: "repression → repression → repression" is only a change in amount, not in quality; it needs a turning point in the middle that turns the emotion from repression toward anticipation or anger

> **Conflict escalation reference:** When designing the obstacles at each layer of the conflict ladder, consult the conflict escalation techniques in `.claude/knowledge/plot-craft/index.md` (value mismatch / environmental pressure / goal substitution / chain reaction) and the plot twist techniques (logic misdirection / character substitution / nested dolls), so each layer's conflict type changes instead of just being "a stronger person shows up".

## 3. Set the Conflict Ladder

The core conflict is "who fights whom"; the conflict ladder is "how the fight proceeds step by step".

### Ladder design method

Break one core conflict into 2-4 layers of obstacles that rise step by step:

```
Core conflict: "陆征 investigates the old case, and someone inside the police force stops him"
  ↓
Layer 1: information blocked: the case file is incomplete, and 方岩 dares not speak    ← entry level
  ↓ turning point: discovering the old case was suppressed
Layer 2: outside pressure: someone tails / warns him              ← escalation
  ↓ turning point: the protector shows their true face
Layer 3: inside loss: a witness disappears, the evidence chain breaks      ← major setback
  ↓ turning point: the protagonist is forced to choose
Layer 4: head-on confrontation: showdown with the power behind the scenes            ← ultimate
```

Show it to the author and confirm whether each layer's "rising difficulty" is reasonable.

### Mark the key turning points

Mark 2-4 turning points in the ladder where "the situation fundamentally changes":

| Turning Point Type | Example | Mark |
|---------|------|------|
| Information turning point | "Discovering the old case was suppressed" | The goal changes after this |
| Relationship turning point | "The collaborator is actually the enemy" | The camp changes after this |
| State turning point | "Losing police support" | The means change after this |
| Event turning point | "The witness is killed" | The situation becomes irreversible after this |

**Bottom line:** Each layer's obstacle is harder than the last. If layer 2 is about as hard as layer 1, merge or delete it.

## 4. Build the Information Gap

Conflict pushes the plot forward; the information gap pushes the reader forward. The information gap is the root source of "why the reader wants to turn the page".

### How the Information Gap Is Set

**Step 1: Identify who holds the information**

Confirm with the author category by category. The key is "who knows what, and who does not know what":

| Relationship | Ask the author | Example |
|------|--------|------|
| **The protagonist knows, others do not** | "What key information does the protagonist know this volume that the villain / supporting characters do not?" | The protagonist has a golden finger; the protagonist learned of the conspiracy in advance |
| **The villain / supporting character knows, the protagonist does not** | "What secret / trap does the villain or a supporting character have that the protagonist does not know?" | The villain set an ambush; a supporting character has a double identity |
| **The reader knows, the protagonist does not** | "What does the reader know through the narration that the protagonist is still in the dark about?" | The reader knows it is a misunderstanding but the protagonist is angry; the reader knows who the traitor is |

**Step 2: Fix the volume-level start → end**

A volume does not define each chapter's information gap detail. It only defines **the information gap at the start of this volume** and **the information gap after this volume ends**. The changes in between are acted out by the chapter outlines.

> "At the start of this volume, what does the protagonist know and what does the villain know? At the end of this volume, what does the protagonist know that they did not know before?"

```
At the volume's start:
  The protagonist knows: 苏棠 is missing, and the police ruled it a voluntary departure
  The villain knows: the inside story of the case suppressed three years ago, and where 苏棠 is
  The reader knows: the same as the protagonist

At the volume's end:
  The protagonist newly knows: the old case was suppressed, and a protector exists
  The villain newly knows: the protagonist is investigating, and is hard to deal with
  The reader knows: the same as the protagonist

Arc direction: the information gap moves from "completely asymmetric" to "partly balanced",
          the protagonist caught up a step but not enough, supporting the next volume
```

**Step 3: Fix the dominant driving force**

Decide from the start → end arc direction what drives the reader this volume:

| Arc Direction | Driving Force | Chapter Rhythm |
|---------|---------|---------|
| Information gradually revealed to the protagonist | Suspense driven | Each chapter leaves a hook and releases one layer of new information |
| The villain's trap gradually surfaces | Threat driven | The safe period gets shorter and shorter |
| The protagonist's advantage gradually shows | Goal driven | Staged results lead to new obstacles, cycling forward |
| The reader knows but the characters do not | Relationship driven / information gap driven | Tension accumulates until the reveal |

**Step 4: Mark it on each chapter**

When breaking into chapters, mark each chapter's information gap. Each chapter is one dynamic change point on the information gap arc:

```
### 1-4: The Trap
- **Conflict event**: 陆征 goes to the warehouse; the tip was fake, and the other side set an ambush
- **Emotional anchor**: tension
- **Information gap**: the villain knows it is a trap, and the protagonist does not ⬅ this chapter's information gap change: from "the protagonist in the open" to "the protagonist walking into the trap"

### 1-5: The Counter-Kill
- **Conflict event**: 陆征 plays along and fishes out the person behind the informant
- **Emotional anchor**: satisfaction
- **Information gap**: the protagonist has a backup plan, and the villain does not know ✅ the information gap reversed: from "passive" to "active"
```

### Bottom line

- **At volume level, fix the start → end; do not set the middle details**. Each chapter's information gap change is left to the chapter outline to act out
- **The end information gap cannot equal the start**: if the protagonist knows the same things at the volume's end as at its start, the volume was written for nothing
- **The end information gap cannot be fully balanced**: if the protagonist "knows everything" at the volume's end, the next volume has no information driving force

## 5. Break into Scene Cards

> Volume outline → chapter (emotional anchor + conflict event + information gap + suspense hook)
> Chapter outline → scene card (what the protagonist wants to do + what blocks them + what suspense makes the reader want to keep reading)

Using the conflict ladder stages confirmed in the previous step as the skeleton, fill in chapter by chapter. For each chapter's "what suspense makes the reader want to keep reading", design it with the three hook techniques in `.claude/knowledge/plot-craft/hook-techniques.md`.

> **Special handling for volume 1, chapter 1:** If it is the first volume's first chapter, the agent picks the most suitable opening technique on its own from the genre and style (see `.claude/knowledge/plot-craft/opening-hooks.md`), drafts the opening scene card, and shows it to the author for confirmation. Do not show a list of techniques for the author to pick from.

Each chapter contains three dimensions:

| Field | Standard | Failing Example |
|------|------|-----------|
| id | "volume-chapter" (such as 1-1), consecutive with no skipped numbers | 1-1, 1-3 (1-2 skipped) |
| title | Has information; the chapter's core event can be guessed from it | "Chapter One" / "A New Beginning" / "Turning Point" |
| Conflict event | **Three elements: who does what + the conflict event + what changed at the end** | "The protagonist keeps investigating" (nothing changed) |
| Emotional anchor | The reader's core feeling this chapter (matching the current stage of the volume-level emotional arc) | None |
| Information gap | {who knows what} → {who does not know what} | None |

### Scene card detail (used at the chapter outline stage)

One chapter is made of 2-5 scene cards; each scene card has three pieces of information:

| Field | Meaning | Notes |
|------|------|------|
| **What the protagonist wants to do** | Goal: what the protagonist wants to achieve in this scene | Even a passive scene has a goal ("stay alive" / "figure it out") |
| **What blocks them** | Obstacle: what the obstacle is | Person against person, event against event, inner self against inner self |
| **What suspense makes the reader want to keep reading** | Hook: why the reader cares about this passage | Comes from the emotional anchor + information gap |

**Example:**
```
### Scene 1: 方岩's Office
- **What the protagonist wants to do**: 陆征 wants to get the inside story of the case suppressed three years ago from 方岩
- **What blocks them**: 方岩 dares not speak. There are other people in the office, hinting "someone is watching"
- **What suspense makes the reader want to keep reading**: the reader wonders what 方岩 actually knows and why he dares not say it
```

### 4 kinds of failing chapter outlines

| Type | Typical Wording | Fix Direction |
|------|---------|---------|
| **Theme-style** | "This chapter is about trust" (no event) | Turn the concept into a concrete event |
| **Function-style** | "Build the character relationships" (a function is not progress) | Fold the function into the conflict event |
| **Synopsis-style** | "The protagonist went through a day of adventure" (no conflict point) | Point out the single most core event |
| **Result-style** | "The protagonist won the competition" (only the result, no process) | Write the obstacle and the confrontation process |

**A causal chain must exist between chapters:** the previous chapter's end-of-chapter change is the next chapter's starting point or motive.

## 6. New Characters and Setting Appends

New characters / settings added during the volume outline discussion are appended as a setting-change notice block at the end of volume-{N}.md, for novel-agent to dispatch updater to execute before the writing loop:

```
## Setting Change Notice

- **Target:** settings/character-setting/{id}.md
- **Type:** New character / status update / worldview update / timeline
- **Reason:** {why this change is needed}
- **Details:** {change description}
```

> **Consumption rule**: Before writing the next chapter, novel-agent greps `volumes/` + `chapters/` for the `## Setting Change Notice` heading; when found, it dispatches a setting-update-order (inputs pointing at the source file); after updater finishes the change, it **removes the notice block from the source file** (deleting the block with Edit, to prevent repeat consumption). If the block conflicts with an already archived chapter, STOP and give it to the author.

Consistency check: the new settings do not contradict already archived chapters.

## 7. Write the Output

Write it into `volumes/volume-{N}.md` in the set format:

```markdown
# Volume N: {Title}

## Volume Information

- **Emotional direction**: this volume's arc of the reader's emotional change (repression → repression → rise → face-slap → showing off)
- **Core conflict**: who + does what + is blocked by what
- **Dominant driving force**: suspense driven / threat driven / goal driven / relationship driven / information gap driven
- **Conflict ladder**: Layer 1 (entry) → Layer 2 (escalation) → Layer 3 (turning point) → Layer 4 (ultimate)
- **Estimated chapters**: N

## Chapter List

### N-1: {Informative Title}

- **Conflict event**: who does what + the conflict event + what changed at the end
- **Emotional anchor**: this chapter's reader feeling
- **Information gap**: {who knows what} → {who does not know what}
```

## 8. Acceptance

**Three-dimensional acceptance:**

**Dimension 1: Emotional direction acceptance**
- [ ] **The emotional direction is set**: it is an arc (repression → rise → face-slap), not a single emotion word
- [ ] **The emotional direction progresses**: the arc has a start, a turning point, and an end, with an emotional change at each step
- [ ] **Each chapter is marked with an emotional anchor**, matching the emotional direction's current stage

**Dimension 2: Conflict ladder acceptance**
- [ ] **Both sides of the conflict have a reason they cannot back down**: derivable from the characters' layer 3 values, with mutually exclusive motives. If it cannot be derived, the settings are flawed or the conflict architecture is hollow
- [ ] **Each layer's obstacle is harder than the last**: not the same confrontation repeated
- [ ] **Clear turning points between layers**: the situation fundamentally changes
- [ ] **2-4 turning points**: too few is flat, too many leaves no room to breathe
- [ ] **Each chapter is marked with an information gap**, stating "who knows what → who does not know what"
- [ ] **The information gap has a complete "set → use → reveal" cycle within the volume**

**Dimension 3: Chapter structure acceptance (the original volume-level 4 checks)**
1. **Do the chapters together tell this volume?** Read every summary chapter by chapter; together, are they a complete story?
2. **Can each chapter be traced back to the volume conflict?** Point at the core conflict and ask for each chapter, "Which step of the conflict does this chapter advance?"
3. **Did the volume's story advance after each chapter?** Does the end-of-chapter change affect what follows?
4. **Does the title match the story?** Can you guess what happens in this chapter from the title alone?

**15-second quick sniff test (all three passing means roughly qualified):**
1. Can you state the core conflict in one sentence without looking at the file?
2. Point at any chapter: can you say "what changed after this chapter ended"?
3. Point at any two chapters: can you say "why chapter 1 is followed by chapter 2, and not skipped straight to chapter 3"?

**Volume N+1 supplement:** Verify whether the character states in the character voices (see volume-direction.md) are consistent with the archived chapters. Inconsistency means the archive-time state update missed something and needs fixing.

## 9. AI Flavor Self-Check and Removal

Scan the whole volume outline; if any pattern matches, revise and re-check, and only confirm it as passed once everything is cleared.

**Pattern 1: Hollow conflict descriptions**
The core conflict or chapter summary uses adjectives to state a position but does not write a concrete event.
- Bad: "unfolds a thrilling showdown" (展开精彩对决) → Good: "陆征 confronts the man in the gray short sleeves in an abandoned factory, and the other side pulls out the old case file as leverage" (陆征在废弃工厂与灰短袖男人对峙，对方掏出旧案卷宗要挟)
- Bad: "the conflict escalates fiercely" (冲突激烈升级) → Good: "方岩 is suspended by his superior, and 陆征 loses his information source inside the police" (方岩被上级停职，陆征失去警队内部信息源)
- Quick check: search the whole text for "thrilling", "fierce", "heart-stopping" (精彩 / 激烈 / 惊心动魄). If found, it matches

**Pattern 2: "All-purpose advance sentences"**
All-purpose sentences that advance no concrete plot and only fill a position.
- Bad: "As the investigation deepened, the truth gradually surfaced" (随着调查的深入，真相逐渐浮出水面)
- Bad: "In this process, the protagonist met new challenges" (在这个过程中，主角遇到了新的挑战)
- Bad: "The story began moving in an unpredictable direction" (故事开始朝着不可预测的方向发展)
- Quick check: search the whole text for "as", "in this process", "at the same time" (随着 / 在这个过程中 / 与此同时). If found, it matches

**Pattern 3: Trailer-style language**
Language that sketches atmosphere like a trailer but gives no event.
- Bad: "A bigger conspiracy is brewing" (更大的阴谋正在酝酿). Who is brewing it? Brewing what? Is there an action?
- Bad: "The gears of fate begin to turn" (命运的齿轮开始转动). Which event triggered what?
- Quick check: search the whole text for "brewing", "the curtain rises", "gears of fate" (酝酿 / 拉开帷幕 / 命运的齿轮). If found, it matches

**Pattern 4: Hollow rhythm filler words**
Rhythm words used to pad length, with no matching event later in the text.
- Bad: "undercurrents surge" (暗流涌动) (appears in the volume outline without writing what is surging) → must state who is fighting whom
- Bad: "treacherous and unpredictable" (波谲云诡) (same as above)
- Quick check: search the whole text for "undercurrent", "treacherous", "murky and unpredictable" (暗流 / 波谲 / 扑朔迷离). If found, it matches

**Pattern 5: AI self-reference meta**
- Bad: "After a series of adventures" (经过一系列的冒险)
- Bad: "The core conflict of the story is" (故事的核心冲突在于)
- Bad: "What we are about to tell next is" (我们接下来要讲述的是)
- Quick check: search the whole text for "after a series of", "the core conflict is", "what we are about to tell" (经过一系列 / 核心冲突在于 / 我们要讲述). If found, it matches
