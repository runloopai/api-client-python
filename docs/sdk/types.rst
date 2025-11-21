Type Reference
==============

The Runloop Python SDK uses TypeDict objects for configuration parameters to the various API calls. This page documents the TypeDict objects used throughout the SDK.

Blueprint Parameters
--------------------

These TypeDicts define parameters for blueprint creation and listing.

.. autotypeddict:: runloop_api_client.sdk._types.SDKBlueprintCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKBlueprintListParams

Devbox Parameters
-----------------

These TypeDicts define parameters for devbox creation, listing, and operations.

Creation Parameters
~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxCreateFromImageParams

Listing Parameters
~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxListParams

Command Execution Parameters
~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExecuteParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExecuteAsyncParams

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
-------------------

These TypeDicts define parameters for snapshot creation, listing, and updating.

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxSnapshotDiskParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxSnapshotDiskAsyncParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDiskSnapshotListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDiskSnapshotUpdateParams

Storage Object Parameters
-------------------------

These TypeDicts define parameters for storage object creation, listing, and downloading.

.. autotypeddict:: runloop_api_client.sdk._types.SDKObjectCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKObjectListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKObjectDownloadParams

Core Request Options
--------------------

These TypeDicts define options for timeouts, idempotency, polling, and other low-level request configuration. All other TypeDicts in the SDK extend from one of these core types.

.. autotypeddict:: runloop_api_client.sdk._types.RequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.LongRequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.PollingRequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.LongPollingRequestOptions
