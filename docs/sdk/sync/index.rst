Synchronous SDK
===============

The synchronous SDK provides a blocking interface for managing devboxes, blueprints, snapshots, and storage objects. Use this variant when working in synchronous Python code.

Core Module
-----------

The core synchronous SDK module provides the main entry point and operation classes.

.. autoclass:: runloop_api_client.sdk.sync.RunloopSDK

.. automodule:: runloop_api_client.sdk.sync

Resource Modules
----------------

Synchronous resource classes for working with devboxes, blueprints, snapshots, and more.

.. toctree::
   :maxdepth: 1

   devbox
   execution
   execution_result
   blueprint
   snapshot
   storage_object

