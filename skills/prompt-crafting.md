# prompt-crafter skill


## Process Overview

```text
Step 1: Read the input sources (10 kinds of files)
Step 2: Fill in by the 6-element Prompt structure: role / task instructions / background / examples / input / output
Step 3: Conflict detection
Step 4: Acceptance self-check
```

## Step 1: Read the Input Sources

> 10 kinds of files (including writing memory / prompt memory / permanent memory).

1. **writing-style.md (main card)** → extract the main text's qualitative layer four fields (narrative identity / hard constraints / common AI mistakes / description layers and techniques) + the quantitative layer's 9 dimensions + confidence. **Two states**: confidence=0 → inject only the qualitative layer (read the main card's main text → inject the qualitative four fields, unchanged); confidence>0 → render Case 2 per rendering-rules.md (read the main card + scene card frontmatter → quantitative section + voice layer passed through)
2. **Previous chapter's chapter.md** (`chapters/vol-{N}-ch-{M-1}.md`) → extract emotional_design (emotional hook emotional_hook + chapter-end landing, taking the last stretch of mood_progression) + required_changes, and from them reconstruct the previous chapter's ending scene; `volume.md`'s previous chapter summary helps
3. **chapter.md** → extract memo, emotional_design, scene cards, outline (scene breakdown), payoff_plan
4. **Character settings files** → read the involved characters and extract this chapter's relevant states
5. **genre-example** → take the matching genre's prompt injection passage (for Output, Writing Standards)
6. **Anti-AI rules file** (`.claude/knowledge/anti-ai.md`) → inject only the parts generation needs: human-feel positive points (the character has something to do right now / details follow the character's point of view / dialogue is doing work), the T1 most toxic sentence pattern short table ("not A but B", "with..." adverbials, cognitive verb first, "meanwhile", and similar; replace on sight), meta-narrative bans, genre anti-AI positive and negative examples. **Fatigue word thresholds, T2/T3 tiers, and tier 2 banned words are not injected**. Cleanup is left for the anti-ai agent to run after the draft is finished; writer does not check a negative list while writing (generation and cleanup are separate)
7. **Writing memory** (`.claude/memory/writing-memory.md`) → extract the author's style / rhythm / description / dialogue preferences relevant to this chapter and inject them into Background, Author Preference Memory
8. **Permanent memory** (`.claude/knowledge/permanent-memory.md`) → extract the author's high-frequency banked rules, deduplicate them against the writing memory, then inject them
9. **style-profiles/ scene cards** → for each scene type in this chapter, look up `settings/style-profiles/{scene_type}.md`; when present, merge that card's override into the main card's quantitative layer (only for that scene's injection; a confidence>0 render stacks the override on top); when absent, the main card is the fallback. **Merging is done by hand by the LLM, with no script check (review #34). After merging, check the value scales in the Step 4 acceptance self-check (0-100 percentages, non-negative); on an anomaly, check the source card**
10. **Prompt memory** (`.claude/memory/prompt-memory.md`) → extract the author's feedback entries related to this chapter's prompt assembly / conflict ruling / checks, and apply them when filling in Step 2 and detecting conflicts in Step 3; after citing them, increment use_count following skills/memory-recording.md Section 4.1
**Note: the prior context reads only the previous chapter's outline (chapters/vol-{N}-ch-{M-1}.md) emotional_design and required_changes; do not read the previous chapter's main text in full; archives/ is always forbidden to read.**

**Placeholder guard:** If `settings/writing-style.md` / `settings/genre-setting.md` still contain unreplaced `{...}` placeholders (such as `{role}` or `{genre_id}`, meaning the settings stage was not run after initialization), **do not inject the placeholders into the prompt as-is**. Instead, extract the matching genre's "narrator role / style blueprint / genre taboos / genre configuration" from `.claude/knowledge/genre-example.md` as the default style injection, and mark the completion report `[settings not filled in; genre-example default used as fallback]`, telling novel-agent to fill in the settings later.

## Step 1.5: Global Conflict Ruling Preload

Before filling in the 6 elements, load the following global conflict ruling table. Whenever a rule conflict appears in the later filling steps (such as insufficient word count vs sensory detail, or red line preservation vs word count compression), rule by this priority. This step is an internal reference and is not output into the prompt text.

### Priority hierarchy (high to low)

| Priority | Rule | Description | Execution Requirement |
|--------|------|------|---------|
| 1 (highest) | Constraint red lines | Plot red lines, character forbidden zones, boundary bans | Never delete or change red line content at any time. Word count compression must not cause red lines to go missing. Sensory exceptions apply only to sound clues that are red line key information. The style card's `banned_words` / `hard_constraints` merge into red line level; no compression may delete or change them |
| 2 | Word count | Target word count hard constraint (based on the chapter outline memo's target word count, plus or minus 10%) | When over the limit, use the compression strategy: compress low-weight scenes first (scenes 1/2 transitions / medium-weight passages), recommending compression to within 100 words (keeping 1 environment switch sentence + 1 character action sentence + 1 emotion / atmosphere blank sentence); compression must not touch red lines. The core conflict passages of high-weight scenes do not move |
| 3 | T1 words (style words) | Seemingly, a trace of, could not help, involuntarily, and similar (suddenly / abruptly / fiercely are context-sensitive, at most 4 per chapter, with red line passages treated leniently) | When over the threshold, keep the ones with a narrative function first and delete functionless filler words. When they appear in red line passages, treat them leniently (keeping the rhythm function) |
| 4 | Cognitive verbs | Realized, discovered, understood, felt, thought, believed | Replace with external actions or direct perception description; they may be used briefly at key emotional nodes (at most 2 per chapter, see narrative-rules.md Rule 2); otherwise no concession |
| 5 | Senses / "X for a moment" | 2 senses per scene as the main ones, rising to 3 when the atmosphere allows; the "X for a moment" structure (X了一下) | A sound clue that is red line key information may not count. When other senses exceed the threshold, trim them. Keep an "X for a moment" when it has a rhythm function |
| 6 (lowest) | Writing standards | All other writing standards and technique guidance (including narrative rules and the base iron rules) | Automatically yields when it conflicts with items 1-5 above. Narrative rules outrank same-level writing standards rules and sit below layers 1-5. Priority within the writing standards level when they conflict: **style (style card quantitative values) > the author's latest memory preferences (writing-memory) > base iron rules (writing-base) > genre-example genre baseline**. Quality-layer trade-offs (such as the compression order once the word count target is met) follow this order: cut environment / passerby / transition description first, keeping emotional passages and style-required passages |

### Word Count Compression Details (priority 2 execution rules)

```
1. Never delete: plot red line content (2-4 items), character key turning points, emotional turning point passages
2. Compress first: low-weight scenes (first the transition passage of the first low-weight scene), non-core passages of medium-weight scenes
3. Compress next: secondary elements of high-weight scenes (environment description from 3 sentences to 1, passerby description trimmed)
4. Do not move: the core conflict passages of high-weight scenes
```

### Sensory Conflict Details (priority 5 execution rules)

```
1. Detail each scene mainly with 2 senses, rising to 3 when the atmosphere allows (such as hearing + touch); write the rest in a passing line
2. Exception: a sound clue (a character's hearing judgment, a key environmental sound) that is red line key information for this chapter may be kept as a brief plain description and does not count toward the 2-sense quota
3. Exception trigger condition: the sound clue must be part of the red line content (such as a gunshot as a combat key signal, or approaching footsteps as a danger marker), not an environmental decoration sound
4. When the "X for a moment" structure in a scene exceeds the threshold, keep the ones with a rhythm function (such as "paused for a moment", which has a sense of stopping) and delete the redundant ones
```

### Ambiguous Condition Coverage (boundary examples for priority 5)

The following examples help judge whether a rule triggers:

| Rule | Applies when the condition holds | Does not apply when the condition does not hold |
|------|-----------------|-------------------|
| Word count compression, low-weight scene compression | The scene weight is labeled "low" and its content is not red line key information | The scene weight is "low" but it carries red line key information (such as a key foreshadowing appearing in a low-weight scene) |
| Sensory exception, sound clue | The sound is red line key information and is presented as a brief plain description ("the door opened", three words) | The sound is a long environmental description (200 words of wind / footsteps detail) or non-red line information |
| Cognitive verb replacement | The cognitive verb can be replaced with an external action or direct perception ("he felt afraid" becomes "his fingers dug hard into his palm") | Outside key emotional nodes, always replace (at most 2 per chapter, see narrative-rules.md Rule 2); do not yield for word count or other rules. When the word count is over the limit, use the compression strategy (compress low-weight scenes first, see the "cognitive verbs vs word count" ruling in the global conflict ruling table) |

## Step 2: Fill In by the 6-Element Prompt Structure

Filling order: role → task instructions → background (prior context + character initial states) → input (scene raw material + scene type identification) → scene methodology loading and conversion → examples → output (constraint red lines + writing standards + texture requirements)

### Role

Extract the genre from genre-setting.md and copy it verbatim without expanding it.

### Task Instructions

Extract from chapter.md memo + volume.md + writing-style:

- Chapter number, its role in the whole volume, this chapter's driving force, information release rhythm
  **Word count and compression strategy (a standalone section, injected under the "word count and compression strategy" subsection of the Task Instructions paragraph):** format as below.
- **Narrative goal**:
  - Core suspense (in question form, not a plot summary) + suspense state (resolved / deepened / shifted)
  - Reader emotion (the feeling on leaving, one emotion word or scene)
  - Satisfying beat design (type + planting scene + release scene)

### Background

#### Prior Context

Extract the ending scene from the previous chapter's outline (`chapters/vol-{N}-ch-{M-1}.md`) emotional_design (emotional hook emotional_hook + chapter-end landing, taking the last stretch of mood_progression) + required_changes; the volume outline's previous chapter summary helps (do not read the previous chapter's main text in full; archives/ is forbidden to read):
- The previous chapter's ending scene, emotional residue, reader information gap

When the previous chapter is ch-1: always write "No prior chapters; the opening cuts straight into the character's current action", and ban long world background introductions.

#### Author Preference Memory

Extract entries relevant to this chapter's writing from `.claude/memory/writing-memory.md` + `.claude/knowledge/permanent-memory.md` and inject them:
- Only inject **actionable** author preferences (style / rhythm / description / dialogue); filter out entries whose scenario does not match or whose wording is vague
- Keep each entry in "original text → conclusion" form, so writer knows this is the author's explicit requirement, not a general suggestion
- Deduplicate the writing memory and permanent memory (permanent memory was promoted by high frequency; keep only the permanent version of a repeated entry)
- If the memory files are empty or have no matching entries, mark this subsection "(none)" and do not force-fill it

Injection example:
```
Author preference memory:
- "The dialogue is too wordy → keep dialogue short and broken; if half a sentence says it, do not use a whole sentence" (对话太啰嗦了 → 对话要短、要碎，能用半句说完不用整句) applies to this chapter's dialogue scenes
- "The action description is not detailed enough → write the key action's process clearly; do not write 'he opened the door', write 'he turned the doorknob, and the door hinge sounded once'" (动作描写不够细 → 关键动作写清过程，不写'他打开门'，写'他拧门把、门轴响了一声') applies to this chapter's action scenes
```

#### Character Initial State

Extract from chapter.md character states + the character files:
- Each character's start → turn → landing + micro-habits

### Input

#### Scene Raw Material

Extract from chapter.md **scene cards** + information gap relationships:
- Split scenes by boundary signals (location change / time jump / emotional turn), 2-4 scenes, matching the chapter outline's scene cards one by one
- Fill four fields per scene: core event / **information gap** / emotional turning point + scene weight

**Core event filling:**
- Input source: the chapter outline **scene card's three elements** (what the protagonist wants to do / what blocks them / what suspense there is), not from outline.key_points
- Format: an external event chain, linked with arrows ("action A → action B → action C"), not written as a narrative paragraph
- Forbidden: character inner activity, cognitive verbs (realized / discovered / understood), emotion conclusions

The information gap takes the matching pair of relationships for this scene from the chapter outline knowledge_state's "information gap relationships".

**Scene type identification:** Analyze each scene's core event and identify the scene type (allowed values: dialogue / fight / environment / inner-mono / transition / group-scene). Record them as a list, for loading the scene methodology and picking narrative rules in the next step.

#### Narrative Rule Selection

Pick the narrative rules to inject from the identified scene type list, using the mapping below (Rules 1-7 are defined in `.claude/knowledge/narrative-rules.md`, the single authoritative source). When a rule is written into the prompt's "writing standards" section, it needs to carry a character settings link: derive the behavior traits from the character settings file's concrete fields before injecting; do not just write the character name.

**Use the character settings data already read in Step 1** (Step 1.4 already read this chapter's involved character files) and extract the fields used for rule link derivation:

| Field Needed | Source | Purpose |
|---------|------|------|
| Basic information, language traits | Catchphrases, swearing, speaking habits | Rule 6 dialogue style |
| Layer 2 self-positioning | How the character sees themself | Rule 3 narrative order, Rule 6 expression posture |
| Layer 3 values | What cannot be yielded | Rule 3 perception priority, Rule 6 dialogue at key moments |
| Layer 4 abilities | Combat experience, perception precision | Rule 1 perception signals, Rule 3 combat perception |
| Layer 5 skills | What they are good at, what they can do | Rule 1 perception types, Rule 4 example range |
| Layer 6 environment | Birthplace, upbringing | Rule 1 perception habits, Rule 4 life experience, Rule 6 register |

**Character link derivation table (the agent derives concrete behavior from the field values per this table):**

| Rule | Fields Read | Derivation Logic | Injected into the Rule Note |
|------|---------|---------|---------------|
| Rule 1 (perception signal first) | Layer 6 + Layer 4 + Layer 5 | Upbringing decides perception familiarity (a hunter notices animal sounds / footprints; a dock worker notices voices / boat sounds), ability decides precision, skill decides the type | "This chapter's POV character {name} comes from {layer 6 keyword} and is good at {layer 5 skill}; the perception signal they notice first is {derived type}" |
| Rule 2 (restrained cognitive verbs) | Layer 6 + Layer 5 + Layer 4 + Layers 1/2/3 (supporting) | Perceptions inside the character's experience range are written directly; things outside the range do not appear in the narration. Derive the blind spot from the most information-rich layer of the 6 cognitive layers: layer 1 (world rules they do not understand), layer 2 (knowledge that does not fit their positioning), layer 3 (behavior logic they do not accept), layer 4 (techniques beyond their ability), layer 5 (skill areas not mastered), layer 6 (environment rules never encountered) | "Delete 'he felt' and start directly from {character name}'s experience: they are good at {skill}, so they would notice {related perception}, but do not understand {blind spot} (derived from cognitive layer {number})" |
| Rule 3 (order by perception intensity) | Layer 3 + Layer 2 + Layer 4 | Layer 3 decides the information priority (a brother's safety > the mission), layer 2 decides the narrative posture, layer 4 decides how much detail can be captured | "The narration orders by what matters most in {character name}'s heart: layer 3 values {entry} decide {entry A} comes before {entry B}" |
| Rule 4 (use concrete experience) | Layer 6 + Layer 5 + language traits + Layer 1 | Examples come from the character's own experience; language traits decide the wording; worldview decides the description scale | "Examples come from {layer 6 upbringing}; the language carries the flavor of {language trait}; do not use metaphors the character has never encountered" |
| Rule 6 (dialogue fits the character) | Language traits + Layer 6 + Layer 2 + Layer 3 | Language traits decide catchphrases / swearing, layer 6 decides the register, layer 2 decides the expression posture, layer 3 decides the dialogue at key moments | "{Character A}'s language trait is {catchphrase}; coming from {layer 6}, they are used to {derived register}. It is not speaking like a person; it is speaking like this person" |

**General narrative rules (must be injected in any chapter):**
The following 3 rules are the general web novel baseline, applying to all genres (the rule definitions are in `.claude/knowledge/narrative-rules.md`; this is the injection operation detail). The genre example file's (genre-example) special style requirements stack on top of this baseline; they do not replace it. That is, the genre injection passage may add point of view / rhythm / atmosphere requirements, but it does not override the baseline's "has warmth" positioning.
- Rule 2: restrained cognitive verb use (at most 2 per chapter). Prefer replacing them with actions or direct perception ("he felt afraid" becomes "his fingers dug hard into his palm"), but they may be used briefly at key emotional nodes
- Rule 5: causality presented naturally. Delete excess explanatory connectors (because / so / therefore), but keep necessary causal links. Write them only when the causal relationship needs to be clear to the reader
- Rule 7: narration natural and warm. A moderate narrative presence is allowed: natural atmosphere buildup, psychological summaries, and sensory description are fine as long as they are not piled up. Do not go to extreme plain description just to "not perform" and lose the reading warmth

**Append by scene type:**
| Scene Type | Rules Appended | Character Link Focus |
|---------|---------|-------------|
| dialogue | Rule 6 | Language traits → catchphrases / swearing; layer 6 → register; layer 2 → expression posture; layer 3 → dialogue at key moments |
| environment | Rule 1 + Rule 4 | Layer 6 → perception priority classification; layer 5 → example sources; layer 1 → description scale |
| inner-mono | Rule 2 strengthened | Layer 3 → current conflict trigger point; layer 6 + layer 2 → the character's possible bodily reactions right now |
| fight | Rule 3 | Layer 4 → combat experience level; layer 3 → priority judgment in combat; layer 2 → attack / defense / roaming style |
| transition | Rule 4 + Rule 7 | Layer 6 → what the character might drift off thinking about right now; layer 2 → how they drift off |
| group-scene | Rule 6 | Each character's language traits + layer 6 + layer 2 (derived independently per character) |

Requirements for each rule's examples:
- Write the positive and negative examples with the "speaking with impurities" feel of a real person; do not use purified "standard human speech"
- Vague summaries are allowed ("anyway, it was like that" / "so noisy it was unbearable", 反正就那样 / 吵得要命)
- Tone words and half-finished sentences are allowed
- Uneven information density is allowed: not every sentence pushes the plot

**Output example** (the complete style for injecting into the writing standards, narrative rules section):

```

General narrative rules (must be injected):
· Rule 2: restrained cognitive verbs. Wrong: "He realized he had walked into a noisy tavern" (他发现自己走进了一家嘈杂的酒馆)
  Right: "The door opened, and it was unbearably noisy. Drinkers, people playing drinking games. Anyway, that kind of place." (门一开，吵得要命。喝酒的、划拳的。反正就那种地方。)
  Character link: 陆征 is a former criminal police officer (layer 6); his reconnaissance experience (layer 5) makes him notice people first,
  not the drinks. He scans the seat layout, where the back door is, and whether anyone is watching him.
· Rule 5: only state the action result. Wrong: "He accidentally bumped into the person next to him" (他不小心蹭到了旁边的人)
  Right: "The aisle was that narrow; two steps and he bumped into three people." (过道就那么窄，两步路蹭了三个人。)
· Rule 7: narration natural and warm.
  Wrong: "He squinted at the doorway, and only after a long while made out a rough picture" (他眯着眼站在门口，好半天才瞅出个大概) → overworked description, dragging rhythm
  Okay: "The doorway was packed with people. He stood there watching for a good while, a bit irritated inside. All heads; he could not see what was going on inside at all." (门口挤满了人。他站在那儿看了好一会儿，心里有点烦躁，全是人头，根本看不清里面什么情况。) → the warm version
  Right: "He stood at the doorway watching for a good while. All people, packed with nowhere to stand." (他站门口看了好一会儿。全是人，挤得没地方站。) → the minimal version, suits fast-paced passages
  Note: both versions are usable; pick by the passage's rhythm. Do not use the minimal version throughout the whole text.

Scene type additions (dialogue + environment):
· Rule 6: dialogue fits the character. 陆征 speaks directly, in short questions (language trait, former criminal police officer);
  方岩 avoids conflict; when nervous he lowers his head and drinks tea instead of answering (layer 3, does not want trouble).
· Rule 1: perception signal first. When 陆征 enters, he scans people first (layer 5, reconnaissance habit),
  not the decoration / menu.
· Rule 4: use concrete experience. Examples come from the criminal police career (layer 6); do not use metaphors the character has never seen.
```

→ Inject into **Output, Writing Standards**

**Scene focus + weight labels (written at the end of each scene):**
```
This scene's focus: core conflict / character emotion / information gap (pick one of the three)
This scene's weight: high / medium / low
```
Focus replaces the generic "focus lock" description in the writing methodology. Each scene declares its own focus type, so writer no longer checks back across passages. A high-weight scene's focus must be applied together with the "sensory layering trade-off".
- High weight = detail the actions, micro-expressions, and psychology; takes more than 70% of this chapter's ink
- Medium weight = normal narration; neither deliberately trimmed nor lavish
- Low weight = quick transition, brief strokes, no extra details added
- Each chapter must have 1 high-weight scene and at least 1 low-weight scene
- The first scene is forced to high weight (volume-x chapter-1's first scene must cut straight into action; long worldview asides are banned)

#### Paragraph Breakdown (write the paragraph structure guidance)

Extract the paragraph structure guidance from chapter.md **outline.key_points**. Do not rewrite the narration: the core event already wrote "what happens"; the paragraph breakdown only answers "how this paragraph is written".

**Splitting rules:**
- Match the key_points split one by one; each key_point maps to one paragraph
- Write structure guidance per paragraph (not narrative description), including:
  - Paragraph function (advance / transition / build suspense / dialogue)
  - Rhythm emphasis (fast short sentences / medium / relaxed)
  - Shot cue (close-up / medium shot / long shot)
  - Notes ("do not write inner life" / "pure external action" and similar constraints)
- One sentence may be added about "how this paragraph differs in rhythm from the other paragraphs"

**Format (written at the end of Input, Scene Raw Material):**

```
¶1 [function] | [rhythm emphasis] | notes
¶2 [function] | [rhythm emphasis] | notes
...
```

Each ¶ maps to one key_point. This list lets writer's paragraph structure and rhythm be decided by the key_points, **different in every chapter**.

#### Writing Methodology

```
Before writing, execute in this order:
1. Focus lock: for each scene, identify its single "core conflict" or "character emotion" or "information gap" (pick one of the three, do not stack them). 70% of the whole text's ink concentrates on this focus object; secondary environment, passersby, and background are all brief strokes. Do not describe every element with equal length. High-weight scenes are detailed to the action and perception level and must apply the "sensory layering trade-off" rule at the same time (see the next item); low-weight scenes may transition quickly, but must not violate the focus lock or sensory layering trade-off rules.
2. Sensory layering trade-off: detail mainly with 2 senses, rising to 3 when the atmosphere allows; write the remaining senses in a passing line. Avoid even stacking across all dimensions. **Sound exception: when a sound clue is red line key information for this chapter and is presented as a brief plain description (1-2 sentences), it may not count toward the sense quota (such as a gunshot as a combat key signal, or approaching footsteps as a danger marker); environmental decoration sounds (birdsong, hawkers, and similar) are not exceptions**
3. Narrative rhythm alternation: one dense action / dialogue passage + one short psychological blank + one light environment transition, cycling. No consecutive long description, consecutive dialogue, or paragraphs of equal length throughout
4. Information release control: key foreshadowing and character secrets are released in fragmented pieces, never fully explained at once. Blank space is allowed; do not write every setting and psychology through to the end
5. Structural red lines (avoiding paragraph structures that look machine-written at a glance at the source; the ruling details are in the "structural heat source law" section of `.claude/knowledge/anti-ai.md`. When they conflict with the author's settings or this chapter's other requirements, the author side wins):
   a. Do not play Q&A as a ping-pong chain: when one question and one answer run for more than about 8 beats in a row, split them. Insert action beats, turn the answers into reported speech, or cut the beat count. This is a "round" scale, running alongside the "pure dialogue 6-8 sentences, insert an action" sentence-count scale; neither replaces the other
   b. Cold open at the chapter start: enter dialogue or action directly, with time and place carried in the passing narration; do not open with a "time marker + scene state" pattern
   c. At most one result per scene gets an explicit receipt (signature taking effect / resources arriving / authorization confirmed / a clue verified; only one is paid off). Face-slapping, establishing authority, and other satisfying beat payoffs are written as usual, but do not fire multiple receipt sets in the same scene
   d. No bridge chains or proof chains: new information must not run straight through "appears → confirmed unknown → pointed at who can know → immediately approved"; private memories do not lay out evidence in a row or stamp "so he cared a lot" at the paragraph end
   e. No summary, elevation, or preview at the chapter end (same direction as the anti-AI ending rules); this chapter follows its chapter-end landing. Hooks are planted as usual, only do not let every sentence line up evidence for the final sentence
```

→ Inject into **Task Instructions** (the writing methodology section)

#### Scene Methodology Loading (scene type → examples + Output, Writing Standards)

Based on the scene type list identified from the scene raw material, dynamically load the matching scene writing methodology. After loading, the methodology goes through the four-step conversion: **short examples go into Examples, detailed guidance goes into Output, Writing Standards**.

**Core principle: sparse extraction; full coverage is forbidden.** For each scene type, pick only 1-2 techniques to write into the prompt; the rest do not appear. Applying all of them is strictly forbidden.

**Loading mechanism:**

1. **Deduplicate** the scene type list to get this chapter's non-repeating scene types (such as ["dialogue", "environment"])
2. For each type, read in this order:
   a. General methodology: `.claude/knowledge/scene-craft/<type>/universal.md` (must exist)
   b. Genre specialization: `.claude/knowledge/scene-craft/<type>/<current-genre>.md` (read when present; skip otherwise)
3. The general methodology + genre specialization merge into that scene type's methodology source
4. **Filter by tag**: read the `## Tag Selection Guide` section of `.claude/knowledge/scene-craft/<type>/universal.md` and match suitable tags from the scene's core event. From the merged methodology, randomly pick 1-2 methodology entries matching the tags. If a scene matches no tag, randomly pick 1-2 of the most general entries from the general methodology
5. **Special check 1: character appearance description**. Additionally check whether each scene's core event triggers appearance description conditions (a new character appears / a character's appearance changes / the scene involves appearance perception). If triggered, load `.claude/knowledge/scene-craft/appearance/universal.md` + `.claude/knowledge/scene-craft/appearance/{genre}.md` (when present), and after the four-step conversion, append them to Output, Writing Standards
6. **Special check 2: psychological activity / inner monologue**. Additionally check whether each scene's core event + emotional design + key decisions trigger psychological description conditions (the character meets a major event / violent emotional swing / faces a major decision / a face-slapping reversal / inner conflict). If triggered, load `.claude/knowledge/scene-craft/inner-mono/universal.md` + `.claude/knowledge/scene-craft/inner-mono/{genre}.md` (when present), and after the four-step conversion, append them to Output, Writing Standards
7. **Special check 3: death / sacrifice scenes**. Additionally check whether each scene's core event involves a character's death / sacrifice / exit (keywords: killed in battle, fallen, sacrificed, killed). If triggered, load `.claude/knowledge/scene-craft/death-scene/universal.md`, and after the four-step conversion, append it to Output, Writing Standards
8. **Always loaded (always loaded but sparsely injected)**. No matter what scenes this chapter contains, always load the following files, but each only needs 1-2 refined guidance sentences injected, without expanding all the techniques:
   - `.claude/knowledge/scene-craft/prose/universal.md` (always pick the 1 most relevant: concretizing abstractions / shot rhythm / verbs instead of adjectives / sensory stacking, pick one of the four)
   - `.claude/knowledge/scene-craft/pov/universal.md` (always pick the 1 most relevant: point of view boundary / physical transition / information gap mismatch, pick one of the three)
9. If a type's directory does not exist (such as `group-scene/` or `transition/`, temporarily empty frameworks), skip that type

**Context filtering (key step):**

After reading the methodology, do not copy it directly into Output, Writing Standards. It must go through the **four-step conversion method**, turning the general methodology into writing guidance for the concrete scene.### Four-Step Conversion Method: General Methodology → Scene Writing

Using the "action interweaving" methodology in `dialogue/universal.md` as an example, showing the four-step conversion flow:

```
Methodology original text received:
  "Dialogue needs action interweaving. Once pure dialogue passes 6-8 sentences, the reader loses the sense of the scene"

What was read in the character settings (the characters involved in the current chapter):
  方岩: cautious by nature, avoids conflict, lowers his head to drink tea / looks away when nervous
  陆征: former criminal police officer, direct, leans forward / taps the table with a finger when pressing with questions

What was read in the information gap:
  方岩 knows the inside story of the case suppressed three years ago, and 陆征 does not

This chapter's emotional rhythm:
  A tense stretch (陆征 is pressing with questions)
```

#### Step 1: Anchor the Character

Do not apply the methodology to "Character A" / "Character B"; apply it to concrete people.

> **Ask: what is this character's personality? What state are they in this scene?**

- How a cautious person dodges vs how a direct person presses with questions
- How an arrogant person shows impatience vs how an insecure person dodges
- The same scene, the same methodology, comes out completely differently with a different character

#### Step 2: Anchor the Information Gap

Fix the **information asymmetry** between characters. This decides the direction and manner of "not telling the truth".

> **Ask: who is hiding? Hiding what? Why hide it?**

| Information Gap Type | Effect on Dialogue Writing |
|-----------|----------------|
| 方岩 knows, and 陆征 does not | 方岩 is dodging and defending; 陆征 is probing and closing in |
| 陆征 knows, and 方岩 does not | 陆征 is guiding and laying out; 方岩 is responding passively |
| The reader knows, and the characters do not | The reader waits anxiously for the character to expose it; the dialogue plants foreshadowing that "the audience can see but the character cannot" |

#### Step 3: Anchor Emotion and Rhythm

The methodology's concrete writing must match this chapter's emotional direction.

> **Ask: is this scene's emotion tense, relaxed, or turning?**

| Emotion Stretch | Dialogue Rhythm | Action Interweaving Frequency | Sentence Length |
|--------|---------|-------------|---------|
| Tense / confrontation | Fast, interrupting each other | Low (actions disturb the tension) | Short fragmented sentences |
| Repressed / hiding | Slow, long pauses | High (actions answer instead of words) | Sentences cut off halfway |
| Relaxed / reconciliation | Natural, with pauses | Medium (intermittent actions) | Complete sentences |

#### Step 4: Fused Output

Combine the conclusions of the first three steps into one **scene writing guidance that can go directly into Output, Writing Standards**.

```
Wrong example (general methodology, no conversion):
"Dialogue needs action interweaving; insert an action every 6-8 sentences."
→ Every chapter's dialogue is written to one template; the characters have no distinction.

Right example (after the four-step conversion):
"This dialogue's information gap is 方岩 knows the inside story, and 陆征 does not.
方岩 is cautious by nature; when dodging, he lowers his head and drinks tea. Every time 陆征 asks a question, he takes a sip and does not answer.
陆征's way of pressing as a former criminal police officer is to lean forward and close the distance. With every question, he moves a little closer.
The emotion is a tense stretch, so the dialogue rhythm is fast. 陆征 presses with short sentences, and 方岩 dodges with actions; no long explanatory sentences."
→ The methodology lands on concrete characters, a concrete information gap, and a concrete emotion, so each character is written differently.
```**Four-step conversion method flowchart:**

```
scene-craft methodology
↓
Step 1: Anchor the character (extract personality and micro-habits from the character settings)
↓
Step 2: Anchor the information gap (extract who is hiding from whom from knowledge_state)
↓
Step 3: Anchor the emotional rhythm (extract the current emotional stretch from emotional_design)
↓
Step 4: Fused output → write into Output, Writing Standards
```

**Bottom line:**
- Wrong: each methodology applied by rote, so every character's dialogue is written the same way
- Right: after Steps 1-4 conversion, the same methodology shows differently on different characters
- Wrong: copying a whole passage of a scene-craft file
- Right: randomly picking 1-2 of the most relevant entries from the methodology, refining them after the four-step conversion
- Wrong: skipping the conversion and writing generic guidance such as "Character A says... Character B says..."
- Right: the converted guidance lets writer directly write dialogue that fits the character's personality
- Right: sparse technique use, at most 2 per type; the rest of the techniques do not appear in the prompt

> If this chapter has only dialogue scenes, pick 1-2 methodology entries from `dialogue/universal.md` + `dialogue/{genre}.md` (when present), inject them into Output, Writing Standards after the four-step conversion each.
> If there is both dialogue and combat, pick 1-2 methodology entries from each of the two scene directories (including genre specialization), convert each against its own scene's characters and conflict, then inject them.
> If a methodology entry's character does not take part in the current scene, skip that entry.### Conversion Example Library (few-shot)

The following shows two methodology entries going through the complete process from "general → four-step conversion → Output, Writing Standards injection". Your conversion output should reach the same level of concreteness and context awareness.

#### Example 1: Dialogue Scene · 方岩 and 陆征 (suspense · hiding and probing)

```

"A character does not tell the truth. The gap between the surface words and the deeper meaning is the tension of the dialogue."


Characters:
方岩: police insider, knows the inside story of the case suppressed three years ago, cautious by nature, avoids conflict
陆征: former criminal police officer, investigating this case, direct and sharp, leans forward when pressing with questions
Information gap:
方岩 knows the inside story, and 陆征 does not (方岩 is hiding, 陆征 is pursuing)
Emotional rhythm:
A tense stretch: 陆征 is applying pressure, 方岩 is defending


Step 1 anchor the character:
方岩 is cautious, so his way of dodging is lowering his head to drink tea, looking out the window, not answering
陆征 is direct, so his way of pressing is leaning forward, closing the distance, staring at the other side
Step 2 anchor the information gap:
方岩 knows but cannot say, so he is defending, deflecting with "I do not know about this case"
陆征 does not know but wants to confirm, so he is probing, forcing a reaction with concrete details
Step 3 anchor the emotional rhythm:
A tense stretch means short sentences and a fast rhythm, with little action interweaving (but key actions are amplified at the crucial moment)
Step 4 fused output:
方岩 knows what happened three years ago but cannot say it (information gap), and 陆征 is pressing with questions.
陆征 leans forward and presses with short sentences; 方岩 lowers his head and drinks tea without answering, using dodging actions instead of answers.
The tense stretch is fast-paced. There are no long explanatory sentences, only pressing questions and silence alternating.


"The information gap: 方岩 knows the inside story, and 陆征 does not. 陆征 presses with short sentences, leaning forward;
方岩 dodges, lowering his head to drink tea and not answering. A fast rhythm in the tense stretch, with no long explanatory sentences,
only pressing questions and silence alternating. 方岩's dodging is not silence; every time 陆征 asks about something key,
he deflects with an action (drinking tea / looking out the window / asking back 'how far have you gotten')."
```

#### Example 2: Combat Scene · 叶秋 and 王虎 (xianxia (immortal cultivation) · power suppression)

```

"Results > process. The reader cares who won and what it cost, not the details of every move.
Make the cost visible. Do not write 'the protagonist was hurt'; write the consequences of the wound."


Characters:
叶秋: Qi Refining layer 3, just broke through not long ago, still unfamiliar with the newly gained power
王虎: Qi Refining layer 2, a thug leader who bullies people with his cultivation
Information gap:
叶秋 just broke through, and 王虎 does not know (王虎 thinks 叶秋 is still at the cultivation he saw last time)
Emotional rhythm:
A satisfying beat stretch: the reader expects 叶秋 to show his strength


Step 1 anchor the character:
叶秋 just broke through and has not adapted to the new power, so his strikes have the rawness of "not holding back"
王虎 thinks the other side is still a weakling, so he starts by underestimating him and only gets serious after taking a loss
Step 2 anchor the information gap:
王虎 does not know 叶秋 broke through, so his underestimation comes from the information gap, not on purpose
叶秋 knows he got stronger, but he is not sure exactly how much stronger, so there is a probing element
Step 3 anchor the emotional rhythm:
A satisfying beat stretch means the rhythm is fast first (王虎's shock at being crushed) then slow (showing the consequences)
Step 4 fused output:
Do not write the moves one by one; focus on "result → 王虎's reaction → visible cost".
Write it from 王虎's point of view: before he reacts, he has already flown out; only then does he see that 叶秋's
realm is already different.


"This combat is driven by the information gap: 王虎 does not know 叶秋 already broke through.
Do not write the move details; use results + reactions instead: before 王虎 sees clearly what happened, he has already flown out.
Make the cost visible: 叶秋 did not hold back, his fist smashed through the wall, and the tiger's mouth of his hand split open and bled.
Rhythm: fast (王虎 flies out) → slow (he looks up at 叶秋 and realizes the realm changed)
→ lingering resonance (叶秋 looks at his own hand, not quite sure how strong he is now)."
```

### Examples

Fill them in from the scene methodology after the four-step conversion. For each scene type, pick 1-2 methodology entries and write them as examples after the four-step conversion. An example is a demonstration of "how a concrete character writes in a concrete scene", not a copy of the general methodology.

**Example labeling requirement:** At the end of each example, mark in parentheses the methodology name it demonstrates, such as "(demonstrates: sensory layering trade-off, touch + hearing)". The label helps writer understand the mapping between the example and the writing methodology and improves the methodology's transferability. When the same methodology has multiple examples, label only the first one.

### Output

Assemble it as a **flat structure**, merging the writing standards, narrative rules, and constraint red lines into one "non-violable rules" list to reduce nesting and priority judgment cost. **Scene writing guidance** (loaded from the scene methodology and converted in four steps) and **texture requirements** keep their own subsections.

#### Non-Violable Rules

**Priority (high to low):**
1. **Constraint red lines**: plot red lines, character forbidden zones, boundary bans (when red lines conflict with narrative rules, satisfy the red lines first)
2. **Word count**: target word count hard constraint (use the compression strategy when over the limit)
3. **T1 words / cognitive verbs / senses**: style thresholds, restrained cognitive verbs, sensory layering
4. **Narrative rules** (outranking same-level, other writing standards rules)
5. **Other same-level writing standards rules**

**Red line constraints:**
- Conflict ladder, plot red lines (2-4 items), boundary bans, character forbidden zones. Extract them from chapter.md memo and fill them in completely, with no placeholders

**Web novel style baseline (applies to any chapter):**
- Linear narration throughout; refuse perfect narration: blank space and jumping thoughts are allowed; deliberately piled-up techniques are forbidden; poetry-style tone is forbidden
- Restrained cognitive verbs (Rule 2), natural causality (Rule 5), narration with warmth (Rule 7) are injected by the "concrete narrative rules" section above; this baseline does not repeat them

**Style suggestions (may be departed from):** (**Inject only in the undistilled state; delete this section in the distilled state**. Style follows the Case 2 rendering section, strictly matching with deviation at most 20%, with no may-depart clauses)
- Point of view: the point of view type is passed per settings/writing-style.md (undistilled = the main text's "narrative identity" field; distilled = the rendered [Point of View] section). It is defined at the settings stage and consistent across the whole book, **not redefined in the prompt**; this chapter's POV character is read from chapter.md outline.pov (chosen within the set point of view type).
- Description: use action perception to drive the narration; senses serve the atmosphere.
- Rhythm: paragraphs rise and fall naturally; sentence patterns alternate long and short. The above may be departed from moderately when it serves emotion or plot.

The genre example file's (genre-example) prompt injection passage stacks on top of the web novel style baseline; it does not replace the baseline.
- **Concrete narrative rules**: {pick the matching rules from the "narrative rule selection" section by this chapter's scene types, injecting each rule after linking it to the character settings}

**Deduplication check after assembly:** the same meaning appears only once in the output.

#### Scene Writing Guidance

(Picked from the scene methodology loading and four-step conversion results): this chapter involves {N} scene types ({type list}. Allowed values: dialogue / fight / environment / inner-mono / transition / group-scene). For each type, inject 1-2 concrete writing guidance entries.

#### Writing Style Constraints

**Two-state branch:**

- **confidence=0 (undistilled) → inject the main text's qualitative four fields:** read the main card's four fields (narrative identity / hard constraints / common AI mistakes / description layers) and inject them into this section; the section title stays "Writing Style Constraints", unchanged.
- **confidence>0 (distilled) → Case 2 rendering:** this section outputs `[Vocabulary] [Sentence Patterns] [Rhythm] [Rhetoric and Senses] [Emotional Expression] [Dialogue Style] [Transitions] [Point of View] [Hard Rules] [Overall Tone] [Style Reference Examples] [Plot Context] [Writing Requirements]` (the Case 2 structure), with the rendering steps following `.claude/knowledge/style-distill/prompt-templates/rendering-rules.md` (exact values self-contained: ranges / enums / sparse injection matrix). banned_words / hard constraints go into "Non-Violable Rules, Red Line Constraints".

**Division of labor:** when confidence>0, the quantitative sections ([Vocabulary] through [Point of View]) come from the rendering rules, and the voice layer ([Hard Rules] [Overall Tone] [Style Reference Examples]) is passed through verbatim; the scene-craft methodology only injects "how to write" (the scene writing guidance subsection), and the two are not listed side by side as duplicates.

#### Texture Requirements

Extract from chapter.md memo + the author's additions. **Append the "imperfection" constraints:**
- Useless details: allow fragmented everyday-life details that do not serve the main line (when present); they must belong to the current scene and the character's point of view, and are not inserted by quota
- Dialogue rhythm: allow half-finished sentences, tone words, pauses, repetition
- Paragraph precision layering (assign ink by weight): high-weight scenes (at least 3 action / perception level details for the core conflict / emotion / information gap development), medium-weight scenes (normal narration rhythm, with character interaction driving the plot), low-weight scenes (optional transition template reference. Note: the following is a reference structure and may be fine-tuned by context. 1 environment switch sentence + 1 character action sentence + 1 emotion / atmosphere blank sentence, at most 100 words)

#### Appendix: Model Paragraphs (non-binding reference)

**Statement:** The model paragraphs below are only a style reference; writer may choose whether to follow them, and they must not replace any instruction above. Fill them in from the case methodology after the four-step conversion, with methodology tags attached.

## Step 3: Conflict Detection

After filling in, check:
- The prior context's emotional residue equals the first character's starting point in the character initial states (consistent)
- The character initial states' landings equal the scene raw material's turning points (consistent)
- The scene raw material's information gap is consistent with the task instructions' chapter driving force (suspense driven means every scene has an information gap)
- The constraint red lines' conflict ladder layer matches the task instructions' chapter driving force (threat driven means the layer should not be entry level)
- The writing standards are filled in (non-empty)
- The texture requirements field is filled in (non-empty) and contains the "imperfection" constraints

After filling everything in, read through the whole thing once. Cover the field names and check whether each seed reads as a narrative scene or a writing instruction.

## Step 4: Acceptance Self-Check

Check prompt.md item by item:

| Check Item | Standard |
|--------|------|
| Structure complete | Role / task instructions / background / examples / input / output, all 6 elements present |
| Fields filled completely | Each element's fields have values, no `______` placeholder left |
| writing-style injected | Two states: confidence=0 → qualitative four fields injected (unchanged); confidence>0 → all eleven Case 2 sections present (quantitative sections rendered per rendering-rules; hard rules / tone / examples passed through; no voice layer means the Section 6.0b fallback); banned_words deduplicated against the anti-ai banned words with no duplicates; no placeholder leakage |
| Style block and guidance without duplicates | The "Writing Style Constraints" block and the "Scene Writing Guidance" block have no semantic duplicates (quantitative constraints are not injected side by side with methodology techniques) |
| banned_words without duplicates | The injected banned_words, merged and deduplicated with the anti-ai banned words, appear with no duplicates |
| Hard constraints complete | Character red lines, worldview forbidden zones, and plot red lines all present |
| Prior context has a sense of scene | A concrete ending scene description (ch-1 marked as having no prior text, cutting straight into action) |
| Scene weights labeled | Every scene's end is labeled high / medium / low, with 1 high-weight + at least 1 low-weight scene |
| Writing methodology | The task instructions already inject the four: focus lock / sensory layering / rhythm alternation / information control |
| Examples filled | At least 1 scene writing example after the four-step conversion |
| Sparse techniques | Each scene type is injected with only 1-2 technique guidance entries, without full coverage (techniques are covered by the anti-ai step) |
| Anti-AI injection range | The writing standards contain the human-feel positive points + T1 most toxic sentence pattern short table + meta-narrative ban + genre anti-AI positive and negative examples; fatigue word thresholds / T2 / T3 / tier 2 banned words are not injected (cleanup belongs to the anti-ai agent after the draft is finished) |
| Point of view strategy | Read from outline.pov; inject the POV character + the narrator's limited scope + the supporting character information passing rules |
| Description / rhythm / sentence pattern requirements | Description techniques have values; rhythm contains the whole + emotional stretch changes + natural paragraph length rise and fall; sentence patterns alternate long and short, with no 4 consecutive sentences of the same structure |
| Emotion requirements | Subtle emotional contrast is allowed (when present); it must come from the character's personality or the scene's pressure, without breaking emotional coherence |
| Information requirements | Idle brushstrokes / digressions / dead clues are allowed (when present); they must belong to the current scene and character, without requiring one per chapter by quota |
| Paragraph breakdown | The scene raw material's end contains ¶ structure guidance (at least 2 paragraphs, each with function / rhythm / notes) |
| Narrative rules injected | The writing standards section contains a "narrative rules" subsection; the 3 general rules + the scene-appended rules are all filled in, and each rule has a linked character settings derivation |
| No source labels | The prompt text contains no `来源：` / `(来源)` or similar source labels; writer does not need to know where a rule came from |
| Texture fields | Have the "imperfection" constraints (half-finished sentences / everyday-life details / paragraph precision layering) |
| No meta leakage | Contains no self-referential phrases such as "the following is the novel's main text" |
| No whole-paragraph copying of the chapter outline | Each layer's content is injected after distilling, not copied verbatim |
| Word count compression strategy injected | The task instructions, target word count field contains an elasticity note + compression strategy description ("plus or minus 10% acceptable, narrative completeness first" / "when over the word count, compress low-weight scenes first; never delete red lines", or similar wording) |
| Sensory exception injected | The writing methodology, sensory layering trade-off contains the sound exception rule (key sound clues may not count toward the 2-sense quota) |

**After everything passes**, write it to `prompts/vol-{N}-ch-{M}-prompt.md`.
If it fails, go back to Step 2 and fix the matching elements.
