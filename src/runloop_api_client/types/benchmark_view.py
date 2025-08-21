# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional

from pydantic import Field as FieldInfo

from .._models import BaseModel

__all__ = ["BenchmarkView"]


class BenchmarkView(BaseModel):
    id: str
    """The ID of the Benchmark."""

    metadata: Dict[str, str]
    """User defined metadata to attach to the benchmark for organization."""

    name: str
    """The name of the Benchmark."""

    scenario_ids: List[str] = FieldInfo(alias="scenarioIds")
    """List of Scenario IDs that make up the benchmark."""

    attribution: Optional[str] = None
    """Attribution information for the benchmark."""

    description: Optional[str] = None
    """Detailed description of the benchmark."""

    is_public: Optional[bool] = None
    """Whether this benchmark is public."""

    required_environment_variables: Optional[List[str]] = None
    """Required environment variables used to run the benchmark.

    If any required environment variables are missing, the benchmark will fail to
    start.
    """

    required_secret_names: Optional[List[str]] = None
    """Required secrets used to run the benchmark.

    If any required secrets are missing, the benchmark will fail to start.
    """
