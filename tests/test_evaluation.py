"""Tests for the attack-success-rate report and the command line interface."""

from __future__ import annotations

from red_teaming.cli import main
from red_teaming.evaluation import format_table, run_report


def test_report_shows_expected_gradient() -> None:
    rows = run_report()
    by = {row.strategy: row for row in rows}
    direct = by["direct (no attack)"].attack_success_rate
    single = by["best single mutator"].attack_success_rate
    evolved = by["evolutionary search"].attack_success_rate
    hardened = by["evolutionary vs hardened guard (defense)"].attack_success_rate
    assert direct == 0.0
    assert evolved == 1.0
    assert direct <= single <= evolved
    assert hardened < evolved


def test_format_table_contents() -> None:
    table = format_table(run_report())
    assert "attack success rate" in table
    assert "evolutionary search" in table


def test_cli_report(capsys) -> None:
    main(["report"])
    out = capsys.readouterr().out
    assert "evolutionary search" in out


def test_cli_attack(capsys) -> None:
    main(["attack", "strict-guard"])
    out = capsys.readouterr().out
    assert "VIOLATION" in out
    assert "attack:" in out


def test_cli_attack_hardened(capsys) -> None:
    main(["attack", "medium-guard", "--hardened"])
    out = capsys.readouterr().out
    assert "REFUSAL" in out


def test_cli_attack_unknown_goal() -> None:
    try:
        main(["attack", "no-such-goal"])
    except SystemExit as exit_error:
        assert "unknown goal" in str(exit_error)
    else:  # pragma: no cover
        raise AssertionError("expected SystemExit")
