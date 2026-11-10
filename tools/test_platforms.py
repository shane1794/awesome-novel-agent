#!/usr/bin/env python3
"""Platform adapter layer verification script.

Usage: python tools/test_platforms.py
Exit code 0 = all passed; non-zero = failures (used by CI).

Coverage:
- Unit: the platforms module (config / detection / reference rewriting / yaml pre-check)
- Unit: check-python.py version threshold (fail-fast at install time)
- E2E: init.py layouts on all platforms + reference rewriting + reasonix 11 skills + codex TOML agents (including tomllib parsing)
- E2E: sync-project.py sync on all platforms + --check
- E2E: install.sh first install into a fresh HOME (F1 regression) + version-threshold fail-fast (P-ver regression) + pyyaml install-threshold fail-fast (Y-ver regression) + missing-pyyaml negative case (F5 regression)
"""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

# Force UTF-8 output to avoid errors on the Windows GBK console (AGENTS.md:79)
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

try:
    import tomllib
except ImportError:  # Python < 3.11
    tomllib = None
TOOLS = Path(__file__).resolve().parent
sys.path.insert(0, str(TOOLS))

from test_util import check
import test_util as _tu


def run(cmd, cwd=None, env=None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, encoding="utf-8", env=env)


def init_project(tmp: Path, platform_key: str, genre: str = "1"):
    return run([sys.executable, str(TOOLS / "init.py"), str(tmp),
                "--genre", genre, "--platform", platform_key])


def init_short_project(tmp: Path, platform_key: str = "claude", genre: str = "1"):
    return run([sys.executable, str(TOOLS / "init.py"), str(tmp),
                "--length", "short", "--genre", genre, "--platform", platform_key])


# ---------------- Unit ----------------

def test_detect():
    print("[unit] detect_platform")
    import platforms as p
    check("override=reasonix", p.detect_platform(Path("d:/x"), "reasonix").key == "reasonix")
    check("override=opencode", p.detect_platform(Path("d:/x"), "opencode").key == "opencode")
    check("override=claude", p.detect_platform(Path("d:/x"), "claude").key == "claude")
    check("override=zcode", p.detect_platform(Path("d:/x"), "zcode").key == "zcode")
    check("override=dsh", p.detect_platform(Path("d:/x"), "dsh").key == "dsh")
    check("override=grok", p.detect_platform(Path("d:/x"), "grok").key == "grok")
    check("path reasonix",
          p.detect_platform(Path("d:/proj/.reasonix/skills/awesome-novel")).key == "reasonix")
    check("path opencode",
          p.detect_platform(Path("d:/proj/.config/opencode/skills/awesome-novel")).key == "opencode")
    check("path zcode",
          p.detect_platform(Path("d:/proj/.zcode/skills/awesome-novel")).key == "zcode")
    check("path dsh",
          p.detect_platform(Path("d:/proj/.dsh/skills/awesome-novel")).key == "dsh")
    check("path grok",
          p.detect_platform(Path("d:/proj/.grok/skills/awesome-novel")).key == "grok")
    check("default claude",
          p.detect_platform(Path("d:/code/awesome-novel-agent")).key == "claude")


def test_rewrite():
    print("[unit] rewrite_refs")
    import platforms as p
    text = "First read `.claude/knowledge/anti-ai.md` and `.claude/memory/volume-memory.md`"
    out = p.rewrite_refs(text, p.PLATFORMS["reasonix"])
    check("reasonix rewrites two places",
          out == "First read `.reasonix/knowledge/anti-ai.md` and `.reasonix/memory/volume-memory.md`",
          out)
    check("claude unchanged", p.rewrite_refs(text, p.PLATFORMS["claude"]) == text)
    out = p.rewrite_refs(text, p.PLATFORMS["codex"])
    check("codex rewrites two places",
          out == "First read `.codex/knowledge/anti-ai.md` and `.codex/memory/volume-memory.md`",
          out)
    out = p.rewrite_refs(text, p.PLATFORMS["zcode"])
    check("zcode rewrites two places",
          out == "First read `.zcode/knowledge/anti-ai.md` and `.zcode/memory/volume-memory.md`",
          out)
    out = p.rewrite_refs(text, p.PLATFORMS["dsh"])
    check("dsh rewrites two places",
          out == "First read `.dsh/knowledge/anti-ai.md` and `.dsh/memory/volume-memory.md`",
          out)
    out = p.rewrite_refs(text, p.PLATFORMS["grok"])
    check("grok rewrites two places",
          out == "First read `.grok/knowledge/anti-ai.md` and `.grok/memory/volume-memory.md`",
          out)


def test_config():
    print("[unit] platform config")
    import platforms as p
    check("claude agents path",
          p.PLATFORMS["claude"].agents_dir(Path("P")) == Path("P") / ".claude" / "agents")
    check("reasonix agents=None", p.PLATFORMS["reasonix"].agents_dir(Path("P")) is None)
    check("reasonix skills path",
          p.PLATFORMS["reasonix"].skills_dir(Path("P")) == Path("P") / ".reasonix" / "skills")
    check("codex agents path",
          p.PLATFORMS["codex"].agents_dir(Path("P")) == Path("P") / ".codex" / "agents")
    check("codex skills path",
          p.PLATFORMS["codex"].skills_dir(Path("P")) == Path("P") / ".codex" / "skills")
    check("zcode agents=None", p.PLATFORMS["zcode"].agents_dir(Path("P")) is None)
    check("zcode skills path",
          p.PLATFORMS["zcode"].skills_dir(Path("P")) == Path("P") / ".zcode" / "skills")
    check("dsh agents=None", p.PLATFORMS["dsh"].agents_dir(Path("P")) is None)
    check("dsh skills path",
          p.PLATFORMS["dsh"].skills_dir(Path("P")) == Path("P") / ".dsh" / "skills")
    check("grok agents path",
          p.PLATFORMS["grok"].agents_dir(Path("P")) == Path("P") / ".grok" / "agents")
    check("grok skills path",
          p.PLATFORMS["grok"].skills_dir(Path("P")) == Path("P") / ".grok" / "skills")
    check("unknown key raises", _raises(p.platform_from_key, "bad-key"))
    check("detection prefers the explicit override", p.detect_platform(Path("d:/x/.reasonix/skills"), "claude").key == "claude")
    check("detect codex path",
          p.detect_platform(Path("d:/x/.codex/skills/awesome-novel")).key == "codex")
    check("detect zcode path",
          p.detect_platform(Path("d:/x/.zcode/skills/awesome-novel")).key == "zcode")
    check("detect dsh path",
          p.detect_platform(Path("d:/x/.dsh/skills/awesome-novel")).key == "dsh")
    check("detect grok path",
          p.detect_platform(Path("d:/x/.grok/skills/awesome-novel")).key == "grok")
    check("a claude path containing the codex substring falls back to claude",
          p.detect_platform(Path("/Users/codex-dev/.claude/skills/awesome-novel")).key == "claude")
    check("a claude path containing the grok substring falls back to claude",
          p.detect_platform(Path("/Users/grok-dev/.claude/skills/awesome-novel")).key == "claude")


def test_yaml_precheck():
    print("[unit] ensure_yaml")
    import platforms as p
    p.ensure_yaml(p.PLATFORMS["claude"])  # claude copies without converting and does not need pyyaml
    import builtins
    real_import = builtins.__import__

    def fake_import(name, *args, **kwargs):
        if name == "yaml":
            raise ImportError("simulate missing pyyaml")
        return real_import(name, *args, **kwargs)

    builtins.__import__ = fake_import
    try:
        check("codex errors without yaml", _raises_system_exit(p.ensure_yaml, p.PLATFORMS["codex"]))
        check("opencode errors without yaml",
              _raises_system_exit(p.ensure_yaml, p.PLATFORMS["opencode"]))
        check("reasonix errors without yaml",
              _raises_system_exit(p.ensure_yaml, p.PLATFORMS["reasonix"]))
        check("zcode errors without yaml",
              _raises_system_exit(p.ensure_yaml, p.PLATFORMS["zcode"]))
        check("grok errors without yaml",
              _raises_system_exit(p.ensure_yaml, p.PLATFORMS["grok"]))
    finally:
        builtins.__import__ = real_import


def test_check_python():
    """P-ver regression: check-python.py surfaces version problems at install time instead of only reporting a SyntaxError at run time."""
    print("[unit] check-python.py version threshold")
    r = run([sys.executable, str(TOOLS / "check-python.py")])
    check("the current interpreter passes", r.returncode == 0, (r.stdout + r.stderr)[-200:])
    r = run([sys.executable, str(TOOLS / "check-python.py"), "--min", "99.0"])
    check("an impossibly high threshold refuses", r.returncode == 1, str(r.returncode))
    check("the refusal message contains the version number and an upgrade hint",
          "Python 99.0" in (r.stdout + r.stderr) and "upgrade" in (r.stdout + r.stderr),
          (r.stdout + r.stderr)[-300:])


def test_check_yaml():
    """Y-ver regression: check-yaml.py surfaces missing pyyaml at install time instead of only erroring at init."""
    print("[unit] check-yaml.py pyyaml threshold")
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "yaml.py").write_text('raise ImportError("blocked")\n', encoding="utf-8")
        env = dict(os.environ)
        env["PYTHONPATH"] = str(td) + os.pathsep + env.get("PYTHONPATH", "")
        r = run([sys.executable, str(TOOLS / "check-yaml.py"), "codex"], env=env)
        check("missing yaml exit 1", r.returncode == 1, str(r.returncode))
        check("the missing-yaml error mentions pyyaml and pip",
              "needs pyyaml" in (r.stdout + r.stderr)
              and "pip install pyyaml" in (r.stdout + r.stderr),
              (r.stdout + r.stderr)[-300:])
        check("the missing-yaml error contains the interpreter path", sys.executable in (r.stdout + r.stderr),
              (r.stdout + r.stderr)[-300:])
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "yaml.py").write_text("# stub\n", encoding="utf-8")
        env = dict(os.environ)
        env["PYTHONPATH"] = str(td) + os.pathsep + env.get("PYTHONPATH", "")
        r = run([sys.executable, str(TOOLS / "check-yaml.py"), "opencode"], env=env)
        check("yaml present exit 0", r.returncode == 0, (r.stdout + r.stderr)[-200:])


def _fake_version_repo(tmp: Path, version: str, drift: dict) -> None:
    """Mini repo: VERSION is authoritative + four copies (check-version.py tests inject NOVEL_REPO_ROOT).

    drift: {relative path: drifted version number}, building a single-inconsistency scenario.
    """
    (tmp / "VERSION").write_text(f"v{version}\n", encoding="utf-8")
    (tmp / "ARCHITECTURE.md").write_text(f"# x\n\n> Current version: v{version}\n", encoding="utf-8")
    (tmp / "skill.json").write_text(f'{{"version": "{version}"}}\n', encoding="utf-8")
    tpl = tmp / "templates" / ".agent"
    tpl.mkdir(parents=True)
    (tpl / "status.md").write_text(f"- **skill_version:** {version}\n", encoding="utf-8")
    tools = tmp / "tools"
    tools.mkdir(parents=True)
    (tools / "init.py").write_text(f'status = """- **skill_version:** {version}"""\n',
                                   encoding="utf-8")
    for name, ver in drift.items():
        if name == "ARCHITECTURE.md":
            (tmp / name).write_text(f"# x\n\n> Current version: v{ver}\n", encoding="utf-8")
        elif name == "skill.json":
            (tmp / name).write_text(f'{{"version": "{ver}"}}\n', encoding="utf-8")
        elif name == "templates/.agent/status.md":
            (tmp / name).write_text(f"- **skill_version:** {ver}\n", encoding="utf-8")
        elif name == "tools/init.py":
            (tmp / name).write_text(f'status = """- **skill_version:** {ver}"""\n',
                                    encoding="utf-8")


def test_check_version():
    """Self-test for the version-consistency guard (arch-review tech debt: the check scripts lack test coverage)."""
    print("[unit] check-version.py consistency")
    with tempfile.TemporaryDirectory() as td:
        _fake_version_repo(Path(td), "4.16.0", {})
        env = dict(os.environ, NOVEL_REPO_ROOT=td)
        r = run([sys.executable, str(TOOLS / "check-version.py")], env=env)
        check("all five consistent exit 0", r.returncode == 0, (r.stdout + r.stderr)[-200:])
        check("the output contains the pass message", "Version numbers match" in r.stdout, r.stdout[-200:])
    for name, ver, expect in [
        ("ARCHITECTURE.md", "4.13.0", "ARCHITECTURE.md"),
        ("skill.json", "1.0.0", "skill.json"),
        ("templates/.agent/status.md", "4.13.0", "templates/.agent/status.md"),
        ("tools/init.py", "4.13.0", "tools/init.py"),
    ]:
        with tempfile.TemporaryDirectory() as td:
            _fake_version_repo(Path(td), "4.16.0", {name: ver})
            env = dict(os.environ, NOVEL_REPO_ROOT=td)
            r = run([sys.executable, str(TOOLS / "check-version.py")], env=env)
            check(f"drift {name} exit 1", r.returncode == 1, str(r.returncode))
            check(f"drift {name} error contains the label", expect in (r.stdout + r.stderr),
                  (r.stdout + r.stderr)[-200:])
    with tempfile.TemporaryDirectory() as td:
        (Path(td) / "VERSION").write_text("abc\n", encoding="utf-8")
        env = dict(os.environ, NOVEL_REPO_ROOT=td)
        r = run([sys.executable, str(TOOLS / "check-version.py")], env=env)
        check("invalid VERSION format exit 1", r.returncode == 1, str(r.returncode))


def _raises(fn, *a) -> bool:
    try:
        fn(*a)
        return False
    except ValueError:
        return True


def _raises_system_exit(fn, *a) -> bool:
    try:
        fn(*a)
        return False
    except SystemExit:
        return True


# ---------------- E2E init ----------------

def test_init_layout():
    print("[e2e] init.py layouts on all platforms")
    expect_map = {
        "claude":   (["agents", "knowledge", "memory"], [".reasonix"]),
        "opencode": (["agents", "knowledge", "memory"], [".claude", ".reasonix"]),
        "reasonix": (["skills", "knowledge", "memory"], [".claude"]),
        "codex":    (["agents", "knowledge", "memory"], [".claude", ".opencode", ".reasonix"]),
        "zcode":    (["skills", "knowledge", "memory"], [".claude", ".opencode", ".reasonix"]),
        "grok":     (["agents", "knowledge", "memory"], [".claude", ".opencode", ".reasonix"]),
    }
    for key, (subs, absents) in expect_map.items():
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            r = init_project(tmp, key)
            check(f"{key} init exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
            for sub in subs:
                check(f"{key} has .{key}/{sub}", (tmp / f".{key}" / sub).exists())
            check(f"{key} has novel-samples/ (distillation sample directory)", (tmp / "novel-samples").exists())
            t = tmp / f".{key}" / "tools" / "check-prose.py"
            check(f"{key} deploys tools/check-prose.py", t.exists())
            if t.exists():
                check(f"{key} check-prose.py content matches the source",
                      t.read_text(encoding="utf-8") ==
                      (TOOLS / "check-prose.py").read_text(encoding="utf-8"))
            t2 = tmp / f".{key}" / "tools" / "check-chapter.py"
            check(f"{key} deploys tools/check-chapter.py", t2.exists())
            if t2.exists():
                check(f"{key} check-chapter.py content matches the source",
                      t2.read_text(encoding="utf-8") ==
                      (TOOLS / "check-chapter.py").read_text(encoding="utf-8"))
            aa = tmp / f".{key}" / "knowledge" / "anti-ai.md"
            check(f"{key} anti-ai.md merges the structural-heat law",
                  aa.exists() and "Structural Heat: Avoiding AI Detection at the Source" in aa.read_text(encoding="utf-8"))
            for sb in ("detect-battles.md", "prose-regressions.txt", "locked-lines.txt"):
                check(f"{key} generates sandbox/{sb}", (tmp / "sandbox" / sb).exists())
            for a in absents:
                check(f"{key} has no {a}", not (tmp / a).exists())

    # reasonix 11 skills
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "reasonix")
        names = ["novel-agent", "writer", "volume-planner", "chapter-planner",
                 "prompt-crafter", "anti-ai", "reader", "updater", "style-distiller",
                 "memory-recording", "roleplay-sandbox"]  # matches the 11 skill names of deploy_reasonix_skills (spec contract)
        for n in names:
            check(f"reasonix skill {n}", (tmp / ".reasonix/skills" / n / "SKILL.md").exists())
        w = (tmp / ".reasonix/skills/writer/SKILL.md").read_text(encoding="utf-8")
        check("reasonix writer reference rewriting",
              ".reasonix/knowledge/" in w and ".claude/knowledge/" not in w)
        nv = (tmp / ".reasonix/skills/novel-agent/SKILL.md").read_text(encoding="utf-8")
        check("reasonix novel-agent has no .claude residue", ".claude" not in nv)

    # reasonix AGENTS.md template rewriting
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "reasonix")
        ag = (tmp / "AGENTS.md").read_text(encoding="utf-8")
        check("reasonix AGENTS.md has no .opencode/agents",
              ".opencode/" not in ag and ".reasonix/skills/" in ag, ag[:200])
        cl = (tmp / "CLAUDE.md").read_text(encoding="utf-8")
        check("reasonix CLAUDE.md has no .claude/agents",
              ".claude/agents" not in cl and ".reasonix/skills/" in cl, cl[:200])

    # zcode 11 skills (isomorphic to reasonix: agents are skills)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "zcode")
        names = ["novel-agent", "writer", "volume-planner", "chapter-planner",
                 "prompt-crafter", "anti-ai", "reader", "updater", "style-distiller",
                 "memory-recording", "roleplay-sandbox"]  # matches the 11 skill names of deploy_zcode_skills (spec contract)
        for n in names:
            check(f"zcode skill {n}", (tmp / ".zcode/skills" / n / "SKILL.md").exists())
        w = (tmp / ".zcode/skills/writer/SKILL.md").read_text(encoding="utf-8")
        check("zcode writer frontmatter",
              "name: writer" in w and "allowed-tools: Read, Write" in w
              and "Agent" not in w.split("---", 2)[1], w.split("---", 2)[1][:200])
        check("zcode writer reference rewriting",
              ".zcode/knowledge/" in w and ".claude/knowledge/" not in w)
        nv = (tmp / ".zcode/skills/novel-agent/SKILL.md").read_text(encoding="utf-8")
        check("zcode novel-agent dispatch adapter",
              "Agent" in nv and ".zcode/skills/" in nv and "ZCode dispatch adapter" in nv)
        check("zcode novel-agent has no .claude residue", ".claude" not in nv)
        all_skills = "".join(
            f.read_text(encoding="utf-8") for f in sorted(
                (tmp / ".zcode/skills").rglob("SKILL.md"))
        )
        check("no .claude residue in all zcode skills", ".claude" not in all_skills)

    # zcode AGENTS.md / CLAUDE.md template rewriting
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "zcode")
        ag = (tmp / "AGENTS.md").read_text(encoding="utf-8")
        check("zcode AGENTS.md points to .zcode/skills",
              ".opencode/agents" not in ag and ".zcode/skills/" in ag, ag[:200])
        cl = (tmp / "CLAUDE.md").read_text(encoding="utf-8")
        check("zcode CLAUDE.md has no .claude/agents",
              ".claude/agents" not in cl and ".zcode/skills/" in cl, cl[:200])

    # claude agent count
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "claude")
        n = len(list((tmp / ".claude/agents").glob("*.md")))
        check("claude agent count=9", n == 9, f"actual {n}")  # agents/ has 9 source .md files (spec contract)

    # opencode agent reference rewriting
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "opencode")
        w = (tmp / ".opencode/agents/writer.md").read_text(encoding="utf-8")
        check("opencode writer reference rewriting",
              ".opencode/knowledge/" in w and ".claude/knowledge/" not in w)

    # codex TOML agent + skill + templates
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "codex")
        n = len(list((tmp / ".codex/agents").glob("*.toml")))
        check("codex agent count=9", n == 9, f"actual {n}")
        w = (tmp / ".codex/agents/writer.toml").read_text(encoding="utf-8")
        check("codex writer TOML fields",
              'name = "writer"' in w and "description" in w
              and "developer_instructions" in w, w[:200])
        check("codex writer reference rewriting",
              ".codex/knowledge/" in w and ".claude/knowledge/" not in w)
        all_toml = "".join(
            f.read_text(encoding="utf-8") for f in sorted((tmp / ".codex/agents").glob("*.toml"))
        )
        check("no .claude residue in all codex TOML", ".claude" not in all_toml)
        nv = (tmp / ".codex/agents/novel-agent.toml").read_text(encoding="utf-8")
        check("codex novel-agent dispatch adapter",
              "spawn_agent" in nv and ".codex/agents/" in nv)
        sub_toml = "".join(
            f.read_text(encoding="utf-8")
            for f in sorted((tmp / ".codex/agents").glob("*.toml"))
            if f.name != "novel-agent.toml"
        )
        check("codex subagent gets the dispatch hard constraint injected",
              "Dispatch-permission hard constraint" in sub_toml and "spawn_agent" in sub_toml
              and "Never use" in sub_toml,
              "the subagent TOML is missing the no-spawning instruction")
        check("codex novel-agent gets no ban injected",
              "Dispatch-permission hard constraint" not in nv, "novel-agent is the only dispatcher; the ban must not be injected")
        vp = (tmp / ".codex/agents/volume-planner.toml").read_text(encoding="utf-8")
        check("codex volume-planner source OOS contains a no-dispatch statement",
              "Do not dispatch other agents" in vp, "the volume-planner source file is missing its no-dispatch statement")
        check("codex skill roleplay-sandbox",
              (tmp / ".codex/skills/roleplay-sandbox/SKILL.md").exists())
        check("codex skill memory-recording",
              (tmp / ".codex/skills/memory-recording/SKILL.md").exists())
        ag = (tmp / "AGENTS.md").read_text(encoding="utf-8")
        check("codex AGENTS.md points to .codex/agents", ".codex/agents/" in ag, ag[:200])
        check("codex AGENTS.md only-dispatcher rule", "Single dispatcher" in ag, ag[:400])
        check("codex has no CLAUDE.md", not (tmp / "CLAUDE.md").exists())
        check("codex has no AGENTS.codex.md template copy",
              not (tmp / "AGENTS.codex.md").exists())
        if tomllib is not None:
            parse_ok = True
            for f in sorted((tmp / ".codex/agents").glob("*.toml")):
                try:
                    tomllib.loads(f.read_text(encoding="utf-8"))
                except Exception as e:
                    parse_ok = False
                    detail = f"{f.name}: {e}"
                    break
            check("codex TOML parses with tomllib", parse_ok, detail if not parse_ok else "")

    # dsh skill deployment (11 SKILL.md files; frontmatter has only name/description)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "dsh")
        names = ["novel-agent", "writer", "volume-planner", "chapter-planner",
                 "prompt-crafter", "anti-ai", "reader", "updater", "style-distiller",
                 "memory-recording", "roleplay-sandbox"]  # matches the 11 skill names of deploy_dsh_skills (spec contract)
        for n in names:
            check(f"dsh skill {n}", (tmp / ".dsh/skills" / n / "SKILL.md").exists())
        check("dsh deploys tools/check-prose.py",
              (tmp / ".dsh/tools/check-prose.py").exists())
        w = (tmp / ".dsh/skills/writer/SKILL.md").read_text(encoding="utf-8")
        fm = w.split("---", 2)[1]
        check("dsh writer frontmatter has only name/description",
              "name: writer" in fm and "description:" in fm
              and "allowed-tools" not in fm and "tools:" not in fm
              and "runAs" not in fm, fm[:200])
        check("dsh writer reference rewriting",
              ".dsh/knowledge/" in w and ".claude/knowledge/" not in w)
        nv = (tmp / ".dsh/skills/novel-agent/SKILL.md").read_text(encoding="utf-8")
        check("dsh novel-agent dispatch adapter",
              "subagent" in nv and ".dsh/skills/" in nv and "DeepSeek Harness dispatch adapter" in nv)
        check("dsh novel-agent has no .claude residue", ".claude" not in nv)
        all_skills = "".join(
            f.read_text(encoding="utf-8") for f in sorted(
                (tmp / ".dsh/skills").rglob("SKILL.md"))
        )
        check("no .claude residue in all dsh skills", ".claude" not in all_skills)

    # dsh AGENTS.md / CLAUDE.md template rewriting
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "dsh")
        ag = (tmp / "AGENTS.md").read_text(encoding="utf-8")
        check("dsh AGENTS.md points to .dsh/skills",
              ".opencode/agents" not in ag and ".dsh/skills/" in ag, ag[:200])
        cl = (tmp / "CLAUDE.md").read_text(encoding="utf-8")
        check("dsh CLAUDE.md has no .claude/agents",
              ".claude/agents" not in cl and ".dsh/skills/" in cl, cl[:200])

    # grok agent Markdown + skill + templates
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "grok")
        n = len(list((tmp / ".grok/agents").glob("*.md")))
        check("grok agent count=9", n == 9, f"actual {n}")
        w = (tmp / ".grok/agents/writer.md").read_text(encoding="utf-8")
        fm = w.split("---", 2)[1]
        fm_data = yaml.safe_load(fm)
        check("grok writer frontmatter",
              "name: writer" in fm and "description:" in fm
              and "read_file" in fm and "write" in fm, fm[:400])
        check("grok subagent is banned and not authorized for Agent",
              "Agent" not in fm_data.get("tools", [])
              and fm_data.get("disallowedTools") == ["Agent"], fm[:400])
        check("grok subagent frontmatter does not use the model call name",
              "spawn_subagent" not in fm_data.get("tools", [])
              and "spawn_subagent" not in fm_data.get("disallowedTools", []), fm[:400])
        check("grok writer reference rewriting",
              ".grok/knowledge/" in w and ".claude/knowledge/" not in w)
        check("grok writer SOP inlined", "Execution SOP: writing-execution.md" in w)
        check("grok subagent gets the dispatch hard constraint injected",
              "Dispatch-permission hard constraint" in w and "spawn_subagent" in w)
        nv = (tmp / ".grok/agents/novel-agent.md").read_text(encoding="utf-8")
        nfm = nv.split("---", 2)[1]
        nfm_data = yaml.safe_load(nfm)
        check("grok novel-agent dispatch adapter",
              "spawn_subagent" in nv and ".grok/agents/" in nv
              and "Grok Build dispatch adapter" in nv)
        check("grok novel-agent frontmatter enables the Agent instruction",
              "Agent" in nfm_data.get("tools", [])
              and "spawn_subagent" not in nfm_data.get("tools", [])
              and "disallowedTools" not in nfm_data, nfm[:300])
        check("grok novel-agent gets no ban injected",
              "Dispatch-permission hard constraint" not in nv, "novel-agent is the only dispatcher; the ban must not be injected")
        all_md = "".join(
            f.read_text(encoding="utf-8") for f in sorted((tmp / ".grok/agents").glob("*.md"))
        )
        check("no .claude residue in all grok agents", ".claude" not in all_md)
        aa = (tmp / ".grok/agents/anti-ai.md").read_text(encoding="utf-8")
        aafm = aa.split("---", 2)[1]
        check("grok anti-ai keeps the shell",
              "run_terminal_command" in aafm, aafm[:300])
        check("grok skill roleplay-sandbox",
              (tmp / ".grok/skills/roleplay-sandbox/SKILL.md").exists())
        check("grok skill memory-recording",
              (tmp / ".grok/skills/memory-recording/SKILL.md").exists())
        ag = (tmp / "AGENTS.md").read_text(encoding="utf-8")
        check("grok AGENTS.md points to .grok/agents", ".grok/agents/" in ag, ag[:200])
        cl = (tmp / "CLAUDE.md").read_text(encoding="utf-8")
        check("grok CLAUDE.md has no .claude/agents",
              ".claude/agents" not in cl and ".grok/agents/" in cl, cl[:200])
        check("grok deploys tools/check-prose.py",
              (tmp / ".grok/tools/check-prose.py").exists())


# ---------------- E2E sync ----------------

def test_short_init_layout():
    """Short-form E2E: the product shapes of --length short on all 7 platforms, and long/short mutual exclusion.

    Product shapes in three platform classes:
    - agents-directory type (claude/opencode/grok): .platform/agents/*.md, 6 files (5 short-form + reader);
      the platform skills directory also deploys 2 standalone tools (short-scan / short-analyze)
    - codex TOML: .codex/agents/*.toml, 6 files
    - inline skill (reasonix/zcode/dsh): .platform/skills/<name>/SKILL.md, 6 files (no standalone tools)
    Knowledge products (short-anti-ai.md + short-craft/ + short-genres/) are isomorphic across platforms.
    """
    print("[e2e] init.py --length short layouts (all platforms)")
    short_names = {"short-agent", "short-planner", "short-writer", "short-editor",
                   "short-verifier", "reader"}
    long_only = {"novel-agent", "volume-planner", "chapter-planner", "prompt-crafter",
                 "updater", "anti-ai", "style-distiller", "writer"}
    for key in ("claude", "opencode", "reasonix", "codex", "zcode", "dsh", "grok"):
        with tempfile.TemporaryDirectory() as td:
            tmp = Path(td)
            r = init_short_project(tmp, key)
            check(f"short {key} init exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
            # Skeleton: short-form-only directories and markers (isomorphic across platforms)
            check(f"short {key} has stories/", (tmp / "stories").exists())
            check(f"short {key} story.md contains the length marker",
                  "**length:** short" in (tmp / "story.md").read_text(encoding="utf-8"))
            check(f"short {key} state machine contains phase=setup",
                  "**phase:** setup" in (tmp / ".agent/status.md").read_text(encoding="utf-8"))
            for d in ("volumes", "chapters", "prompts", "archives", "novel-samples"):
                check(f"short {key} produces no {d}/", not (tmp / d).exists())
            # Agent-set products (in the three platform shapes)
            root = tmp / f".{key}"
            if key in ("claude", "opencode", "grok"):
                names = {p.stem for p in (root / "agents").glob("*.md")}
            elif key == "codex":
                names = {p.stem for p in (root / "agents").glob("*.toml")}
            else:  # reasonix / zcode / dsh: inline skill directory
                skills = root / "skills"
                names = {p.name for p in skills.iterdir() if (p / "SKILL.md").exists()} \
                    if skills.exists() else set()
                check(f"short {key} inline skill count=8 (6 agents + 2 standalone tools)",
                      len(names) == 8, f"actual {sorted(names)}")
            for a in short_names:
                check(f"short {key} deploys {a}", a in names)
            for a in long_only:
                check(f"short {key} does not deploy {a}", a not in names)
            # Knowledge products (isomorphic across platforms)
            know = root / "knowledge"
            check(f"short {key} deploys short-anti-ai.md", (know / "short-anti-ai.md").exists())
            check(f"short {key} does not merge the long-form anti-ai.md", not (know / "anti-ai.md").exists())
            check(f"short {key} deploys short-genres/zhuiqi.md",
                  (know / "short-genres" / "zhuiqi.md").exists())
            sdir = root / "skills"
            check(f"short {key} deploys standalone tool short-scan",
                  (sdir / "short-scan" / "SKILL.md").exists())
            check(f"short {key} deploys standalone tool short-analyze",
                  (sdir / "short-analyze" / "SKILL.md").exists())
            check(f"short {key} short-craft references fully deployed (13)",
                  len(list((know / "short-craft").glob("*.md"))) == 13)
            check(f"short {key} deploys 10 genre style packs",
                  len(list((know / "short-genres").glob("*.md"))) == 11)  # index + 10
            check(f"short {key} seeds cross-story preference memory",
                  (root / "memory" / "author-feedback.md").exists())

    # Dispatch-adapter spot check: the inline-platform short-agent contains the short-form subagent list and the dispatcher's own name
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_short_project(tmp, "zcode")
        skill = tmp / ".zcode" / "skills" / "short-agent" / "SKILL.md"
        text = skill.read_text(encoding="utf-8")
        check("short zcode dispatch section contains short-planner", "short-planner" in text)
        check("short zcode dispatch section constrains with short-agent's own name", "never dispatch short-agent itself as a subagent" in text)
        check("short zcode SOP inlines short-dispatch", "Execution SOP: short-dispatch.md" in text)

    # codex TOML spot check: short-agent dispatch section + TOML parses
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_short_project(tmp, "codex")
        toml_text = (tmp / ".codex" / "agents" / "short-agent.toml").read_text(encoding="utf-8")
        check("short codex dispatch section contains the short subagent list", "short-planner" in toml_text)
        check("short codex AGENTS.md is the short-form version",
              "Short Story Project" in (tmp / "AGENTS.md").read_text(encoding="utf-8")
              and "@short-agent" in (tmp / "AGENTS.md").read_text(encoding="utf-8"))

    # Number out of range: the short-form registry valid range is 1-10
    with tempfile.TemporaryDirectory() as td:
        r = run([sys.executable, str(TOOLS / "init.py"), str(Path(td)),
                 "--length", "short", "--genre", "25", "--platform", "claude"])
        check("short number out of range exit 1", r.returncode == 1, (r.stdout + r.stderr)[-200:])

    # Genre pool: registry 1-10 all initializable (genre 2 used to be a to-be-added genre)
    with tempfile.TemporaryDirectory() as td:
        r = run([sys.executable, str(TOOLS / "init.py"), str(Path(td)),
                 "--length", "short", "--genre", "2", "--platform", "claude"])
        check("short genre 2 (shiqing) exit 0", r.returncode == 0, (r.stdout + r.stderr)[-200:])
        check("short genre 2 deploys the shiqing style pack",
              (Path(td) / ".claude/knowledge/short-genres/shiqing.md").exists())

    # Invalid length value
    with tempfile.TemporaryDirectory() as td:
        r = run([sys.executable, str(TOOLS / "init.py"), str(Path(td)),
                 "--length", "medium", "--platform", "claude"])
        check("invalid --length exit 1", r.returncode == 1, (r.stdout + r.stderr)[-200:])
        check("invalid --length creates no directory", not (Path(td) / "proj").exists() and list(Path(td).iterdir()) == [])

    # Short-form sync: standalone tools redeploy idempotently + deleted ones are restored + long-form projects have no short-form standalone tools
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_short_project(tmp, "claude")
        r1 = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                  "--platform", "claude"], cwd=str(tmp))
        check("short claude sync exit 0 (with standalone-tool redeploy)", r1.returncode == 0,
              (r1.stdout + r1.stderr)[-400:])
        scan = tmp / ".claude" / "skills" / "short-scan" / "SKILL.md"
        check("standalone tools exist after short sync", scan.exists())
        scan.unlink()
        r2 = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                  "--platform", "claude"], cwd=str(tmp))
        check("short sync restores a deleted standalone tool", r2.returncode == 0 and scan.exists(),
              (r2.stdout + r2.stderr)[-400:])
        r3 = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                  "--platform", "claude", "--check"], cwd=str(tmp))
        check("--check exit 0 after short sync", r3.returncode == 0, (r3.stdout + r3.stderr)[-400:])

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "zcode")
        names = {p.name for p in (tmp / ".zcode" / "skills").iterdir()
                 if (p / "SKILL.md").exists()}
        check("long zcode 11 skills (no short-form standalone tools)",
              len(names) == 11 and "short-scan" not in names and "short-analyze" not in names,
              f"actual {sorted(names)}")

    # Long/short mixing guard: a long-form project refuses repeated short initialization
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "claude")
        r = run([sys.executable, str(TOOLS / "init.py"), str(tmp),
                 "--length", "short", "--platform", "claude"])
        check("long/short mixing guard exit 1", r.returncode == 1, (r.stdout + r.stderr)[-200:])

    # Long-form regression: no short-form products when --length is not passed
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        r = init_project(tmp, "claude")
        check("long init exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        check("long story.md has no short marker",
              "**length:**" not in (tmp / "story.md").read_text(encoding="utf-8"))
        check("long produces no stories/", not (tmp / "stories").exists())
        agents_dir = tmp / ".claude" / "agents"
        names = {p.stem for p in agents_dir.glob("*.md")}
        check("long deploys novel-agent", "novel-agent" in names)
        check("long does not deploy short-agent", "short-agent" not in names)
        check("long produces no short-anti-ai.md",
              not ((tmp / ".claude" / "knowledge" / "short-anti-ai.md")).exists())


def test_sync():
    print("[e2e] sync-project.py syncs on all platforms")
    # P1 regression: after syncing a long-form project, --check must exit 0 (fingerprint match + no project-side drift)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "claude")
        r1 = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                  "--platform", "claude"], cwd=str(tmp))
        check("claude sync exit 0", r1.returncode == 0, (r1.stdout + r1.stderr)[-400:])
        check("claude sync generates .claude/skills", (tmp / ".claude/skills").exists())
        r2 = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                  "--platform", "claude", "--check"], cwd=str(tmp))
        check("--check exit 0 after claude sync (no false project-side drift report)", r2.returncode == 0,
              (r2.stdout + r2.stderr)[-400:])
        # Upgrade guard: sync must not introduce short/ story directories or short-form knowledge into a long-form project
        check("claude sync produces no short/ story directory", not (tmp / "short").exists())
        check("claude sync produces no short-anti-ai.md",
              not (tmp / ".claude/knowledge/short-anti-ai.md").exists())

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "opencode")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "opencode"], cwd=str(tmp))
        check("opencode sync exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        w = (tmp / ".opencode/agents/writer.md").read_text(encoding="utf-8")
        check("opencode sync keeps the permission format",
              "permission:" in w and "tools:" not in w and ".opencode/knowledge/" in w)

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "reasonix")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "reasonix"], cwd=str(tmp))
        check("reasonix sync exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        check("reasonix sync keeps the skill", (tmp / ".reasonix/skills/writer/SKILL.md").exists())
        check("reasonix sync has no .claude", not (tmp / ".claude").exists())

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "codex")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "codex"], cwd=str(tmp))
        check("codex sync exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        w = (tmp / ".codex/agents/writer.toml").read_text(encoding="utf-8")
        check("codex sync keeps the TOML format",
              'name = "writer"' in w and "developer_instructions" in w
              and ".codex/knowledge/" in w and ".claude/" not in w)
        check("codex sync has no .claude", not (tmp / ".claude").exists())

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "zcode")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "zcode"], cwd=str(tmp))
        check("zcode sync exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        check("zcode sync keeps the skill", (tmp / ".zcode/skills/writer/SKILL.md").exists())
        w = (tmp / ".zcode/skills/writer/SKILL.md").read_text(encoding="utf-8")
        check("zcode sync keeps the frontmatter format",
              "allowed-tools:" in w and "\ntools:" not in w.split("---", 2)[1]
              and ".zcode/knowledge/" in w and ".claude/" not in w)
        check("zcode sync has no .claude", not (tmp / ".claude").exists())

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "dsh")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "dsh"], cwd=str(tmp))
        check("dsh sync exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        check("dsh sync keeps the skill", (tmp / ".dsh/skills/writer/SKILL.md").exists())
        w = (tmp / ".dsh/skills/writer/SKILL.md").read_text(encoding="utf-8")
        check("dsh sync keeps the frontmatter format",
              "allowed-tools:" not in w.split("---", 2)[1]
              and ".dsh/knowledge/" in w and ".claude/" not in w)
        check("dsh sync has no .claude", not (tmp / ".claude").exists())

    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "grok")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "grok"], cwd=str(tmp))
        check("grok sync exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        w = (tmp / ".grok/agents/writer.md").read_text(encoding="utf-8")
        fm_data = yaml.safe_load(w.split("---", 2)[1])
        check("grok sync keeps the agent Markdown",
              fm_data.get("name") == "writer"
              and ".grok/knowledge/" in w and ".claude/" not in w)
        check("grok sync subagent is banned and not authorized for Agent",
              "Agent" not in fm_data.get("tools", [])
              and fm_data.get("disallowedTools") == ["Agent"], str(fm_data))
        check("grok sync keeps the skill",
              (tmp / ".grok/skills/roleplay-sandbox/SKILL.md").exists())
        check("grok sync has no .claude", not (tmp / ".claude").exists())

    # tools/check-prose.py sync restore (simulated upgrade: script deleted/aged, sync redeploys)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "zcode")
        f = tmp / ".zcode" / "tools" / "check-prose.py"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("# old-version placeholder\n", encoding="utf-8")
        fc = tmp / ".zcode" / "tools" / "check-chapter.py"
        fc.write_text("# old-version placeholder\n", encoding="utf-8")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "zcode"], cwd=str(tmp))
        check("zcode sync exit 0 (script restored)", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        check("zcode sync restores check-prose.py",
              f.exists() and f.read_text(encoding="utf-8") ==
              (TOOLS / "check-prose.py").read_text(encoding="utf-8"))
        check("zcode sync restores check-chapter.py",
              fc.exists() and fc.read_text(encoding="utf-8") ==
              (TOOLS / "check-chapter.py").read_text(encoding="utf-8"))

    # The fingerprint covers tools/check-prose.py: after the script source changes, --check should report updates available
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "claude")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "claude"], cwd=str(tmp))
        check("fingerprint baseline sync exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        src = TOOLS / "check-prose.py"
        bak = src.read_text(encoding="utf-8")
        src.write_text(bak + "\n# fingerprint probe\n", encoding="utf-8")
        try:
            r2 = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                      "--platform", "claude", "--check"], cwd=str(tmp))
            check("--check exit 1 after check-prose.py changes", r2.returncode == 1,
                  (r2.stdout + r2.stderr)[-200:])
        finally:
            src.write_text(bak, encoding="utf-8")

    # --check: first run with no fingerprint exits 1
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "reasonix")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "reasonix", "--check"], cwd=str(tmp))
        check("reasonix --check with no fingerprint exit 1", r.returncode == 1, str(r.returncode))


# ---------------- E2E style seed guard / scaffold sync (review #13-17 regressions) ----------------

def test_style_seed_guard():
    """#13/#14 regressions: no placeholders ship after init; re-running init does not overwrite author edits and fills leftover placeholders in place."""
    print("[e2e] style seed guard")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "claude")
        sc = tmp / "settings" / "writing-style.md"
        text = sc.read_text(encoding="utf-8")
        check("no {role} placeholder after init", "{role}" not in text, text[:200])
        check("no other style placeholders after init",
              all(t not in text for t in ("{principle_1}", "{mistake_1}", "{depiction_techniques}")),
              text[:200])

    # Re-run init: author edits kept + leftover placeholders filled in place (no whole-card overwrite)
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "claude")
        sc = tmp / "settings" / "writing-style.md"
        text = sc.read_text(encoding="utf-8")
        text = text.replace("## 叙事身份（原 role）\n\n",
                            "## 叙事身份（原 role）\n\nthe role setting written by the author\n\n", 1)
        text += "\n- {mistake_1}\n"          # simulate a leftover placeholder from an old init
        sc.write_text(text, encoding="utf-8")
        init_project(tmp, "claude")
        t2 = sc.read_text(encoding="utf-8")
        check("re-running init keeps author edits", "the role setting written by the author" in t2, t2[:300])
        check("re-running init fills placeholders in place", "{mistake_1}" not in t2 and "{role}" not in t2, t2[:300])


def test_sync_style_missing_and_scaffold():
    """#15/#17 regressions: when syncing a missing main card, write （待设定） instead of placeholders; scaffold CLAUDE.md/skill_version refresh."""
    print("[e2e] sync with a missing main card + scaffold refresh")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "claude")
        sc = tmp / "settings" / "writing-style.md"
        sc.unlink()                          # simulate a project with a missing card
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "claude"], cwd=str(tmp))
        check("sync with a missing card exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        check("sync fills in the main card", sc.exists())
        t = sc.read_text(encoding="utf-8")
        check("the filled-in main card has no {role} placeholder", "{role}" not in t, t[:200])
        check("the filled-in main card contains （待设定）", "（待设定）" in t, t[:200])

    # Scaffold refresh: CLAUDE.md restores 9 agents, status.md skill_version updates
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        init_project(tmp, "claude")
        cl = tmp / "CLAUDE.md"
        cl.write_text(cl.read_text(encoding="utf-8").replace("9 collaborating agents", "8 collaborating agents"),
                      encoding="utf-8")
        st = tmp / ".agent" / "status.md"
        st.write_text(st.read_text(encoding="utf-8")
                      .replace("skill_version:** ", "skill_version:** v0.0.0"), encoding="utf-8")
        r = run([sys.executable, str(TOOLS / "sync-project.py"), str(tmp),
                 "--platform", "claude"], cwd=str(tmp))
        check("scaffold sync exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        check("CLAUDE.md restores 9 agents", "9 collaborating agents" in cl.read_text(encoding="utf-8"),
              cl.read_text(encoding="utf-8")[:200])
        st2 = st.read_text(encoding="utf-8")
        check("status.md skill_version updates (not v0.0.0)",
              "- **skill_version:** v0.0.0" not in st2, st2[:200])



def test_install_fresh_home():
    """F1 regression: a first install into a fresh HOME (skills directory does not exist yet) is not wrongly rejected by the safety check."""
    print("[e2e] install.sh codex first install into a fresh HOME")
    with tempfile.TemporaryDirectory() as td:
        home = Path(td) / "home"
        home.mkdir()
        stub = Path(td) / "stub"
        stub.mkdir()
        (stub / "yaml.py").write_text("# stub\n", encoding="utf-8")
        env = dict(os.environ)
        env["HOME"] = str(home)
        env["PYTHONPATH"] = str(stub) + os.pathsep + env.get("PYTHONPATH", "")
        r = run(["bash", str(TOOLS.parent / "install.sh"), "codex"],
                cwd=str(TOOLS.parent), env=env)
        check("fresh home install exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        dest = home / ".codex" / "skills" / "awesome-novel"
        check("fresh home SKILL.md exists", (dest / "SKILL.md").exists())
        check("fresh home agents exist", (dest / "agents").is_dir())


def test_install_ps1_fresh_home():
    """E2E: install.ps1 first install into a fresh HOME (Linux pwsh smoke test, semantically equivalent to Windows).

    Skipped when pwsh is missing (local dev machine); the CI ubuntu runner ships pwsh and runs it for real,
    covering install.ps1's path/copy/threshold flow (arch-review tech debt: ps1 has no tests).
    """
    pwsh = shutil.which("pwsh")
    if not pwsh:
        print("[e2e] install.ps1 smoke test (skipped: no pwsh; CI ubuntu will run it)")
        return
    print("[e2e] install.ps1 first install into a fresh HOME (pwsh)")
    with tempfile.TemporaryDirectory() as td:
        fake_home = Path(td) / "home"
        fake_bin = Path(td) / "bin"
        fake_bin.mkdir()
        os.symlink(sys.executable, fake_bin / "python")   # ps1 uses Get-Command python
        env = dict(os.environ)
        env["USERPROFILE"] = str(fake_home)               # ps1 uses $env:USERPROFILE
        env["PATH"] = str(fake_bin) + os.pathsep + env.get("PATH", "")
        r = run([pwsh, "-NoProfile", "-File", str(TOOLS.parent / "install.ps1"), "claude-code"],
                cwd=str(TOOLS.parent), env=env)
        check("ps1 fresh home install exit 0", r.returncode == 0, (r.stdout + r.stderr)[-400:])
        check("ps1 output contains installation complete", "Installation complete" in r.stdout, r.stdout[-300:])
        # install.ps1 joins paths with Join-Path: on Windows it lands in $HOME\.claude\skills\awesome-novel,
        # on Linux pwsh it lands in $USERPROFILE/.claude/skills/awesome-novel (a real nested directory)
        dest = fake_home / ".claude" / "skills" / "awesome-novel"
        check("ps1 fresh home SKILL.md exists", (dest / "SKILL.md").exists())
        check("ps1 fresh home agents exist", (dest / "agents").is_dir())


def test_install_no_home():
    """P2 regression: when HOME is unset, the install script refuses before creating any directory (reports a path error)."""
    print("[e2e] install.sh refuses install with no HOME")
    with tempfile.TemporaryDirectory() as td:
        stub = Path(td) / "stub"
        stub.mkdir()
        (stub / "yaml.py").write_text("# stub\n", encoding="utf-8")
        env = dict(os.environ)
        env.pop("HOME", None)
        env["PYTHONPATH"] = str(stub) + os.pathsep + env.get("PYTHONPATH", "")
        r = run(["bash", str(TOOLS.parent / "install.sh"), "codex"],
                cwd=str(TOOLS.parent), env=env)
        check("no HOME exit 1", r.returncode == 1, str(r.returncode))
        check("no HOME reports a path error", "abnormal install target path" in (r.stdout + r.stderr))


def test_install_python_gate():
    """P-ver regression: when the version check fails, install.sh aborts before creating or deleting any directory."""
    print("[e2e] install.sh Python version threshold fail-fast")
    with tempfile.TemporaryDirectory() as td:
        home = Path(td) / "home"
        home.mkdir()
        env = dict(os.environ)
        env["HOME"] = str(home)
        env["NOVEL_PYTHON"] = "/bin/false"
        r = run(["bash", str(TOOLS.parent / "install.sh"), "codex"],
                cwd=str(TOOLS.parent), env=env)
        check("version threshold refuses, exit 1", r.returncode == 1, str(r.returncode))
        check("refusal message contains install aborted", "Installation aborted" in (r.stdout + r.stderr),
              (r.stdout + r.stderr)[-300:])
        dest = home / ".codex" / "skills" / "awesome-novel"
        check("no target directory is created on refusal", not dest.exists())


def test_install_yaml_gate():
    """Y-ver E2E regression: without pyyaml, install.sh codex aborts before creating the target directory."""
    print("[e2e] install.sh pyyaml threshold fail-fast")
    with tempfile.TemporaryDirectory() as td:
        home = Path(td) / "home"
        home.mkdir()
        block = Path(td) / "block"
        block.mkdir()
        (block / "yaml.py").write_text('raise ImportError("blocked")\n', encoding="utf-8")
        env = dict(os.environ)
        env["HOME"] = str(home)
        env["PYTHONPATH"] = str(block) + os.pathsep + env.get("PYTHONPATH", "")
        r = run(["bash", str(TOOLS.parent / "install.sh"), "codex"],
                cwd=str(TOOLS.parent), env=env)
        check("missing pyyaml refuses, exit 1", r.returncode == 1, str(r.returncode))
        check("missing pyyaml reports install aborted", "Installation aborted" in (r.stdout + r.stderr)
              and "pyyaml" in (r.stdout + r.stderr), (r.stdout + r.stderr)[-300:])
        dest = home / ".codex" / "skills" / "awesome-novel"
        check("no target directory is created on refusal", not dest.exists())


def test_noyaml_e2e():
    """F5 regression: without pyyaml, init --platform codex exits with a clear error and produces no damaged TOML."""
    print("[e2e] init --platform codex errors clearly without pyyaml")
    with tempfile.TemporaryDirectory() as td:
        tmp = Path(td)
        (tmp / "yaml.py").write_text('raise ImportError("blocked")\n', encoding="utf-8")
        env = dict(os.environ)
        env["PYTHONPATH"] = str(tmp) + os.pathsep + env.get("PYTHONPATH", "")
        r = run([sys.executable, str(TOOLS / "init.py"), str(tmp / "proj"),
                 "--genre", "1", "--platform", "codex"], cwd=str(tmp), env=env)
        check("missing yaml exit 1", r.returncode == 1, str(r.returncode))
        check("missing yaml error message", "needs pyyaml" in (r.stdout + r.stderr))
        check("missing yaml produces no damaged TOML",
              not (tmp / "proj" / ".codex" / "agents" / "writer.toml").exists())


def main():
    for name, fn in [
        ("test_detect", test_detect),
        ("test_rewrite", test_rewrite),
        ("test_config", test_config),
        ("test_yaml_precheck", test_yaml_precheck),
        ("test_check_python", test_check_python),
        ("test_check_yaml", test_check_yaml),
        ("test_check_version", test_check_version),
        ("test_init_layout", test_init_layout),
        ("test_short_init_layout", test_short_init_layout),
        ("test_sync", test_sync),
        ("test_style_seed_guard", test_style_seed_guard),
        ("test_sync_style_missing_and_scaffold", test_sync_style_missing_and_scaffold),
        ("test_install_fresh_home", test_install_fresh_home),
        ("test_install_ps1_fresh_home", test_install_ps1_fresh_home),
        ("test_install_no_home", test_install_no_home),
        ("test_install_python_gate", test_install_python_gate),
        ("test_install_yaml_gate", test_install_yaml_gate),
        ("test_noyaml_e2e", test_noyaml_e2e),
    ]:
        try:
            fn()
        except Exception as e:
            check(f"{name} raised", False, repr(e))
    print(f"\nResult: {_tu.PASS} passed, {_tu.FAIL} failed")
    sys.exit(0 if _tu.FAIL == 0 else 1)


if __name__ == "__main__":
    main()
