#!/usr/bin/env python3
"""pyyaml gate check (fail-fast at install time).

Agent conversion for non-claude platforms such as opencode / codex / grok depends on pyyaml; install.sh / install.ps1
call this script before creating/deleting any directory, and abort immediately when it is missing, instead of waiting until init.py /
sync-project.py runs to fail. The claude platform is a plain copy with no conversion, so it does not need this check.

Usage:
  python tools/check-yaml.py                # only check whether the current interpreter can import yaml
  python tools/check-yaml.py codex          # pass a platform name for a more specific error message

Exit codes:
  0 = installed
  1 = missing (prints a pip install hint)
  2 = argument error
"""

import sys


def main(argv) -> int:
    platform = None
    if len(argv) > 2:
        print("Error: accepts at most one platform argument.", file=sys.stderr)
        return 2
    if len(argv) == 2:
        platform = argv[1]

    try:
        import yaml  # noqa: F401
    except ImportError:
        label = platform or "current"
        print(
            f"Error: the {label} platform needs pyyaml (pip install pyyaml),"
            f"the current interpreter {sys.executable} does not have it installed.",
            file=sys.stderr,
        )
        return 1

    print(f"pyyaml is installed (interpreter {sys.executable}).")
    return 0


if __name__ == "__main__":
    for s in (sys.stdin, sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    sys.exit(main(sys.argv))
