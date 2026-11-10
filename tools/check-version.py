#!/usr/bin/env python3
"""Version consistency check (arch-review 2026-08)

The VERSION file is the single authoritative source for the version number; check that the copies elsewhere have not drifted:
  1. ARCHITECTURE.md version header (> Current version: vX.Y.Z)
  2. skill.json version field
  3. templates/.agent/status.md skill_version (sync-project writes the project status back from it)
  4. tools/init.py write_status skill_version seed value (the source of the status file for new projects)

When releasing, change VERSION and sync the four copies (chore: bump version); missing one here turns the check red.

Usage: python tools/check-version.py
Exit code 0 = consistent, 1 = drift found (used by CI). Standard library only.

Test injection: NOVEL_REPO_ROOT points at a miniature repository directory (used by test_platforms to construct drift scenarios).
"""

from __future__ import annotations  # str | None annotations are evaluated lazily under Python 3.9

import os
import re
import sys

from pathlib import Path

from style_common import force_utf8

force_utf8()

ROOT = Path(os.environ.get("NOVEL_REPO_ROOT") or Path(__file__).resolve().parent.parent)


def _version_from_version_file() -> str:
    """VERSION file to a bare version number (strip the v prefix and whitespace)."""
    text = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    return text.lstrip("vV")


def main() -> int:
    errors = []
    version = _version_from_version_file()
    if not re.fullmatch(r"\d+\.\d+\.\d+", version):
        print(f"❌ VERSION file has an abnormal format: {version!r} (expected vX.Y.Z)")
        return 1

    def expect(label: str, actual: str | None) -> None:
        if actual != version:
            errors.append(f"{label}: {actual or '(not found)'} != VERSION's {version}")

    # 1. ARCHITECTURE.md version header
    arch = ROOT / "ARCHITECTURE.md"
    m = re.search(r"Current version[：:]\s*v?(\d+\.\d+\.\d+)", arch.read_text(encoding="utf-8"))
    expect("ARCHITECTURE.md version header", m.group(1) if m else None)

    # 2. skill.json version
    sj = ROOT / "skill.json"
    try:
        import json
        data = json.loads(sj.read_text(encoding="utf-8"))
        expect("skill.json version", str(data.get("version") or "") or None)
    except Exception as e:
        errors.append(f"skill.json parse failed: {e}")

    # 3. templates/.agent/status.md skill_version
    status_tpl = ROOT / "templates" / ".agent" / "status.md"
    m = re.search(r"skill_version:\*\*\s*(\d+\.\d+\.\d+)",
                  status_tpl.read_text(encoding="utf-8"))
    expect("templates/.agent/status.md skill_version", m.group(1) if m else None)

    # 4. tools/init.py write_status seed value
    init_src = ROOT / "tools" / "init.py"
    m = re.search(r"skill_version:\*\*\s*(\d+\.\d+\.\d+)",
                  init_src.read_text(encoding="utf-8"))
    expect("tools/init.py write_status seed value", m.group(1) if m else None)

    for e in errors:
        print(f"❌ {e}")
    if errors:
        print(f"\n{len(errors)} version drift(s) found (sync to VERSION=v{version})")
        return 1
    print(f"✅ Version numbers match (v{version}, five copies aligned to a single source)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
