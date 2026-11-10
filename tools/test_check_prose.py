#!/usr/bin/env python3
"""Unit tests for check-prose.py rules (human-feel port, Task D, issue #111).

Usage: python tools/test_check_prose.py
Exit code 0 = all passed.
"""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_util import check, summary, exit_code, load_module

CHECK_PROSE = load_module(
    "check_prose_mod", Path(__file__).resolve().parent / "check-prose.py"
)

CLEAN_TEXT = "\n".join([
    "陈放把借条折了两次，塞回口袋。",
    "老板问他是不是嫌少。他说没有，手却一直按着口袋。",
    "门外有人催货。老板起身去接电话。",
    "他站了一会儿，又把借条掏出来放回桌上。",
    "“日期写错了。”",
    "老板看了一眼。日期没有错。",
])


def run_check(text: str):
    """Write a temp file, run main(), and return (exit code, stdout)."""
    with tempfile.NamedTemporaryFile(
        "w", suffix=".md", delete=False, encoding="utf-8"
    ) as f:
        f.write(text)
        path = f.name
    argv_backup = sys.argv[:]
    sys.argv = ["check-prose.py", path]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            code = CHECK_PROSE.main()
    finally:
        sys.argv = argv_backup
        Path(path).unlink(missing_ok=True)
    return code, buf.getvalue()


def test_pivot_hard_fail():
    code, out = run_check("他不是生气，而是失望。他转身走了。")
    check("reversal sentence fails (exit code 1)", code == 1, code)
    check("output contains banned reversal sentence", "Banned reversal sentence" in out, out[:200])


def test_semantic_pivot_warning_only():
    code, out = run_check("你以为他赢了，其实他输了。第二天他照常上班。")
    check("reversal-rhetoric variant only warns (exit code 0)", code == 0, code)
    check("output contains suspected reversal-rhetoric variant", "Suspected reversal-rhetoric variant" in out, out[:200])


def test_dash_colon_not_hard_fail():
    code, _ = run_check("他顿了顿——没接话。他说：“走吧。”门关上了。")
    check("a single dash / quoted colon does not fail (web-novel rule)", code == 0, code)


def test_dash_dense_warning():
    code, out = run_check("他进门——先看左边——又看右边——最后盯着柜子。")
    check(
        "three dashes in one paragraph warn but do not fail",
        code == 0 and "dashes" in out and "Needs human review" in out,
        (code, out[:200]),
    )


def test_road_sign_fail():
    code, out = run_check("值得注意的是，他没走。")
    check("model signpost fails", code == 1 and "Model signpost" in out, (code, out[:200]))


def test_uniform_sentence_cv_warning():
    code, out = run_check("他数了一遍又数一遍。\n" * 13)
    check("too-similar sentence lengths warn", "too close in length" in out, out[:200])


def test_clean_text_pass():
    code, _ = run_check(CLEAN_TEXT)
    check("clean text exits 0", code == 0, code)


def test_read_error():
    argv_backup = sys.argv[:]
    sys.argv = ["check-prose.py", "/nonexistent/__no_such_file__.md"]
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            code = CHECK_PROSE.main()
    finally:
        sys.argv = argv_backup
    check("read failure exits 2", code == 2, code)


if __name__ == "__main__":
    test_pivot_hard_fail()
    test_semantic_pivot_warning_only()
    test_dash_colon_not_hard_fail()
    test_dash_dense_warning()
    test_road_sign_fail()
    test_uniform_sentence_cv_warning()
    test_clean_text_pass()
    test_read_error()
    print(f"\n{summary()}")
    sys.exit(exit_code())
