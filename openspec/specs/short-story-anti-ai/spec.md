# short-story-anti-ai Specification

## Purpose
The short story's de-AI track stands on its own: short stories hold readers with blunt resonance, not restrained understatement, and direct emotion words, first-person judgment sentences, and crematorium previews are the short story's signature, not a flaw. This capability defines the short story's own keep-or-cut criteria, banned words, self-check list, and paragraph-shape boundaries, and guarantees its judgments rely only on the short story's own calibration.

## Requirements

### Requirement: AR1 Short-story de-AI judgments must be decided item by item as reuse or independent

Short-story de-AI MUST decide, **per check item**, whether to reuse an existing tool or use the short story's own calibration; it MUST NOT apply one blanket decision to a whole tool. It must not drop a whole tool because it contains a genre-bound word list, and must not apply a whole tool just because most of its entries are general.

Decision principles:

- **Genre-independent check items MUST reuse existing tools**: format and layout (sandwiches, nested quotes, half- vs full-width quotes, word-count reconciliation, punctuation density), general AI-tone items (cliché stop words, business jargon, signpost language, repeated paragraph openings, sentence-length variation), and project-level asset items (regression pattern library, locked-lines whitelist). Duplicate implementations of the same kind of check MUST NOT occur.
- **Check items bound to genre wording MUST use the short story's own calibration**: lyrical word choice, reversal sentence patterns (such as "thought... only to discover" types), paragraph shape and single-sentence paragraph share, and universal-metaphor thresholds. Judgment output calibrated for another party MUST NOT be used directly as the basis for a short-story violation.

The short-story de-AI criteria MUST live in the short story's own knowledge files and MUST deploy as a standalone product file.

#### Scenario: AR1.1 Item-by-item grading is set, with reasons
- **WHEN** checking the short-story de-AI check-item list
- **THEN** each check item is marked reuse or independent, with a stated reason (genre-independent / bound to genre wording), and there is no blanket conclusion of the "reuse the whole tool" or "drop the whole tool" kind

#### Scenario: AR1.2 Genre-independent items reuse existing tools
- **WHEN** a short-story project runs machine checks
- **THEN** format and layout, general AI-tone, and model-degradation checks are handled by existing tools, and no duplicate implementation of the same kind of check appears in the repo

#### Scenario: AR1.3 Genre-bound items use short-story calibration
- **WHEN** a short-story project judges lyrical word choice, reversal sentence patterns, paragraph shape, and similar items
- **THEN** it uses the short story's own word lists and criteria, without taking judgment output calibrated for another party directly as the basis for a short-story violation

#### Scenario: AR1.4 Knowledge criteria are independent
- **WHEN** checking the short-story de-AI criteria in the knowledge layer
- **THEN** they sit in the short-story-specific directory and deploy as a standalone product file

### Requirement: AR2 The keep-or-cut table and its criterion must be explicit

The short-story de-AI criteria MUST provide a "keep / cut" comparison table (a three-column structure: banned in other genres / kept in short stories / cut only in short stories) and MUST give a single criterion. The criterion MUST be directly usable for judging whether a single sentence stays or goes, without extra explanation tied to genre or length.

#### Scenario: AR2.1 Three categories must be kept
- **WHEN** checking the short-story criteria comparison table
- **THEN** it explicitly lists the three categories to keep: writing emotion words directly, first-person judgment sentences and spoiler previews, and judgment one-liners and heart-death chapter endings; each notes why it is a short-story selling point

#### Scenario: AR2.2 Two categories must be cut
- **WHEN** checking the short-story criteria comparison table
- **THEN** it explicitly lists the two categories to cut: emotional summary sentences that appear alone with no concrete reaction following them, and neutral author explanations unrelated to the characters' emotions; each gives recognizable features and a rewrite direction

#### Scenario: AR2.3 The criterion is single and usable
- **WHEN** applying the criterion to any doubtful sentence
- **THEN** the criterion is "does this sentence carry the protagonist's subjective emotion right now": keep it if it does, cut it if it is neutral and objective; the same sentence does not produce conflicting conclusions across the keep and cut categories

### Requirement: AR3 Emotions must be written directly, with concrete follow-through

Short stories MUST allow writing emotion words directly, but an emotion word MUST be followed by a concrete action or object specific to this scene right now. Emotion words MUST NOT be left floating alone, and the same emotion MUST NOT be written repeatedly and then explained again for how much it hurts.

**The first-person possessive "my" (我的 in Chinese) MUST be removed as much as possible**: body and mental parts are written directly without a subject: "my heart gave a sudden jolt" becomes "heart gave a jolt", "my soul floats in midair" becomes "soul floats in midair", "my eyes reddened" becomes "eyes reddened in an instant". The criterion is: in first-person narration, the reader is already inside the protagonist, so repeatedly marking "my X" pushes the narrative position back outside the body, which is a bystander trace.

The same constraint applies to leading mini-clauses: "I know / I understand / I realize" becomes a plain statement, "I feel / I sense" becomes the feeling written directly, and "I see myself" is deleted and the action written directly.

#### Scenario: AR3.1 Emotion words are followed by concrete follow-through
- **WHEN** checking any sentence containing an emotion word in the main text
- **THEN** it is followed by a concrete action, object, or body reaction specific to that scene, not a generic physiological reaction that fits any scene written alone

#### Scenario: AR3.2 One emotion is written once
- **WHEN** reading through any section
- **THEN** the same emotion is not written repeatedly with an explanatory sentence appended

#### Scenario: AR3.3 Emotion words are not wrongly deleted
- **WHEN** the editor sub-agent runs the de-AI pass
- **THEN** direct emotion words themselves are not in the deletion scope; only when no concrete follow-through follows them is the summary sentence supplemented or deleted

#### Scenario: AR3.4 First-person possessives are cleared
- **WHEN** checking how body and mental parts are written in the main text
- **THEN** there are no possessive forms such as "my heart / my soul / my eyes", rewritten in subject-less form; leading mini-clauses such as "I know / I understand / I realize / I feel / I see myself" have been changed directly into statements, feelings, or actions, with no bystander traces kept

### Requirement: AR4 The short-story banned-word list must be independent and contain no emotion words

Short stories MUST have their own banned-word list. The list MUST only collect pure clichés unrelated to emotional intensity and MUST NOT collect emotion words themselves. Aggregated categories in the list MUST give quantitative caps.

#### Scenario: AR4.1 List location and ownership
- **WHEN** checking the short-story banned-word file
- **THEN** the file exists and sits in the short-story-specific directory, and is not referenced by non-short-story products

#### Scenario: AR4.2 Categories are complete
- **WHEN** checking the list content
- **THEN** it covers at least eight categories (cliché actions, psychological labels, dialogue-label tone, essay style, written-conjunction flooding, degree-adverb clustering, universal metaphors, vague emotional summaries), each giving a handling method

#### Scenario: AR4.3 Emotion words are not in the list
- **WHEN** searching the list for direct emotion words
- **THEN** emotion words themselves are not in the deletion list

#### Scenario: AR4.4 Quantitative caps are usable and conflict-free
- **WHEN** checking the weak-adverb category
- **THEN** the list gives a per-thousand-word cap, and that value passes this repo's rule-conflict check (if it conflicts with an existing threshold, it must be explicitly exempted with its reason recorded)

#### Scenario: AR4.5 The degree-adverb category covers both weak and strong ends
- **WHEN** checking the degree-adverb category
- **THEN** it collects both weak adverbs (slightly / faintly / slowly / gently) and strong adverbs (right / currently / very / extremely / increasingly / indeed / seemingly) under one per-thousand-word cap; it MUST NOT list only the weak end. The handling method is density-based trimming, and MUST NOT delete them all indiscriminately

### Requirement: AR5 The self-check list must be decidable item by item

Short stories MUST provide a self-check list to scan item by item after finishing each section. The list MUST cover five categories: present-tense narration not wrongly deleted, emotion words with concrete follow-through, chapter endings with a hook or a judgment, clichés at zero, and each story's writing unlike the last. Each item MUST be mechanically decidable or give a clear criterion.

#### Scenario: AR5.1 Emotion follow-through item
- **WHEN** running the self-check list
- **THEN** there is an item "every emotion word is followed by a concrete reaction; if not, it is empty talk, so add one or delete it"

#### Scenario: AR5.2 Present-tense narration kept item
- **WHEN** running the self-check list
- **THEN** there is an item "first-person judgment sentences / spoilers / crematorium previews are kept, not wrongly deleted"

#### Scenario: AR5.3 Chapter-ending quality items
- **WHEN** running the self-check list
- **THEN** there are two items: "the chapter ending has a judgment one-liner / crematorium preview / heart-death aftertaste, and no hollow philosophical elevation" and "the chapter ending is not rounded off for neatness (forced parallelism / listing / rhyme / showing off)"

#### Scenario: AR5.4 Anti-templating item
- **WHEN** running the self-check list
- **THEN** there is an item "this story's techniques, opening, and ending differ from the previous story", preventing multiple stories from sharing one template

### Requirement: AR6 Punctuation hard constraints must be declared by the short story itself

Short-story main text MUST NOT contain banned pause punctuation. Pauses, choking up, trailing off, interruptions, and blank space MUST be done with short sentences, periods, commas, actions, or line breaks. The constraint MUST be declared once each in the short-story format spec and the short-story de-AI criteria.

#### Scenario: AR6.1 Banned punctuation
- **WHEN** checking the finished main text and dialogue
- **THEN** the whole text contains no ellipses, dashes, long dashes, or double hyphens

#### Scenario: AR6.2 Pauses done by replacement
- **WHEN** locating a semantic position that needs a pause
- **THEN** it is done with a short sentence, end-of-sentence punctuation, an action beat, or a line break

#### Scenario: AR6.3 Declared on the short-story side
- **WHEN** checking the short-story format spec and short-story de-AI criteria files
- **THEN** both contain a statement of this punctuation constraint

### Requirement: AR7 Paragraph shape must have both a floor and a ceiling

Short stories MUST state both the **floor** of paragraph shape (a platform-shape requirement, supporting a short-paragraph base color with one sentence per paragraph) and the **ceiling** (an anti-telegram-style requirement). Stating only the floor lets short stories fall into the shape of "hard-splitting speech into three-word fragments arranged in sheets", a known high-AI-suspicion form.

The ceiling MUST give a decidable signal (such as a test for consecutive fragments in sheets) and MUST state that short sentences are occasional emotional beats landing on peaks, not the base color throughout. The positioning statement for short sentences MUST appear together with the ceiling and MUST NOT appear with only the floor or only the ceiling.

#### Scenario: AR7.1 Floor and ceiling stated together
- **WHEN** checking the short-story format spec and short-story de-AI criteria files
- **THEN** both contain the paragraph-shape floor (short-paragraph base color / one-sentence-per-paragraph platform shape) and ceiling (anti-fragment-sheet) together, with no wording that states only the floor

#### Scenario: AR7.2 The ceiling is decidable
- **WHEN** running the paragraph-shape self-check
- **THEN** a decidable ceiling signal and criterion exist, not depending on subjective feel

#### Scenario: AR7.3 Short-sentence positioning stated
- **WHEN** checking the paragraph-shape constraint
- **THEN** it states clearly that short sentences are occasional beats landing on emotional peaks, not the base color throughout

### Requirement: AR8 Character naming must avoid the convergent name pool and be reproducible across passes

Short stories MUST have a character-naming constraint that avoids the model's highly convergent naming pool (the same batch of characters and names recurring across many stories is a machine trace readers can spot directly).

The constraint MUST be given as a **decidable banned list**: it includes both high-frequency convergent full names and high-frequency convergent characters plus their homophones, scannable by machine. It MUST NOT use "random generation" as the mechanism: randomness is not reproducible in a language model, and revising the same story would produce different names.

Naming MUST be stable across passes: when revising, rewriting a few sections, or regenerating, the same character's name MUST stay unchanged. So naming results MUST be saved as a readable record and written into the story's settings, and all later stages MUST follow that record and MUST NOT regenerate names.

#### Scenario: AR8.1 The banned-name list is decidable
- **WHEN** checking the short-story naming constraint
- **THEN** it gives high-convergence full names and characters (including their homophones) as a list, scannable by machine, and does not use "random generation" as the constraint mechanism

#### Scenario: AR8.2 Naming is stable across passes
- **WHEN** revising the same story or rewriting some of its sections
- **THEN** character names stay unchanged and do not drift from regeneration

#### Scenario: AR8.3 The naming record is saved and followed
- **WHEN** checking the story settings and later stages' inputs
- **THEN** they contain the character-naming record, later stages follow that record, and names are not regenerated

### Requirement: AR9 Modern concepts must not appear bare in ancient or fictional-world main text

When writing short stories with an ancient or fictional-world setting, **modern concepts** used during planning and reasoning MUST NOT appear in the main text in their original form. The typical leak is not spoken words but reasoning-layer concepts: frameworks the model uses to think through character relationships, such as "psychological trauma / family of origin / boundaries / internal friction", which break immersion the moment they enter the text.

Each modern concept entering the main text MUST first complete one **in-world translation**: find a functionally equivalent expression inside this story's era framework. It MUST NOT be kept because "readers can understand it" when it breaks immersion; when no translation holds, the concept MUST be deleted and the same meaning conveyed through senses and behavior instead, and MUST NOT be bypassed with a generic metaphor.

This constraint and "the main text must not contain writing-engineering words" are two faces of the same kind of problem: the former stops modern vocabulary leaking into ancient settings, the latter stops workflow words leaking into the work. The constraint MUST provide a **machine-scannable word list** covering five categories: modern science and technology terms, internet slang, academic terms, modern institutions and job titles, and modern time and measurement units. The list MUST mark its scope: it does not apply to modern-setting genres.

#### Scenario: AR9.1 The word list exists and is scannable
- **WHEN** checking the short-story de-AI criteria
- **THEN** it contains a machine-scannable modern-word list covering five categories (modern science and technology terms, internet slang, academic terms, modern institutions and job titles, modern time and measurement units), marked as applying only to ancient- and fictional-world-setting genres

#### Scenario: AR9.2 Main text has no bare modern words
- **WHEN** scanning the main text and dialogue of an ancient- or fictional-world-setting short story
- **THEN** there are no word-list hits; characters use no modern spoken language; narration contains no reasoning-layer modern concepts (psychological trauma / family of origin / boundaries and similar)

#### Scenario: AR9.3 Failed translation means deletion, not a workaround
- **WHEN** a modern concept finds no functionally equivalent expression inside this story's era framework
- **THEN** the concept is deleted and the same meaning conveyed through senses and behavior, with no generic metaphor used to bypass translation

#### Scenario: AR9.4 Modern genres are exempt
- **WHEN** the genre has a modern setting
- **THEN** the constraint does not apply and is not mechanically applied to modern-genre main text
