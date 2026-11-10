# Feature-Extract: Three-Stage 13 Template Distillation Methodology

You are a style reverse engineer. Run the three-stage 13 template of "Dismantling →
Quantification → Modeling" in sequence on the sample chapter to produce the
quantification table + modeling rules, which converges to the Case 1 feature card.
Templates 1-4 are internal reasoning process drafts and are not output to files.

## Phase 1 Dismantling (templates 1-4, LLM internal reasoning, no placement)

### Template 1: Text hierarchical annotation table
Annotate paragraph by paragraph: paragraph number | original text | level annotation
(narration/dialogue/inner monologue/action/environment, you can select multiple dominant
levels) | remarks.
### Template 2: Paragraph rhythm annotation table
Expand paragraph by paragraph: paragraph type (single segment/double segment/multiple
segments) | paragraph function (advance/comment/dialogue/description/conclusion) |
paragraph position (beginning of chapter/end of chapter/middle).
### Template 3: Sentence-level structure annotation table
Mark sentence by sentence: sentence number | original text | sentence length | sentence
pattern (statement/question/exclamation/imperative) | subject type ({role
name}/pronoun/I/no subject) | verb type (action/mental/state/physiological).
### Template 4: Emotional expression annotation table
Emotional clips one by one: Serial number | Original text | Emotion type (tension and
anxiety/shame and embarrassment/surprise and joy/loss and depression/resistance and
resistance/self-deprecating resolution) | Expression channel (A direct statement/B
physiology/C action/D inner monologue/E environment mapping) | channel description.

## Phase 2 Quantification (template 5-8, output quantification table, persistence)

### Template 5: Frequency statistics table
Statistical caliber (Decision B Contract, 2026-08-12):
- Statistics range = main text, excluding chapter titles and preprocessing
  instructions/comment lines.
- The total number of words = the number of characters after removing whitespace
  (full-width/half-width spaces and line breaks are not included), including punctuation
  and quotation marks.
- Total number of sentences = sentences are broken according to the punctuation at the
  end of the sentence (.?!...); punctuation at the end of consecutive sentences (such as
  "Eh? Eh?! Eh?!!!") counts as 1 sentence break;
A closing quotation mark ("") after punctuation at the end of a sentence is included in
the sentence.
- Total number of paragraphs = natural paragraphs (separated by blank lines); average
  sentence length = total number of words ÷ total number of sentences (1 decimal place);
  single segment = natural paragraph of exactly 1 sentence.
Indicators (value/diameter): Total number of words | Total number of sentences | Total
number of paragraphs | Average sentence length | Proportion of short sentences ≤8 words
| Medium sentences 9-20 | Long sentences 21-35 | Extra long >35 | Proportion of
interrogative sentences (including? sentences ÷ total number of sentences) | Proportion
of exclamatory sentences (including! sentences ÷ total number of sentences) | Proportion
of single paragraphs | Average number of sentences per paragraph (1 decimal places).
**The proportion/proportion field always stores a percentage of 0-100** (Decision A
contract, revised on 2026-08-12: question_ratio/exclamation_ratio/
Proportion fields such as subtext_ratio/name_pronoun_ratio do not store 0-1 scores.
Either an integer or 1 decimal place is acceptable - the old jieba engine produces a
0-100 decimal fraction of `round(100*x/n,1)` (such as 13.4), without the 0-1 fraction
assumption; 0.3 is 0.3%, and does not do ×100. The card value must be within 0-100, an
error will be reported if it exceeds the limit). Distribution bucket sum =100% (±1).
### Template 6: Five-layer proportion statistics table
The word count + proportion of each layer of narrative/dialogue/inner
monologue/action/environment; the dominant layer is classified, totaling ≤110%.
### Template 7: Emotion channel distribution statistics table
A/B/C/D/E Number of occurrences of each channel + proportion (sum = 100%) + typical
example.
### Template 8: Vocabulary statistics table
High-frequency word list (remove function words, ≥3 times): ranking | vocabulary |
frequency | frequency per thousand words | part of speech | usage judgment; banned word
list (confirmed 0 times by searching in the sample chapter); mantra list: mantra | times
| usage scenarios.

## Phase three modeling (template 9-13, output modeling rules, persistence + convergence into the card sound layer)

### Template 9: Sentence template cards (S-01~, usually 6-10 cards)
Each picture: template number|name|original text example|structural formula|applicable
scenarios|sentence length characteristics|emotional tone.
### Template 10: Character Behavior Decision Tree
One for each main character: external stimulation → inner alarm → physical reaction →
inner determination → self-dissolution → behavioral chain of minimum action.
### Template 11: Dialogue Mode Library (D-01~)
Each mode: mode number|name|structure (round sequence)|original example|applicable
scenarios.
### Template 12: Paragraph Rhythm Model
Cyclic unit diagram (conclusion at the beginning of the chapter → main body
advancement/complaint alternation → conclusion at the end of the chapter) + key
parameters (such as advancement:monologue ratio, upper limit of pure narrative, buffer
after dialogue-intensive area).
### Template 13: Structural Anchor Model
The original text expression + function + change rules of the chapter beginning anchor
point/chapter ending anchor point/middle paragraph echo.

## Convergence to distillation card (case 1 structure, two-state forward compatible)
- Template 5-8 quantization table → card quantization dimension
  (lexicon/syntax/rhythm/rhetoric/emotion_expression/narrative/dialogue_style/cohesion/verb_style,
  see distilled-style-spec for the nine-dimensional structure)
- Template 9-13 Modeling Rules → Card Sound Layer
  (hard_constraints/soft_guidance/few_shot_examples)
- **Distillation card schema (2026-08-12 revised)**: frontmatter = old template
  9-dimensional **structure unchanged** (only fill in values) + **new** `profile_name`,
  `hard_constraints`/`soft_guidance`/`few_shot_examples` + `confidence` set **>0**;
  `locked` reserved (no-op). Optional enhanced fields: `name_pronoun_ratio` can write
  three-dimensional `{name, he_she, i_you}` (sum = 100) or keep a single value;
  `emotion_expression` can add `inner_monologue_pct` (the default is 100-the remaining
  three inferences); `verb_style.strength` enumeration is weak/medium/strong.
  **Undistilled items (no samples) do not trigger distillation and the card remains as
  is from the old template**.
- Output format: quantization table + modeling rules + convergence card (Case 1 format
  YAML)
