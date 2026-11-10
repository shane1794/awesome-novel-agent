#!/usr/bin/env python3
"""Shared test utilities: check assertions + PASS/FAIL summary + module loading.

Shared by the three test files test_style_rules.py / test_style_distill.py / test_platforms.py,
so they do not each copy a check() (previously the three copies risked signature/behavior drift).

Usage:
  from test_util import check, summary, exit_code
  check("description", cond, detail_if_fail)
  ...
  print(f"\n{summary()}"); sys.exit(exit_code())
"""
import importlib.util
import sys
from pathlib import Path

PASS = 0
FAIL = 0


def check(name: str, cond: bool, detail: str = ""):
    global PASS, FAIL
    if cond:
        PASS += 1
        print(f"  ok  {name}")
    else:
        FAIL += 1
        print(f"  FAIL {name}  {detail}")


def summary() -> str:
    return f"{PASS} passed, {FAIL} failed"


def exit_code() -> int:
    return 1 if FAIL else 0


def load_module(name: str, path) -> object:
    """Load a module by file path (file names containing hyphens cannot be imported directly, e.g. check-agents.py).
    Shared importlib boilerplate for the test files (review #41: previously copied x5).
    Register it in sys.modules before exec, since a module using @dataclass needs a resolvable __module__."""
    spec = importlib.util.spec_from_file_location(name, str(Path(path)))
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod
