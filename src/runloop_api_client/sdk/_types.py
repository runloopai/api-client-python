from typing import Union, Callable, Optional
from typing_extensions import TypedDict

from ..types import (
    InputContext,
    ScenarioView,
    AgentListParams,
    DevboxListParams,
    ObjectListParams,
    AgentCreateParams,
    DevboxCreateParams,
    ObjectCreateParams,
    ScenarioListParams,
    BenchmarkListParams,
    BlueprintListParams,
    ObjectDownloadParams,
    ScenarioUpdateParams,
    BenchmarkCreateParams,
    BenchmarkUpdateParams,
    BlueprintCreateParams,
    DevboxUploadFileParams,
    NetworkPolicyListParams,
    DevboxCreateTunnelParams,
    DevboxDownloadFileParams,
    DevboxEnableTunnelParams,
    DevboxRemoveTunnelParams,
    DevboxSnapshotDiskParams,
    NetworkPolicyCreateParams,
    NetworkPolicyUpdateParams,
    DevboxReadFileContentsParams,
    DevboxWriteFileContentsParams,
    BenchmarkRunListScenarioRunsParams,
)
from .._types import Body, Query, Headers, Timeout, NotGiven
from ..lib.polling import PollingConfig
from ..types.devboxes import DiskSnapshotListParams, DiskSnapshotUpdateParams
from ..types.scenarios import ScorerListParams, ScorerCreateParams, ScorerUpdateParams, ScorerValidateParams
from ..types.devbox_create_params import DevboxBaseCreateParams
from ..types.scenario_start_run_params import ScenarioStartRunBaseParams
from ..types.benchmark_start_run_params import BenchmarkSelfStartRunParams
from ..types.devbox_execute_async_params import DevboxNiceExecuteAsyncParams

LogCallback = Callable[[str], None]


class ExecuteStreamingCallbacks(TypedDict, total=False):
    stdout: Optional[LogCallback]
    """Callback invoked for each stdout log line"""

    stderr: Optional[LogCallback]
    """Callback invoked for each stderr log line"""

    output: Optional[LogCallback]
    """Callback invoked for all log lines (both stdout and stderr)"""


class BaseRequestOptions(TypedDict, total=False):
    extra_headers: Optional[Headers]
    """Send extra headers"""

    extra_query: Optional[Query]
    """Add additional query parameters to the request"""

    extra_body: Optional[Body]
    """Add additional JSON properties to the request"""

    timeout: Union[float, Timeout, NotGiven, None]
    """Override the client-level default timeout for this request, in seconds"""


class LongRequestOptions(BaseRequestOptions, total=False):
    idempotency_key: Optional[str]
    """Specify a custom idempotency key for this request"""


class PollingRequestOptions(BaseRequestOptions, total=False):
    polling_config: Optional[PollingConfig]
    """Configuration for polling behavior"""


class LongPollingRequestOptions(LongRequestOptions, PollingRequestOptions):  # type: ignore[misc]
    pass


class SDKDevboxCreateParams(DevboxCreateParams, LongPollingRequestOptions):
    pass


class SDKDevboxCreateFromImageParams(DevboxBaseCreateParams, LongPollingRequestOptions):
    pass


class SDKDevboxExecuteParams(DevboxNiceExecuteAsyncParams, ExecuteStreamingCallbacks, LongPollingRequestOptions):
    pass


class SDKDevboxExecuteAsyncParams(DevboxNiceExecuteAsyncParams, ExecuteStreamingCallbacks, LongRequestOptions):
    pass


class SDKDevboxListParams(DevboxListParams, BaseRequestOptions):
    pass


class SDKDevboxReadFileContentsParams(DevboxReadFileContentsParams, LongRequestOptions):
    pass


class SDKDevboxWriteFileContentsParams(DevboxWriteFileContentsParams, LongRequestOptions):
    pass


class SDKDevboxDownloadFileParams(DevboxDownloadFileParams, LongRequestOptions):
    pass


class SDKDevboxUploadFileParams(DevboxUploadFileParams, LongRequestOptions):
    pass


class SDKDevboxCreateTunnelParams(DevboxCreateTunnelParams, LongRequestOptions):
    pass


class SDKDevboxEnableTunnelParams(DevboxEnableTunnelParams, LongRequestOptions):
    pass


class SDKDevboxRemoveTunnelParams(DevboxRemoveTunnelParams, LongRequestOptions):
    pass


class SDKDevboxSnapshotDiskAsyncParams(DevboxSnapshotDiskParams, LongRequestOptions):
    pass


class SDKDevboxSnapshotDiskParams(DevboxSnapshotDiskParams, LongPollingRequestOptions):
    pass


class SDKDiskSnapshotListParams(DiskSnapshotListParams, BaseRequestOptions):
    pass


class SDKDiskSnapshotUpdateParams(DiskSnapshotUpdateParams, LongRequestOptions):
    pass


class SDKBlueprintCreateParams(BlueprintCreateParams, LongPollingRequestOptions):
    pass


class SDKBlueprintListParams(BlueprintListParams, BaseRequestOptions):
    pass


class SDKObjectListParams(ObjectListParams, BaseRequestOptions):
    pass


class SDKObjectCreateParams(ObjectCreateParams, LongRequestOptions):
    pass


class SDKObjectDownloadParams(ObjectDownloadParams, BaseRequestOptions):
    pass


class SDKScorerCreateParams(ScorerCreateParams, LongRequestOptions):
    pass


class SDKScorerListParams(ScorerListParams, BaseRequestOptions):
    pass


class SDKScorerUpdateParams(ScorerUpdateParams, LongRequestOptions):
    pass


class SDKScorerValidateParams(ScorerValidateParams, LongRequestOptions):
    pass


class SDKAgentCreateParams(AgentCreateParams, LongRequestOptions):
    pass


class SDKAgentListParams(AgentListParams, BaseRequestOptions):
    pass


class SDKScenarioListParams(ScenarioListParams, BaseRequestOptions):
    pass


class SDKScenarioUpdateParams(ScenarioUpdateParams, LongRequestOptions):
    pass


class SDKScenarioRunAsyncParams(ScenarioStartRunBaseParams, LongRequestOptions):
    pass


class SDKScenarioRunParams(ScenarioStartRunBaseParams, LongPollingRequestOptions):
    pass


class InputContextPreview(InputContext):
    problem_statement: Optional[str] = None  # type: ignore[assignment]
    """The problem statement for the Scenario."""


class ScenarioPreview(ScenarioView):
    """Preview of scenario configuration with all fields optional."""

    id: Optional[str] = None  # type: ignore[assignment]
    """The ID of the Scenario."""

    input_context: InputContextPreview  # type: ignore[assignment]
    """The input context for the Scenario."""


class SDKBenchmarkCreateParams(BenchmarkCreateParams, LongRequestOptions):
    pass


class SDKBenchmarkListParams(BenchmarkListParams, BaseRequestOptions):
    pass


class SDKBenchmarkUpdateParams(BenchmarkUpdateParams, LongRequestOptions):
    pass


class SDKBenchmarkStartRunParams(BenchmarkSelfStartRunParams, LongRequestOptions):
    pass


class SDKBenchmarkListRunsParams(BaseRequestOptions, total=False):
    limit: int
    """The limit of items to return. Default is 20. Max is 5000."""

    name: str
    """Filter by name"""

    starting_after: str
    """Load the next page of data starting after the item with the given ID."""


class SDKBenchmarkRunListScenarioRunsParams(BenchmarkRunListScenarioRunsParams, BaseRequestOptions):
    pass


class SDKNetworkPolicyCreateParams(NetworkPolicyCreateParams, LongRequestOptions):
    pass


class SDKNetworkPolicyListParams(NetworkPolicyListParams, BaseRequestOptions):
    pass


class SDKNetworkPolicyUpdateParams(NetworkPolicyUpdateParams, LongRequestOptions):
    pass
