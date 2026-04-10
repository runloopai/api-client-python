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
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExecuteParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxExecuteAsyncParams

File Operation Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxReadFileContentsParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxWriteFileContentsParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxDownloadFileParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxUploadFileParams

Network Tunnel Parameters
~~~~~~~~~~~~~~~~~~~~~~~~~

.. autotypeddict:: runloop_api_client.sdk._types.SDKDevboxEnableTunnelParams

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

Agent Parameters
----------------

These TypeDicts define parameters for agent creation and listing.

.. autotypeddict:: runloop_api_client.sdk._types.SDKAgentCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKAgentListParams

Scorer Parameters
-----------------

These TypeDicts define parameters for scorer creation, listing, and updating.

.. autotypeddict:: runloop_api_client.sdk._types.SDKScorerCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKScorerListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKScorerUpdateParams

Axon Parameters
---------------

These TypeDicts define parameters for axon creation, listing, publishing, and SQL operations.

.. autotypeddict:: runloop_api_client.sdk._types.SDKAxonCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKAxonListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKAxonPublishParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKAxonSqlQueryParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKAxonSqlBatchParams

Scenario Parameters
-------------------

These TypeDicts define parameters for scenario listing, updating, and running.

.. autotypeddict:: runloop_api_client.sdk._types.SDKScenarioListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKScenarioUpdateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKScenarioRunParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKScenarioRunAsyncParams

Benchmark Parameters
--------------------

These TypeDicts define parameters for benchmark creation, listing, updating, and running.

.. autotypeddict:: runloop_api_client.sdk._types.SDKBenchmarkCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKBenchmarkListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKBenchmarkUpdateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKBenchmarkStartRunParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKBenchmarkListRunsParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKBenchmarkRunListScenarioRunsParams

Network Policy Parameters
-------------------------

These TypeDicts define parameters for network policy creation, listing, and updating.

.. autotypeddict:: runloop_api_client.sdk._types.SDKNetworkPolicyCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKNetworkPolicyListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKNetworkPolicyUpdateParams

MCP Config Parameters
---------------------

These TypeDicts define parameters for MCP (Model Context Protocol) configuration creation, listing, and updating.

.. autotypeddict:: runloop_api_client.sdk._types.SDKMcpConfigCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKMcpConfigListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKMcpConfigUpdateParams

Gateway Config Parameters
-------------------------

These TypeDicts define parameters for gateway configuration creation, listing, and updating.

.. autotypeddict:: runloop_api_client.sdk._types.SDKGatewayConfigCreateParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKGatewayConfigListParams

.. autotypeddict:: runloop_api_client.sdk._types.SDKGatewayConfigUpdateParams

Core Request Options
--------------------

These TypeDicts define options for timeouts, idempotency, polling, and other low-level request configuration. All other TypeDicts in the SDK extend from one of these core types.

.. autotypeddict:: runloop_api_client.sdk._types.BaseRequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.LongRequestOptions

.. autoclass:: runloop_api_client.sdk._types.PollingConfig
   :members:
   :undoc-members:

.. autotypeddict:: runloop_api_client.sdk._types.PollingRequestOptions

.. autotypeddict:: runloop_api_client.sdk._types.LongPollingRequestOptions

Base API Type Reference
-----------------------

.. auto-all-types::
