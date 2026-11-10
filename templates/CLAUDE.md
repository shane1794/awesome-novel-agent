# {project-name}

## AI Guide

The writing workflow for this project is carried out by 9 collaborating agents, defined under `.claude/agents/`.

**Start writing:** Enter `@novel-agent` to enter the writing loop.

**Writing flow:** Settings -> (author confirms) -> Volume outline -> (author confirms) -> Chapter outline -> (author confirms) -> Prompt -> Main text -> Acceptance -> Archive -> Next chapter

**Soul and brushwork:** Settings, volume outlines, and chapter outlines are the soul of the story. At each step, show the author a summary first and continue only after the author nods. The main text and polishing after the prompt are the AI's brushwork.

**Project structure:**
- `story.md`: Project index + main story arc outline
- `settings/`: Worldbuilding, characters, writing style, timeline
- `volumes/`: Volume outlines
- `chapters/`: Chapter outlines
- `prompts/`: Prompts
- `archives/`: Main text
- `.agent/`: Status tracking + agent communication
- `.claude/memory/`: Live writing memory (author feedback from each stage, accumulated over time)
- `.claude/knowledge/`: Anti-AI rules, style preferences, permanent memory, genre reference material
