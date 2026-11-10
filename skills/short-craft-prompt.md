# short-craft-prompt SOP: Writing Contract Assembly

> Executed by short-planner. After the outline is confirmed and before writing begins, assemble the story-level writing contract `stories/{slug}/prompt.md`.
> The contract has a dual identity: the basis for writing plus the acceptance baseline (after the final draft, short-verifier checks fulfillment against it).

## Six-Element Structure

```
# Writing Contract: {Story Title}

## Role
(Genre + this story's narrative identity; copy setting verbatim, do not expand)

## Task Instructions
(Emotional goal / core suspense / reader emotion / satisfying-beat design / word count and compression strategy, plus or minus 10% /
  paywall point position and density before and after it)

## Background
(Prior context: when this story is the first, write "No prior content, the opening cuts straight into action" /
  author preference memory: take entries relevant to this story from `<platform>/memory/author-feedback.md`,
  noting only actionable entries as "original text → conclusion", writing "(none)" when nothing matches / character initial states)

## Input
(Scene sequence: each scene's core event / information gap / emotional turning point / weight + this story's emotional chain and stage coverage +
  technique landing points + the throughline prop's three semantic steps + catalytic anomaly position)

## Examples
(1-2 entries per scene type, after the four-step conversion, with the demonstrated technique name noted at the end)

## Output
### Non-Violable Rules (priority, descending)
1. Constraint red lines (plot red lines / character forbidden zones / boundary bans, filled in completely, no placeholders)
2. Word count (per-section floor + total word count + compression strategy: cut transitions first, never touch the red lines)
3. Banned items (banned punctuation / naming ban list / modern vocabulary table (for historical-style stories) / degree adverb cap)
4. Narrative rules (a concrete follow-through after each emotion word / possessive clearing / late entry and early exit / dialogue four functions / prop's three semantic steps)
5. Other same-level writing standards

### Conflict Ruling Table (the writing side only executes, never rules)
Numeric: the concession order among section length floor vs total word count vs five-part proportions vs reversal position vs paragraph form
Qualitative: logical consistency takes priority over satisfying or tormenting beats. When a satisfying beat would require a character to act against their motive, change the satisfying beat design, not the character logic;
      every key character action must have a motive source and stay consistent throughout

### Texture Requirements (advisory, not in the hard-rules zone)
(Imperfection constraints: half-finished sentences / everyday-life details / paragraph precision layered by weight)

### Emotional Chain and Rhythm
(Chain name + stage coverage section numbers + target emotional intensity per section + reversal peak hold)
```

## Three Assembly Tasks

1. **Conversion (four steps)**: genre pack technique becomes this story's writing. Step 1 anchors the protagonist (character name + how personality affects the writing); Step 2 anchors the information gap (who is hiding / who is pursuing); Step 3 anchors the emotional rhythm (what this passage's emotion demands of sentence rhythm); Step 4 fuses them into one directly executable instruction. Copying the methodology's original text is forbidden
2. **Descending order**: hard rules are arranged by the priority above; advisory techniques (texture requirements) do not enter the hard-rules zone
3. **Deduplication**: the same meaning appears only once; a quantity line or ban for the same object (section length / word count / punctuation / dialogue density) is defined in only one place; equivalent constraints worded differently but each with its own emphasis may be kept

## Hard Constraints

- Every hard-rule entry must be **checkable**: mechanically decidable, or with a clear criterion; abstract wording that cannot be checked (such as "keep a good grip on the rhythm") does not enter the hard-rules zone
- The conflict ruling table must have **both** the numeric and qualitative types (see the skeleton)
- Self-check after assembly: all six elements present, no placeholders, no duplicates, descending order correct
- After this contract is assembled, send it to short-verifier for audit; **if the audit fails, it goes back for reassembly**; once it passes it is frozen, and writing and fulfillment checks both use the frozen version as the standard

## Acceptance

- [ ] All six elements present, fields have values, no placeholders
- [ ] Technique entries contain the character name and the information gap (spot-check that they are not copies of the source text)
- [ ] Priority in descending order, advisory techniques not mixed in
- [ ] The same object in the same format is defined only once
- [ ] Conflict ruling table has all five numeric items plus the logic-priority clause
