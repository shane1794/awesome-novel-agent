# Contributing to awesome-novel-agent

## 1. Project overview

awesome-novel-agent is a free, open source AI novel-writing assistant that runs on AI terminal tools such as DeepSeek TUI, Claude Code, Hermes, and OpenClaw, under the AGPL-3.0 open source license. The project aims to lower the barrier to novel writing, giving creators one-stop novel-writing ability: world building, character creation, chapter outlines, prose writing, style optimization, and foreshadowing tracking. It is permanently free for personal users; commercial use requires official authorization from the author.

The project is maintained by the community. All kinds of contributors are welcome: technical people, web-novel writers, and enthusiasts. No advanced programming skill is needed; copy improvements, material contributions, and bug reports are all valid contributions.

## 2. Rules before contributing

### 2.1 Open source license requirements

- All submitted code, documentation, and config files follow AGPL-3.0; submitting means you agree to the license terms.
- Do not submit closed-source, infringing, or rule-breaking third-party resources, and do not upload copyrighted novel material or commercial copy.
- You may use your own modified version privately; redistribution and derivative versions must follow the open source license and keep the project's original copyright notice.

### 2.2 Basic submission rules

- All submissions must fit the project scope: AI-assisted novel writing only. Do not add unrelated features or redundant plugins.
- Use clear code and document naming, with comments in plain, easy language, suited to users in China.
- Test your submission yourself before submitting, make sure it has no breaking bugs, and keep it compatible with mainstream terminals such as DeepSeek TUI.

## 3. Ways to contribute (for everyone)

### 3.1 Non-technical contributions (no programming needed)

#### 3.1.1 Issue reports and bug submissions

As a user of the project, you are the most likely to spot problems. You can submit feedback in GitHub Issues, covering these types of problems:

- **Functional problems**: installer errors, chapter archiving failures, character status recording errors.
- **Generation defects**: stiff AI prose, weak AI-flavor removal, broken foreshadowing tracking, broken pacing detection.
- **Compatibility problems**: terminal version compatibility failures, installation errors on different systems (Windows/Linux).

Submission requirements: describe the steps, the error, and the terminal tool you used (DeepSeek TUI, Claude Code, etc.) clearly. Screenshots and logs help with reproduction and troubleshooting.

#### 3.1.2 Material and template contributions

- **Genre files**: add character archetypes, narrative templates, and chapter frameworks for web-novel genres such as xianxia (immortal cultivation), urban, mystery, sci-fi, and fantasy.
- **Style material**: improve style-analysis rules and add to the mainstream web-novel author style feature library.
- **Prompt optimization**: improve the built-in prompts for chapter generation, character creation, and plot roleplay to reduce the mechanical AI feel.

#### 3.1.3 Documentation improvements and translation

- Improve the official documentation: installation tutorials for beginners, command explanations, advanced usage, and simpler step-by-step guides for users with no background.
- Add usage examples: new hands-on novel cases (xianxia (immortal cultivation), urban, etc.) to enrich the teaching content in docs.
- Polish copy: improve the wording of the README and SKILL.md so it is plain and easy to follow, suited to web-novel writers in China.

#### 3.1.4 Financial contributions

The project stays non-commercial: all features are permanently free for personal users. If you value the project, you can support its continued development:

- **GitHub Sponsors**: fund project maintenance regularly through the GitHub Sponsors program
- **Aifadian**: support the project financially on the Aifadian platform
- **Ko-fi**: sponsor development once through Ko-fi

Funds go to server costs, AI API call subsidies, open source license purchases, developer incentives, and similar costs. All fund usage is published regularly in the project community.

#### 3.1.5 Promotion

- Share the project on social platforms and writing communities to help more web-novel writers use AI writing tools for free.
- Write project reviews, tutorials, and usage notes, and publish them on blogs, CSDN, Zhihu, and similar platforms.
- Answer beginners' questions about installation, commands, and project migration, and help keep the community welcoming.
- Make video tutorials and operation demos, and publish them on Bilibili, YouTube, and other video platforms.
- Translate the project documentation into other languages to help overseas writers learn about and use this tool.

### 3.2 Technical contributions (programming experience needed)

#### 3.2.1 Code development and optimization

- **Script optimization**: iterate on the install.sh and install.ps1 installer scripts, fix installation errors, and improve the installation flow.
- **Feature iteration**: optimize the 9-agent collaboration flow and the SOLO fully automatic mode, and improve agent definitions and skill SOPs.
- **Compatibility work**: adapt the project to more AI terminal tools, improve DeepSeek TUI compatibility, and remove redundant model dependencies.
- **Algorithm optimization**: upgrade the AI machine-tone detection, foreshadowing and hook tracking, and plot pacing detection algorithms.

#### 3.2.2 Code review and maintenance

- Review Pull Requests (PRs) from the community, checking code safety, compatibility, and logic.
- Clean up redundant files, optimize the project directory structure, and remove useless scripts and reference files.
- Maintain GitHub Actions automated deployment and improve the GitHub Pages deployment flow.

#### 3.2.3 Ecosystem development

- Build derived tools: novel project migration tools, style-analysis visualization tools.
- Improve the resource directories: agents/ (agent definitions) and knowledge/ (format specs, anti-AI rules, writing methodology), and expand supporting writing features.

## 4. Submission rules

### 4.1 Issue submission rules

- **Label by category**: bug report, feature suggestion, material contribution, documentation improvement.
- **Keep titles short and direct**, and describe the request, problem, or improvement clearly in the body. Avoid meaningless filler.
- Do not submit the same problem twice; add a comment with extra information under the existing issue instead.

### 4.2 Pull Request submission rules

- **Branch requirement**: create a development branch from the project main branch. Never edit the main branch directly.
- **Commit messages**: strictly follow the project commit message format, e.g. `fix: fix Windows install path error`, `docs: add urban genre writing case`.
- **Testing requirement**: test in at least one AI terminal before submitting, and make sure there are no breaking bugs.
- **Scope limit**: one PR focuses on one feature improvement or fix. No batched, unrelated changes.

## 5. Branches and versions

| Branch | Description |
|------|------|
| main | Stable release branch, holding officially usable versions; only reviewed, finished code is merged |
| Development branch | For iteration and testing; new features and code optimization go to a development branch first, and merge to main after testing |

- **Version migration**: the project supports one-click migration of old versions to 4.0. Contributors must keep the migration logic compatible with historical project data and preserve user writing backups.

## 6. Prohibited behavior

- Do not submit malicious code, virus scripts, or infringing resources.
- Do not alter the project open source license or copyright notice, and do not privately turn the project into closed-source commercial software.
- Do not farm commits, make meaningless file changes, or flood Issues and PRs.
- Do not use this project to create illegal, vulgar, or rule-breaking novel content.

## 7. Contact and licensing

| Type | Description |
|------|------|
| Personal use | All features permanently free, no subscription, no API fees |
| Commercial use | You must contact the project author for official authorization; commercial use without authorization is strictly prohibited |
| Contribution discussion | Submit Issues and PRs in the GitHub repository; project maintainers review and reply regularly |
| Copyright notice | This project is open source under AGPL-3.0; derivative works must be open sourced under the same terms and credit the original project |

## 8. Acknowledgments

Thanks to all open source contributors and web-novel writers for their generous work; thanks to the DeepSeek TUI project for providing a free terminal environment; parts of this project's design were inspired by InkOS, and sincere thanks go to its developers.
