# v4.28.0 Release Notes

> **Keywords:** Switch to the AGPL-3.0 license + third-party LLM service statement

---

## In One Sentence

The project license switches as a whole from GPLv3 to AGPL-3.0, and the READMEs (Chinese and English) gain a third-party LLM API and Token service statement. The open-source license tightens by one notch, and the boundary of responsibility between the project and third-party paid services is written down.

## What Changed in This Release

| Change | Description |
|------|------|
| **AGPL-3.0 license** | LICENSE is replaced with the official AGPL-3.0 text from gnu.org (byte-for-byte identical to the official text). 11 files synced: both LICENSE-DECLARATION files, both README badges and statements, the install.sh / install.ps1 header license statements (keeping the or-later semantics), skill.json, the index.html landing page, AGENTS.md, and CONTRIBUTING.md |
| **Third-party LLM service statement** | A "Third-Party LLM API and Token Service Statement" is added to the end of README.md / README-en.md: the project itself provides no large-model or Token paid services; third-party LLM providers in the docs and example configs are only technical-compatibility demonstrations; top-ups, API calls, content generation, refunds, and stability are the sole responsibility of the third-party providers; the project endorses no third-party paid API; when generating content with a third-party API, comply with the relevant laws and regulations yourself |

## Compatibility

- Pure license and documentation changes, with no code behavior changes; the install scripts only change comment headers (bash -n passes)
- The "free for personal use, commercial use needs author authorization" stance is unchanged; AGPL-3.0 Article 13 (offering the service over a network also triggers the open-source obligation) is consistent with that stance
- GPLv3 wording in the docs/releasenotes/ history is kept as-is and not rewritten; the AGPL text's references to the GPL are part of the license text itself

## Tests

- CI lint green (including check-version version consistency); skill.json parses as JSON; no GPLv3 remains anywhere in the repo (except historical release records and the license text itself)
- LICENSE matches https://www.gnu.org/licenses/agpl-3.0.txt in a byte-for-byte diff
- review-agent reviewed two rounds (PR #135 / #136) with no findings
