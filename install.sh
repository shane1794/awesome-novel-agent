#!/bin/bash
# Novel Agent Skill install script
#
# awesome-novel-agent - AI-assisted novel writing workflow system
# Copyright (C) 2026  modoojunko
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

set -e

usage() {
    echo "Usage: $0 <platform>"
    echo "Platforms: claude-code, opencode, codex, zcode, dsh, grok, hermes, openclaw, deepseek-tui"
    exit 1
}

if [ $# -lt 1 ]; then
    usage
fi

PLATFORM="$1"

case "$PLATFORM" in
    claude-code)
        SKILLS_DIR="$HOME/.claude/skills"
        ;;
    hermes)
        SKILLS_DIR="$HOME/.hermes/skills"
        ;;
    openclaw)
        SKILLS_DIR="$HOME/.openclaw/skills"
        ;;
    deepseek-tui)
        SKILLS_DIR="$HOME/.deepseek/skills"
        ;;
    opencode)
        SKILLS_DIR="$HOME/.config/opencode/skills"
        ;;
    codex)
        SKILLS_DIR="$HOME/.codex/skills"
        ;;
    zcode)
        SKILLS_DIR="$HOME/.zcode/skills"
        ;;
    dsh)
        SKILLS_DIR="$HOME/.dsh/skills"
        ;;
    grok)
        SKILLS_DIR="$HOME/.grok/skills"
        ;;
    *)
        echo "Unsupported platform: $PLATFORM"
        usage
        ;;
esac

DEST="$SKILLS_DIR/awesome-novel"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Python version gate: check before creating/deleting any directory (fail-fast).
# If the version is not met, installation aborts immediately instead of failing later when init.py / sync-project.py runs.
# Use NOVEL_PYTHON to specify the interpreter explicitly (e.g. Homebrew's python3.12).
PY_BIN="${NOVEL_PYTHON:-}"
if [ -z "$PY_BIN" ]; then
    PY_BIN="$(command -v python3 || true)"
fi
if [ -z "$PY_BIN" ]; then
    echo "Error: python3 not found. Please install Python 3.9+ first (https://www.python.org/downloads/)"
    exit 1
fi
if ! "$PY_BIN" "$SCRIPT_DIR/tools/check-python.py"; then
    echo "Installation aborted: please upgrade Python and try again."
    exit 1
fi

# pyyaml gate: agent/skill conversion for opencode / codex / zcode / dsh / grok depends on pyyaml (aligned
# with the runtime rule in tools/platforms.py ensure_yaml); the claude platform is a plain copy with no conversion,
# and hermes/openclaw/deepseek-tui do not go through conversion either, so none of them need it. When it is missing,
# fail-fast likewise happens before any directory is created/deleted, instead of failing later when init.py / sync-project.py runs.
case "$PLATFORM" in
    opencode|codex|zcode|dsh|grok)
        if ! "$PY_BIN" "$SCRIPT_DIR/tools/check-yaml.py" "$PLATFORM"; then
            echo "Installation aborted: pyyaml is missing. Please run pip install pyyaml first (use pip install --user pyyaml if the system Python has restricted permissions), then try again."
            exit 1
        fi
        ;;
esac

echo "Installing to: $DEST"
export NOVEL_SKILL_HOME="$DEST"

# Note: NOVEL_SKILL_HOME only takes effect within this script session; it is no longer written to ~/.profile / ~/.bashrc or similar.
# Persisting it would shadow the repository source (init.py resolves the skill root from __file__, and env taking precedence would deploy stale installed prompts to new projects).

# Safety check: DEST must be a skills/awesome-novel path starting with $HOME.
# First do a side-effect-free string check (reject before creating any directory when HOME is unset or the path is abnormal),
# then create the parent directory and re-check the canonical path (to avoid false rejection when dirname cannot resolve under a fresh HOME).
HOME_NORM="${HOME%/}"
if [[ -z "$HOME_NORM" || -z "$DEST" || "$DEST" == "/" \
      || "$DEST" != "$HOME_NORM/."*"/skills/awesome-novel" ]]; then
    echo "Error: abnormal install target path ($DEST), aborting."
    exit 1
fi
mkdir -p "$(dirname "$DEST")"
CANONICAL_DEST="$(cd "$(dirname "$DEST")" && pwd)/$(basename "$DEST")"
if [[ "$CANONICAL_DEST" != "$HOME_NORM/."*"/skills/awesome-novel" ]]; then
    echo "Error: abnormal install target path ($DEST), aborting."
    exit 1
fi

# Create the skill directory; empty it if it already exists
rm -rf "$DEST"
mkdir -p "$DEST"

# Copy the files needed at runtime (include list, to avoid leaking repository metadata)
cp "$SCRIPT_DIR/SKILL.md" "$DEST/"
cp -r "$SCRIPT_DIR/agents" "$DEST/"
cp -r "$SCRIPT_DIR/skills" "$DEST/"
cp -r "$SCRIPT_DIR/knowledge" "$DEST/"
cp -r "$SCRIPT_DIR/templates" "$DEST/"
cp -r "$SCRIPT_DIR/tools" "$DEST/"
# memory/ is deprecated (writer-style has moved to knowledge/format-specs/); keep the guard for compatibility with old repositories
[ -d "$SCRIPT_DIR/memory" ] && cp -r "$SCRIPT_DIR/memory" "$DEST/"

echo "Installation complete!"
