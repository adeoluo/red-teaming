# Data Card - Red Teaming Engine

The project bundles one small suite of red-teaming goals. There is no training data and
nothing is downloaded.

## bundled goals (`src/red_teaming/data.py`)

- **Provenance:** hand-authored for this project. Five goals, each asking the guarded
  assistant about a **fictional, invented restricted term** (``zorblax``, ``quarnex``,
  ``driftwing``, ``nullspar``, ``vexhollow``).
- **Difficulty:** each goal sets a guard threshold from 0.40 (strict) to 0.60 (lax), so the
  search works harder on some goals than others.
- **Licensing:** authored by this repository; MIT.
- **Known gaps:** small and illustrative; the restricted terms are placeholders, not real
  policy categories.

## Ethical considerations

Every restricted term is fictional and meaningless, and the engine never produces real
disallowed content. The goals contain no personal, sensitive, or copyrighted material.
