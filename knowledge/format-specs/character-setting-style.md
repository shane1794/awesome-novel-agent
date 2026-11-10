# Character setting guide

> Fill in the basic information first, and then talk about the 6-layer model layer by
> layer. After the chat, write it into `settings/character-setting/<id>.md`. Villain
> setting reference `.claude/knowledge/character-craft/villain-types.md` - three types
> of high-intelligence villain templates (chess player type/martyr type/mimic type).
> The 6 layers start from layer 1 and work their way down. Levels 1-3 are pragmatic
> (deciding why to do something), and levels 4-6 are pragmatic (deciding how to do
> something).

---

## Principle 1: Personas are decision engines, not resumes

**Rules:** After completing the setting, you must be able to infer what the character
would think and do in any situation. Filled in a bunch of information but can’t derive
any behavior → That’s a resume, not a role setting.

✅ Correct:
> **World view**: The strong make the rules and the weak follow the rules. → When
> something unfair happens, the character will not complain, but will think about how
> to become stronger.

❌ Error:
> Personality: smart, calm, rational → tag stacking. How to show "smart"? How calm are
> you? Are you still calm when your relatives and friends are in danger?

**Judgment Criteria:** Given an unexpected situation ("Someone assassinated the stranger
next to him on the street"), can you tell what the character will do without thinking?
Can't tell → The setting is not specific enough, so continue chatting.

---

## Principle 2: The protagonist must have real flaws

**Rules:** "Too honest", "Too kind", "Too trusting" are not flaws - they are ways to
compliment the character. A true flaw is something that causes a character to make the
wrong choice at a critical moment.

✅ Correct:
> Impulsive (rushing forward when relatives and friends are in danger, regardless of
> the consequences) Suspicious (cannot trust anyone, and do not ask for help when in
> need) Inferior self-esteem (feeling that they are not worthy of being rescued,
> giving up asking for help at critical moments)

❌ Error:
> "He is too kind" / "He is too honest" / "He is too trusting" → These are variations
> of strengths. The reader can feel that the author is praising the character.

**Judgment Criteria:** Does this flaw lead to the character making poor decisions in
Chapters 3-5? No → This is not a real shortcoming, change it.

---

## Principle 3: Supporting Characters Have Self-Driven Purposes

**Rules:** Supporting characters are not there for the main character. Take away the
main character and the supporting characters have their own desires and fears and can
act independently.

✅ Correct:
> Lin Yan is a darknet informant. She helps the protagonist because she owes a favor,
> but she has her own rules of survival - don't take sides, don't stand out, and live
> as long as possible. Will betray the protagonist when necessary to protect himself.
> → Take away the protagonist, Lin Yan is still the woman who survives in the gray
> area and continues her intelligence business.

❌ Error:
> Lao Zhang is the protagonist's friend and always appears to help the protagonist
> when he needs it. → Tool man. Take away the protagonist and Lao Zhang disappears.

**Judgment Criteria:** Take the protagonist out of the story. Does the supporting
character still have something to do? No → return plus self-driven purpose.

---

## Basic information

Determine these first, and then enter the cognitive model.

Ask the author:
1. "What is the name of the character? Is it the protagonist, antagonist or supporting
   role in the story? (protagonist / antagonist / supporting)"
2. "What does he look like? What are his iconic features?"
3. "What is his background - origin, experience, where he comes from?"
4. "What are his signature catchphrases, foul language and other language features?"

Write to file:

```markdown
### Basic information
- **Code**: <Pinyin id>
- **Name**: <Chinese name>
- **Story Role**: protagonist / antagonist / supporting
- **Appearance**: Physical characteristics
- **Background**: Life experience
- **Language Features**: Iconic catchphrases, foul language
```

**Basic information is not the core of the setting, but it determines the character's
position in the story and the reader's first impression of him or her. **

---

## Cognitive 6-layer model

Start from level 1 and work your way down. Each layer's dependence on the previous layer
has been determined, and there will be no skipping of layers or reversing the order.

**Structure:**
```
Retreat (why to do it) Pragmatism (how to do it)
Level 1 World View ← Difficulty Level 4 Ability ← Variable
  ↓                       ↓
Level 2 My Position ← Difficulty Level 5 Skills ← Variable
  ↓                       ↓
Level 3 Values ← Difficult Level 6 Environment ← Variable
```

**Rule of variability:** The upper three levels (worldview→self-positioning→values)
become more difficult to change as you go up - the worldview is almost fixed, and values
may loosen under the impact of major events. The lower three layers (ability → skill →
environment) can change naturally according to the plot: characters can learn new
skills, change environments, and grow in ability. The essence of the plot promotion is
the process of "the lower three levels are changing and the upper three levels are
shaken".

**Changes on the upper three levels must be very difficult. ** It doesn’t rely on a
single conversation or a sudden incident - it requires continuous impact, repeated
verification, making the characters unable to use old beliefs to explain the new
reality, and finally collapse and rebuild.

**Example - Layer 2 Self-positioning:**
> The character believes that he is a "devil", killing people for no reason and
> destroying sects, and he has a lot to do. But his worldview (level 1) has a bottom
> line - "This world must exist and cannot be destroyed." Therefore, everything he
> does has a premise: it does not affect the survival of the world. As long as the
> world is not destroyed, he can kill and destroy without any psychological burden.
> This is the subtle relationship between layer 1 and layer 2: the worldview does not
> make him better, it just draws a boundary for the "devil". He objectively eliminated
> some existences that threatened the survival of the world - but he was not doing it
> for the sake of the world, just because those threats hit his bottom line. He still
> felt that he was a demon and that the world's fear of him was not wrong. To change
> the self-positioning of "I am a devil", it is not to rely on others to say good
> things about him - it is to let him see with his own eyes that a truly good person
> has done what he did and still chooses to be a good person. He needs to realize that
> "I chose to be a devil because I am afraid of the cost of being a good person", and
> this awareness requires him to sacrifice himself to protect someone in a
> life-or-death situation, and then survive to face the question "Why did I do this?"

**Example - Layer 3 Values:**
> When both the country and your family need a character, which character should you
> choose? If the character's values are "Country first, then family", then when the
> country calls for help, he will leave his family behind and go to the front line.
> It's not because he doesn't care about his family - it's because when two values
> conflict, "country" comes first. This choice does not need to change, it is values
> that work. The real test of values is not "choosing the right one" - it is "both
> are right but you can only choose one." The character must choose between two things
> he values equally, and the outcome of that choice defines who he really is.

**Comparison - Level 4 Abilities:**
> In turn, changes to Tier 4 capabilities do not require this level of ordeal. Shen
> Mu's bow and arrow ability can be improved in the first chapter: from missing the
> target with three arrows to hitting two of three arrows, it can happen naturally in
> practice and actual combat.

### Layer 1: Worldview - how the character sees the world

Talk clearly about "how the character thinks the world works." It's not the author's
setting, it's the character's own version of what he believes.

Ask this:
> "What does the world look like in the eyes of your character? Who can survive and
> who cannot survive?"

✅ Correct:
> The strong make the rules and the weak follow the rules. Complaining is useless,
> becoming stronger is useful.

❌ Error:
> He believes in justice. (Too abstract - what specific actions does justice mean?)

**Judgment Criteria:** Does the worldview cause the character to conflict with other
people (especially other characters)? Wouldn't → be too gentle and make the character a
little paranoid.

**Self-check in this section (go to level 2 after passing this):**
- [ ] Is the worldview the version the character believes in, not the rules of the world
      set by the author?
- [ ] Can the worldview explain why the character behaves the way he does?

---

### Layer 2: My Positioning,How the character sees himself or herself

Talk clearly about "what kind of person the character thinks he is." Note: Not
necessarily what he actually looks like - cognitive biases are the space for drama.

Ask this:
> "What kind of person does the character think he is? - Note that you are asking what
> he thinks, which may not necessarily be true."

✅ Correct:
> I think I am calm, rational and make decisions before taking action, but in reality,
> when my relatives and friends are in danger, my first reaction is to rush forward,
> and my rationality is to make amends afterwards. → Self-perception is biased. The
> character will find reasons for himself every time he is impulsive.

❌ Error:
> He is very confident. (Confidence is the result, not the way you view yourself.)

**Judgment Criteria:** Is there a gap between self-perception and actual behavior? No →
The character is too "self-consistent" and has no room for growth.

**Self-check in this section (go to level 3 after passing this):**
- [ ] Self-positioning is how the character sees himself, not the author's evaluation of
      him or her?
- [ ] Is there a gap between self-positioning and actual behavior (cognitive bias)?

---

### Layer 3: Values,the source of hard choices

Let’s talk clearly about “what things the character will not do and what things will be
made an exception to”. Values are meant to be challenged - the character's choice when
"value A and value B conflict" is the real character creation.

This is enough to ask:
> "What is there that a character wouldn't do if he was killed? - What if he had to do
> it? What conditions would make him make an exception?"

✅ Correct:
> Don't betray your brothers. Do not bully civilians. You can take advantage of your
> opponent but you can't insult your opponent's dignity. → Everyone can be challenged
> - What if betraying your brothers can save more people?

❌ Error:
> Value friendship, kindness and integrity. → Too abstract. To what extent does it
> matter? Would you kill someone for your friends?

**Judgement criteria:** Can you design a "what if..." challenge scenario for each value?
Cannot → be too abstract and keep asking for details.

**Self-check in this section (go to level 4 after passing this):**
- [ ] Values at least 2 concrete behavioral boundaries (not abstract virtues)?
- [ ] Each value can be challenged with "What if..."?

---

### Layer 4: Abilities - What abilities does the character have?

Let's talk clearly about "what the character can actually do and what the upper limit of
output is." Ability is not a title - "Golden Core Realm" is not an ability description,
"Golden Core Realm can fly with a sword" is.

Ask this:
> "What can the character actually do? What is the upper limit of the output? How many
> hits can it take? What is the range? Under what circumstances will it fail?"

✅ Correct:
> He can detect the source of murderous intent within ten steps; he can pull an
> eighty-pound bow with one hand and fire three arrows without missing the target; he
> has a photographic memory but it takes time to recall.

❌ Error:
> Highly skilled in martial arts. (How tall? How many people can you beat? Who are you
> similar to?)

**Judgment criteria:** Can you answer "scope, upper limit, and restrictions" for each
ability? Cannot → Not specific enough.

**Self-check in this section (go to level 5 after passing this):**
- [ ] Does the ability have a clear output upper limit (how many can it hit/how big is
      its range/under what circumstances does it fail)?
- [ ] Is the ability a specific performance ("Sword Flying"), not a title ("Golden Core
      Realm")?

---

### Layer 5: Skills - specific things the character does

Skills and abilities are different - abilities are "whether you can fight", skills are
"can you cook or settle accounts". Skills have sources and limitations.

Ask this:
> "What specific skills has the character learned? Where did they learn it? - The
> street skills learned by the dock workers are useless in court."

✅ Correct:
> He is a member of the lower-level Qinggang gang and has acquired the skills of
> survival in the market (identifying people by listening to footsteps and identifying
> identities by looking at clothes); he has learned abacus and bookkeeping from the
> accountant.

❌ Error:
> Proficient in chess, calligraphy and painting. (Where’s the source? No one is born a
> master.)

**Judgment Criteria:** Are there any restrictions on the usage scenarios of skills? (In
what situation is this skill useless?) No → Too versatile.

**Self-check in this section (go to level 6 after passing it):**
- [ ] At least 1 skill, with source description (where did you learn it/why did you get
      it)?
- [ ] Does the skill have usage scenario restrictions (in what places/situations is it
      not applicable)?

---

### Layer 6: Environment - growth environment and current situation

Talk clearly about "the environment in which the character grew up and where he is now."
Origin determines the baseline of behavior - the choices of a poor boy will not be the
same as those of a rich boy.

Ask these two questions:
1. "What environment did the character grow up in? How does it affect him now?"
2. "Where is the character now? Is there any baggage that he can't shake off?"

✅ Correct:
> The son of an Orion at the foot of Cangwu Mountain, his parents died in a monster
> attack on the village, and he was adopted by the old boss of the Qing Gang. I grew
> up working as a dock worker and saw all kinds of people.

❌ Error:
> Born into poverty. (How poor is it? What specific burdens do you currently have? How
> does this relate to the main line of the story?)

**Judgment criteria:** Can the current situation explain "why the character is in this
position in the first chapter"? Cannot → The situation is disconnected from the plot.

**Self-test in this section (input and output after completion):**
- [ ] Are the origin and situation consistent with the world setting (the character has
      a corresponding position in the worldview)?
- [ ] Does the current situation explain the character's position and state at the
      beginning of the story?
- [ ] All six fields have values and there are no empty fields?

---

## Common mistakes

| Error | Performance | Correction |
|------|------|------|
| Tags instead of settings | "Aloof/Dirty/Tsundere" | Divided into worldview and positioning - why aloof? What experience led to it? |
| Fake flaws | "Too honest/too kind/too trusting of others" | Replaced with real flaws that make the character make wrong choices (impulsiveness/suspiciousness/low self-esteem) |
| Tool man supporting role | The supporting role only exists for the protagonist, and will disappear if you take away the protagonist | Give the supporting role his own desires and fears |
| Ability without boundaries | "Strong martial arts" and "Strong ability" | Add specific upper limits - how many can be hit, what is the range, and under what circumstances it will fail |
| The situation is disconnected from the plot | I wrote a lot about my background, but it has nothing to do with the main plot | Every situation information must be able to answer "What is the use of this to the plot" |
| The sense of substitution is misplaced | The protagonist is the person the readers substitute for, not the person the readers look up to | The protagonist is not the perfect idol, but the person who makes the readers feel "I might do the same thing if it were me" |

---

## Where does the output go?

`settings/character-setting/<pinyin-id>.md`, one file per character.

### Possessions

The items, equipment, props, etc. currently owned by the character. When archiving, the
updater automatically adds, deletes, and updates based on text changes.

```markdown
### Possessions
| Name | Type | Source | Status | Remarks |
|------|------|------|------|------|
| Qingshuang Sword | Magic weapon | Seized by Heifeng Village | In use | The sword has cracks and needs to be repaired |
| Peiyuan Pill × 3 | Pill | Sect Monthly Rules | Unused |, |
```

- **Type:** The general category identification of the item (magic
  weapon/elixir/equipment/document/weapon/intelligence, etc.), no limit
- **Source:** Where did you get it (capture/purchase/gift/refining, etc.)
- **Status:** In use/unused/consumed/destroyed/rewarded - when archived updater changes
  according to the plot

### Experience

Major events the character has participated in, locations explored, and tasks completed.
There is no limit to the subject matter - secret realm exploration, dungeon strategy,
case investigation, and battlefield experience all count as "experience".

```markdown
### Experience
| Event/Place | Type | Result | Status |
|-----------|------|------|------|
| Cangwu Ruins | Secret Realm Exploration | Obtaining the Peiyuan Pill Formula | In Progress |
| Ten Thousand Bone Cave | Secret Realm Exploration | Obtain Xuanming Bone Armor | Completed |
```

- **Type:** Event categories (secret exploration/dungeon
  guide/mission/battlefield/investigation, etc.), no limit
- **Results:** Main takeaways, changes
- **Status:** In progress/completed - updated by updater when archiving

### Plot resume

Record what the characters actually do in each chapter and how their relationships
change. When archiving, the updater extracts and appends from the body.

```markdown
### Plot resume

#### Volume 1 Chapter 3
- **Behavior:** Killed Zhao Hu, the leader of Black Wind Village, and rescued the captive villagers
- **Relationship changes:** Became hostile with the remnants of Heifeng Village; the rescued villager Zhang Bo owed him a life

#### Volume 1 Chapter 5
- **Behavior:** Rejected the solicitation of the old shopkeeper of the Qing Gang and chose to trace the source of the monster alone
- **Changes in relationship:** Cooperation with the Qinggang changed to alienation; Lin Yan secretly paid attention to his movements
```

- **Behavior:** What the character actually did in this chapter (including objects and
  results), stated clearly in one sentence
- **Relationship changes:** What changes have occurred in the nature of the relationship
  with whom (hostility/cooperation/estrangement/owing favors, etc.), if not, it will be
  empty

---

## Case

The following cases are for reference when talking about the corresponding role types.

### Case 1: xianxiaxuanhuan, Protagonist Shen Mu

```markdown
### Basic information
- **Codename**: shen-mu
- **Name**: Shen Mu
- **Story Role**: protagonist
- **Appearance**: Slender build, rough palms, an old scar on the left eyebrow
- **Background**: The son of Orion at the foot of Cangwu Mountain, his parents died when monsters attacked the village, and he was adopted by the old shopkeeper of the Qing Gang
- **Language Features**: He speaks in a rough voice, scolds his mother when he is anxious, and his catchphrase is "his grandma's"

### Cognitive 6-layer model
- **World view**: The strong make the rules and the weak follow the rules. Complaining is useless, becoming stronger is useful.
- **Self-positioning**: I think I am calm, rational and make decisions before taking action, but in reality, when my relatives and friends are in danger, my first reaction is to rush forward, and my rationality is to make amends afterwards.
- **Values**: Never betray your brothers. Do not bully civilians. You can take advantage of your opponent but you can't insult your opponent's dignity.
- **Ability**: Can detect the source of murderous intent within ten steps; can pull an 80-pound bow with one hand and fire three arrows without missing the target; has photographic memory but needs time to recall.
- **Skills**: Survival skills from the bottom of the Qing Gang (identifying people by footsteps, identifying identities by looking at clothes); learned abacus and bookkeeping from the accountant.
- **Environment**: I grew up working as a dock worker and saw all kinds of people. The current place of residence is a side room given by the old shopkeeper of the Qinggang, in an alley near the dock.

### Plot resume

#### Volume 1 Chapter 3
- **Behavior:** Killed Zhao Hu, the leader of Black Wind Village, and rescued the captive villagers
- **Relationship changes:** Became hostile with the remnants of Heifeng Village; the rescued villager Zhang Bo owed him a life

#### Volume 1 Chapter 5
- **Behavior:** Rejected the solicitation of the old shopkeeper of the Qing Gang and chose to trace the source of the monster alone
- **Changes in relationship:** Cooperation with the Qinggang changed to alienation; Lin Yan secretly paid attention to his movements
```

### Case 2: Urban Supernatural Power - Supporting Actor Lin Yan

```markdown
### Basic information
- **Codename**: lin-yan
- **Name**: Lin Yan
- **Story Role**: supporting
- **Appearance**: He is in his early thirties, dressed inconspicuously, walks silently, and has a face that cannot be remembered even if he is seen in the crowd.
- **Background**: I grew up in a shantytown in Jiangcheng City. My father is in prison and my mother works in a factory. Started living on the streets at the age of thirteen
- **Language Features**: Speech without swear words, but every sentence is pungent, and the catchphrase is "What do you say?"

### Cognitive 6-layer model
- **World view**: There is no right or wrong in this world, only "what you can't afford to provoke". Neither the Special Administrative Office nor the Dark Web are good things, but those who go against them are even worse.
- **Self-positioning**: I feel that I am a careful middleman, not taking sides, not standing out, and living as long as possible. But occasionally he would help others when he shouldn't have done so - and he couldn't explain it afterwards.
- **Values**: No drugs or human trafficking. You can sell information but not your life. The favors owed must be repaid.
- **Ability**: Can remember the face and voiceprint of someone you have met once, and still recognize it three years later. Lock opening - from ordinary padlocks to electronic combination locks, they can all be opened within three minutes. Disguise - After changing your clothes and walking posture, you won't be able to recognize someone you know when they walk by you.
- **Skills**: Jiangcheng City Urban Living Map - Know all surveillance blind spots, dark alleys, and abandoned buildings. I learned lockpicking from an old locksmith for three months, and then I learned it myself.
- **Environment**: I have been delivering goods to the dark web for three years, and I know too many things that I shouldn’t know. The Special Branch was unaware of her existence. Now I live in a rental house in the south of the city. The window faces the back alley and I can climb out at any time.
```

---

## Two-step general inspection (leave after chatting)

After you have finished chatting and writing the file, do a two-step self-check. But
don't go to the next stage.

### Step One: Format Check

- [ ] The file name is Pinyin ID, not Chinese?
- [ ] `story-role` is one of the three (protagonist / antagonist / supporting)?
- [ ] Are the basic information fields complete (codename/name/story
      character/appearance/background/language characteristics)?
- [ ] All six levels have values and no empty fields?

### Step Two: Availability Check

| Check items | How to check | Failed processing |
|--------|--------|-----------|
| Behavior can be inferred | If the character is given an unexpected situation, can you tell the character's reaction? | Can't tell → Return, the setting is not specific enough |
| Protagonist’s True Weaknesses | Will the shortcomings cause the character to make wrong choices in Chapters 3-5? | False shortcomings → return and rewrite |
| Supporting characters are self-driven | Take away the protagonist, will the supporting characters still have something to do? | Toolman → return plus self-driving purpose |
| Abilities have boundaries | Is there a clear output upper limit for each ability? | "Very strong" without boundaries → return and add restrictions |
| Skills have sources | Where did you learn each skill? | No source → Return for supplement |
| Consistent with the world | Do origins and circumstances have corresponding positions in the worldview? | Disjointed→Return to Adjustment |

---

## Step Three: Character Biopsy (Scenario Play Test)

After the format and usability checks pass, let the character live in the scene for
once. Agent dynamically generates test scenarios based on the 6-layer settings of the
character, and then answers as the character: what to choose, how to do it, and what to
say. The author determines whether it is "like or not".

**Rules:** The scene grows from the character's specific settings - he has a level 3
value conflict, and the scene overrides that conflict. He has a level 1 world view and
creed, and the scene conforms to that creed. Don’t take general questions.

### Process

1. Agent reads character level 6 + language features
2. Agent generates **3 test scenarios** according to the settings (see the case below),
   each scenario comes with a clear question
3. Agent answers as a character - giving the character's choices, actions, and original
   words
4. The author evaluates each item: "similar" / "not very similar" / "not at all right"
5. There are "not very similar" or "not right at all" → Agent traces back to which layer
   the positioning deviation occurs → returns to the corresponding layer for additional
   discussion → retests the scenario after modification

### Scene generation principles

| Test dimensions | Target layer | Where the scene grows from |
|---------|--------|----------------|
| Values Conflict | Layer 3 | Grows from the character's value items - he has "not betraying brothers", and the scene has a choice between brothers and justice |
| World view impact | Layer 1 | Grows from the character's world view creed - he believes that "the strong make the rules", the scene allows him to witness the weak defeat the strong |
| Self-perception bias | Layer 2 | Grows from the gap between self-positioning and actual behavior - he felt "I am a devil", and the scene made him save a person who shouldn't be saved |
| Situation reaction | Layer 6+ language features | Growing up from birth and environment - growing up on the dock, the scene is the conflict between the dock and the official |
| Limit of Ability | Layer 4 | Grow from the upper limit of ability - if he has the upper limit, the scene will exceed that line |

### Case

> **Character: Shen Mu (xianxia (immortal cultivation), born in the dock, believes that the strong make the
> rules)** Test scenario generated by Agent: Scene 1 (Layer 1 World View): You see an
> unarmed mortal pointing at the Jindan monk’s nose and cursing. The monk raised his
> hand to kill. No one dares to care around. what will you do? What do you think?
> Scenario 2 (Layer 3 Values + Layer 2 Self-positioning): You find that the old
> shopkeeper of the Qing Gang to whom you owe a favor is selling monster cubs to rogue
> cultivators who practice evil arts. You promised that you would repay the life you
> owed him. He lets you look out. What should you do? Scene 3 (Layer 6 Situation +
> Language Features): You return to the dock injured and find that your side room is
> occupied by a businessman from out of town. He throws you a bag of money and tells
> you to get lost. Surrounded by dock workers you know. What do you say and do?
> Scenario 1 where Agent answered as Shen Mu: Choice: rush forward and pull away the
> mortal, blocking the middle. Behavior: Push the mortal back three steps with your
> left hand, hold the bow string with your right hand, and do not pull out the arrow.
> His eyes were fixed on the monk's hands. Original words: "He can't give you a slap
> in the face. If you want to kill me, kill me. Don't dirty my land at the dock." I
> thought to myself: It's none of my business that this person is seeking death, but
> the monks are killing people at the dock and the government has closed the harbor.
> Where the hell am I going to fish. Author's judgment: "Like." → Passed. If the
> author says "It's not like that - Shen Mu doesn't mind his own business" → Agent
> fallback analysis: There is a conflict in the world view at level 1 - Thaksin
> believed that "the strong make the rules", but chose to intervene. Is it that level
> 1 is not accurate enough, or does level 2 have an unexpressed self-positioning (he
> thinks he is cold-blooded but actually has a bottom line)? → After additional
> discussion, retest scenario 1.

### Biopsy passing criteria

All three scenes were judged "like" by the author → character settings are available.
There is no need to strive for perfection in every detail, as long as the characters’
reactions to key conflicts are predictable and consistent.
