# Distilled style card format specification (distilled-style-spec)

There are two types of style cards: main card `settings/writing-style.md` (scene_type:
general, global default) and scene card `settings/style-profiles/{scene_type}.md`
(differences by scene). Both share the same frontmatter schema.

## 1. Frontmatter Quantization Layer

Required fields: `profile_version` ("1.0"), `scene_type`, `source_sample_length` (total
word count of distilled samples), `confidence` (0-100, 0=manual setting/not distilled),
`last_updated` (YYYY-MM-DD). There are other scene cards: `inherits` (inherit the main
card path), `override` (only write difference dimensions), `locked` (manually lock
dimensions, F5 incremental skip).

9 major dimensions (PRD definition, unique key name, cannot be renamed):

| Dimensions | Fields | Description |
|------|------|------|
| lexicon | adj_density_per_100 / adv_density_per_100 / four_phrase_freq_per_100 / preferred_words[] / banned_words[] / name_pronoun_ratio | Lexicon: script statistics |
| syntax | avg_sentence_length / sentence_length_dist{} / single_sentence_paragraph_pct / avg_sentences_per_paragraph / question_ratio / exclamation_ratio | syntax: script statistics |
| rhythm | dialogue_pct / action_pct / environment_pct / inner_thought_pct / narration_pct | Rhythm proportion: dialogue_pct script statistics, the rest LLM estimation |
| rhetoric | metaphor_density_per_100 / metaphor_preference / sensory_dist | Rhetoric: LLM |
| emotion_expression | direct_pct / action_physiology_pct / environment_projection_pct | emotion expression: LLM |
| narrative | perspective / focal_character / inner_monologue_style | narrative: LLM |
| dialogue_style | tag_style / avg_dialogue_length / interrupt_freq_per_100 / subtext_ratio | Dialogue: LLM |
| cohesion | conjunction_freq_per_100 / transition_sentence_ratio / paragraph_bridge_style | Cohesion: first two scripts, bridge LLM |
| verb_style | action_verb_ratio / mental_verb_ratio / state_verb_ratio / strength | Verb: first three scripts, strength LLM |

## 2. Qualitative layer of text

The main card body retains the old 4-field mapping (zero loss in migration):

| old field | new location |
|--------|--------|
| role | Text "Narrative Identity" section |
| core_principles | Text "Hard Constraints" section (regarded as redline level when injected) |
| possible_mistakes | Text "AI is prone to mistakes" section (complementary to banned_words) |
| depiction_techniques | Section "Description Levels and Techniques" in the text (retain as it is) |

The text also contains `few-shot example sentences`: Iconic example sentences selected by distillation
(grouped by scene type).

## 3. Inheritance and synthesis

- Scene card `inherits` points to the main card, `override` only covers the difference
  dimension; prompt-crafter merges override when reading the card (inheritance chain
  parsing is placed in Step 1, and no new parser is introduced).
- Main card backup: When there is no scene card in a certain scene, only the main card
  is used.

## 4. Confidence and Tolerance

`confidence = min(100, 20 + min(40, sample_length/150) + min(40, chapter_count*5))`
(sample coefficient /150: 6000 words reaches the upper limit of sample items, aligned
with the minimum sample size of "about 3 chapters, 6000-10000 words" - previously /50
made 2000 words the cap, and the increase in sample size has no difference in
confidence) tolerance level (2026-08-12 Alignment to implement RANGE_TIERS, three levels
replace the old four levels, see design spec §6.1a): `confidence ≥ 70 → ±10%`/`≥ 50 →
±20%`/`other → ±30%`. When confidence=0, the quantification layer is not injected, and the
prompt words only go to the qualitative layer until the first distillation.

## 5. Acceptance self-inspection

1. frontmatter contains all 9 dimension keys, and the field types are consistent with
   the schema
2. scene_type is within the 6-category enumeration (main card general)
3. confidence 0-100 integer; locked only contains defined dimension keys
4. Scene card inherits points to an existing card (main card or other scene card)
5. The quantified value is expressed as "about X (±Y%)" and is not hard-coded.
