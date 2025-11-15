from typing import Union, Callable, Optional
from typing_extensions import TypedDict

from runloop_api_client.types.devboxes import DiskSnapshotUpdateParams

from .._types import Body, Query, Headers, Timeout, NotGiven
from ..lib.polling import PollingConfig
from ..types.devbox_list_params import DevboxListParams
from ..types.object_list_params import ObjectListParams
from ..types.devbox_create_params import DevboxCreateParams, DevboxBaseCreateParams
from ..types.object_create_params import ObjectCreateParams
from ..types.blueprint_list_params import BlueprintListParams
from ..types.object_download_params import ObjectDownloadParams
from ..types.blueprint_create_params import BlueprintCreateParams
from ..types.devbox_upload_file_params import DevboxUploadFileParams
from ..types.devbox_create_tunnel_params import DevboxCreateTunnelParams
from ..types.devbox_download_file_params import DevboxDownloadFileParams
from ..types.devbox_execute_async_params import DevboxExecuteAsyncParams
from ..types.devbox_remove_tunnel_params import DevboxRemoveTunnelParams
from ..types.devbox_snapshot_disk_params import DevboxSnapshotDiskParams
from ..types.devbox_read_file_contents_params import DevboxReadFileContentsParams
from ..types.devbox_write_file_contents_params import DevboxWriteFileContentsParams
from ..types.devboxes.disk_snapshot_list_params import DiskSnapshotListParams

LogCallback = Callable[[str], None]


class ExecuteStreamingCallbacks(TypedDict, total=False):
    stdout: Optional[LogCallback]
    """Callback invoked for each stdout log line"""

    stderr: Optional[LogCallback]
    """Callback invoked for each stderr log line"""

    output: Optional[LogCallback]
    """Callback invoked for all log lines (both stdout and stderr)"""


class RequestOptions(TypedDict, total=False):
    extra_headers: Optional[Headers]
    """Send extra headers"""

    extra_query: Optional[Query]
    """Add additional query parameters to the request"""

    extra_body: Optional[Body]
    """Add additional JSON properties to the request"""

    timeout: Union[float, Timeout, NotGiven, None]
    """Override the client-level default timeout for this request, in seconds"""


class LongRequestOptions(RequestOptions, total=False):
    idempotency_key: Optional[str]
    """Specify a custom idempotency key for this request"""


class PollingRequestOptions(RequestOptions, total=False):
    polling_config: Optional[PollingConfig]
    """Configuration for polling behavior"""


class LongPollingRequestOptions(LongRequestOptions, PollingRequestOptions):
    pass


class SDKDevboxCreateParams(DevboxCreateParams, LongPollingRequestOptions):
    pass


class SDKDevboxExtraCreateParams(DevboxBaseCreateParams, LongPollingRequestOptions):
    pass


class SDKDevboxExecuteParams(DevboxExecuteAsyncParams, ExecuteStreamingCallbacks, LongPollingRequestOptions):
    pass


class SDKDevboxExecuteAsyncParams(DevboxExecuteAsyncParams, ExecuteStreamingCallbacks, LongRequestOptions):
    pass


class SDKDevboxListParams(DevboxListParams, RequestOptions):
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


class SDKDevboxRemoveTunnelParams(DevboxRemoveTunnelParams, LongRequestOptions):
    pass


class SDKDevboxSnapshotDiskAsyncParams(DevboxSnapshotDiskParams, LongRequestOptions):
    pass


class SDKDevboxSnapshotDiskParams(DevboxSnapshotDiskParams, LongPollingRequestOptions):
    pass


class SDKDiskSnapshotListParams(DiskSnapshotListParams, RequestOptions):
    pass


class SDKDiskSnapshotUpdateParams(DiskSnapshotUpdateParams, LongRequestOptions):
    pass


class SDKBlueprintCreateParams(BlueprintCreateParams, LongPollingRequestOptions):
    pass


class SDKBlueprintListParams(BlueprintListParams, RequestOptions):
    pass


class SDKObjectListParams(ObjectListParams, RequestOptions):
    pass


class SDKObjectCreateParams(ObjectCreateParams, LongRequestOptions):
    pass


class SDKObjectDownloadParams(ObjectDownloadParams, RequestOptions):
    pass
