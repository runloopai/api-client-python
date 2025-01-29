# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["BenchmarkView"]


class BenchmarkView(BaseModel):
    id: str
    """The ID of the Benchmark."""

    name: str
    """The name of the Benchmark."""

    scenario_ids: List[str] = FieldInfo(alias="scenarioIds")
    """List of Scenario IDs that make up the benchmark."""
