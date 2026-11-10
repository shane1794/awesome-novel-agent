# {project-name}

## OpenCode Guide

The novel-writing workflow for this project is carried out by 9 collaborating agents, defined under `.opencode/agents/`.

**Start writing:** In OpenCode, call novel-agent via `@novel-agent` or the Task tool to enter the writing loop.

**Writing flow:** Settings -> (author confirms) -> Volume outline -> (author confirms) -> Chapter outline -> (author confirms) -> Prompt -> Main text -> De-AI pass -> Acceptance -> Archive -> Next chapter

**Soul and brushwork:** Settings, volume outlines, and chapter outlines are the soul of the story. At each step, show the author a summary first and continue only after the author nods. The main text and polishing after the prompt are the AI's brushwork.

**Project structure:**
- `story.md`: Project index + main story arc outline
- `settings/`: Worldbuilding, characters, writing style, timeline
- `volumes/`: Volume outlines
- `chapters/`: Chapter outlines
- `prompts/`: Prompts
- `archives/`: Main text
- `.agent/`: Status tracking + agent communication (order files)
- `.opencode/agents/`: Agent definitions (novel-agent, volume-planner, chapter-planner, etc.)
- `.claude/memory/`: Live writing memory (author feedback from each stage, accumulated over time)
- `.claude/knowledge/`: Anti-AI rules, style preferences, permanent memory, genre reference material
