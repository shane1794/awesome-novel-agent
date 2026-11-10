# Scene-Craft, Scene Writing Methodology

> **Purpose: After four steps of transformation, prompt words are injected and AI can
> be used directly without the need for author decision-making**

The methodology documents in this directory are automatically loaded on demand by
**prompt-crafter** in the writing cycle. After a four-step transformation method
(anchoring role → anchoring information difference → anchoring emotional rhythm → fusion
output), output and writing specs are injected.

**No need** to ask the author "What technique was used to write this dialogue?" - the
choice of scene-level writing method is an execution-level operation, not a creative
decision.

## Loading Mechanism

```
Input and scene raw materials are filled in
  │
  ├─ General scene types → scene-craft/{type}/universal.md
  │ + scene-craft/{type}/{theme}.md (overwrite if exists)
  │
  ├─ Special inspection → appearance/(when a new character appears/appearance changes)
  │ inner-mono/(major events/during emotional fluctuations)
  │
  └─ Output → Four-step transformation → Inject output and writing specs
```

## Directory structure

```
scene-craft/
├── README.md
├── index.md
├── prose/writing techniques (always loaded)
├── pov/ perspective switching (always loaded)
├── death-scene/ character death/offline
├── dialogue/ dialogue scene
├── fight/ fight scene
├── appearance/ character appearance description
├── inner-mono/ psychological activity
├── environment/ environment description
├── group-scene/ group portrait scene
└── transition/ transition scene
```

## Add rules for new files

1. One directory for each scene type, containing `universal.md` (general) + `{genre}.md`
   (specialized coverage)
2. Each technique starts with `[tag]` to facilitate prompt-crafter to match according to
   scene events.
3. Example sentences must meet three elements (subject + action + dialogue/result +
   emotional suggestion)
4. **No need to write "when to use" in the file - it is automatically detected by
   prompt-crafter** (scene type detection or triggering by special conditions)
