Type Reference
==============

This page documents all TypeDict parameter types used throughout the SDK.

Core Request Options
--------------------

These TypeDicts define options for streaming, timeouts, polling, and other request configuration.

.. autotypeddict:: runloop_api_client.sdk._types.ExecuteStreamingCallbacks

.. autotypeddict:: runloop_api_client.sdk._types.RequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.LongRequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.PollingRequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.LongPollingRequestOptions

Devbox Parameters
-----------------

These TypeDicts define parameters for devbox creation, execution, file operations, network tunnels, and snapshots.

Creation Parameters
~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExtraCreateParams

Execution Parameters
~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExecuteParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExecuteAsyncParams

Listing Parameters
~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxListParams

File Operation Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxReadFileContentsParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxWriteFileContentsParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxDownloadFileParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxUploadFileParams

Network Tunnel Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxCreateTunnelParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxRemoveTunnelParams

Snapshot Parameters
~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxSnapshotDiskParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxSnapshotDiskAsyncParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDiskSnapshotListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDiskSnapshotUpdateParams

Blueprint Parameters
--------------------

These TypeDicts define parameters for blueprint creation and listing.

.. autotypeddict:: runloop_api_client.sdk._types.SDKBlueprintCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKBlueprintListParams

Storage Object Parameters
-------------------------

These TypeDicts define parameters for storage object creation, listing, and downloading.

.. autotypeddict:: runloop_api_client.sdk._types.SDKObjectCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKObjectListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKObjectDownloadParams
