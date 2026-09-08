API Reference
=============

The Runloop Python SDK provides both synchronous and asynchronous variants for every resource.
Each page below documents both variants together. The async API mirrors the sync API exactly,
with ``await`` required on all methods.

.. toctree::
   :maxdepth: 1
   :caption: Compute & Execution

   core
   devbox
   execution
   execution_result
   blueprint
   snapshot
   storage_object

.. toctree::
   :maxdepth: 1
   :caption: Agents & Evaluation

   agent
   scorer
   scenario
   scenario_builder
   scenario_run
   benchmark
   benchmark_run

.. toctree::
   :maxdepth: 1
   :caption: Communication

   axon

.. toctree::
   :maxdepth: 1
   :caption: Security & Configuration

   secret
   mcp_config
   gateway_config
   network_policy

.. toctree::
   :maxdepth: 1
   :caption: Type Reference

   types
