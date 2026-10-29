"""A dependency-free HTTP service exposing the red-teaming engine.

The service runs the evolutionary attack search over the goal suite and reports
attack success rate, or evolves an attack for one named goal. A pure handler is
separated from the socket binding for testing.

Endpoints
---------
``GET  /health``   liveness and goal count.
``GET  /report``   attack success rate for each strategy over the goal suite.
``POST /attack``   body ``{"goal": str, "seed"?: int, "hardened"?: bool}``;
                   returns the evolved attack and whether it jailbreaks the guard.
"""

from __future__ import annotations

import json
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any

from red_teaming.data import GOALS
from red_teaming.evaluation import format_table, run_report
from red_teaming.mutators import apply_mutators
from red_teaming.observability import ServiceMetrics
from red_teaming.search import EvolutionarySearch
from red_teaming.target import respond
from red_teaming.types import Goal

JsonObject = dict[str, Any]
_MAX_SEED = 1_000_000


@dataclass(frozen=True)
class RedTeamService:
    """Serves attack-success reports and single-goal attack searches."""

    goals: tuple[Goal, ...] = GOALS
    metrics: ServiceMetrics = field(default_factory=ServiceMetrics)

    def report(self) -> JsonObject:
        rows = run_report(self.goals)
        return {
            "text": format_table(rows),
            "strategies": [
                {
                    "strategy": row.strategy,
                    "successes": row.successes,
                    "total": row.total,
                    "attack_success_rate": round(row.attack_success_rate, 4),
                }
                for row in rows
            ],
        }

    def attack(self, goal: Goal, *, seed: int, hardened: bool) -> JsonObject:
        result = EvolutionarySearch(seed=seed).search(goal, hardened=hardened)
        return {
            "goal": goal.name,
            "guard_threshold": goal.guard_threshold,
            "attack": list(result.attack),
            "succeeded": result.succeeded,
            "detection": round(result.detection, 4),
            "comprehension": round(result.comprehension, 4),
            "mutated_prompt": apply_mutators(goal.prompt, result.attack),
            "response": respond(goal, result.attack, hardened=hardened),
        }


def _validate_attack(body: Mapping[str, Any], goals: Mapping[str, Goal]) -> tuple[Goal, int, bool]:
    name = body.get("goal")
    if not isinstance(name, str) or name not in goals:
        choices = ", ".join(goals)
        raise ValueError(f"'goal' must be one of: {choices}")
    seed = body.get("seed", 0)
    if not isinstance(seed, int) or not 0 <= seed <= _MAX_SEED:
        raise ValueError(f"'seed' must be an integer in [0, {_MAX_SEED}]")
    hardened = body.get("hardened", False)
    if not isinstance(hardened, bool):
        raise ValueError("'hardened' must be a boolean")
    return goals[name], seed, hardened


def _route(
    method: str, path: str, body: Mapping[str, Any], service: RedTeamService
) -> tuple[int, JsonObject]:
    if method == "GET" and path == "/health":
        return 200, {"status": "ok", "goals": len(service.goals)}
    if method == "GET" and path == "/report":
        return 200, service.report()
    if method == "POST" and path == "/attack":
        goals = {goal.name: goal for goal in service.goals}
        try:
            goal, seed, hardened = _validate_attack(body, goals)
        except ValueError as error:
            return 400, {"error": str(error)}
        return 200, service.attack(goal, seed=seed, hardened=hardened)
    return 404, {"error": f"no route for {method} {path}"}


def handle(
    method: str, path: str, body: Mapping[str, Any], service: RedTeamService
) -> tuple[int, JsonObject]:
    """Route a request, recording per-route metrics, and return status and payload."""

    if method == "GET" and path == "/ready":
        return 200, {"status": "ready"}
    start = time.perf_counter()
    status, payload = _route(method, path, body, service)
    service.metrics.observe(
        f"{method} {path}", (time.perf_counter() - start) * 1000.0, error=status >= 400
    )
    return status, payload


class _Handler(BaseHTTPRequestHandler):  # pragma: no cover - exercised over sockets
    service: RedTeamService

    def _respond(self, status: int, payload: JsonObject) -> None:
        encoded = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self) -> None:
        if self.path == "/metrics":
            body = self.service.metrics.render_prometheus().encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        status, payload = handle("GET", self.path, {}, self.service)
        self._respond(status, payload)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length) if length else b"{}"
        try:
            body = json.loads(raw or b"{}")
        except json.JSONDecodeError:
            self._respond(400, {"error": "request body is not valid JSON"})
            return
        status, payload = handle("POST", self.path, body, self.service)
        self._respond(status, payload)

    def log_message(self, *_: Any) -> None:
        return


def serve(host: str = "127.0.0.1", port: int = 8000) -> None:  # pragma: no cover
    """Start the HTTP service (blocking)."""

    handler = type("_BoundHandler", (_Handler,), {"service": RedTeamService()})
    server = ThreadingHTTPServer((host, port), handler)
    print(f"red-teaming service listening on http://{host}:{port}")
    server.serve_forever()
