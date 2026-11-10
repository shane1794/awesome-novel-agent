#!/usr/bin/env python3
"""Unit tests for check-chapter.py rules (openspec change: add-zhuque-source-defense).

Usage: python tools/test_check_chapter.py
Exit code 0 = all passed.
"""
import contextlib
import io
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from test_util import check, summary, exit_code

TOOL = Path(__file__).resolve().parent / "check-chapter.py"

CLEAN_TEXT = "\n".join([
    "# 第一章 试探",
    "陈放把借条折了两次，塞回口袋。",
    "老板问他是不是嫌少。他说没有，手却一直按着口袋。",
    "“日期写错了。”",
    "老板看了一眼。日期没有错。他把借条推回去，没接话。",
])

# Minimal chapter skeleton that triggers warning-level checks (enough for adverb/fragment counts)
CLEAN_LONG_TEXT = "\n".join([CLEAN_TEXT] + [
    "他把杯里的凉茶喝完，起身去柜台结账。窗外的巷子已经亮起灯，收废品的三轮车慢慢骑过去。",
]) * 8


def run_tool(args, cwd=None):
    """Run the tool from the command line; return (exit code, stdout)."""
    import subprocess
    proc = subprocess.run(
        [sys.executable, str(TOOL)] + args,
        capture_output=True, text=True, cwd=cwd,
    )
    return proc.returncode, proc.stdout + proc.stderr


def write_chapter(text: str, dir_name: str = "正文", name: str = "vol-1-ch-1.md"):
    """Build a temp project: <tmp>/<dir_name>/<name>; return (tmp, chapter path)."""
    tmp = Path(tempfile.mkdtemp())
    chdir = tmp / dir_name
    chdir.mkdir(parents=True)
    path = chdir / name
    path.write_text(text, encoding="utf-8")
    return tmp, path


def test_clean_pass():
    tmp, path = write_chapter(CLEAN_LONG_TEXT)
    code, out = run_tool([str(path)])
    check("clean text exits 0", code == 0, out)
    check("clean text prints the platform word count", "Platform word count" in out, out)
    check("clean text has no hard hits", "hard hit(s)" not in out, out)
    sys.stdout.write("ok test_clean_pass\n")


def test_sandwich_tag_hard():
    tmp, path = write_chapter(CLEAN_TEXT + "\n“对数据。就这吧。”他说，“下不为例。”")
    code, out = run_tool([str(path)])
    check("sandwich (labelled) hard fail", code == 1, out)
    check("sandwich (labelled) flagged", "sandwich (labelled)" in out, out)
    sys.stdout.write("ok test_sandwich_tag_hard\n")


def test_nested_quotes_hard():
    tmp, path = write_chapter(CLEAN_TEXT + "\n群里都在刷“重启“重启”的话题，没人说话。")
    code, out = run_tool([str(path)])
    check("nested double quotes hard fail", code == 1, out)
    check("nested double quotes flagged", "nested double quotes" in out, out)
    sys.stdout.write("ok test_nested_quotes_hard\n")


def test_halfwidth_quotes_hard():
    tmp, path = write_chapter(CLEAN_TEXT + '\n他说"就这吧"，说完就走。')
    code, out = run_tool([str(path)])
    check("half-width quotes hard fail", code == 1, out)
    check("half-width quotes flagged", "half-width quotes" in out, out)
    sys.stdout.write("ok test_halfwidth_quotes_hard\n")


def test_dash_ellipsis_warning_only():
    text = CLEAN_TEXT + "\n他——一个干了二十年的老师傅——拿起锤子——又放下。"
    tmp, path = write_chapter(text)
    code, out = run_tool([str(path)])
    check("dashes only warn, do not hard-fail", code == 0, out)
    check("dashes have a needs-review marker", "needs review" in out and "dash" in out, out)
    sys.stdout.write("ok test_dash_ellipsis_warning_only\n")


def test_wordcount_mismatch_hard():
    # "这四个字" (four characters) but 5 Chinese characters inside the quotes: hard failure
    tmp, path = write_chapter(CLEAN_TEXT + "\n“我不干了啊”这四个字，他说得很轻。")
    code, out = run_tool([str(path)])
    check("word-count claim mismatch hard fail", code == 1, out)
    check("word-count claim flagged", "word-count claim mismatch" in out, out)
    sys.stdout.write("ok test_wordcount_mismatch_hard\n")


def test_wordcount_manual_warning():
    # "X个字" with no quote to check against: warning only
    tmp, path = write_chapter(CLEAN_TEXT + "\n回信就三个字，看得他手心冒汗。")
    code, out = run_tool([str(path)])
    check("word-count claim for manual check only warns", code == 0, out)
    check("word-count claim for manual check flagged", "word-count claim" in out, out)
    sys.stdout.write("ok test_wordcount_manual_warning\n")


def test_qa_density_warning():
    line = "他问她吃了没。她说吃了。他又问去了哪里。她说你别管。他还想问，她把电话挂了。"
    tmp, path = write_chapter(CLEAN_TEXT + "\n" + line)
    code, out = run_tool([str(path)])
    check("multi-turn Q&A in one paragraph only warns", code == 0, out)
    check("multi-turn Q&A flagged", "multi-turn Q&A" in out, out)
    sys.stdout.write("ok test_qa_density_warning\n")


def test_adverb_density_warning():
    line = "他缓缓起身。她微微点头。他轻轻把门带上。她淡淡应了一声。"
    tmp, path = write_chapter(CLEAN_TEXT + "\n" + line)
    code, out = run_tool([str(path)])
    check("weak-adverb density only warns", code == 0, out)
    check("weak adverb flagged", "weak-adverb" in out, out)
    sys.stdout.write("ok test_adverb_density_warning\n")


def test_trailing_tag_warning():
    tmp, path = write_chapter(CLEAN_TEXT + "\n“先这样吧。”我说。")
    code, out = run_tool([str(path)])
    check("trailing tag only warns", code == 0, out)
    check("trailing tag flagged", "trailing tag" in out, out)
    sys.stdout.write("ok test_trailing_tag_warning\n")


def test_regression_hit_hard():
    tmp, path = write_chapter(CLEAN_TEXT + "\n他把手机反扣在桌面上，盯着那行字。")
    sandbox = tmp / "sandbox"
    sandbox.mkdir()
    (sandbox / "prose-regressions.txt").write_text(
        "把手机反扣在桌面上，盯着那行字\n", encoding="utf-8"
    )
    code, out = run_tool([str(path)])
    check("regression string hit hard-fails", code == 1, out)
    check("regression string flagged", "regression library" in out, out)
    sys.stdout.write("ok test_regression_hit_hard\n")


def test_regression_comment_ignored():
    # # comment lines do not participate in matching (template explanation lines stay inert)
    tmp, path = write_chapter(CLEAN_LONG_TEXT)
    sandbox = tmp / "sandbox"
    sandbox.mkdir()
    (sandbox / "prose-regressions.txt").write_text(
        "# 这是注释说明，不参与匹配\n", encoding="utf-8"
    )
    code, out = run_tool([str(path)])
    check("regression library comment lines do not match", code == 0, out)
    sys.stdout.write("ok test_regression_comment_ignored\n")


def test_regression_missing_ok():
    # No sandbox files: run the remaining checks normally
    tmp, path = write_chapter(CLEAN_LONG_TEXT)
    code, out = run_tool([str(path)])
    check("passes normally without a regression library", code == 0, out)
    sys.stdout.write("ok test_regression_missing_ok\n")


def test_whitelist_skip():
    line = "“先这样吧。”我说。"
    tmp, path = write_chapter(CLEAN_TEXT + "\n" + line)
    sandbox = tmp / "sandbox"
    sandbox.mkdir()
    (sandbox / "locked-lines.txt").write_text(line + "\n", encoding="utf-8")
    code, out = run_tool([str(path)])
    check("passes after the whitelist line is skipped", code == 0, out)
    check("whitelist noted", "whitelist" in out, out)
    sys.stdout.write("ok test_whitelist_skip\n")


def test_crlf_input():
    tmp, path = write_chapter(CLEAN_LONG_TEXT.replace("\n", "\r\n"))
    code, out = run_tool([str(path)])
    check("CRLF input passes normally", code == 0, out)
    sys.stdout.write("ok test_crlf_input\n")


def test_missing_file_exit2():
    code, out = run_tool(["/nonexistent/no-such-file.md"])
    check("missing file exits 2", code == 2, out)
    sys.stdout.write("ok test_missing_file_exit2\n")


def test_dir_input():
    tmp, path = write_chapter(CLEAN_TEXT + "\n“对数据。”他说，“下不为例。”")
    code, out = run_tool([str(tmp / "正文")])
    check("directory input scans md and hard-fails", code == 1, out)
    sys.stdout.write("ok test_dir_input\n")


def main() -> int:
    if not TOOL.exists():
        print(f"FAIL: {TOOL.name} does not exist (implement the tool before running the tests)")
        return 1
    for fn in [v for k, v in sorted(globals().items()) if k.startswith("test_")]:
        fn()
    summary()
    return exit_code()


if __name__ == "__main__":
    sys.exit(main())
