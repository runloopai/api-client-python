from __future__ import annotations

from typing import Iterator

import pytest

from runloop_api_client import Runloop
from runloop_api_client.lib.polling import PollingConfig

from .utils import unique_name

pytestmark = [pytest.mark.smoketest]


@pytest.fixture(autouse=True, scope="module")
def _cleanup(client: Runloop) -> Iterator[None]:  # pyright: ignore[reportUnusedFunction]
    yield
    global _devbox_id
    if _devbox_id:
        try:
            client.devboxes.shutdown(_devbox_id)
        except Exception:
            pass


"""
Tests are run sequentially and can be dependent on each other. 
This is to avoid overloading resources and save efficiency.
"""
_scenario_id = None
_run_id = None
_devbox_id = None


@pytest.mark.timeout(30)
def test_create_scenario(client: Runloop) -> None:
    global _scenario_id
    scenario = client.scenarios.create(
        name=unique_name("scenario"),
        input_context={"problem_statement": "echo hello"},
        scoring_contract={
            "scoring_function_parameters": [
                {
                    "name": "cmd-zero",
                    "scorer": {"type": "command_scorer", "command": "true"},
                    "weight": 1,
                }
            ]
        },
    )
    _scenario_id = scenario.id


@pytest.mark.timeout(30)
def test_start_scenario_run_and_await_env_ready(client: Runloop) -> None:
    assert _scenario_id
    run = client.scenarios.start_run_and_await_env_ready(
        scenario_id=_scenario_id,
        polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60),
    )
    assert run.scenario_id == _scenario_id
    global _run_id, _devbox_id
    _run_id = run.id
    _devbox_id = run.devbox_id


@pytest.mark.timeout(30)
def test_score_and_complete_scenario_run(client: Runloop) -> None:
    assert _run_id
    scored = client.scenarios.runs.score_and_complete(
        _run_id, polling_config=PollingConfig(max_attempts=120, interval_seconds=5.0, timeout_seconds=20 * 60)
    )
    assert scored.state in {"completed", "scored", "running", "failed", "timeout", "canceled"}


@pytest.mark.timeout(30)
def test_create_benchmark_and_start_run(client: Runloop) -> None:
    assert _scenario_id
    benchmark = client.benchmarks.create(name=unique_name("benchmark"), scenario_ids=[_scenario_id])
    assert benchmark.id
    run = client.benchmarks.start_run(benchmark_id=benchmark.id)
    assert run.benchmark_id == benchmark.id
