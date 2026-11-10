# Prompt Audit SOP

## Core Principles

- **You are not prompt-crafter**; you carry no burden of "maintaining your own work"
- **Your only duty is to find problems**, not to fix them and not to explain why it was written that way
- The more problems found, the more successful the audit
- Every finding must include verbatim evidence and a knowledge base comparison
- The bar for passing the audit is "no sufficient evidence of a problem", not "it looks fine"

## Inputs

- `prompts/vol-{N}-ch-{M}-prompt.md`: the prompt to audit
- `chapters/vol-{N}-ch-{M}.md`: the chapter outline (especially the outline matching the scene sequence)
- `settings/genre-setting.md`: the genre type
- The methodology files under `.claude/knowledge/scene-craft/` matching this chapter's scene types
- `.claude/knowledge/scene-craft/index.md`: the scene methodology index

## Audit Dimensions

### Dimension A: Scene-Technique Coverage (sparsity check)

**Purpose:** Make sure Output, Writing Standards has writing guidance for the matching scene types, without requiring full coverage.

**Steps:**
1. Extract every scene type from the chapter outline's scene sequence into a deduplicated list
2. Check the index structure of `scene-craft/index.md` to confirm a methodology exists for each scene type
3. Check Output, Writing Standards item by item. **Each scene type needs at least 1 technique guidance; full coverage is not required, and some scene types may have no technique guidance**

**Checklist:**

| Check Item | PASS Standard |
|--------|-----------|
| At least 1 scene type has technique guidance | Output, Writing Standards contains writing guidance for at least 1 scene type |
| Scene weights labeled | Every scene in the scene sequence has a high / medium / low weight label |
| Comparison consistency (loose) | The number of scene types with technique guidance is at most the scene type count minus 1 |

**Ruling standard:**
- Scene type count > 2 and no technique guidance at all → **FAIL**
- Everything else → **PASS (relaxed check; incomplete coverage allowed)**


### Dimension B: Knowledge Point Traceability

**Purpose:** Make sure every scene writing guidance in Output, Writing Standards has an original knowledge source and went through contextual adaptation (the four-step conversion), rather than copying the methodology's original text directly.

**Steps:**
1. Extract each scene writing guidance from Output, Writing Standards (independent semantic blocks appearing as "guidance", "requirement", "rule", or similar)
2. For each guidance, find the matching methodology original text in `scene-craft/`
3. Judge the conversion quality

**Conversion quality levels:**

| Level | Ruling Standard | Example |
|------|----------|------|
| Successful conversion | The methodology went through the four-step conversion, adapted to a concrete character name, information gap relationship, and emotion stretch | "When 方岩 dodges, he lowers his head and drinks tea. Every time 陆征 presses with a question, he takes a sip and does not answer" |
| Partial conversion | The methodology was cited but the applied formula shows through; at least one of character / information gap / emotion is missing | "When a cautious character dodges, they use actions instead of answering" (does not say which character, or what action) |
| Not converted | The methodology's original text was copied directly, or only the character name was changed | "A character does not tell the truth. The gap between the surface words and the deeper meaning is the tension of the dialogue" |
| No-source guidance | A writing requirement in Output, Writing Standards has no matching methodology in scene-craft | It may have been invented by prompt-crafter or brought in from another source |

**Ruling standard:**
- Any "not converted" entry → **FAIL**
- "No-source guidance" at least 2 entries → **WARN**
- "Partial conversion" at least 50% of all guidance → **WARN**
- Everything else → **PASS**


### Dimension C: Executability Evaluation

**Purpose:** Judge whether the writing guidance in Output, Writing Standards is concrete enough for writer to execute directly.

**Steps:**
1. Judge the writer executability of each instruction in Output, Writing Standards, one by one

| Level | Features | Example |
|------|----------|------|
| Concrete | writer can write directly from it, with clear operating instructions | "When 方岩 dodges, he lowers his head and drinks tea. Every time 陆征 presses with a question, he takes a sip and looks away" |
| Abstract | writer knows what to do but not how to write it concretely | "Use actions to show the scene's tense atmosphere" |
| Vague | writer reads it and does not know where to start writing | "Pay attention to the dialogue's tension" / "Keep a good grip on the rhythm" |

**Ruling standard:**
- Vague instructions at least 1 → **FAIL**
- Abstract instructions at least 50% of all guidance → **WARN**
- Everything else → **PASS**


### Dimension D: Four-Step Conversion Completeness

**Purpose:** For each methodology loaded from scene-craft, check whether it fully went through the four-step conversion.

**Checklist (check each methodology one by one):**

| Conversion Step | PASS Standard |
|----------|-----------|
| Step 1 anchor the character | The guidance names a concrete character and shows how that character's personality / current state affects the writing |
| Step 2 anchor the information gap | The guidance shows how the information asymmetry between characters affects the writing (who is hiding / who is pursuing / what effect it has) |
| Step 3 anchor the emotional rhythm | The guidance states how the current emotional stretch affects the writing (short sentences in tense stretches / long sentences in relaxed stretches, and similar) |
| Step 4 fused output | The three above are fused into one directly executable guidance, not three parallel explanations |

**Ruling standard:**
- Any methodology missing any of Steps 1-3 → **FAIL**
- All methodologies completed the four-step conversion → **PASS**


### Dimension E: Inter-Layer Consistency

**Purpose:** Make sure the rules in Output, Writing Standards do not contradict other sections.

**Checklist:**

| Check Item | PASS Standard |
|--------|-----------|
| Output, Writing Standards point of view vs scene sequence emotional turning points | Does the point of view choice support the scene's emotional goal (first person strengthens immersion vs third person pulls back for distance) |
| Output, Writing Standards rhythm vs Task Instructions, Narrative Goal | The rhythm requirement does not suppress the satisfying beat's release (a tense stretch still using a relaxed rhythm is a contradiction) |
| Output, Writing Standards description vs constraint red lines | The description method does not violate a plot red line |
| Output, Writing Standards anti-AI rules vs texture requirements | The anti-AI rules and the texture requirements do not cancel each other out |

**Ruling standard:**
- Any contradiction → **FAIL**
- All consistent → **PASS**


### Dimension F: De-AI Check (new core dimension)

**Purpose:** Make sure the prompt suppresses the AI's even, tidy writing habits at the root.

**Checklist:**

| Check Item | PASS Standard | FAIL Signal |
|--------|-----------|----------|
| Sparse technique use | Each scene type is injected with only 1-2 techniques; full coverage is not required | Requires each scene type to use 3 or more techniques, or "all techniques" |
| Primary vs secondary distinction | Output, Writing Standards explicitly requires primary vs secondary ink distinction (repeat high-weight passages, keep low-weight passages brief) | No primary vs secondary distinction rule at all, implying "even description" |
| Four-step execution logic | Output, Writing Standards contains all four: focus lock / sensory layering / rhythm alternation / information control | 2 or more of the four missing |
| Imperfection constraints | The texture requirements contain half-finished sentences / everyday-life details / paragraph precision layering | No "imperfection" constraint at all |
| Ban on even stacking | There is an explicit instruction banning full-dimension sensory stacking, equal-length paragraphs, and sets of rhetoric | No related ban |
| Warmth balance | The prompt does not demand extreme fragmentation (no hard indicator such as "single-sentence paragraphs at least X%") | The prompt demands single-sentence paragraphs at least 25% or "forced hard cuts" |

**Ruling standard:**
- All 6 items PASS → **PASS (de-AI design complete)**
- 4-5 items PASS → **WARN (suggest adding the missing items)**
- 3 or fewer items PASS → **FAIL (serious de-AI defect)**


### Dimension G: Conflict Ruling Execution Check

**Purpose:** Make sure the prompt already has a conflict ruling strategy built in, rather than leaving the ruling responsibility to writer. This dimension is the core verification of "inlined optimization": writer should only execute, not make priority decisions.

**Steps:**
1. Check whether the prompt's task instructions contain a word count compression strategy
2. Check whether the prompt's writing methodology, sensory layering trade-off, contains a sound exception note
3. Check whether the prompt's constraint red lines are marked as highest priority (explicitly saying "red line content cannot be compressed")
4. Check whether the prompt's writing standards contain anything contradicting the conflict ruling above (especially old wording such as "narrative rules have higher priority than all constraints")

**Checklist:**

| Check Item | PASS Standard | FAIL Signal |
|--------|-----------|----------|
| Word count compression strategy injected | The task instructions, target word count field contains an elasticity note (plus or minus 10% acceptable) and a compression strategy ("when over the word count, compress low-weight scenes first; never delete red lines", or similar wording) | The target word count field has no elasticity note or compression strategy, leaving word count control to writer |
| Sensory exception injected | The writing methodology, sensory layering trade-off has a sound exception rule (a key sound clue may not count toward the 2-sense limit) | No sound exception, or the sound exception's conditions are incomplete (missing the two conditions "red line key information" and "brief plain description") |
| Red line priority confirmed | The constraint red lines section explicitly states "red line content cannot be compressed / cannot be deleted" | The red lines only list content, without stating their highest priority status |
| No internal contradiction | The writing standards state that narrative rules are "lower priority than red lines / word count / T1 words / cognitive verbs / sensory rules" or similar wording | Old wording such as "narrative rules have higher priority than all constraints" remains, contradicting the level table |

**Ruling standard:**
- All 4 items PASS → **PASS (conflict ruling inlining complete)**
- 3 items PASS → **WARN (suggest adding the missing items, but deliverable)**
- 2 or fewer items PASS → **FAIL (conflict ruling inlining seriously defective, must be fixed)**


### Dimension H: Rule Deduplication (hard gate)

**Purpose:** Make sure the same meaning appears only once in the prompt, with no duplicate rules brought in from multiple sources (writing-style / anti-ai / scene-craft / genre-example). This is the check on the "deduplication check after assembly" (prompt-crafting.md Step 2): the assembly flow required it, but an independent view must confirm it was actually done.

**Steps:**
1. Read the whole prompt and extract every rule with a constraining nature (quantity lines, bans, thresholds, hard requirements)
2. For each rule, ask: has this meaning already appeared elsewhere in the prompt?
3. Group by category: cross-source duplicates / quantity line duplicates

**Checklist:**

| Check Item | PASS Standard | FAIL Signal |
|--------|-----------|----------|
| Cross-source duplicates | The same constraint (dialogue density / em dash / word count, and similar) appears only once in the whole prompt | The same rule appears once each in the writing standards, scene guidance, and texture requirements |
| Quantity line duplicates | The same object has only one definition (such as "dialogue at most 8 lines" appearing only once, at the anti-AI injection) | The same quantity line is written once in the anti-AI injection and once in the scene methodology |

**Ruling standard:**
- Any duplicate → **FAIL** (when sending it back, point out which two entries are the same thing and suggest which one to merge)
- All unique → **PASS**

**Operation criteria (a hard gate must be decidable):**

The two cases ruled as duplicates (FAIL):
1. **Same-format duplicate**: the same object is defined twice in the same format (a quantity line / threshold / ban fully repeated, such as "dialogue at most 8 lines" appearing twice)
2. **Complete duplicate**: two rules worded almost identically, about the same thing, with no added information

Cases not ruled as duplicates (effective redundancy, not FAIL):
- **Equivalently worded constraints**: "keep dialogue short" + "pure dialogue at most 8 lines" + "let characters speak at length less often" point at the same thing but each has its own emphasis (one gives the principle, one gives the number, one gives the counter-example). That is effective redundancy; keep it. The audit only requires **same-format complete duplicates** to be merged; it does not require every semantically equivalent constraint to be merged into one.


### Dimension I: Rule Reordering (position effect check, hard gate)

**Purpose:** Make sure the least violable rules sit at the front of the prompt, using the LLM's property of following the start / end most strongly. This is the practical landing check of the "non-violable rules" list in descending priority.

**Steps:**
1. Locate the prompt's "non-violable rules" list (and the constraining paragraphs such as the writing standards and texture requirements)
2. Check the order of the arrangement against the priority levels
3. Check whether low-priority rules have mixed into the hard-rules zone

**Priority levels (high to low):**
Red lines (plot red lines / character forbidden zones / boundary bans) > word count (hard target) > T1 words / cognitive verbs / senses (style thresholds) > narrative rules > other same-level writing standards rules

**Checklist:**

| Check Item | PASS Standard | FAIL Signal |
|--------|-----------|----------|
| Red lines on top | The constraint red lines sit at the very front of the "non-violable rules" list | Red lines sit behind techniques / suggestions |
| Priority descending | The whole thing is ordered red lines > word count > T1 words > narrative rules > writing standards | Priority inverted (technique before red lines, narrative rules before word count) |
| Scene guidance at the bottom | Advisory techniques (scene writing guidance, texture requirements) sit in the appendix / examples section and do not enter the hard-rules zone | Low-priority techniques mixed into the "non-violable" zone |

**Ruling standard:**
- Any priority inversion → **FAIL**
- All in order → **PASS**

**Note:** Reordering only concerns order; it does not change content. If the audit finds a hard rule in the wrong position, send it back noting "this entry should move up / down"; do not rewrite the rule itself.

## Audit Ruling General Rule

| Condition | Conclusion |
|------|------|
| Any of Dimensions B / E / F / G FAIL | **Audit fails** → prompt-crafter must return to THINK and fix it |
| Any of Dimensions H (deduplication) / I (reordering) FAIL | **Audit fails** → rules are duplicated or priority is inverted; must be fixed and re-audited (hard gate; delivering with the defect is not allowed) |
| Only one of Dimensions A / C / D FAIL, everything else PASS | **Audit passes** → technique coverage / executability / conversion completeness do not block; incomplete is allowed |
| No FAIL, WARN at least 4 items | **Audit fails** → suggest fixing |
| No FAIL, WARN at most 3 items | **Audit passes** → deliverable |

**FAIL scenarios (must return for fixing):**
- Missing hard worldview / character / plot red line constraints (Dimensions B / E)
- Meta leakage exists (Dimension E)
- No primary vs secondary writing rules, serious de-AI design defect (Dimension F)
- Rules duplicated and not merged (Dimension H), priority inverted (Dimension I)

**PASS scenarios (allowed even when incomplete):**
- Techniques incomplete (Dimension A: some scenes have no guidance) → allowed
- Some scenes brief, description asymmetric (Dimension C: some abstract) → allowed
- Some methodologies incompletely converted (Dimension D: some incomplete) → allowed
- **Core principle: as long as the hard constraints are complete, the de-AI rules exist, there is no meta leakage, the rules are not duplicated, and the priority is not inverted, it can be delivered.**

When the audit fails, state during the handover:
- Which dimensions had what problems
- The evidence for each problem (verbatim quote + knowledge base comparison)
- The suggested fix direction (not specific to how to write it; only point out where the problem is)
