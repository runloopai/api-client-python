from typing import Union, Callable, Optional
from typing_extensions import TypedDict

from ..types import (
    AxonListParams,
    AgentListParams,
    AxonCreateParams,
    DevboxListParams,
    ObjectListParams,
    AgentCreateParams,
    AxonPublishParams,
    DevboxCreateParams,
    ObjectCreateParams,
    BlueprintListParams,
    McpConfigListParams,
    ObjectDownloadParams,
    AgentListPublicParams,
    BlueprintCreateParams,
    McpConfigCreateParams,
    McpConfigUpdateParams,
    DevboxUploadFileParams,
    GatewayConfigListParams,
    NetworkPolicyListParams,
    DevboxDownloadFileParams,
    DevboxEnableTunnelParams,
    DevboxSnapshotDiskParams,
    GatewayConfigCreateParams,
    GatewayConfigUpdateParams,
    NetworkPolicyCreateParams,
    NetworkPolicyUpdateParams,
    DevboxReadFileContentsParams,
    DevboxWriteFileContentsParams,
)
from .._types import Body, Query, Headers, Timeout, NotGiven
from ..lib.polling import PollingConfig
from ..types.devboxes import DiskSnapshotListParams, DiskSnapshotUpdateParams
from ..types.devbox_create_params import DevboxBaseCreateParams
from ..types.axons.sql_batch_params import SqlBatchParams
from ..types.axons.sql_query_params import SqlQueryParams
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


class SDKDevboxEnableTunnelParams(DevboxEnableTunnelParams, LongRequestOptions):
    pass


class SDKDevboxRemoveTunnelParams(LongRequestOptions):
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


class SDKAgentCreateParams(AgentCreateParams, LongRequestOptions):
    pass


class SDKAgentListParams(AgentListParams, BaseRequestOptions):
    pass


class SDKAgentListPublicParams(AgentListPublicParams, BaseRequestOptions):
    pass


class SDKAxonListParams(AxonListParams, BaseRequestOptions):
    pass


class SDKAxonCreateParams(AxonCreateParams, LongRequestOptions):
    pass


class SDKAxonPublishParams(AxonPublishParams, LongRequestOptions):
    pass


class SDKAxonSqlQueryParams(SqlQueryParams, LongRequestOptions):
    pass


class SDKAxonSqlBatchParams(SqlBatchParams, LongRequestOptions):
    pass


class SDKNetworkPolicyCreateParams(NetworkPolicyCreateParams, LongRequestOptions):
    pass


class SDKNetworkPolicyListParams(NetworkPolicyListParams, BaseRequestOptions):
    pass


class SDKNetworkPolicyUpdateParams(NetworkPolicyUpdateParams, LongRequestOptions):
    pass


class SDKMcpConfigCreateParams(McpConfigCreateParams, LongRequestOptions):
    pass


class SDKMcpConfigListParams(McpConfigListParams, BaseRequestOptions):
    pass


class SDKMcpConfigUpdateParams(McpConfigUpdateParams, LongRequestOptions):
    pass


class SDKGatewayConfigCreateParams(GatewayConfigCreateParams, LongRequestOptions):
    pass


class SDKGatewayConfigListParams(GatewayConfigListParams, BaseRequestOptions):
    pass


class SDKGatewayConfigUpdateParams(GatewayConfigUpdateParams, LongRequestOptions):
    pass
