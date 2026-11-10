# How to write dialogue scenes

> Each technique begins with `[tag]`. prompt-crafter matches tags based on scene core
> events, and only selects corresponding techniques to inject into output and writing
> specs.

## Label Selection Guide

Analyze the input scene raw materials, the **core events** and **character status** of
the scene, and match the appropriate tags according to the following rules:

| Scene characteristics | Matching tags | Reason for selection |
|---------|---------|---------|
| There is a big gap in role status (supervisor/subordinate, elder/junior, noble/commoner) | [Identity] | People with different statuses use different wording to avoid unified speech |
| The character is concealing, lying, avoiding, and not saying anything | [Subtext] | Saying A actually wants B, borrowing things to illustrate things |
| Characters are fighting, confronting, negotiating, and fighting for the right to speak | [Pull] | Breaking up questions and answers, using rhetorical questions/emotional cutting to create tension |
| Characters are quarreling, questioning, interrogating, and showing off | [Pull] [Subtext] | Confrontation + concealment coexist |
| More than 8 consecutive pure lines (the threshold is subject to chapter-quality-checklist.md) | [Action] | Insert actions/expressions to prevent readers from losing the sense of the image |
| Two characters chatting, daily communication, conflict-free scenes | [Action] [Identity] | Use action interspersed and identity distinction to maintain the scene |
| The character has inner activities and desires, but does not say them verbally | [Subtext] [Pull] → Answer the wrong question | Conflict between heart and lines |

**Quantity to select:** Select 2-4 items for each scene. If the scene matches multiple
tags at the same time, the 2 most relevant to the core event will be selected first.




## [Identity] Identification language,Farewell to unified discourse

**Core:** People with different identities say different things. By hiding the
character's name, readers should be able to identify who it is by the way they speak.

### Implementation details

| Identity | Speaking characteristics | Avoid pitfalls |
|------|---------|------|
| **Little people in the market** | Lots of slang, short sentences, and interjections, loose word order, and little written vocabulary | No need to regularize long sentences |
| **Intellectual/Superior** | Words are tactful, leave room for words, and are used to expressing in roundabout ways, and do not say it to death | Don’t speak plainly |
| **Cold character (killer/enemy)** | Minimalist words, flat tone, few emotional words, indifferent surface | No emotional catharsis |

### Template sentences + practical examples

```
❌ You are fired. You don’t have to come tomorrow.

✅ He lit a cigarette and was in no hurry to speak. He spoke only when the smoke cleared, and his tone was calm. "You are well aware of the current difficulties in the company. There is no room for you here. Go out and find another way out."
```

**Avoid pitfalls:** Characters with different identities share a speaking style; use
written language to write dialogues between lower-level characters.


## [Subtext] Subtext & contrasting tension - the core of game/confrontation

**Core logic:** Say A, but actually want B. Never directly express core purposes such as
appeals, hatred, breakup, and transactions.

### Technique 1: Borrowing objects to describe things

Replace the core conflict with the sight/food/object in front of you.

```
❌ Let’s get a divorce, I don’t want to do it.

✅ He gave her a piece of fat. "This meat has been stewed all afternoon and is already rotten. It's time to pour it out."
He stared at the plate without moving. "It's not cold yet, so I can eat if I make a living, and the days will be the same."
```

### Technique 2: Don’t mean what you say

He was extremely conflicted inside, but his tone was calm and gentle.

**Avoid pitfalls:** Characters express their feelings directly and argue directly;
conflicts are all pointed out through lines.


## [Pull] Breaking down questions and answers - creating a sense of pulling

**Core:** The character does not answer according to the other party's expectations,
creating unpredictability.

### Technique 1: Answer the wrong question

> Applicable to: Avoiding problems, unwilling to express opinions, and internally
> entangled

**Execution:** Do not respond to questions, jump to irrelevant scenes/events, and avoid
them with silence + digressions.

```
"Do you love me or not?"
He walked to the window and looked at the rain outside. "If this rain doesn't stop, all the crops in the south will be destroyed."
```

### Technique 2: Questioning and suppressing

> Applicable: confrontation, testing, occupying the right to speak, strong game

**Execution:** Do not admit/deny directly, throw the question back to the other party,
and attach suggestive questions.

```
"Did you do this?"
She didn't look up and continued to flip through the documents in her hand. "What do you think? Besides you, who else in this room can do such a great job?"
```

### Technique 3: Emotional Cutoff

> Applicable to: Enemies meeting, life and death confrontation, contempt of
> high-ranking people

**Execution:** The other party releases intense emotions, while the other party ignores
the conflict, focuses on trivial matters, and then responds lightly.

```
"Ten years of hatred, I will definitely kill you today!"
He lowered his head and blew on the soup in the bowl, frowning. "The soup is too salty and the noodles are overcooked. What did you just say? I can't remember what happened ten years ago. Sit down and try this chili oil?"
```

**Avoid pitfalls:** Mechanical dialogue with one question and one answer; in conflict
scenes, both parties simultaneously amplify their emotions and curse each other.


## [Action] Dialogue + action/environment interweaving - getting rid of pure script lines

**Core:** Insert 1 micro-action/expression/environmental detail in the middle of every
1-2 lines.

### Detail selection principles

There is a contrast between the actions and the emotions of the lines: nervousness →
carelessness, lying → subconscious little actions.

### General action library (direct call)

| Emotion | Action as |
|------|-------|
| Guilty/lying | Scratching thighs, trimming nails, shaking cigarette ash on body, wandering eyes |
| Indifference/contempt | Working with your head down, not looking up, fiddling with objects at hand |
| Suppression and forbearance | Clenched fingers, rolled Adam's apple, paused in silence |

### Example sentence template

```
His fingertips unconsciously rubbed the rim of the cup. "I can't promise you this."
```

**Key points of writing:** Action first → Dialogue last → Actions imply emotions and do
not rely on lines to explain. No parentheses are required.

**Avoid pitfalls:** The whole paragraph of continuous quotation marks, without any
supplementary actions or expressions.
