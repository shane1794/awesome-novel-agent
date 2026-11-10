# Scenario Writing Methodology

> A guide to writing novels organized by scene type. One directory for each scene,
> containing general methodology + specialized coverage of each theme.

## Directory structure

```
scene-craft/
├── index.md # Index
├── README.md # Instructions for use
├── prose/ # Writing techniques (always loaded)
├── dialogue/ # dialogue scene
│ ├── universal.md # Universal dialogue methodology
│ ├── xianxia.md # xianxia theme specialization
│ └── suspense-crime.md # Suspense criminal investigation specialization
├── fight/ # fight/confrontation
│ ├── universal.md # Universal combat methodology
│ ├── xianxia.md # xianxia theme specialization
│ └── suspense-crime.md # Suspense criminal investigation specialization
├── environment/ # Environment/atmosphere description
│ ├── universal.md # ✅ Five-sense writing/emotion rendering/detail interaction
│ ├── xianxia.md # xianxia theme specialization
│ └── suspense-crime.md # Suspense criminal investigation specialization
├── appearance/ # Character appearance description
│ └── universal.md # ✅ Anchor/dynamic/story/side foil
├── inner-mono/ # psychological activity/inner monologue
│ └── universal.md # ✅ Physiological synaesthesia/thought fragmentation/progressive collapse
├── group-scene/ # Group portrait scene (to be added)
│   └── universal.md
└── transition/ # Transition scene
    └── universal.md # ✅ Emotional delay/crisis hook/contrast of five senses/object clues/moving lens/empty scene/dialogue continuation
```

## Labeling System

Technique entries in each scene type file begin with `[tag]`. The label is the filter
basis for prompt-crafter selection:

```
## [Power] Power dynamics - who dominates and who defends
## [Subtext] Dislocation - lines and actions are inconsistent
## [rhythm] Rhythm Changes
## [Information gap] Information gap drives dialogue
```

After prompt-crafter loads the file, it does not inject all output and writing specs -
it matches tags based on the core events of the scene and only selects the relevant 2-4
items.

### Tag matching logic

```
Input / Scene raw materials Scene core event: "Fang Yan avoids Lu Zheng's questioning in the office"
  → Trigger tags: [concealment], [power], [subtext]
  → Select these three items from dialogue/universal.md → Four-step conversion → output and writing specs

Input / Scene raw materials Scene core event: "Two characters chatting on the street"
  → Trigger tag: no direct conflict tag
  → Select [Action], [Distinction] from dialogue/universal.md → Four-step conversion → output and writing specs
```

Priority: Techniques matching tags > Generic techniques without tags.

## Loading method

prompt-crafter reads according to the following path according to the scene type
recognized by input / scene raw material:

1. General methodology: `scene-craft/{type}/universal.md`
2. Subject specialization: `scene-craft/{type}/{current-genre}.md` (read if it exists, otherwise
   skip)

General methodology + theme-specific merger → Filter by tag → Four-step transformation →
Inject output and writing specs.
