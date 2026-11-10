# {project-name}

## AI Guide (Short Story Project)

The short-story writing workflow for this project is carried out by 6 collaborating agents, defined under `.claude/agents/`.

**Start writing:** Enter `@short-agent` to enter the writing loop, or just say "write me a short story".

**Writing flow:** Set the emotion and direction -> (author confirms) -> Concept and outline -> (author confirms) -> Writing contract assembly -> Independent contract audit -> Write the main text in batches -> De-AI pass and polish -> Payoff check -> Acceptance and delivery -> (author may revise or write the next story)

**Soul and brushwork:** The emotion goal, framework, and outline are the soul of the story. At each step, show the author a summary first and continue only after the author nods. The main text and polishing after the contract are the AI's brushwork.

**Project structure:**
- `story.md`: Project index + story list (with a `length: short` marker)
- `stories/{slug}/`: One directory per story: `setting.md` (framework), `outline.md` (outline), `prompt.md` (writing contract), `manuscript.md` (finished main text)
- `sandbox/`: Check assets (regression pattern library, locked-lines whitelist)
- `.agent/`: Status tracking + agent communication (order files)
- `.claude/agents/`: Agent definitions
- `.claude/knowledge/`: Short-story de-AI criteria, short-story format specs, short-story writing references, genre style packs
- `.claude/memory/`: Live writing memory (author feedback from each stage, accumulated over time)
