# Short text format specifications

> Must read before writing the text. Just deliver the layout: chapter markers,
> paragraph form, dialogue, punctuation, meta information prohibitions. This is the
> default delivery format for short stories in this repo; if the author or the
> target platform has other explicit requirements, the author/platform requirements
> will override it.

## Chapter markers

The whole text is unified, no mixing, and the short sections are **without titles**
(purely numbered):

| Format | Platform Applicable | Example |
|------|----------|------|
| `###1.` | Short story default, Hongguo, Heiyan | `###1.` `###2.` |
| `###第N章` | Fanqie / Qimao / long ancient-style pieces | `###第一章` |
| `1.` (pure numbers) | Zhihu Yanyan | `1.` `2.` |

## Paragraph: Two sets of platform templates

First identify the background color of the platform, and then allocate the number of
words according to the principle of density; **There is no uniform hard line for the
number of sentences in each paragraph**, only long and short sentences are interlaced to
make it lively.

### Heiyan: One sentence at a time, leave the space blank and read quickly

Mainly one sentence and one paragraph, with frequent line breaks to create a sense of
falling; it is normal to form single sentences into paragraphs; hooks must be left at
the end of each section.

### Fanqie / Qimao: Short paragraphs as the background, narrative intertwined with dialogue

Short paragraphs are still the background, but multi-sentence retrospective narrative
paragraphs and dialogues are intertwined; ancient-style romance and realistic family drama can use longer narrative paragraphs
to carry a complete emotional chain; satisfying payoff, face-slapping, and reversal
points are shortened, and transitions are carried with a single sentence.

### Two sets of common hard constraints

- Only one line break `\n` is allowed between adjacent paragraphs of the text, and no
  blank lines or continuous line breaks are allowed (not counting before and after
  chapter marks)
- **No indent** (no full-width/half-width spaces for indentation)
- **Body paragraph Markdown is prohibited** (except for unified section marks, `**` `*`
  `#` `---` is not used)
- **Upper and lower limits of paragraph form** (see Section 7 of
  `.claude/knowledge/short-anti-ai.md`): The background color of short paragraphs is the
  lower limit; more than 3 consecutive paragraphs, 3-5 word fragments and not at the
  emotional peak = telegraph style; revise it

## Dialogue

- Quotation marks: Default is `"dialogue content"` (half-width double quotation marks); use `「」`
  when specified by Zhihu Yanyan or the author. Do not change `「」` as an error.
- Dialogue **stands on its own line** and is not embedded in a narrative paragraph
- Use actions instead of dialogue tags; ordinary "say" can be retained according to
  context; tags are omitted for continuous conversations between two people
- Each line of dialogue should at least advance the plot/reveal character/create
  conflict/lay foreshadowing; if there are multiple consecutive sentences that are just
  pleasantries or connections, they will be deleted.

## Punctuation hard constraints

`...` / `double em dash` / `em dash` / `--` will not appear in the text (including dialogue).
Pauses, chokes, unfinished words, interruptions, and blank spaces should all be realized
with short sentences, periods, commas, action beats, and line breaks. Punctuation should
follow the tone: use question marks for questioning; use 1 exclamation mark for a real explosive point, with at most 1-2 in a row; do not
flatten the whole text into declarative periods.

## It is forbidden to mix meta information into the body text.

In the text narrative, dialogue, and psychological description, the following shall not
appear: `第[一二三...]章` (referring to one's own chapter), previous chapter, this chapter,
previous text, following text, foreshadowing, outline, and reader. Change it to an event
anchor point or relative time that the character can perceive. Exception: Characters
actually read/discuss the "Chapter X" text within the story world.

## Platform coverage table

| Platform | Chapter Markers | Conversation Format | Paragraph Background | Special Requirements |
|------|----------|----------|----------|----------|
| Zhihu Yanyan | `1.` (pure numbers) | `「」` | Short paragraph + narrative interweaving | The introduction needs to be polished separately (150-220 words) |
| Fanqie | `###第N章` | `""` | The short paragraph is the background color, allowing the narrative to interweave dialogue | The first paragraph must be attractive |
| Hongguo | `###1.` | `""` | The short section is the background color | None |
| Heiyan | `###1.` | `""` | One sentence per paragraph, multiple line breaks and blank space | A hook must be left at the end of each section |

When the author does not specify a platform, the default short story general format is:
`###1.` + `""` + Fanqie short paragraph background color.

## Quick check after writing each paragraph

- [ ] Does the paragraph shape conform to the target platform template? Long and short
      are interlaced and not cut into an outline with the same number of words?
- [ ] Only one `\n` between adjacent paragraphs?
- [ ] No indentation, no Markdown in the body?
- [ ] Does the dialogue stand on its own line and the quote style matches the platform?
- [ ] No forbidden punctuation, use short sentences/actions/line breaks for pauses?
- [ ] Does each line of dialogue have a function
      (progression/character/conflict/foreshadowing)?
- [ ] Meta-information words?
