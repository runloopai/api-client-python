# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["BenchmarkUpdateParams"]


class BenchmarkUpdateParams(TypedDict, total=False):
    attribution: Optional[str]
    """Attribution information for the benchmark. Pass in empty string to clear."""

    description: Optional[str]
    """Detailed description of the benchmark. Pass in empty string to clear."""

    metadata: Optional[Dict[str, str]]
    """User defined metadata to attach to the benchmark. Pass in empty map to clear."""

    name: Optional[str]
    """The unique name of the Benchmark. Cannot be blank."""

    required_environment_variables: Optional[SequenceNotStr[str]]
    """Environment variables required to run the benchmark.

    If any required variables are not supplied, the benchmark will fail to start.
    Pass in empty list to clear.
    """

    required_secret_names: Optional[SequenceNotStr[str]]
    """
    Secrets required to run the benchmark with (environment variable name will be
    mapped to the your user secret by name). If any of these secrets are not
    provided or the mapping is incorrect, the benchmark will fail to start. Pass in
    empty list to clear.
    """

    scenario_ids: Optional[SequenceNotStr[str]]
    """The Scenario IDs that make up the Benchmark. Pass in empty list to clear."""
