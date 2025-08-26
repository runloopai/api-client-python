# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Optional
from typing_extensions import Required, TypedDict

__all__ = ["BenchmarkCreateParams"]


class BenchmarkCreateParams(TypedDict, total=False):
    name: Required[str]
    """The name of the Benchmark. This must be unique."""

    attribution: Optional[str]
    """Attribution information for the benchmark."""

    description: Optional[str]
    """Detailed description of the benchmark."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the benchmark for organization."""

    required_environment_variables: Optional[List[str]]
    """Environment variables required to run the benchmark.

    If any required variables are not supplied, the benchmark will fail to start
    """

    required_secret_names: List[str]
    """
    Secrets required to run the benchmark with (environment variable name will be
    mapped to the your user secret by name). If any of these secrets are not
    provided or the mapping is incorrect, the benchmark will fail to start.
    """

    scenario_ids: Optional[List[str]]
    """The Scenario IDs that make up the Benchmark."""
