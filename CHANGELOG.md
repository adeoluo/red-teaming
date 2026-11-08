# Changelog

All notable changes to this project are documented here. The file is generated
from Conventional Commits by [git-cliff](https://git-cliff.org) when a release is cut
with `make cut-release`.

## [0.1.1] 2026-11-08

### Documentation

- Complete citation metadata and bump it on release (#7)
- Map the threat model to OWASP LLM 2026 and MITRE ATLAS v2026.10 (#9)
- Add standards keywords to the citation metadata (#10)

### Maintenance

- Latest toolchain and CI versions (#6)
- Release script keeps hard-coded version strings in step (#8)

## [0.1.0] 2026-11-03

### Features

- Add goals, mutators, and the guarded target system
- Add direct, single-mutator, and evolutionary attack search
- Add goal suite, attack-success-rate report, and command line interface
- Add a deterministic attack-search micro-benchmark
- Add HTTP service, stress benchmark, and operations documentation
- Add production observability (metrics and readiness) and reword footer

### Documentation

- Write README, architecture diagram, and responsible-AI cards
- Use plain, factual wording (#14)
- Standard README structure and language framing (#16)
- Vertical layered architecture diagram
- Horizontal layered architecture diagram
- Compact horizontal architecture diagram
- Recorded terminal demo of a real run, with its vhs tape (#1)
- Recorded demos of more commands, with their vhs tapes (#2)
- Recorded demos of the HTTP service and more commands (#3)
- Describe the supply chain accurately (#4)

### Build and CI

- Run CodeQL on main and on a weekly schedule only

### Maintenance

- Scaffold red-teaming project
- Bump continuous integration action versions and dev dependencies
- Remove Dependabot configuration
- Release tooling, changelog and agent guides (#5)
