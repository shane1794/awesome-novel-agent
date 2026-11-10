# {project-name}

## Codex Guide

The novel-writing workflow for this project is carried out by 9 collaborating agents, defined under `.codex/agents/` (TOML custom agents).

**Start writing:** In Codex, call novel-agent via `@novel-agent` or `spawn_agent` to enter the writing loop.

**Writing flow:** Settings -> (author confirms) -> Volume outline -> (author confirms) -> Chapter outline -> (author confirms) -> Prompt -> Main text -> De-AI pass -> Acceptance -> Archive -> Next chapter

**Soul and brushwork:** Settings, volume outlines, and chapter outlines are the soul of the story. At each step, show the author a summary first and continue only after the author nods. The main text and polishing after the prompt are the AI's brushwork.

## Dispatch Boundaries (Highest Priority)

- **Single dispatcher:** novel-agent is the only agent allowed to spawn sub-agents; any spawned sub-agent is forbidden from spawning further agents (including recursively spawning an agent of the same name).
- A sub-agent must not use the spawn_agent tool even if it holds it; when collaboration is needed, report to novel-agent and let novel-agent dispatch.
- After each spawn, novel-agent watches the agent tree; if a sub-agent spawns recursively, interrupt it immediately and re-dispatch.

**Project structure:**
- `story.md`: Project index + main story arc outline
- `settings/`: Worldbuilding, characters, writing style, timeline
- `volumes/`: Volume outlines
- `chapters/`: Chapter outlines
- `prompts/`: Prompts
- `archives/`: Main text
- `.agent/`: Status tracking + agent communication (order files)
- `.codex/agents/`: 9 custom agent definitions (novel-agent, volume-planner, chapter-planner, etc.)
- `.codex/skills/`: Standalone interaction tools (memory-recording, roleplay-sandbox)
- `.codex/memory/`: Live writing memory (author feedback from each stage, accumulated over time)
- `.codex/knowledge/`: Anti-AI rules, style preferences, permanent memory, genre reference material
