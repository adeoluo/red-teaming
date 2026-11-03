# AGENTS.md

Working notes for coding agents and contributors in **Red Teaming Engine**. The [README](README.md)
explains what the project does and why; this file explains how to change it safely.

## Project

An automated guardrail red-teaming engine built from scratch: evolve guardrail-evasion strategies, measure attack success rate, and demonstrate a defense.

## Layout

- `benchmarks/`: benchmark scripts and recorded results
- `docker-compose.yml`: local container setup
- `docs/`: documentation, architecture diagram source and render, design records
- `src/`: library and service source
- `tests/`: test suite

Key modules:

- `src/red_teaming/__init__.py`: Red Teaming - an automated guardrail red-teaming engine built from scratch.
- `src/red_teaming/cli.py`: Command line interface for the red-teaming engine.
- `src/red_teaming/data.py`: A bundled suite of red-teaming goals over fictional restricted terms.
- `src/red_teaming/evaluation.py`: Measure attack success rate across the goal suite.
- `src/red_teaming/mutators.py`: Prompt mutators: transformations that attempt to evade a guardrail.
- `src/red_teaming/observability.py`: In-process request metrics for the HTTP service.
- `src/red_teaming/search.py`: Search strategies that discover guardrail-evasion attacks.
- `src/red_teaming/service.py`: A standard-library HTTP service exposing the red-teaming engine.
- `src/red_teaming/target.py`: The system under test: a guarded assistant and its guardrail.
- `src/red_teaming/types.py`: Core data types for the red-teaming engine.

## Commands

| Command | Purpose |
|---|---|
| `make help` | Show this help |
| `make setup` | Install dependencies and pre-commit hooks |
| `make format` | Format automatically |
| `make lint` | Lint (no fixes) |
| `make type` | Type-check |
| `make test` | Run tests |
| `make coverage` | Tests with coverage gate |
| `make evaluation` | Reproduce the results table |
| `make run` | Run the application entrypoint |
| `make diagram` | Render architecture diagram to SVG |
| `make docker-build` | Build the image |
| `make docker-up` | Run via docker compose |
| `make clean` | Remove caches and artifacts |
| `make all` | Full local gate (mirror of continuous integration) |
| `make changelog` | Regenerate CHANGELOG.md from Conventional Commits (git-cliff) |
| `make cut-release` | Cut a release locally: version bump, changelog, tag, GitHub release (RELEASE_VERSION=vX.Y.Z optional) |

Run the full local gate (`make all`) before committing; CI runs the same checks.

## Conventions

- Commits follow Conventional Commits (`feat:`, `fix:`, `perf:`, `refactor:`, `docs:`, `test:`, `ci:`, `chore:`).
  The changelog and the next version number are derived from them.
- Every number quoted in the README is produced by a command in this repository. When behavior
  changes, rerun that command and update the number in the same commit.
- When a component is added, removed or renamed, update `docs/architecture/architecture.mmd`
  and re-render `architecture.svg` so the diagram matches the code.
- README sections keep their fixed order. Prose avoids em and en dashes and promotional wording.
- Tests accompany behavior changes; a bug fix comes with a test that fails without it.
- Releases are cut with `make cut-release`.

## Python notes

- Python is managed with `uv`; run commands through `uv run` so the locked environment is used.
- Lint and format with `ruff`; type-check with `mypy`; tests use `pytest`.
- Public functions carry type hints and a docstring that states the contract, not the steps.
