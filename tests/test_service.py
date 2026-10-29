"""Tests for the dependency-free HTTP red-teaming service (pure handler layer)."""

from __future__ import annotations

from red_teaming.service import RedTeamService, handle


def _service() -> RedTeamService:
    return RedTeamService()


def test_health() -> None:
    status, payload = handle("GET", "/health", {}, _service())
    assert status == 200
    assert payload["status"] == "ok"
    assert payload["goals"] > 0


def test_report() -> None:
    status, payload = handle("GET", "/report", {}, _service())
    assert status == 200
    strategies = {row["strategy"]: row for row in payload["strategies"]}
    assert any("evolutionary" in name for name in strategies)


def test_attack_jailbreaks_known_goal() -> None:
    status, payload = handle("POST", "/attack", {"goal": "strict-guard"}, _service())
    assert status == 200
    assert payload["succeeded"] is True
    assert "VIOLATION" in payload["response"]
    assert len(payload["attack"]) >= 1


def test_attack_hardened_defense() -> None:
    status, payload = handle(
        "POST", "/attack", {"goal": "medium-guard", "hardened": True}, _service()
    )
    assert status == 200
    assert payload["succeeded"] is False


def test_attack_rejects_unknown_goal() -> None:
    status, payload = handle("POST", "/attack", {"goal": "nope"}, _service())
    assert status == 400
    assert "goal" in payload["error"]


def test_attack_rejects_bad_seed() -> None:
    status, _ = handle("POST", "/attack", {"goal": "strict-guard", "seed": -1}, _service())
    assert status == 400


def test_unknown_route() -> None:
    status, payload = handle("GET", "/nope", {}, _service())
    assert status == 404
    assert "error" in payload
