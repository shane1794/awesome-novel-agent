# short-story-scan Specification

## Purpose
The market entry point for short-story topic selection: identify the emotional landscape of the short-story market from chart samples, and output actionable emotional directions, genre candidates, risk thresholds, and verification actions, so the author knows before writing "which emotions are hot right now, and which are about to saturate".

## Requirements

### Requirement: S1 List scanning must first confirm the platform and direction

List scanning MUST first confirm the target platform and the author's genre direction. When the author already has a clear direction, it MUST do a deep scan of that direction; with no direction, it MUST do a full-chart overview and look for trends; when a cross-platform comparison is requested, it MUST do a platform-comparison analysis.

#### Scenario: S1.1 Platform confirmation
- **WHEN** the author starts a list scan
- **THEN** first ask for the target platform and the genre direction they want to write; MUST NOT assume a platform

#### Scenario: S1.2 Pick the form by direction
- **WHEN** the author gives a direction / says they have none / asks for a comparison
- **THEN** enter the deep scan / full-chart overview / platform comparison form respectively

### Requirement: S2 Data sources must degrade across three tiers, and failures must not stop the scan

List scanning MUST use the three-tier data sources in priority order: live collection (when the runtime environment has the capability), then author-provided (screenshots / text / links), then built-in knowledge. When degrading to built-in knowledge, it MUST mark the output "based on historical trends, live verification not completed, candidate hypothesis only" and list the pages to re-scan. When a single platform's collection fails, it MUST mark that platform skipped and continue with the rest, noting the gap in the report.

#### Scenario: S2.1 Degradation marking
- **WHEN** there is no live collection and the author provides no data
- **THEN** the report marks the output as not live-verified and candidate hypothesis only, and lists the pages to re-scan

#### Scenario: S2.2 One platform failing does not stop the scan
- **WHEN** one platform's collection fails
- **THEN** that platform is marked skipped, the rest proceed as usual, and the report notes the data gap

### Requirement: S3 Analysis must cover seven actionable dimensions

Analysis MUST cover: emotion-type distribution, genre hotspots, length distribution, opening patterns, ending-type ratios, title patterns, and character models, with concrete findings per item rather than a genre list; and it must give a tone-fit comparison for the target platform.

#### Scenario: S3.1 All seven dimensions present
- **WHEN** reading the list-scan output
- **THEN** all seven items have concrete findings

### Requirement: S4 Reports must mark freshness and give trend warnings

Reports MUST mark the sample date, trend confidence, and the next re-scan time; before a re-scan, they MUST NOT be treated as long-term trends. They MUST give trend warnings (currently exploding / about to take off / about to saturate) and directions worth writing, each with its emotional-pull method and feasibility.

#### Scenario: S4.1 Freshness statement
- **WHEN** checking the report header
- **THEN** it contains the sample date, the next re-scan time, and the not-yet-rescanned statement

#### Scenario: S4.2 Directions come with a playbook
- **WHEN** checking the "directions worth writing"
- **THEN** each entry carries its emotional-pull method and feasibility, and MUST NOT list only genre names

### Requirement: S5 Topic matching must grade and cover spread risk

Topic matching MUST separate low- and high-complexity candidates and give cross-priorities against the project's capabilities; when a recommended direction contains no reversal, it MUST require strong resonance, strong topicality, or strong aftertaste to cover the spread risk.

#### Scenario: S5.1 Spread-risk coverage
- **WHEN** a recommended direction contains no reversal
- **THEN** the coverage method is written out explicitly; without it, the direction must not be recommended
