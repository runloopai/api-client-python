# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, Annotated, TypeAlias

from pydantic import Field as FieldInfo

from .._utils import PropertyInfo
from .._models import BaseModel

__all__ = [
    "BenchmarkJobView",
    "BenchmarkOutcome",
    "BenchmarkOutcomeScenarioOutcome",
    "BenchmarkOutcomeScenarioOutcomeFailureReason",
    "InProgressRun",
    "InProgressRunAgentConfig",
    "InProgressRunAgentConfigExternalAPIAgentConfig",
    "InProgressRunAgentConfigJobAgentConfig",
    "InProgressRunAgentConfigJobAgentConfigAgentEnvironment",
    "JobSource",
    "JobSourceHarborJobSource",
    "JobSourceBenchmarkDefJobSource",
    "JobSourceScenariosJobSource",
    "JobSpec",
    "JobSpecAgentConfig",
    "JobSpecAgentConfigAgentEnvironment",
    "JobSpecOrchestratorConfig",
]


class BenchmarkOutcomeScenarioOutcomeFailureReason(BaseModel):
    """Failure information if the scenario failed or timed out.

    Contains exception type and message.
    """

    exception_message: str
    """The exception message providing context"""

    exception_type: str
    """The exception class name (e.g., 'TimeoutException', 'AgentTimeoutError')"""


class BenchmarkOutcomeScenarioOutcome(BaseModel):
    """
    Outcome data for a single scenario execution, including its final state and scoring results.
    """

    scenario_definition_id: str
    """The ID of the scenario definition that was executed."""

    scenario_name: str
    """The name of the scenario."""

    scenario_run_id: str
    """The ID of the scenario run."""

    state: Literal["COMPLETED", "FAILED", "TIMEOUT", "CANCELED"]
    """The final state of the scenario execution."""

    duration_ms: Optional[int] = None
    """Duration of the scenario execution in milliseconds."""

    failure_reason: Optional[BenchmarkOutcomeScenarioOutcomeFailureReason] = None
    """Failure information if the scenario failed or timed out.

    Contains exception type and message.
    """

    score: Optional[float] = None
    """The score achieved for this scenario (0.0 to 1.0).

    Only present if state is COMPLETED.
    """


class BenchmarkOutcome(BaseModel):
    """
    Outcome data for a single benchmark run within a benchmark job, representing results for one agent configuration.
    """

    agent_name: str
    """The name of the agent configuration used."""

    benchmark_run_id: str
    """The ID of the benchmark run."""

    n_completed: int
    """Number of scenarios that completed successfully."""

    n_failed: int
    """Number of scenarios that failed."""

    n_timeout: int
    """Number of scenarios that timed out."""

    scenario_outcomes: List[BenchmarkOutcomeScenarioOutcome]
    """Detailed outcomes for each scenario in this benchmark run."""

    average_score: Optional[float] = None
    """Average score across all completed scenarios (0.0 to 1.0)."""

    duration_ms: Optional[int] = None
    """Total duration of the benchmark run in milliseconds."""

    api_model_name: Optional[str] = FieldInfo(alias="model_name", default=None)
    """The model name used by the agent."""


class InProgressRunAgentConfigExternalAPIAgentConfig(BaseModel):
    """Configuration for externally-driven benchmark runs via API"""

    type: Literal["external_api"]

    info: Optional[str] = None
    """Placeholder for future external agent metadata"""


class InProgressRunAgentConfigJobAgentConfigAgentEnvironment(BaseModel):
    """Environment configuration to use for this agent"""

    environment_variables: Optional[Dict[str, str]] = None
    """Environment variables to set when launching the agent."""

    secrets: Optional[Dict[str, str]] = None
    """Secrets to inject as environment variables when launching the agent.

    Map of environment variable names to secret IDs.
    """


class InProgressRunAgentConfigJobAgentConfig(BaseModel):
    """Configuration for an agent in a benchmark job"""

    name: str
    """Name of the agent"""

    type: Literal["job_agent"]

    agent_environment: Optional[InProgressRunAgentConfigJobAgentConfigAgentEnvironment] = None
    """Environment configuration to use for this agent"""

    agent_id: Optional[str] = None
    """ID of the agent to use (optional if agent exists by name)"""

    kwargs: Optional[Dict[str, str]] = None
    """Additional kwargs for agent configuration"""

    api_model_name: Optional[str] = FieldInfo(alias="model_name", default=None)
    """Model name override for this agent"""

    timeout_seconds: Optional[float] = None
    """Timeout in seconds for this agent"""


InProgressRunAgentConfig: TypeAlias = Annotated[
    Union[InProgressRunAgentConfigExternalAPIAgentConfig, InProgressRunAgentConfigJobAgentConfig, None],
    PropertyInfo(discriminator="type"),
]


class InProgressRun(BaseModel):
    """
    A lightweight view of a benchmark run currently in progress, showing basic execution details without full outcome data.
    """

    benchmark_run_id: str
    """The ID of the benchmark run."""

    start_time_ms: int
    """Start time (Unix milliseconds)."""

    state: Literal["running", "canceled", "completed"]
    """The current state of the run."""

    agent_config: Optional[InProgressRunAgentConfig] = None
    """Agent configuration used for this run.

    Specifies whether the run was driven by an external API agent or a job-defined
    agent.
    """

    duration_ms: Optional[int] = None
    """Duration so far in milliseconds."""


class JobSourceHarborJobSource(BaseModel):
    """Harbor job source with inline YAML configuration"""

    inline_yaml: str
    """The Harbor job configuration as inline YAML content"""

    type: Literal["harbor"]


class JobSourceBenchmarkDefJobSource(BaseModel):
    """Benchmark definition job source"""

    benchmark_id: str
    """The ID of the benchmark definition"""

    type: Literal["benchmark"]

    benchmark_name: Optional[str] = None
    """Optional user-provided name for the benchmark definition"""


class JobSourceScenariosJobSource(BaseModel):
    """Scenarios job source with a list of scenario definition IDs"""

    scenario_ids: List[str]
    """List of scenario definition IDs to execute"""

    type: Literal["scenarios"]


JobSource: TypeAlias = Annotated[
    Union[JobSourceHarborJobSource, JobSourceBenchmarkDefJobSource, JobSourceScenariosJobSource, None],
    PropertyInfo(discriminator="type"),
]


class JobSpecAgentConfigAgentEnvironment(BaseModel):
    """Environment configuration to use for this agent"""

    environment_variables: Optional[Dict[str, str]] = None
    """Environment variables to set when launching the agent."""

    secrets: Optional[Dict[str, str]] = None
    """Secrets to inject as environment variables when launching the agent.

    Map of environment variable names to secret IDs.
    """


class JobSpecAgentConfig(BaseModel):
    """Configuration for an agent in a benchmark job"""

    name: str
    """Name of the agent"""

    type: Literal["job_agent"]

    agent_environment: Optional[JobSpecAgentConfigAgentEnvironment] = None
    """Environment configuration to use for this agent"""

    agent_id: Optional[str] = None
    """ID of the agent to use (optional if agent exists by name)"""

    kwargs: Optional[Dict[str, str]] = None
    """Additional kwargs for agent configuration"""

    api_model_name: Optional[str] = FieldInfo(alias="model_name", default=None)
    """Model name override for this agent"""

    timeout_seconds: Optional[float] = None
    """Timeout in seconds for this agent"""


class JobSpecOrchestratorConfig(BaseModel):
    """Orchestrator configuration"""

    n_attempts: Optional[int] = None
    """Number of retry attempts on failure (default: 0).

    This is the retry policy for failed scenarios. Default is 0.
    """

    n_concurrent_trials: Optional[int] = None
    """Number of concurrent trials to run (default: 1).

    Controls parallelism for scenario execution. Default is 1.
    """

    quiet: Optional[bool] = None
    """Suppress verbose output (default: false)"""

    timeout_multiplier: Optional[float] = None
    """Timeout multiplier for retries (default: 1.0).

    Each retry will multiply the timeout by this factor.
    """


class JobSpec(BaseModel):
    """The resolved job specification.

    Contains scenarios, agents, and orchestrator config.
    """

    agent_configs: List[JobSpecAgentConfig]
    """Agent configurations for this job"""

    scenario_ids: List[str]
    """List of scenario IDs to execute"""

    orchestrator_config: Optional[JobSpecOrchestratorConfig] = None
    """Orchestrator configuration"""


class BenchmarkJobView(BaseModel):
    """
    A BenchmarkJobView represents a benchmark job that runs a set of scenarios entirely on runloop.
    """

    id: str
    """The ID of the BenchmarkJob."""

    create_time_ms: int
    """Timestamp when job was created (Unix milliseconds)."""

    name: str
    """The unique name of the BenchmarkJob."""

    state: Literal["initializing", "queued", "running", "completed", "failed", "cancelled", "timeout"]
    """The current state of the benchmark job."""

    benchmark_outcomes: Optional[List[BenchmarkOutcome]] = None
    """Detailed outcome data for each benchmark run created by this job.

    Includes per-agent results and scenario-level details.
    """

    failure_reason: Optional[str] = None
    """Failure reason if job failed."""

    in_progress_runs: Optional[List[InProgressRun]] = None
    """Benchmark runs currently in progress for this job.

    Shows runs that have not yet completed.
    """

    job_source: Optional[JobSource] = None
    """The source configuration that was used to create this job.

    Either Harbor YAML or benchmark definition reference.
    """

    job_spec: Optional[JobSpec] = None
    """The resolved job specification.

    Contains scenarios, agents, and orchestrator config.
    """
