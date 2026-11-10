# Character appearance description

> Don’t overlay the facial features, don’t interrupt the plot, and don’t let the
> appearance be disconnected from the character. Each technique begins with `[tag]`.

## Injection timing

The character's appearance is not a scene type and cannot be automatically detected
through the input scene raw material scene type. prompt-crafter additionally loads this
file to inject output and writing specs when any of the following conditions are met:

| Trigger conditions | Judgment basis | Example |
|---------|---------|------|
| **New characters appear** | Among the characters appearing in this chapter are those who did not appear in the previous chapter | The second volume introduces a new villain, and readers see him for the first time |
| **Character Appearance Changes** | The character has undergone significant changes such as injury, aging, clothing changes, and transformations | The protagonist appears for the first time after being disfigured, and the female supporting character has changed her dressing style |
| **The scene involves appearance perception** | Input / Scene raw materials The core event of the scene or the scene description contains "looking at the face/observing the appearance/sizing", etc. | "He looked at the person opposite", "She noticed the other person's scars" |

### Loading method

Not placed in the regular scene type loading process. After the input scene raw material
scene sequence is filled in, **extra check** whether the core event of each scene
triggers the above conditions. If triggered, load `appearance/universal.md` +
`appearance/{genre}.md` (if it exists), and append to output and writing specs after four
steps of conversion.

## Label Selection Guide

| Scene characteristics | Matching tags | Reason for selection |
|---------|---------|---------|
| The character appears for the first time and needs to give readers the first impression | [Anchor Point] [Dynamic] | Use core visual anchor points to establish memory points and use actions to bring out the appearance |
| There is a mismatch between the character's appearance and personality/experience | [Story] | Let the appearance have a origin, not just design it out of thin air |
| The description of the appearance is like a running account (written from hair to toes) | [Anchor point] | Only capture one iconic feature, and let the reader figure out the rest |
| Appearance description is like a separate introduction after pausing the plot | [Dynamic] | Integrate appearance into continuous actions such as entering/taking a seat/scanning |
| Character characteristics are only used once and never mentioned again | [Story] | Bind the characteristics to the character's experience, and they can be echoed repeatedly in the future |
| I don’t want to describe the appearance directly, but I want a stronger impact | [Side contrast] | Use other people’s demeanor/atmosphere changes to contrast, leaving room for the reader’s imagination |


## [Anchor Point] Refining core visual anchor points - using points to represent surfaces

**Core:** Do not pile up the details of the whole body, only grab 1 iconic feature and
focus on it, and leave the rest to the reader's brain.

### Enforce Rules

- Each character locks a unique core identifier: scars, eye shape, moles, body shape,
  and unique lines.
- Create details around the logo, unevenly describing hair, facial features, body shape
  and other regular parts
- Abandon common template words such as "Shen Yu Luo Yan, sword eyebrows and star eyes,
  face like a crown jade" etc.

```
❌ He has thick eyebrows, round eyes, and a beard on his face, giving him a very fierce look.

✅ The flesh on his face rose and fell with his breathing, a scar extended from the corner of his left eye to the base of his ear, and a violent aura rushed over his face.

❌ She has beautiful appearance and charming eyebrows.

✅ A pair of fox eyes narrow into thin lines when smiling, and the mole at the corner of the eye makes people's hearts tremble.
```

**Disabled:** A running account-style description from head to toe; applying the ancient
style expressions of Internet celebrities; listing multiple common facial features.


## [Dynamic] Visualization of dynamic behaviors,without pausing the plot

**Core:** Abandon the static writing method of "characters stand still and describe
their appearance separately", and integrate appearance into continuous actions such as
entering, sitting down, scanning, and smiling.

### Enforce Rules

- Appearance descriptions are interspersed with the character's action flow without
  interrupting the narrative rhythm.
- Body shape and aura do not rely on straightforward descriptions, but are reflected
  through the environment, clothing, and other people's reactions.
- Iconic features are revealed and extended with changes in movement, enhancing the
  dynamic sense of the picture.

```
❌ He is tall and burly, with a fierce appearance and intimidating momentum.

✅ He pushed the door open and the door frame trembled slightly. When he strode to sit down, his coarse clothes were swollen by the tight muscles.
   His gaze swept across the entire place, and those who were touched by his gaze shrank their necks.
   He grinned, the scar on his face distorting.
```

**Disabled:** The plot is stagnant, and the appearance is purely introduced in separate
sections; the entire process is described statically, without any movement of the
characters.


## [Story] Appearance binds personality/experience/destiny - let the skin tell the story

**Core:** Appearance details are not just about looks, they must be deeply bound to the
character’s occupation, past trauma, personality habits, and life experiences, making
the details narrative.

### Enforce Rules

- Design exclusive body posture, scars, habitual movements, and supplement the causes
  behind them
- Appearance characteristics appear repeatedly depending on the character's status and
  scene. They do not appear once and then become invalid.
- Use external details to imply identity, experience, and mood

```
❌ This veteran is tall and ordinary in appearance.

✅ He always sits as straight as a javelin, and the muscles in his left leg will tighten slightly uncontrollably,
   It was an old disease caused by shrapnel injuries on the battlefield in the early years.
```

**Disabled:** The appearance is completely disconnected from the personality and
experience; the characteristics are only used once and will no longer be echoed later.


## [Side contrast] Use the eyes of others to describe appearance - advanced writing method of leaving blank space

**Core:** Instead of directly describing the character's appearance, the character's
characteristics are reflected by the demeanor of others and the changes in the
atmosphere of the scene, leaving room for the reader's imagination and having a stronger
impact.

### Enforce Rules

- It is forbidden to pile up evaluative adjectives such as "overwhelming the country and
  the city, beautiful like a fairy"
- The effect is presented through physiological reactions, behavioral pauses, and sudden
  changes in the atmosphere from a third-party perspective.
- The more specific the bystander's reaction is (rather than the general "everyone is
  stunned"), the stronger the impact.
- The choice of contrasting perspective should fit the scene: low-level people look at
  high-level people, common people look at nobles, and enemies look at strong people.

```
❌ She was so beautiful that she captivated the country and everyone was shocked by her beauty.

✅ The moment she stepped into the hall, the noise stopped abruptly.
   The guest who was raising his glass hung his glass and forgot to drink, and the waiter suddenly stopped in his tracks.
   The candlelight reflected on her face, making the women present unable to look away from every angle.

❌ He looks fierce and is not easy to mess with.

✅ He stood at the entrance of the alley, and several gangsters on the opposite side took half a step back in unison.
   The one at the front swallowed, and the hand holding the knife trembled slightly.
```

**Disabled:** Directly use evaluative conclusions such as
"beautiful/handsome/ugly/ferocious"; generally write "everyone was stunned" without
explaining specific reaction details.
