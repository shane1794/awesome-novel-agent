# Case 2 Style prompt word rendering specifications (prompt-crafter has been distilled)

## Scope of application (two states)
- This specification is only used for **distilled cards** (confidence>0). Undistilled
  state (confidence=0) by prompt-crafting Step 1.1
The existing branch adopts text qualitative four-field injection (the status quo remains
unchanged, do not read this document).

## Data Source
- Read-only card (settings/writing-style.md main card + overlay by scene_type
  settings/style-profiles/{scene}.md override),
**Do not read the analysis draft** (settings/style-profiles/analysis/).
- The rendering rules are self-contained in this article (see below for exact values)
  and do not depend on any tools/*.py (those are not deployed to the project space).

## Exact render values (aligned with tools/style_render.py)

### Numeric density class intervals (RANGE_TIERS)
According to the card confidence file, the numerical dimension is rendered as "L-U per
hundred words": `L = round(X×(1−t))`, `U = round(X×(1+t))` (rounded half-up, non-banker
rounding; when U ≤ L, the single value `L` is rendered - such as zero value → "0", no
fictitious 0-1 interval).

| confidence file | tolerance t |
|---------------|--------|
| ≥70 | ±10% |
| ≥50 | ±20% |
| <50 (including 0) | ±30% |

### Proportion type Chinese qualitative (pct_zh)
Proportion value → Chinese qualitative words:

| Proportion | Qualitative |
|------|------|
| ≥80% | The vast majority |
| ≥60% | Most |
| ≥40% | Nearly half |
| ≥20% | Part |
| <20% | Small amount |

### Category enumeration → Chinese (ENUM_ZH)

| key | value | render |
|----|----|------|
| tag_style | pure_tags | Tags mainly use 'XX said' |
| tag_style | mixed | Tag mixed use |
| tag_style | no_tags | No tags, action instead |
| strength | weak | verb light intensity |
| strength | medium | verb with medium strength |
| strength | strong | verb intensity |
| paragraph_bridge_style | action | Paragraphs are connected by actions |
| paragraph_bridge_style | dialogue | rely on dialogue to connect |
| paragraph_bridge_style | transition | Use less transitional sentences |
| inner_monologue_style | direct | The inner monologue is presented directly in quotation marks |
| inner_monologue_style | indirect | indirect paraphrase |
| perspective | first_person | first person |
| perspective | second_person | second person |
| perspective | third_limited | Third person limited perspective |
| perspective | third_omniscient | Third person omniscient perspective |

### Scene sparse injection matrix (SCENE_INJECTION)
According to this chapter, scene_type only injects corresponding dimensions; unknown
scene_type is general.

| scene_type | Inject dimension |
|------------|----------|
| general (all in all) | lexicon, syntax, rhythm, rhetoric, emotion_expression, narrative, dialogue_style, cohesion, verb_style |
| dialogue | lexicon, dialogue_style |
| fight | verb_style, syntax |
| environment | rhetoric, rhythm |
| inner-mono | emotion_expression, narrative |
| transition | cohesion, rhythm |
| group-scene | rhythm, dialogue_style |

### Distribution bucket name in Chinese
- Sentence length distribution: short_le_8→short sentence (≤8 words), medium_9_20→medium
  sentence (9-20 words), long_21_35→long sentence (21-35 words), xlong_gt_35→extra long
  sentence (>35 words)
- Metaphor: weapon_metal→weapon metal, nature→nature, body→body, abstract→abstract,
  other→other
- Senses: visual → vision, auditory → hearing, tactile → touch, olfactory → smell,
  gustatory → taste
- Name/pronoun: name→name, he_she→him/her, i_you→I/you

## Rendering steps
0. Fallback guard (§6.0b): Distilled card missing sound layer (legacy jieba distilled
   card, confidence>0 no hard_constraints, etc.)→
The quantification section is rendered as usual; the sound layer section [Hard
Rules]/[Overall Tone]/[Style Reference Sentences] rolls back the qualitative four-field
injection of the card text, and rolls back independently key by key (which key is
missing): [Hard Rules] ← Text "Hard Constraints" + "AI is prone to mistakes" subsection
entries, [Overall Tone] ← Text "Narrative Identity" subsection, [Style Reference
Sentences] ← Text "Descriptive Levels and Techniques" subsection examples.
1. Numerical density class (adj_density_per_100, etc.): Press confidence and use
   RANGE_TIERS to determine the interval → "L-U words per hundred words".
2. Proportion category (dialogue_pct, etc.): "About X% (Chinese qualitative: nearly
   half/most/...)"; missing key/unmeasured/out of bounds (<0 or >100)
→ Do not render this row (not fake 0%).
3. Distribution class
   (sentence_length_dist/metaphor_preference/sensory_dist/name_pronoun_ratio):
Bucket by bucket "{Chinese bucket name} accounts for X%".
4. Category enumeration: mapped to Chinese phrases according to ENUM_ZH (such as mixed →
   "mixed use of dialogue tags").
5. Sparse injection: According to the scene_type in this chapter, use SCENE_INJECTION to
   inject only relevant dimensions; the main card takes care of the general.
6. Sound layer transparent transmission: hard_constraints → "hard rules" without
   deletion one by one; soft_guidance → "overall tone";
few_shot_examples → "Style Reference Examples" are grouped by type.
7. Fixed injection (**prompt-crafter additional, non-rendering section**): In addition
   to the 11 style sections, additional generation targets "strictly match the above
   style parameters,
The deviation does not exceed 20%" + placeholder "plot context" + "writing requirements
(write the main text/number of words directly)". The rendering module (style_render.py)
only produces the following 11 style sections, but not these two sections.

## Output structure (11 style sections + 2 fixed injection sections = complete case 2 prompt words)

Rendering module output (11 sections): [Vocabulary] [Sentence Pattern] [Rhythm]
[Rhetoric and Sensation] [Emotional Expression] [Conversation Style] [Cohesion]
[Perspective] [Hard Rules] [Overall Tone] [Style Reference Examples]

prompt-crafter fixed injection (2 sections): [Plot context] [Writing requirements]
