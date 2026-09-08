Core Module
===========

.. tabs::

   .. tab:: Async

      .. autoclass:: runloop_api_client.sdk.async_.AsyncRunloopSDK

      .. automodule:: runloop_api_client.sdk.async_

   .. tab:: Sync

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
