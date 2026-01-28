# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union, Iterable, Optional
from typing_extensions import Literal, Required, TypeAlias, TypedDict

from .._types import SequenceNotStr

__all__ = [
    "BenchmarkJobCreateParams",
    "Spec",
    "SpecHarborJobSpec",
    "SpecBenchmarkDefinitionJobSpec",
    "SpecBenchmarkDefinitionJobSpecAgentConfig",
    "SpecBenchmarkDefinitionJobSpecAgentConfigAgentEnvironment",
    "SpecBenchmarkDefinitionJobSpecOrchestratorConfig",
    "SpecScenarioDefinitionJobSpec",
    "SpecScenarioDefinitionJobSpecAgentConfig",
    "SpecScenarioDefinitionJobSpecAgentConfigAgentEnvironment",
    "SpecScenarioDefinitionJobSpecOrchestratorConfig",
]


class BenchmarkJobCreateParams(TypedDict, total=False):
    name: Optional[str]
    """The name of the BenchmarkJob.

    If not provided, name will be generated based on target dataset.
    """

    spec: Optional[Spec]
    """The job specification. Exactly one spec type must be set."""


class SpecHarborJobSpec(TypedDict, total=False):
    """Harbor-based job specification with inline YAML configuration."""

    inline_yaml: Required[str]
    """The Harbor job configuration as inline YAML content."""

    type: Required[Literal["harbor"]]


class SpecBenchmarkDefinitionJobSpecAgentConfigAgentEnvironment(TypedDict, total=False):
    """Environment configuration to use for this agent"""

    environment_variables: Optional[Dict[str, str]]
    """Environment variables to set when launching the agent."""

    secrets: Optional[Dict[str, str]]
    """Secrets to inject as environment variables when launching the agent.

    Map of environment variable names to secret IDs.
    """


class SpecBenchmarkDefinitionJobSpecAgentConfig(TypedDict, total=False):
    """Configuration for an agent in a benchmark job"""

    name: Required[str]
    """Name of the agent"""

    type: Required[Literal["job_agent"]]

    agent_environment: Optional[SpecBenchmarkDefinitionJobSpecAgentConfigAgentEnvironment]
    """Environment configuration to use for this agent"""

    agent_id: Optional[str]
    """ID of the agent to use (optional if agent exists by name)"""

    kwargs: Optional[Dict[str, str]]
    """Additional kwargs for agent configuration"""

    model_name: Optional[str]
    """Model name override for this agent"""

    timeout_seconds: Optional[float]
    """Timeout in seconds for this agent"""


class SpecBenchmarkDefinitionJobSpecOrchestratorConfig(TypedDict, total=False):
    """Orchestrator configuration (optional overrides).

    If not provided, default values will be used.
    """

    n_attempts: Optional[int]
    """Number of retry attempts on failure (default: 0).

    This is the retry policy for failed scenarios. Default is 0.
    """

    n_concurrent_trials: Optional[int]
    """Number of concurrent trials to run (default: 1).

    Controls parallelism for scenario execution. Default is 1.
    """

    quiet: Optional[bool]
    """Suppress verbose output (default: false)"""

    timeout_multiplier: Optional[float]
    """Timeout multiplier for retries (default: 1.0).

    Each retry will multiply the timeout by this factor.
    """


class SpecBenchmarkDefinitionJobSpec(TypedDict, total=False):
    """Specifies a benchmark definition with runtime configuration.

    The benchmark definition's scenarios will be executed using the provided agent and orchestrator configurations.
    """

    agent_configs: Required[Iterable[SpecBenchmarkDefinitionJobSpecAgentConfig]]
    """Agent configurations to use for this run. Must specify at least one agent."""

    benchmark_id: Required[str]
    """ID of the benchmark definition to run.

    The scenarios from this benchmark will be executed.
    """

    type: Required[Literal["benchmark"]]

    orchestrator_config: Optional[SpecBenchmarkDefinitionJobSpecOrchestratorConfig]
    """Orchestrator configuration (optional overrides).

    If not provided, default values will be used.
    """


class SpecScenarioDefinitionJobSpecAgentConfigAgentEnvironment(TypedDict, total=False):
    """Environment configuration to use for this agent"""

    environment_variables: Optional[Dict[str, str]]
    """Environment variables to set when launching the agent."""

    secrets: Optional[Dict[str, str]]
    """Secrets to inject as environment variables when launching the agent.

    Map of environment variable names to secret IDs.
    """


class SpecScenarioDefinitionJobSpecAgentConfig(TypedDict, total=False):
    """Configuration for an agent in a benchmark job"""

    name: Required[str]
    """Name of the agent"""

    type: Required[Literal["job_agent"]]

    agent_environment: Optional[SpecScenarioDefinitionJobSpecAgentConfigAgentEnvironment]
    """Environment configuration to use for this agent"""

    agent_id: Optional[str]
    """ID of the agent to use (optional if agent exists by name)"""

    kwargs: Optional[Dict[str, str]]
    """Additional kwargs for agent configuration"""

    model_name: Optional[str]
    """Model name override for this agent"""

    timeout_seconds: Optional[float]
    """Timeout in seconds for this agent"""


class SpecScenarioDefinitionJobSpecOrchestratorConfig(TypedDict, total=False):
    """Orchestrator configuration (optional overrides).

    If not provided, default values will be used.
    """

    n_attempts: Optional[int]
    """Number of retry attempts on failure (default: 0).

    This is the retry policy for failed scenarios. Default is 0.
    """

    n_concurrent_trials: Optional[int]
    """Number of concurrent trials to run (default: 1).

    Controls parallelism for scenario execution. Default is 1.
    """

    quiet: Optional[bool]
    """Suppress verbose output (default: false)"""

    timeout_multiplier: Optional[float]
    """Timeout multiplier for retries (default: 1.0).

    Each retry will multiply the timeout by this factor.
    """


class SpecScenarioDefinitionJobSpec(TypedDict, total=False):
    """Specifies a set of scenarios with runtime configuration.

    The  scenarios will be executed using the provided agent and orchestrator configurations.
    """

    agent_configs: Required[Iterable[SpecScenarioDefinitionJobSpecAgentConfig]]
    """Agent configurations to use for this run. Must specify at least one agent."""

    scenario_ids: Required[SequenceNotStr[str]]
    """List of scenario IDs to execute"""

    type: Required[Literal["scenarios"]]

    orchestrator_config: Optional[SpecScenarioDefinitionJobSpecOrchestratorConfig]
    """Orchestrator configuration (optional overrides).

    If not provided, default values will be used.
    """


Spec: TypeAlias = Union[SpecHarborJobSpec, SpecBenchmarkDefinitionJobSpec, SpecScenarioDefinitionJobSpec]
