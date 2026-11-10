# Repository Guidelines

## Working Principles

Behavioral guidelines to reduce common LLM coding mistakes. Tradeoff: these guidelines lean toward caution over speed. For simple tasks, use your own judgment.

### 1. Think before coding
Do not assume. Do not hide confusion. Make tradeoffs explicit.

Before implementing:
- State your assumptions clearly. If unsure, ask.
- If there are multiple interpretations, present all of them, do not silently pick one.
- If there is a simpler solution, say so. Push back when needed.
- If something is unclear, stop. Point out what is confusing. Ask.

### 2. Simplicity first
Solve the problem with the least code. No speculative design.

- Do not add features beyond what is required.
- Do not abstract code that is only used once.
- Do not introduce "flexibility" or "configurability" that was not requested.
- Do not handle errors for scenarios that cannot happen.
- If you wrote 200 lines but 50 lines would do it, rewrite it.
- Ask yourself: "Would a senior engineer call this over-engineered?" If the answer is yes, simplify it.

### 3. Precise edits
Touch only what you must touch. Clean up only the mess you made yourself.

When editing existing code:
- Do not "improve" adjacent code, comments, or formatting.
- Do not refactor things that are not broken.
- Match the existing style, even if you would not write it that way yourself.
- If you notice unrelated dead code, raise it, do not delete it.

When your change leaves orphaned code behind:
- Delete imports/variables/functions your change made unused.
- Do not delete pre-existing dead code unless asked.
- Test: every changed line should trace directly back to the user's request.

### 4. Goal-driven execution
Define success criteria. Loop and verify until they pass.

Turn a task into verifiable goals:
- "Add validation" becomes "Write tests for invalid input, then make them pass"
- "Fix a bug" becomes "Write a test that reproduces it, then make it pass"
- "Refactor X" becomes "Make sure tests pass before and after the refactor"

For multi-step tasks, briefly list the plan:
1. [Step] → verify: [checkpoint]
2. [Step] → verify: [checkpoint]
3. [Step] → verify: [checkpoint]

Strong success criteria let you loop independently. Weak criteria ("make it run") need constant clarification.

## Communicating with the author

Agents talk to, question, present to, and confirm with the writer always in plain everyday language. The hard rules and the "internal term → author-facing wording" mapping table live in `knowledge/format-specs/author-communication.md` (after deployment: `.claude/knowledge/author-communication.md`, referenced by every agent that talks to the author): internal field names, invented terms, and process words must not appear in author-visible text; use the summary template when showing structure to the author, never the raw structure; common web-novel terms (爽点, 打脸, 钩子, 金手指, 卷纲, 章纲, etc.) stay as-is and are not translated. When changing agent wording, check the mapping table first; when adding a new internal term, add it to the table at the same time.

## Project structure and module organization

- `agents/`, 9 writing agent definitions (novel-agent as director + 8 sub-agents), Markdown + frontmatter.
- `skills/`, SOP instructions for each agent, named `{phase}-{action}.md`.
- `knowledge/`, Knowledge base: `genre-example/` genre files, `anti-ai/` anti-AI rules, `format-specs/` format specs, `{plot|scene|character|title}-craft/` writing methodology, `style-distill/` style-distillation prompt templates.
- `templates/`, Project init templates: `settings/` settings, `chapters|volumes|archives|prompts|sandbox/` and the `story.md` project skeleton, `CLAUDE.md`/`AGENTS.md`/`AGENTS.codex.md` project-level instructions, `migration/` legacy project migration.
- `tools/`, Python tools: `init.py` (init), `sync-project.py` (sync), `platforms.py` (platform adapters), `check-agents.py` / `check-conflicts.py` / `check-version.py` / `check-python.py` / `check-yaml.py` (static checks), `check-prose.py` (prose AI-flavor machine detection, used for anti-ai Phase 2 first pass / Phase 4 re-run, deployed by init/sync to `<platform root>/tools/`), `check-chapter.py` (chapter delivery hard-defect check: sandwiching / nested quotes / half-width quotes / word-count reconciliation are hard requirements, project-level regression library and whitelist live outside in `sandbox/`, also deployed by init/sync), `style_render.py` / `style_verify.py` / `style_common.py` (style-distill rendering / acceptance / shared code), `test_platforms.py` / `test_style_rules.py` / `test_style_distill.py` / `test_check_prose.py` / `test_check_chapter.py` (tests), `test_util.py` (shared test helpers).
- Root directory: `README.md`, `SKILL.md`, `skill.json`, `ARCHITECTURE.md`, `CONTRIBUTING.md`, `install.sh` / `install.ps1`, `index.html` (GitHub Pages landing page); images in `reference/images/`, videos in `reference/video/`.

## Build, test, and development commands

No build step. The Python code uses only the standard library, except for pyyaml: agent conversion for `--platform opencode|reasonix|codex|zcode|dsh|grok` (platforms.py) and style-distill card frontmatter parsing/validation (style_common.py / style_render.py / check-agents.py) (see `tools/requirements.txt`, installed automatically by CI):
- `python tools/init.py <project path> [--genre N] [--platform claude|opencode|reasonix|codex|zcode|dsh|grok]`, initialize a novel project skeleton
- `python tools/sync-project.py <project path> --check`, check whether a project needs syncing (0 = up to date, 1 = updates available, 2 = invalid)
- `python tools/test_platforms.py`, run tests (exit code 0 = pass)
- `python tools/check-agents.py`, validate agent frontmatter reference paths
- `python tools/check-conflicts.py`, check anti-AI rule threshold conflicts
- `python -m py_compile tools/*.py`, syntax check

CI: `.github/workflows/static.yml`, runs syntax / agent / rule checks + the platform test suite on push to main, and deploys GitHub Pages.

## Coding style and naming conventions

- Python: snake_case file names; standard library only; entry scripts call `reconfigure(encoding="utf-8")` at the top to prevent garbled Chinese on Windows; docstrings state usage and exit codes.
- Markdown: Chinese body text, UTF-8; project-internal files referenced in frontmatter and body text always use **post-deployment paths**: knowledge uses the `.claude/knowledge/...` base (format-specs are flattened/merged, so repository-relative paths would break, and check-agents.py validates against the deployed layout), skills/ references use `skills/xxx.md` (repository paths, must exist), settings/ and other project-generated files use paths relative to the project root. Post-deployment paths are rewritten per platform by init.py's rewrite_refs.
- Naming: agent definitions `{role}-agent.md`; chapters `vol-{N}-ch-{M}.md`, volume outlines `volume-{N}.md`; knowledge files organized as `knowledge/<category>/<genre or topic>.md`.
- Changes fit the project scope (AI-assisted novel writing); do not introduce unrelated features or dependencies.

## Test guidelines

- No third-party test framework; `tools/test_platforms.py` uses hand-written assertions, prints `ok/FAIL` to stdout, and a non-zero exit code means failure.
- Test functions start with `test_`; E2E tests use temp directories to verify init/sync output on all seven platforms (claude/opencode/reasonix/codex/zcode/dsh/grok).
- Run `check-agents.py` for changes touching agent definitions, `check-conflicts.py` for changes touching anti-AI rules.
- For behavior changes, follow red-then-green: add a failing test case first, then implement.

## Commit and PR guidelines

- Commit messages follow Conventional Commits + a Chinese description: `feat:` / `fix:` / `docs:` / `test:` / `refactor:` / `chore:`, e.g. `fix: sync-project --platform guard against swallowing --check`.
- On release, `chore: bump version to vX.Y.Z`, updating `VERSION` and `docs/releasenotes/releasenote-X.Y.Z.md` in the same step.
- PRs: create a branch from main, never edit main directly; one PR focuses on one change and links its issue; test in at least one real AI terminal (claude/opencode/reasonix/codex/zcode/dsh/grok) before submitting.

## Security and configuration notes

- Platform adapter logic lives in `tools/platforms.py`; when adding a platform or changing a directory convention, change it there first, then sync init/sync.
- Follow AGPL-3.0: do not commit unlicensed material, infringing copy, or user novel content.
