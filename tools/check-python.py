#!/usr/bin/env python3
"""Python version gate check (fail-fast at install time).

install.sh / install.ps1 call this script before creating/deleting any directory; when the interpreter version does not meet
the requirement it fails immediately, so version problems surface at install time instead of waiting until init.py /
sync-project.py runs and they appear as a TypeError / SyntaxError.

Usage:
  python tools/check-python.py             # check the current interpreter >= 3.9
  python tools/check-python.py --min 3.10  # custom minimum version (for tests)

Exit codes:
  0 = requirement met
  1 = version too low
  2 = argument error
"""

import sys

# Project's actual minimum version (tools/*.py have all been verified 3.9-compatible;
# if new code uses syntax from a higher version, raise this in sync and expose it at install time).
MIN_VERSION = (3, 9)


def _label(version: tuple) -> str:
    return ".".join(str(x) for x in version)


def main(argv) -> int:
    min_version = MIN_VERSION
    if "--min" in argv:
        idx = argv.index("--min")
        if idx + 1 >= len(argv):
            print("Error: --min needs a version number (e.g. 3.10)", file=sys.stderr)
            return 2
        raw = argv[idx + 1]
        try:
            parts = tuple(int(x) for x in raw.split(".")[:2])
            if len(parts) != 2:
                raise ValueError
            min_version = parts
        except ValueError:
            print(f"Error: --min needs a version number like 3.10, got: {raw}", file=sys.stderr)
            return 2

    current = sys.version_info[:2]
    if current < min_version:
        print(
            f"Error: Python {_label(min_version)} or higher is required; current version is {sys.version.split()[0]}.",
            file=sys.stderr,
        )
        print(
            "Please upgrade Python and try again: https://www.python.org/downloads/"
            "(on macOS you can also run `brew install python@3.12`)",
            file=sys.stderr,
        )
        return 1

    print(f"Python {sys.version.split()[0]} meets the requirement (>= {_label(min_version)}).")
    return 0


if __name__ == "__main__":
    for s in (sys.stdin, sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8")
        except AttributeError:
            pass
    sys.exit(main(sys.argv[1:]))
