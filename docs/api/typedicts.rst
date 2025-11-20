TypedDict Reference
===================

This page documents all TypedDict parameter types used throughout the SDK.
These typed dictionaries define the structure of parameters passed to SDK methods.

SDK TypedDicts
--------------

These are the primary TypedDict classes used in SDK methods, combining multiple
parameter types and options.

Core Request Options
~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.ExecuteStreamingCallbacks

.. autotypeddict:: runloop_api_client.sdk._types.RequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.LongRequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.PollingRequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.LongPollingRequestOptions

Devbox Parameters
~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExtraCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExecuteParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExecuteAsyncParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxListParams

File Operation Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxReadFileContentsParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxWriteFileContentsParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxDownloadFileParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxUploadFileParams

Network Operation Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxCreateTunnelParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxRemoveTunnelParams

Snapshot Parameters
~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxSnapshotDiskParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxSnapshotDiskAsyncParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDiskSnapshotListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDiskSnapshotUpdateParams

Blueprint Parameters
~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKBlueprintCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKBlueprintListParams

Storage Object Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKObjectCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKObjectListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKObjectDownloadParams
