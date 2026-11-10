# Chapter Outline Generation Skill

Calibrated reference material becomes one executable chapter outline. Format rules follow `.claude/knowledge/chapter-setting-style.md`.

## Process

Set the emotional anchor → set the conflict ladder → build the information gap → break into scene cards → banned list → Memo fill-in → Hooks → setting-change notice (optional) → output

## Refining the Chapter Outline

Fill in each item following the format rules in `chapter-setting-style.md`. The execution order follows below; the exact format and wording follow that specification. The first three steps (emotional anchor / conflict ladder / information gap) match the volume outline methodology, only with the granularity refined from "volume" to "chapter".

**a. Set the emotional anchor**: Two layers: **read this chapter's position in the volume's emotional direction from the volume outline** + **discuss this chapter's internal emotional direction with the author**. For the first chapter, the agent picks an opening hook technique on its own from the genre and style (see `.claude/knowledge/plot-craft/opening-hooks.md`), drafts an opening scene card, and shows it to the author for confirmation. Do not show a list of techniques for the author to pick from.

> Reading from the volume's emotional direction: where has this chapter reached? Is it "the middle of the repression stage" or "the face-slapping release stage"?

This chapter's dominant emotional tone is set by its position on the volume's arc. A repression stage is written with a repressive tone; a release stage with a satisfying tone.

After fixing the position, ask the author about this chapter's emotional direction (ask only about plot, not technique):

> "The volume has reached the {repression / release / turning point} stage. How do you picture the reader's emotions moving in this chapter? For example, what emotion does it start from, what event turns it midway, and what emotion does it end on?"

After the author answers, the agent judges whether it is specific enough:
- Specific enough (at least 3 steps, with causal anchors, and the chapter-end landing supports the volume's next step) → move to the next step
- Not specific enough (only two nodes such as "repress then lift", or the chapter-end landing contradicts the volume direction) → ask for the concrete event or turning point

Technique choices (arc mode, intensity distribution) are matched by the agent on its own and are not shown to the author to pick. Once the emotional direction is set, record it in mood_progression.

Part of the volume direction becomes a chapter-internal micro-arc (calm → unease → confirmed predicament → repression), and the chapter-end landing must support the volume direction's next step.

**b. Set the conflict ladder**: Two layers: **read this chapter's layer in the volume's conflict ladder from the volume outline** + **discuss the obstacle escalation inside the chapter with the author**.

> Reading from the volume's conflict ladder: which layer has this chapter reached? "Layer 1, entry" or "Layer 4, ultimate"?

This chapter's obstacle intensity is set by the volume's layer. An entry layer is written as blocked information; an ultimate layer as a head-on showdown.

After fixing the layer, ask the author about this chapter's obstacle design (ask only about plot, not technique):

> "This chapter is at the {layer} stage. What obstacles do you picture the protagonist running into this chapter? How many scenes, and where does each scene get stuck?"

After the author answers, the agent judges whether it is specific enough:
- Specific enough (2-3 obstacle steps, each harder than the last, with turning points between layers) → move to the next step
- Not specific enough (only one obstacle named, or no escalation between obstacles) → ask: "After the first obstacle, what then? What did the protagonist do that changed the situation?"

Technique choices (conflict escalation methods: environmental pressure / goal substitution / chain reaction, and similar) are matched by the agent from plot-craft on its own and are not shown to the author to pick.

One layer of the volume becomes a small in-chapter ladder (probe → encounter → escalation), each step harder than the last:

```
Volume conflict ladder: Layer 1 Entry → Layer 2 Escalation → Layer 3 Turning Point → Layer 4 Ultimate
                        ↑
This chapter's position: Layer 2, Escalation

In-chapter small ladder:
  Scene 1: Probe: the protagonist tries to make contact and finds the other side on guard        ← entry level
  Scene 2: Encounter: the protagonist is warned / blocked, confirming the resistance exists        ← escalation
  Scene 3: Conflict escalation: the protagonist persists in investigating, the other side increases pressure       ← in-chapter climax
  End: the protagonist is in a more dangerous position, supporting the volume's next step (Layer 3, Turning Point)
```

**Bottom line:** The in-chapter ladder is not the same thing repeated. If all three scenes are "the protagonist checks information, gets stopped, checks it another way", that is flat, not a ladder.

**c. Build the information gap**: The information gap is defined at the volume level (start → end); at the chapter level it is where the information gap **changes dynamically**.

> Reading from the volume's information gap: which position on the volume's information gap arc does this chapter inherit? Is the volume at the "villain has the advantage" stage or the "protagonist is catching up" stage?

After fixing the position, ask the author about this chapter's information gap design (ask only about plot, not technique):

> "The volume's arc has reached the {stage}, and the characters appearing this chapter are {list}. How do you plan the information to flow this chapter? Who does not know what at the opening, what is revealed midway, and what new question is left at the end?"

After the author answers, the agent judges whether it is specific enough:
- Specific enough (change across opening ↔ middle ↔ ending, with the new information gap driving the next chapter) → move to the next step
- Not specific enough (only the opening state, no change) → ask: "Who discovered what midway? What suspense is left for the reader at the end?"

One stretch of the volume's arc becomes an in-chapter information gap change (set → use → reveal → new), where each reveal creates a new information gap:

```
Volume information gap arc: the protagonist does not know, gradually revealed → information gradually moves toward the protagonist
                       ↑
This chapter's position: the protagonist starts noticing contradictions, but the villain's advantage still stands

In-chapter information gap change:
  Opening: the protagonist does not know what the scene's clues mean (the reader is in the same place as the protagonist)
  Middle: a contradictory detail is found, and the protagonist starts feeling something is wrong (the information gap is narrowing)
  End: being followed, the protagonist knows someone is watching (new information gap: the villain knows, the protagonist does not know who)
```

State clearly which appearing character knows what and who does not know what this chapter, and mark the change process:

```markdown
Information gap relationships (opening → ending):
· Opening: the protagonist does not know where 苏棠 went; the reader is in the same place as the protagonist
· Middle: the protagonist finds a contradiction; the information gap narrows (the protagonist caught up a step)
· End: the villain knows about the tailing; the protagonist does not know who the other side is ⬅ new information gap, driving the next chapter
```

The information gap change sets this chapter's driving rhythm (suspense / threat / goal / relationship / information-gap driven).

**d. Set the point-of-view strategy**: Confirm whose point of view this chapter is narrated from.

> "Whose point of view is this chapter written from? The default is the protagonist's limited POV. If you want to switch POV, for example writing the first two paragraphs from the villain's POV, how do you switch, and where do you switch back? Note: the POV type (limited / omniscient / which person) is defined at the settings stage (settings/writing-style.md narrative.perspective, consistent across the whole book). Here you only set **this chapter's POV character** and how to switch; do not redefine the POV type."

Record it in the outline's POV field (`outline.pov`).

| Strategy | Description | Example |
|------|------|------|
| Single-protagonist limited POV | Locked to one person throughout, writing only what they perceive | `陆征 (single-protagonist limited POV)` |
| Multi-segment POV switching | Switch the POV character by paragraph | `First 2 paragraphs villain POV, then switch back to 陆征` |

After the POV is set, move on to breaking into scene cards (e); the three anchor points of a scene card are based on this POV character's perceptions. For multi-segment switching, each segment uses its own POV character as the baseline.

**e. Break into scene cards**: Break down the key points using the three-anchor method in Section 2 (from direction to outline points). Each key point maps to one scene card, with the same underlying logic as the volume outline. If this chapter involves tragedy or heartbreaking plot, see `.claude/knowledge/plot-craft/tragedy-techniques.md` for the emotional rhythm design; for emotional pull see `.claude/knowledge/plot-craft/emotional-pull.md`:

```
Scene card three elements → how they appear in a key point
  What the protagonist wants to do → action anchor (what the character concretely does)
  What is blocking them → judgment anchor (what obstacle the character meets / what contradiction they discover)
  What suspense makes the reader want to keep reading → the whole text's emotional hook + information gap
```

Break out the key_points (count by the Section 2 word-count back-calculation method: by default 2500 words is about 5 points), writing 2-3 sentences per point with the three-anchor method (senses + action + judgment). When presenting the complete plan, have the author confirm it. Show the key points in the summary format of Step 1 of the acceptance section in `.claude/knowledge/chapter-setting-style.md`; the complete chapter outline (with English field names) is only written to the file and its raw text is not shown. Author-facing wording follows `.claude/knowledge/author-communication.md`.

**f. Banned list**: Ask about and record prohibitions following the section "(What not to do: hard-constraint red lines)".

**g. Chapter Memo fill-in**: Fill in the 8 parts in Section 3 (chapter outline content list) one by one (the emotional anchor / information gap / conflict ladder are already done in a-c; fill in the remaining fields here):
1. current_task (current task)
2. reader_expectation (reader expectation)
3. payoff_plan (payoff plan)
4. downtime_functions (transition functions)
5. key_choices (key decisions)
6. knowledge_state (character information state; the information gap relationships are already done in c, so here add the list of what each character knows / does not know)
7. required_changes (end-of-chapter changes, consistent with "what changes at the end" in the conflict ladder in b)
8. scene_cards (scene cards; the three elements are already done in the scene card breakdown in e, so merge them into the chapter outline here)

After filling them in, show the key points in the summary format of Step 1 of the acceptance section in `.claude/knowledge/chapter-setting-style.md` for the author to confirm. The complete memo contains English field names; only write it to the file, do not show the raw text directly.

**h. Emotional Design (refinement)**: Fill in the emotional details following Section 4 (emotional design): mood_progression (already done in a), intensity_peak, intensity_level, emotional_hook, micro_payoffs.

**i. Hooks operations**: Write this chapter's hook operations (plant / advance / close) into `payoff_plan`. See the three hook design methods (cognitive mismatch / information gap / countdown) in `.claude/knowledge/plot-craft/hook-techniques.md`. At chapter level, the source of truth for a hook is each chapter.md's `payoff_plan` field; at character level, it is the hooks field in `settings/character-setting/*.md`.

**j. Setting-change notice (optional)**: Setting change needs discovered during planning / calibration. Used to notify novel-agent to dispatch updater. When needed, append to the end of the chapter outline:

```
## Setting Change Notice

- **Target:** settings/character-setting/{id}.md
- **Type:** status update / new character / worldview update / timeline
- **Reason:** {why this change is needed}
- **Details:** {concrete description of the change}
```

> **Consumption rule**: Before writing the next chapter, novel-agent greps `volumes/` + `chapters/` for the `## Setting Change Notice` heading; when found, it dispatches a setting-update-order (inputs pointing at the source file); after updater finishes the change, it **removes the notice block from the source file** (delete the block with Edit, to prevent repeat consumption).

Only append when there is a change; omit it otherwise.

## Output

Write to `chapters/vol-{N}-ch-{M}.md`, status becomes `outline`
