"""Command line interface for the red-teaming engine."""

from __future__ import annotations

import argparse

from red_teaming.data import GOALS
from red_teaming.evaluation import format_table, run_report
from red_teaming.mutators import apply_mutators
from red_teaming.search import EvolutionarySearch
from red_teaming.target import respond


def _cmd_report(_: argparse.Namespace) -> None:
    print(format_table(run_report()))


def _cmd_attack(args: argparse.Namespace) -> None:
    goals = {goal.name: goal for goal in GOALS}
    goal = goals.get(args.goal)
    if goal is None:
        names = ", ".join(goals)
        raise SystemExit(f"unknown goal '{args.goal}'. choose from: {names}")
    result = EvolutionarySearch(seed=args.seed).search(goal, hardened=args.hardened)
    print(f"goal: {goal.name} (guard threshold {goal.guard_threshold})")
    print(f"attack: {' -> '.join(result.attack) if result.attack else '(none)'}")
    print(f"mutated prompt: {apply_mutators(goal.prompt, result.attack)}")
    print(f"detection {result.detection:.3f}  comprehension {result.comprehension:.3f}")
    print(f"response: {respond(goal, result.attack, hardened=args.hardened)}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="red-teaming", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("report", help="attack success rate across the goal suite")

    attack = sub.add_parser("attack", help="evolve an attack for a single goal")
    attack.add_argument("goal", help="the goal name (see the report for names)")
    attack.add_argument("--seed", type=int, default=0, help="search seed")
    attack.add_argument(
        "--hardened", action="store_true", help="attack the hardened guard (the defense)"
    )

    handlers = {"report": _cmd_report, "attack": _cmd_attack}
    args = parser.parse_args(argv)
    handlers[args.command](args)


if __name__ == "__main__":
    main()
