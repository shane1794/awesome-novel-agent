# updater-setting-sop

The standard operating procedure for setting changes during planning.

## 1. Input Checks

| Check Item | Pass Condition | Failure Handling |
|--------|---------|---------|
| `.agent/task/setting-update-order.md` | Exists | Report the error to novel-agent |
| Target files named in the order | Exist or can be created | Report a path error |

## 2. Order Parsing

`setting-update-order.md` follows the unified order template (`templates/.agent/task/order-template.md`); `inputs`/`outputs` are lists. There are two carriers for the change specification, distinguished by the `inputs` content:

```markdown
# setting-update-order

status: pending

inputs:
  - Source file path (containing the `## Setting Change Notice` block, see "Carrier 1" below)
  # or
  - content: |                    # Initial settings (setup phase, the spec comes directly from the author's conversation, see "Carrier 2")
      type: character | world | timeline | genre | style | memory
      action: create | modify | delete
      target: settings/character-setting/{id}.md
      content: |
        # The content to write/append (structured)
      reason: Author request

outputs:
  - Target settings file path
```

### Carrier 1: Notice Block in the Source File (planning-phase changes)

`inputs` points at a volume outline / chapter outline file; updater reads its `## Setting Change Notice` block to extract the change spec (the block structure follows the updater-archive consumption convention). **After executing the change, updater removes the notice block from the source file** (removing it with Edit, to prevent repeat consumption).

### Carrier 2: Inline Spec in content (initial settings / no source file to point at)

`inputs` carries a `content:` field giving type/action/target/reason directly (the author's conversation content in the setup phase); updater executes the spec directly, with no source file to clean up.

## 3. Setting Update Flow

### Scenario A: Add a Character

1. Check that the ID is unique under `settings/character-setting/`
2. On a conflict, ask the author to confirm whether to overwrite
3. Create the character file using the standard template:

   ```markdown
   # {Character Name}

   ## Basic Information
   - **ID:** {unique identifier}
   - **First Appearance Volume/Chapter:** vol-{N}-ch-{M}
   - **Faction:** {faction}

   ## Character Positioning
   - **Core Motive:** ...
   - **Relationship to Protagonist:** ...

   ## Abilities / Traits
   - ...

   ## Appearance Record
   - vol-{N}-ch-{M}: First appearance
   ```

4. If the character is related to other characters, append the relationship to the related character files as well

### Scenario B: Change the Worldview / Genre / Style

1. Read the existing file and confirm the change is not contradictory
2. If the new content conflicts with existing content:
   - Minor inconsistency → append an explanation, marked `[updated]`
   - Fundamental contradiction → STOP and show the conflict points to the author
3. No conflict → append or replace the specified paragraph

### Scenario C: Append a Timeline Event

1. Read the existing content of `settings/timeline.md`
2. Insert the new event in chronological order
3. If the event involves a character, sync it to the character file as a marker

### Scenario D: Directly Change Memory

1. Read the target file under `.claude/memory/`
2. Mark appended content `[writer-preference]`
3. Does not go through diff (a rule specified by the author takes effect directly)

### Scenario E: Delete a Setting

1. Confirm the deletion range
2. Check whether any other file references the content to be deleted
3. Has dependent references → show the reference chain to the author for confirmation
4. No dependencies, or confirmed → execute the deletion

**Deletion granularity (S2, no deletion):** Only do **content-level deletion**. Use Edit to remove a paragraph / entry inside a file (such as one state change in a character file, or one creature entry in world-setting); **do not delete a whole file** (the system has no Bash, and neither Edit nor Write can delete a file). If the author asks for a whole file to be deleted (such as deleting a whole character), it is not feasible; instead, mark `[deprecated]` at the top of the file and keep the file itself (as the trace of the authoritative source's deletion, M2), and remove the matching relationship in the files that reference it.

## 4. Consistency Checks (general)

After any setting change, check:

- [ ] The new content does not contradict existing files under `settings/`
- [ ] A new character ID does not duplicate an existing character
- [ ] A worldview change does not create a logic contradiction in already-written chapters (mark chapters that may be affected)
- [ ] A memory change does not mix the `[community-defaults]` and `[writer-preference]` markers

## 5. Acceptance Checklist

- [ ] The change was executed as the order requires
- [ ] Newly created files are correctly formatted
- [ ] No unresolved conflicts (all conflicts have been shown to the author)
- [ ] Related updates (such as a new character's relationship sync) have been executed
- [ ] Carrier 1 (notice block in the source file): the `## Setting Change Notice` block in the source file has been removed
- [ ] The order is marked DONE
