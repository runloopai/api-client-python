Core Module
===========

The core module provides the main SDK entry points and operation manager classes.
Use :class:`~runloop_api_client.sdk.async_.AsyncRunloopSDK` for async/await code or
:class:`~runloop_api_client.sdk.sync.RunloopSDK` for synchronous code.

Asynchronous API
----------------

.. autoclass:: runloop_api_client.sdk.async_.AsyncRunloopSDK

.. automodule:: runloop_api_client.sdk.async_

Synchronous API
---------------

.. autoclass:: runloop_api_client.sdk.sync.RunloopSDK

.. automodule:: runloop_api_client.sdk.sync

Base REST Client
----------------

The SDK wraps the generated REST client. The ``api`` attribute on
:class:`~runloop_api_client.sdk.async_.AsyncRunloopSDK` /
:class:`~runloop_api_client.sdk.sync.RunloopSDK` provides direct access.

.. autoclass:: runloop_api_client.AsyncRunloop
   :no-members:

.. autoclass:: runloop_api_client.Runloop
   :no-members:
