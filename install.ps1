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

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("claude-code", "opencode", "codex", "zcode", "dsh", "grok", "hermes", "openclaw", "deepseek-tui")]
    [string]$Platform
)

$HOME_DIR = $env:USERPROFILE

switch ($Platform) {
    "claude-code" {
        $DEST_DIR = Join-Path $HOME_DIR ".claude/skills/awesome-novel"
    }
    "hermes" {
        $DEST_DIR = Join-Path $HOME_DIR ".hermes/skills/awesome-novel"
    }
    "openclaw" {
        $DEST_DIR = Join-Path $HOME_DIR ".openclaw/skills/awesome-novel"
    }
    "deepseek-tui" {
        $DEST_DIR = Join-Path $HOME_DIR ".deepseek/skills/awesome-novel"
    }
    "opencode" {
        $DEST_DIR = Join-Path $HOME_DIR ".config/opencode/skills/awesome-novel"
    }
    "codex" {
        $DEST_DIR = Join-Path $HOME_DIR ".codex/skills/awesome-novel"
    }
    "zcode" {
        $DEST_DIR = Join-Path $HOME_DIR ".zcode/skills/awesome-novel"
    }
    "dsh" {
        $DEST_DIR = Join-Path $HOME_DIR ".dsh/skills/awesome-novel"
    }
    "grok" {
        $DEST_DIR = Join-Path $HOME_DIR ".grok/skills/awesome-novel"
    }
}

$SCRIPT_DIR = Split-Path -Parent $MyInvocation.MyCommand.Path

# Python version gate: check before creating/deleting any directory (fail-fast).
$PY_BIN = "python"
if (-not (Get-Command $PY_BIN -ErrorAction SilentlyContinue)) {
    Write-Host "Error: python not found. Please install Python 3.9+ first (https://www.python.org/downloads/)"
    exit 1
}
& $PY_BIN (Join-Path $SCRIPT_DIR "tools/check-python.py")
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installation aborted: please upgrade Python and try again."
    exit 1
}

# pyyaml gate: agent/skill conversion for opencode / codex / zcode / dsh / grok depends on pyyaml (aligned
# with the runtime rule in tools/platforms.py ensure_yaml); claude-code is a plain copy with no conversion, so it does not need it.
if ($Platform -in @("opencode", "codex", "zcode", "dsh", "grok")) {
    & $PY_BIN (Join-Path $SCRIPT_DIR "tools/check-yaml.py") $Platform
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Installation aborted: pyyaml is missing. Please run pip install pyyaml first, then try again."
        exit 1
    }
}

Write-Host "Installing to: $DEST_DIR"

# Create the directory; empty it if it already exists
Remove-Item -Recurse -Force $DEST_DIR -ErrorAction SilentlyContinue
New-Item -ItemType Directory -Force -Path $DEST_DIR | Out-Null

# Explicit include list, kept in sync with install.sh
$INCLUDES = @("SKILL.md", "agents", "skills", "knowledge", "templates", "tools")

foreach ($item in $INCLUDES) {
    $src = Join-Path $SCRIPT_DIR $item
    if (Test-Path $src) {
        Copy-Item -Recurse $src $DEST_DIR
    }
}

# memory/ is deprecated (writer-style has moved to knowledge/format-specs/); keep the guard for compatibility with old repositories
$memoryDir = Join-Path $SCRIPT_DIR "memory"
if (Test-Path $memoryDir) {
    Copy-Item -Recurse $memoryDir $DEST_DIR
}

Write-Host "Installation complete!"
