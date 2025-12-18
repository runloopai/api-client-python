Runloop Python SDK Documentation
==================================

The Runloop Python SDK provides a Pythonic, object-oriented interface for managing
devboxes, blueprints, snapshots, and storage objects. The SDK offers both synchronous
and asynchronous variants to match your runtime requirements.

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   sdk/async/index
   sdk/sync/index
   sdk/types

Installation
------------

Install the SDK using pip:

.. code-block:: bash

   pip install runloop_api_client

Quick Start
-----------

Synchronous Example
~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   from runloop_api_client import RunloopSDK

   runloop = RunloopSDK()

   # Create a ready-to-use devbox
   with runloop.devbox.create(name="my-devbox") as devbox:
       result = devbox.cmd.exec("echo 'Hello from Runloop!'")
       print(result.stdout())

Asynchronous Example
~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

   import asyncio
   from runloop_api_client import AsyncRunloopSDK

   async def main():
       runloop = AsyncRunloopSDK()
       
       async with await runloop.devbox.create(name="my-devbox") as devbox:
           result = await devbox.cmd.exec("echo 'Hello from Runloop!'")
           print(await result.stdout())

   asyncio.run(main())

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

