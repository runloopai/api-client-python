# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import Required, TypedDict

__all__ = ["ScenarioStartRunParams"]


class ScenarioStartRunParams(TypedDict, total=False):
    scenario_id: Required[str]
    """ID of the Scenario to run."""

    benchmark_run_id: Optional[str]
    """Benchmark to associate the run."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the run for organization."""

    run_name: Optional[str]
    """Display name of the run."""
