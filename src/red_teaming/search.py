"""Search strategies that discover guardrail-evasion attacks.

An attack is an ordered composition of mutator names. The search space is the
set of such compositions up to a bounded length. Three strategies are provided:

* ``direct_attack`` - the empty composition (a control; it is always blocked).
* ``best_single_mutator`` - the strongest single mutator for a goal.
* ``EvolutionarySearch`` - a deterministic genetic algorithm that composes and
  orders mutators to drop the guard's detection below threshold while keeping
  the model's comprehension above threshold.

Fitness rewards success and, short of it, rewards reducing the detection and
comprehension deficits, so the search has a smooth gradient to climb.
"""

from __future__ import annotations

import random
from dataclasses import dataclass

from red_teaming.mutators import MUTATOR_NAMES
from red_teaming.target import MODEL_THRESHOLD, evaluate_attack
from red_teaming.types import Goal

Attack = tuple[str, ...]


@dataclass(frozen=True)
class SearchResult:
    """The best attack found for a goal and whether it jailbreaks the guard."""

    goal: str
    attack: Attack
    succeeded: bool
    detection: float
    comprehension: float


def _fitness(goal: Goal, attack: Attack, *, hardened: bool) -> float:
    outcome = evaluate_attack(goal, attack, hardened=hardened)
    if outcome.succeeded:
        # Prefer successful attacks, then shorter and more comprehensible ones.
        return 2.0 + outcome.comprehension - 0.01 * len(attack)
    detection_deficit = max(0.0, outcome.detection - goal.guard_threshold)
    comprehension_deficit = max(0.0, MODEL_THRESHOLD - outcome.comprehension)
    return -(detection_deficit + comprehension_deficit)


def direct_attack(goal: Goal, *, hardened: bool = False) -> SearchResult:
    """The control: no mutation at all."""

    outcome = evaluate_attack(goal, (), hardened=hardened)
    return SearchResult(goal.name, (), outcome.succeeded, outcome.detection, outcome.comprehension)


def best_single_mutator(goal: Goal, *, hardened: bool = False) -> SearchResult:
    """The strongest single mutator, by fitness, for a goal."""

    best_name = MUTATOR_NAMES[0]
    best_fitness = float("-inf")
    for name in MUTATOR_NAMES:
        score = _fitness(goal, (name,), hardened=hardened)
        if score > best_fitness:
            best_fitness = score
            best_name = name
    outcome = evaluate_attack(goal, (best_name,), hardened=hardened)
    return SearchResult(
        goal.name, (best_name,), outcome.succeeded, outcome.detection, outcome.comprehension
    )


class EvolutionarySearch:
    """A deterministic genetic algorithm over mutator compositions."""

    def __init__(
        self,
        population_size: int = 16,
        generations: int = 20,
        max_length: int = 5,
        seed: int = 0,
    ) -> None:
        if population_size < 2:
            raise ValueError("population_size must be at least 2")
        if max_length < 1:
            raise ValueError("max_length must be at least 1")
        self.population_size = population_size
        self.generations = generations
        self.max_length = max_length
        self.seed = seed

    def _random_attack(self, rng: random.Random) -> Attack:
        length = rng.randint(1, self.max_length)
        return tuple(rng.choice(MUTATOR_NAMES) for _ in range(length))

    def _mutate(self, attack: Attack, rng: random.Random) -> Attack:
        genes = list(attack)
        operation = rng.random()
        if operation < 0.34 and len(genes) < self.max_length:
            genes.insert(rng.randrange(len(genes) + 1), rng.choice(MUTATOR_NAMES))
        elif operation < 0.67 and len(genes) > 1:
            del genes[rng.randrange(len(genes))]
        elif genes:
            genes[rng.randrange(len(genes))] = rng.choice(MUTATOR_NAMES)
        return tuple(genes)

    def _crossover(self, left: Attack, right: Attack, rng: random.Random) -> Attack:
        cut_left = rng.randint(0, len(left))
        cut_right = rng.randint(0, len(right))
        child = (*left[:cut_left], *right[cut_right:])
        return child[: self.max_length] if child else (rng.choice(MUTATOR_NAMES),)

    def search(self, goal: Goal, *, hardened: bool = False) -> SearchResult:
        rng = random.Random(self.seed)
        population = [self._random_attack(rng) for _ in range(self.population_size)]
        best_attack: Attack = ()
        best_fitness = float("-inf")

        for _ in range(self.generations):
            scored = sorted(
                population,
                key=lambda attack: _fitness(goal, attack, hardened=hardened),
                reverse=True,
            )
            top_fitness = _fitness(goal, scored[0], hardened=hardened)
            if top_fitness > best_fitness:
                best_fitness = top_fitness
                best_attack = scored[0]
            survivors = scored[: max(2, self.population_size // 2)]
            children: list[Attack] = []
            while len(survivors) + len(children) < self.population_size:
                parent_a = rng.choice(survivors)
                parent_b = rng.choice(survivors)
                child = self._mutate(self._crossover(parent_a, parent_b, rng), rng)
                children.append(child)
            population = [*survivors, *children]

        outcome = evaluate_attack(goal, best_attack, hardened=hardened)
        return SearchResult(
            goal.name, best_attack, outcome.succeeded, outcome.detection, outcome.comprehension
        )
