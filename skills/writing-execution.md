
# writer skill


## Process Overview

```text
Step 1: Preparation (confirm volume/chapter numbers and prompt completeness)
Step 2: Clear context (reduce interference)
Step 3: Writing (executed by a sub-agent)
Step 4: Verify output (file exists + word count met)
Step 5: Narrative rules self-check (go through the 7 positive rules one by one)
```

> The AI original snapshot (`.agent/{chapter}-draft-ai.md`) is created by **updater at archive time** (copied from the draft, updater-archive Step 1); writer is not responsible for saving it.

## Rewrite Branch (when writing-order.md contains rewrite_of)

1. Read the rewrite_of / round / violations fields of writing-order.md.
2. Read the original Case 2 prompt prompts/vol-{N}-ch-{M}-prompt.md plus the violations report file.
3. Only rewrite the paragraphs matching the entries marked "violated" in the violations report, moving them toward the "suggestion"; keep all other paragraphs as their original text.
4. After finishing, write archives/*.draft.md as usual and mark the order DONE (keep the round value unchanged; novel-agent increments it).

## Step 1: Preparation

1. Confirm the volume number `{N}` and chapter number `{M}`
2. Read `prompts/vol-{N}-ch-{M}-prompt.md` and confirm all 6 elements are complete. Word count and driving force come from the task instructions; narrative point of view comes from Output, Writing Standards
3. **Breakpoint detection**: read the `resume_from:` field of `writing-order.md`. If present, read the matching partial file and resume writing (see the resume branch in Step 3); if absent, write fresh

## Step 2: Clear Context

Before calling the sub-agent, clear the main agent's reading history (genre-example, anti-ai, and other files are no longer needed after this). Reduce the interfering context for the sub-agent.

## Step 3: Writing (executed by a sub-agent)

Start a sub-agent (a flash model is recommended) and pass it the following complete instructions:

```markdown
## Base (read first, then the instructions below stack on top)
First Read `.claude/knowledge/writing-base.md` as the writing base (the core writing trade-off iron rules + hard output rules + banned behaviors).
The instructions below take effect stacked on top of the base. Ruling rules: the prompt compliance layer constraints (red lines / word count / T1 words / cognitive verbs / senses, and similar, see the conflict ruling table layers 1-5) take priority over the base;
quality trade-offs inside the compliance boundary (style / emotion priority / primary vs secondary distinction, and similar) follow the base. The compression order cuts environment / passerby / transition description first, keeping emotional passages and style-required passages.

## Role
Write the full chapter's main text. Read only the prompt file and write the complete chapter's main text in one pass. All chapter outline constraints have been injected into the prompt.

## Scope
- Do: read the prompt and write the whole chapter in narrative paragraph order
- Do not: do not read the volume outline / chapter outline / archives, do not modify the prompt, do not write other chapters, do not write any file under settings/

## Inputs
- `.claude/knowledge/writing-base.md`: writing base (read first)
- `prompts/vol-{N}-ch-{M}-prompt.md`: main input (6-element prompt, style already rendered inside)
- `settings/genre-setting.md`: genre settings

## Outputs
- `archives/vol-{N}-ch-{M}-{slug}.draft.md`: full chapter main text draft (final)
- `archives/vol-{N}-ch-{M}-{slug}.draft.partial.md`: partial draft (checkpoint during writing, saved as you go)

## Writing Rules
- Write in the prompt's narrative paragraph order 1 to N, with smooth transitions between paragraphs
- **Before writing each scene, run the "five-line anti-closed-loop card"** (to avoid paragraph structures that look machine-written at a glance; the detailed ruling rules are in the "structural heat source law" section of `.claude/knowledge/anti-ai.md`): (1) what does each person in this scene want to get done right now (2) whose immediate reaction produces the resistance (3) how far does this scene play before stopping (4) which results are left unexplained for the reader to see for themselves (5) which piece of information is held for the next scene and not paid off in this one. If (3)-(5) cannot be answered, think them through before starting to write this scene
- Each paragraph's writing guidance must be fulfilled (scene / emotion / character state / ending scene)
- End on the scene or state specified by the last paragraph's ends_with
- The main text contains no explanation, exposition, or guiding words; cognitive verbs are restrained per Rule 2 (at most 2 per chapter at key emotional nodes; elsewhere do not write "he felt" or "he realized")
- Word count is not below 90% of the target word count in the prompt's task instructions (the lower bound of target plus or minus 10%)
- **After finishing each narrative paragraph, immediately do two things (do not wait until everything is written)**:
  1. Append that paragraph to `.draft.partial.md` (overwrite style, keeping the latest progress)
  2. Write that partial path into the `partial_path:` field of `writing-order.md` (overwrite update)
  → This is the interruption checkpoint. **Even if the run is cut off midway, the order still holds the latest partial pointer**, so novel-agent can locate the resume point on restart. After all paragraphs are written, write the complete `.draft.md` and clear `partial_path:`

## Resume (only when resume_from exists)
If this order carries `resume_from: {partial path}`:
1. Read the partial file (allowed, see Inputs) and count how many paragraphs are already written (call it K)
2. Continue writing from narrative paragraph K+1 of the prompt, **without rewriting** the content before paragraph K
3. Keep the content already in the partial file; append newly written paragraphs after it
4. If the partial file is empty or cannot be read, treat it as a fresh write and report it

## Inputs (added when resuming)
- `archives/vol-{N}-ch-{M}-{slug}.draft.partial.md`: the partial file resume_from points at (read only when resuming, to count K paragraphs)

## Prohibited (a violation means a rewrite)
- Do not add character names, details, or descriptions on your own that do not appear in the prompt
- Do not invent information on your own that the chapter outline / prompt did not ask for
- Extra character naming: if the prompt gives no name, do not write a name; use generic references such as "those people" or "another person" instead
- Format violations: the main text must not use `---` separators, Markdown headings (`#` `##` and similar), or other Markdown markers

**Principle: do not add plot, dialogue, or character behavior on your own that the prompt did not write; reasonable detail filling and atmosphere building are allowed. If the prompt wrote "he waits for someone at a cafe", you may write the atmosphere, small actions, and thoughts, but you may not write "he waited and his enemy showed up".**
```

After the sub-agent finishes writing, it returns. The main agent checks whether the output file exists.

### Step 3.5: Partial Record Check (the authoritative signal for interruption recovery)

partial_path is **written into the order by the writing sub-agent in sync after each paragraph** (see the writing rules above); after the main agent returns, it only does the **check fallback**:

1. **Check the order**: read the `partial_path:` of `writing-order.md`. If the sub-agent already wrote it normally, no change is needed
2. **Fallback write**: if the partial file exists but `partial_path:` is missing from the order (the sub-agent failed to write it), the main agent writes that line in
3. **Completion cleanup**: once the complete `.draft.md` is written, clear `partial_path:` (the breakpoint is complete; novel-agent no longer triggers a resume)

> Why partial_path is recorded in the order and not in status.md: writer has no status.md write permission (least-privilege design), but the order is the only dispatch file writer can write. novel-agent reads the order on restart and knows the partial position.

## Step 4: Verify Output

| Check Item | Action |
|--------|------|
| Does the output file exist? | Does `archives/vol-{N}-ch-{M}-*.draft.md` exist? If not, retry once |
| Is the word count met? | At least 90% of the chapter outline word count (the lower bound of target plus or minus 10%)? If short, **first write back to the prompt layer, then ask the author** (see "Handling a word count shortfall" below); do not silently accept it |
| Is the file location correct? | Written into the archives/ directory and not somewhere else? |
| Is the partial cleaned up? | After the complete `.draft.md` is written and verified, delete `.draft.partial.md` and clear the order's `partial_path:` (the breakpoint is complete; leave no residue) |

**Handling a word count shortfall (explicit degradation, not silent):**
If the word count is below 90% of the target (the lower bound of plus or minus 10%):
1. **Record the gap in writing-order.md**: before `status: DONE`, append a line to the file, `quality_gap: ch{M} word count short, target X actually written Y`, so the degradation is traceable (writer has no status.md write permission, so the gap is recorded in the order, and novel-agent syncs it to status.md when it detects DONE)
2. **Write back to the prompt layer**: in the next chapter's prompt, raise the weight of the matching scene (for example, move the word count allocation of a low-weight scene to the compressed core scene), instead of only accepting it this time
3. **Ask the author again**: "This chapter's word count did not reach the target (X/Y). It is recorded and will be written back in the next chapter's prompt. Accept the draft as-is, or rewrite with additions?"
4. Author accepts → continue; author asks for additions → rewrite the chapter; do not silently push an under-target draft into anti-ai

## Step 5: Narrative Rules Self-Check

Read through the freshly written draft and do one quick check against the narrative rules injected in the prompt (Rules 1-7 are defined in `.claude/knowledge/narrative-rules.md`, the single authoritative source; this table only lists the self-check actions):

| Rule | Self-Check |
|------|------|
| Rule 1 (perception signal first) | Does a paragraph start with a "protagonist + perception verb" structure? (he saw / he heard / he discovered) → if so, change it to throw the perceived fact first |
| Rule 2 (restrained cognitive verbs) | Are words such as "he discovered / he felt / he noticed" too dense? → prefer replacing them with actions; keep at most 2 per chapter at key nodes |
| Rule 3 (order by depth of impression) | Is there a continuous "first, then, next, finally" structure? → reorder by perception intensity |
| Rule 4 (use concrete experience) | Are there labels such as "all kinds of / one after another / a series of"? → replace with concrete sensory details |
| Rule 5 (natural causality) | Is there too much causal explanation (because / so / therefore in a row)? → delete the excess and keep what is necessary |
| Rule 6 (dialogue sounds human) | Is the dialogue complete with subject, verb, and object and lacking spoken flavor? → add personal pronouns / tone words / verbal tics |
| Rule 7 (narrative natural and warm) | Is there excessive rhetoric or deliberate affectation? → change to natural narration, allowing moderate narrative warmth. Do not go to extreme plain description just to "not perform" |

Fix problems directly when found; **do not leave banned material for the anti-ai pipeline**. anti-ai's job is to catch what slipped through, not to clean up after you.

## Step 6: (None. The snapshot is created by updater)

The AI original snapshot `.agent/{chapter}-draft-ai.md` is not writer's responsibility: writer's Write whitelist does not include `.agent/`, and the snapshot is **copied from the draft by updater at archive time** (updater-archive Step 1, item 1, as the archive diff baseline). After writer finishes, just hand the draft.md to the pipeline.
