Runloop Python SDK Documentation
==================================

The Runloop Python SDK provides a Pythonic, object-oriented interface for managing
devboxes, blueprints, snapshots, storage objects, scenarios, benchmarks, and more.
The SDK offers both asynchronous and synchronous variants with identical interfaces.

Installation
------------

Install the SDK using pip:

.. code-block:: bash

   pip install runloop_api_client

Quick Start
-----------

.. code-block:: python

   import asyncio
   from runloop_api_client import AsyncRunloopSDK

   async def main():
       runloop = AsyncRunloopSDK()

       async with await runloop.devbox.create(name="my-devbox") as devbox:
           result = await devbox.cmd.exec("echo 'Hello from Runloop!'")
           print(await result.stdout())

   asyncio.run(main())

A synchronous variant is also available:

.. code-block:: python

   from runloop_api_client import RunloopSDK

   runloop = RunloopSDK()

   with runloop.devbox.create(name="my-devbox") as devbox:
       result = devbox.cmd.exec("echo 'Hello from Runloop!'")
       print(result.stdout())

.. toctree::
   :maxdepth: 2
   :caption: API Reference

   api/index

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
