# v4.24.1 Release Notes

> **Keywords:** Windows platform fixes: cross-platform consistency for static checks + install.ps1 PowerShell 5.1 compatibility

---

## In One Sentence

Two Windows-specific fixes: check-agents' deployed-product manifest now uses forward-slash paths, so orphan detection no longer false-positives in bulk on Windows; and install.ps1 gains a UTF-8 BOM, so Windows PowerShell 5.1 (the system default shell) no longer fails to parse it. macOS/Linux behavior is unchanged.

## What Changed in This Release

| Change | Description |
|------|------|
| **check-agents deployment-set paths unified to forward slashes (#128)** | The `_deployed_knowledge_files()` product manifest changes `str()` to `as_posix()`. On Windows, backslash paths never matched the reference scan (forward slashes), so orphan detection and reference checks false-positived in bulk (measured: 96 orphans reported, exit 1, while Ubuntu CI was all green); after the fix, both platforms behave consistently |
| **install.ps1 gains a UTF-8 BOM (#129)** | UTF-8 without a BOM is decoded as ANSI/GBK in PowerShell 5.1, so the Chinese prompt strings inside the script threw a ParserError directly and the installer could not run at all; with the BOM added, both PS 5.1 and pwsh 7 work, with zero content changes |

## Compatibility

- Pure fixes: macOS/Linux behavior is unchanged on all platforms (`as_posix()` and `str()` are equivalent on POSIX); no project-format changes, no migration.
- External contributions: both fixes come from @qikairo7 (Leo), verified on a real Windows 11 machine.

## Tests

- On the fix branch, check-agents / check-conflicts / test_platforms all green (290 passed, 0 failed); main CI is green after merging.
- Real Windows 11 verification: check-agents went from 96 false positives to 0; install.ps1 went from ParserError to a normal install landing (SKILL.md + agents + tools).
