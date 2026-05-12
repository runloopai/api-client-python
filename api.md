# Shared Types

```python
from runloop_api_client.types import (
    AfterIdle,
    AgentMount,
    AgentSource,
    BrokerMount,
    CodeMountParameters,
    LaunchParameters,
    Mount,
    ObjectMount,
    RunProfile,
)
```

# Benchmarks

Types:

```python
from runloop_api_client.types import (
    BenchmarkCreateParameters,
    BenchmarkScenarioUpdateParameters,
    BenchmarkUpdateParameters,
    BenchmarkView,
    ScenarioDefinitionListView,
    StartBenchmarkRunParameters,
)
```

Methods:

- <code title="post /v1/benchmarks">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks.py">create</a>(\*\*<a href="src/runloop_api_client/types/benchmark_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">BenchmarkView</a></code>
- <code title="get /v1/benchmarks/{id}">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_view.py">BenchmarkView</a></code>
- <code title="post /v1/benchmarks/{id}">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/benchmark_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">BenchmarkView</a></code>
- <code title="get /v1/benchmarks">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks.py">list</a>(\*\*<a href="src/runloop_api_client/types/benchmark_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">SyncBenchmarksCursorIDPage[BenchmarkView]</a></code>
- <code title="get /v1/benchmarks/{id}/definitions">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks.py">definitions</a>(id, \*\*<a href="src/runloop_api_client/types/benchmark_definitions_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_definition_list_view.py">ScenarioDefinitionListView</a></code>
- <code title="get /v1/benchmarks/list_public">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks.py">list_public</a>(\*\*<a href="src/runloop_api_client/types/benchmark_list_public_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">SyncBenchmarksCursorIDPage[BenchmarkView]</a></code>
- <code title="post /v1/benchmarks/start_run">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks.py">start_run</a>(\*\*<a href="src/runloop_api_client/types/benchmark_start_run_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>
- <code title="post /v1/benchmarks/{id}/scenarios">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks.py">update_scenarios</a>(id, \*\*<a href="src/runloop_api_client/types/benchmark_update_scenarios_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">BenchmarkView</a></code>

# BenchmarkRuns

Types:

```python
from runloop_api_client.types import BenchmarkRunListView, BenchmarkRunView
```

Methods:

- <code title="get /v1/benchmark_runs/{id}">client.benchmark_runs.<a href="./src/runloop_api_client/resources/benchmark_runs.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>
- <code title="get /v1/benchmark_runs">client.benchmark_runs.<a href="./src/runloop_api_client/resources/benchmark_runs.py">list</a>(\*\*<a href="src/runloop_api_client/types/benchmark_run_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">SyncBenchmarkRunsCursorIDPage[BenchmarkRunView]</a></code>
- <code title="post /v1/benchmark_runs/{id}/cancel">client.benchmark_runs.<a href="./src/runloop_api_client/resources/benchmark_runs.py">cancel</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>
- <code title="post /v1/benchmark_runs/{id}/complete">client.benchmark_runs.<a href="./src/runloop_api_client/resources/benchmark_runs.py">complete</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>
- <code title="get /v1/benchmark_runs/{id}/scenario_runs">client.benchmark_runs.<a href="./src/runloop_api_client/resources/benchmark_runs.py">list_scenario_runs</a>(id, \*\*<a href="src/runloop_api_client/types/benchmark_run_list_scenario_runs_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">SyncBenchmarkRunsCursorIDPage[ScenarioRunView]</a></code>

# BenchmarkJobs

Types:

```python
from runloop_api_client.types import (
    BenchmarkJobCreateParameters,
    BenchmarkJobListView,
    BenchmarkJobView,
)
```

Methods:

- <code title="post /v1/benchmark_jobs">client.benchmark_jobs.<a href="./src/runloop_api_client/resources/benchmark_jobs.py">create</a>(\*\*<a href="src/runloop_api_client/types/benchmark_job_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_job_view.py">BenchmarkJobView</a></code>
- <code title="get /v1/benchmark_jobs/{id}">client.benchmark_jobs.<a href="./src/runloop_api_client/resources/benchmark_jobs.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_job_view.py">BenchmarkJobView</a></code>
- <code title="get /v1/benchmark_jobs">client.benchmark_jobs.<a href="./src/runloop_api_client/resources/benchmark_jobs.py">list</a>(\*\*<a href="src/runloop_api_client/types/benchmark_job_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_job_list_view.py">BenchmarkJobListView</a></code>

# Agents

Types:

```python
from runloop_api_client.types import (
    AgentCreateParameters,
    AgentDevboxCountsView,
    AgentListView,
    AgentView,
)
```

Methods:

- <code title="post /v1/agents">client.agents.<a href="./src/runloop_api_client/resources/agents.py">create</a>(\*\*<a href="src/runloop_api_client/types/agent_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/agent_view.py">AgentView</a></code>
- <code title="get /v1/agents/{id}">client.agents.<a href="./src/runloop_api_client/resources/agents.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/agent_view.py">AgentView</a></code>
- <code title="get /v1/agents">client.agents.<a href="./src/runloop_api_client/resources/agents.py">list</a>(\*\*<a href="src/runloop_api_client/types/agent_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/agent_view.py">SyncAgentsCursorIDPage[AgentView]</a></code>
- <code title="post /v1/agents/{id}/delete">client.agents.<a href="./src/runloop_api_client/resources/agents.py">delete</a>(id) -> object</code>
- <code title="get /v1/agents/devbox_counts">client.agents.<a href="./src/runloop_api_client/resources/agents.py">devbox_counts</a>() -> <a href="./src/runloop_api_client/types/agent_devbox_counts_view.py">AgentDevboxCountsView</a></code>
- <code title="get /v1/agents/list_public">client.agents.<a href="./src/runloop_api_client/resources/agents.py">list_public</a>(\*\*<a href="src/runloop_api_client/types/agent_list_public_params.py">params</a>) -> <a href="./src/runloop_api_client/types/agent_view.py">SyncAgentsCursorIDPage[AgentView]</a></code>

# Axons

Types:

```python
from runloop_api_client.types import (
    AxonCreateParams,
    AxonEventView,
    AxonListView,
    AxonView,
    PublishParams,
    PublishResultView,
)
```

Methods:

- <code title="post /v1/axons">client.axons.<a href="./src/runloop_api_client/resources/axons/axons.py">create</a>(\*\*<a href="src/runloop_api_client/types/axon_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/axon_view.py">AxonView</a></code>
- <code title="get /v1/axons/{id}">client.axons.<a href="./src/runloop_api_client/resources/axons/axons.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/axon_view.py">AxonView</a></code>
- <code title="get /v1/axons">client.axons.<a href="./src/runloop_api_client/resources/axons/axons.py">list</a>(\*\*<a href="src/runloop_api_client/types/axon_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/axon_view.py">SyncAxonsCursorIDPage[AxonView]</a></code>
- <code title="post /v1/axons/{id}/publish">client.axons.<a href="./src/runloop_api_client/resources/axons/axons.py">publish</a>(id, \*\*<a href="src/runloop_api_client/types/axon_publish_params.py">params</a>) -> <a href="./src/runloop_api_client/types/publish_result_view.py">PublishResultView</a></code>
- <code title="get /v1/axons/{id}/subscribe/sse">client.axons.<a href="./src/runloop_api_client/resources/axons/axons.py">subscribe_sse</a>(id, \*\*<a href="src/runloop_api_client/types/axon_subscribe_sse_params.py">params</a>) -> <a href="./src/runloop_api_client/types/axon_event_view.py">AxonEventView</a></code>

## Events

Types:

```python
from runloop_api_client.types.axons import AxonEventListView
```

Methods:

- <code title="get /v1/axons/{id}/events">client.axons.events.<a href="./src/runloop_api_client/resources/axons/events.py">list</a>(id, \*\*<a href="src/runloop_api_client/types/axons/event_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/axons/axon_event_list_view.py">AxonEventListView</a></code>

## Sql

Types:

```python
from runloop_api_client.types.axons import (
    SqlBatchParams,
    SqlBatchResultView,
    SqlColumnMetaView,
    SqlQueryResultView,
    SqlResultMetaView,
    SqlStatementParams,
    SqlStepErrorView,
    SqlStepResultView,
)
```

Methods:

- <code title="post /v1/axons/{id}/sql/batch">client.axons.sql.<a href="./src/runloop_api_client/resources/axons/sql.py">batch</a>(id, \*\*<a href="src/runloop_api_client/types/axons/sql_batch_params.py">params</a>) -> <a href="./src/runloop_api_client/types/axons/sql_batch_result_view.py">SqlBatchResultView</a></code>
- <code title="post /v1/axons/{id}/sql/query">client.axons.sql.<a href="./src/runloop_api_client/resources/axons/sql.py">query</a>(id, \*\*<a href="src/runloop_api_client/types/axons/sql_query_params.py">params</a>) -> <a href="./src/runloop_api_client/types/axons/sql_query_result_view.py">SqlQueryResultView</a></code>

# Blueprints

Types:

```python
from runloop_api_client.types import (
    BlueprintBuildFromInspectionParameters,
    BlueprintBuildLog,
    BlueprintBuildLogsListView,
    BlueprintBuildParameters,
    BlueprintListView,
    BlueprintPreviewView,
    BlueprintView,
    InspectionSource,
)
```

Methods:

- <code title="post /v1/blueprints">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">create</a>(\*\*<a href="src/runloop_api_client/types/blueprint_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_view.py">BlueprintView</a></code>
- <code title="get /v1/blueprints/{id}">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/blueprint_view.py">BlueprintView</a></code>
- <code title="get /v1/blueprints">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">list</a>(\*\*<a href="src/runloop_api_client/types/blueprint_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_view.py">SyncBlueprintsCursorIDPage[BlueprintView]</a></code>
- <code title="post /v1/blueprints/{id}/delete">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">delete</a>(id) -> object</code>
- <code title="post /v1/blueprints/create_from_inspection">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">create_from_inspection</a>(\*\*<a href="src/runloop_api_client/types/blueprint_create_from_inspection_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_view.py">BlueprintView</a></code>
- <code title="get /v1/blueprints/list_public">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">list_public</a>(\*\*<a href="src/runloop_api_client/types/blueprint_list_public_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_view.py">SyncBlueprintsCursorIDPage[BlueprintView]</a></code>
- <code title="get /v1/blueprints/{id}/logs">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">logs</a>(id) -> <a href="./src/runloop_api_client/types/blueprint_build_logs_list_view.py">BlueprintBuildLogsListView</a></code>
- <code title="post /v1/blueprints/preview">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">preview</a>(\*\*<a href="src/runloop_api_client/types/blueprint_preview_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_preview_view.py">BlueprintPreviewView</a></code>

# Devboxes

Types:

```python
from runloop_api_client.types import (
    DevboxAsyncExecutionDetailView,
    DevboxExecutionDetailView,
    DevboxKillExecutionRequest,
    DevboxListView,
    DevboxResourceUsageView,
    DevboxSendStdInRequest,
    DevboxSendStdInResult,
    DevboxSnapshotListView,
    DevboxSnapshotView,
    DevboxView,
    PtyTunnelView,
    TunnelView,
    DevboxCreateSSHKeyResponse,
    DevboxReadFileContentsResponse,
)
```

Methods:

- <code title="post /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create</a>(\*\*<a href="src/runloop_api_client/types/devbox_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes/{id}">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">list</a>(\*\*<a href="src/runloop_api_client/types/devbox_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">SyncDevboxesCursorIDPage[DevboxView]</a></code>
- <code title="post /v1/devboxes/{id}/create_pty_tunnel">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create_pty_tunnel</a>(id) -> <a href="./src/runloop_api_client/types/pty_tunnel_view.py">PtyTunnelView</a></code>
- <code title="post /v1/devboxes/{id}/create_ssh_key">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create_ssh_key</a>(id) -> <a href="./src/runloop_api_client/types/devbox_create_ssh_key_response.py">DevboxCreateSSHKeyResponse</a></code>
- <code title="post /v1/devboxes/disk_snapshots/{id}/delete">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">delete_disk_snapshot</a>(id) -> object</code>
- <code title="post /v1/devboxes/{id}/download_file">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">download_file</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_download_file_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /v1/devboxes/{id}/enable_tunnel">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">enable_tunnel</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_enable_tunnel_params.py">params</a>) -> <a href="./src/runloop_api_client/types/tunnel_view.py">TunnelView</a></code>
- <code title="post /v1/devboxes/{id}/execute">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_async">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute_async</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_sync">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute_sync</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/keep_alive">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">keep_alive</a>(id) -> object</code>
- <code title="get /v1/devboxes/disk_snapshots">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">list_disk_snapshots</a>(\*\*<a href="src/runloop_api_client/types/devbox_list_disk_snapshots_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView]</a></code>
- <code title="post /v1/devboxes/{id}/read_file_contents">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">read_file_contents</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_read_file_contents_params.py">params</a>) -> str</code>
- <code title="post /v1/devboxes/{id}/remove_tunnel">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">remove_tunnel</a>(id) -> object</code>
- <code title="post /v1/devboxes/{id}/resume">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">resume</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes/{id}/usage">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">retrieve_resource_usage</a>(id) -> <a href="./src/runloop_api_client/types/devbox_resource_usage_view.py">DevboxResourceUsageView</a></code>
- <code title="post /v1/devboxes/{id}/shutdown">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">shutdown</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_shutdown_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/snapshot_disk">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">snapshot_disk</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_snapshot_disk_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">DevboxSnapshotView</a></code>
- <code title="post /v1/devboxes/{id}/snapshot_disk_async">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">snapshot_disk_async</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_snapshot_disk_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">DevboxSnapshotView</a></code>
- <code title="post /v1/devboxes/{id}/suspend">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">suspend</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/upload_file">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">upload_file</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_upload_file_params.py">params</a>) -> object</code>
- <code title="post /v1/devboxes/{devbox_id}/executions/{execution_id}/wait_for_status">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">wait_for_command</a>(execution_id, \*, devbox_id, \*\*<a href="src/runloop_api_client/types/devbox_wait_for_command_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/write_file_contents">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">write_file_contents</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_write_file_contents_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>

## DiskSnapshots

Types:

```python
from runloop_api_client.types.devboxes import DevboxSnapshotAsyncStatusView
```

Methods:

- <code title="post /v1/devboxes/disk_snapshots/{id}">client.devboxes.disk_snapshots.<a href="./src/runloop_api_client/resources/devboxes/disk_snapshots.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/disk_snapshot_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">DevboxSnapshotView</a></code>
- <code title="get /v1/devboxes/disk_snapshots">client.devboxes.disk_snapshots.<a href="./src/runloop_api_client/resources/devboxes/disk_snapshots.py">list</a>(\*\*<a href="src/runloop_api_client/types/devboxes/disk_snapshot_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView]</a></code>
- <code title="post /v1/devboxes/disk_snapshots/{id}/delete">client.devboxes.disk_snapshots.<a href="./src/runloop_api_client/resources/devboxes/disk_snapshots.py">delete</a>(id) -> object</code>
- <code title="get /v1/devboxes/disk_snapshots/{id}/status">client.devboxes.disk_snapshots.<a href="./src/runloop_api_client/resources/devboxes/disk_snapshots.py">query_status</a>(id) -> <a href="./src/runloop_api_client/types/devboxes/devbox_snapshot_async_status_view.py">DevboxSnapshotAsyncStatusView</a></code>

## Logs

Types:

```python
from runloop_api_client.types.devboxes import DevboxLogsListView
```

Methods:

- <code title="get /v1/devboxes/{id}/logs">client.devboxes.logs.<a href="./src/runloop_api_client/resources/devboxes/logs.py">list</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/log_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/devbox_logs_list_view.py">DevboxLogsListView</a></code>

## Executions

Types:

```python
from runloop_api_client.types.devboxes import ExecutionUpdateChunk
```

Methods:

- <code title="get /v1/devboxes/{devbox_id}/executions/{execution_id}">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">retrieve</a>(execution_id, \*, devbox_id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_retrieve_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_async">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">execute_async</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_execute_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_sync">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">execute_sync</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_execute_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{devbox_id}/executions/{execution_id}/kill">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">kill</a>(execution_id, \*, devbox_id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_kill_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{devbox_id}/executions/{execution_id}/send_std_in">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">send_std_in</a>(execution_id, \*, devbox_id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_send_std_in_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_send_std_in_result.py">DevboxSendStdInResult</a></code>
- <code title="get /v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stderr_updates">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">stream_stderr_updates</a>(execution_id, \*, devbox_id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_stream_stderr_updates_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/execution_update_chunk.py">ExecutionUpdateChunk</a></code>
- <code title="get /v1/devboxes/{devbox_id}/executions/{execution_id}/stream_stdout_updates">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">stream_stdout_updates</a>(execution_id, \*, devbox_id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_stream_stdout_updates_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/execution_update_chunk.py">ExecutionUpdateChunk</a></code>

# Pty

Types:

```python
from runloop_api_client.types import PtyConnectView, PtyControlParameters, PtyControlResultView
```

Methods:

- <code title="get /pty/{session_name}">client.pty.<a href="./src/runloop_api_client/resources/pty.py">connect</a>(session_name, \*\*<a href="src/runloop_api_client/types/pty_connect_params.py">params</a>) -> <a href="./src/runloop_api_client/types/pty_connect_view.py">PtyConnectView</a></code>
- <code title="post /pty/{session_name}/control">client.pty.<a href="./src/runloop_api_client/resources/pty.py">control</a>(session_name, \*\*<a href="src/runloop_api_client/types/pty_control_params.py">params</a>) -> <a href="./src/runloop_api_client/types/pty_control_result_view.py">PtyControlResultView</a></code>

# Scenarios

Types:

```python
from runloop_api_client.types import (
    InputContext,
    InputContextUpdate,
    ScenarioCreateParameters,
    ScenarioEnvironment,
    ScenarioRunListView,
    ScenarioRunView,
    ScenarioUpdateParameters,
    ScenarioView,
    ScoringContract,
    ScoringContractResultView,
    ScoringContractUpdate,
    ScoringFunction,
    ScoringFunctionResultView,
    StartScenarioRunParameters,
)
```

Methods:

- <code title="post /v1/scenarios">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">create</a>(\*\*<a href="src/runloop_api_client/types/scenario_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_view.py">ScenarioView</a></code>
- <code title="get /v1/scenarios/{id}">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/scenario_view.py">ScenarioView</a></code>
- <code title="post /v1/scenarios/{id}">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/scenario_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_view.py">ScenarioView</a></code>
- <code title="get /v1/scenarios">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">list</a>(\*\*<a href="src/runloop_api_client/types/scenario_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_view.py">SyncScenariosCursorIDPage[ScenarioView]</a></code>
- <code title="post /v1/scenarios/{id}/archive">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">archive</a>(id) -> <a href="./src/runloop_api_client/types/scenario_view.py">ScenarioView</a></code>
- <code title="get /v1/scenarios/list_public">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">list_public</a>(\*\*<a href="src/runloop_api_client/types/scenario_list_public_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_view.py">SyncScenariosCursorIDPage[ScenarioView]</a></code>
- <code title="post /v1/scenarios/start_run">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">start_run</a>(\*\*<a href="src/runloop_api_client/types/scenario_start_run_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">ScenarioRunView</a></code>

## Runs

Methods:

- <code title="get /v1/scenarios/runs/{id}">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">ScenarioRunView</a></code>
- <code title="get /v1/scenarios/runs">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">list</a>(\*\*<a href="src/runloop_api_client/types/scenarios/run_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">SyncBenchmarkRunsCursorIDPage[ScenarioRunView]</a></code>
- <code title="post /v1/scenarios/runs/{id}/cancel">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">cancel</a>(id) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">ScenarioRunView</a></code>
- <code title="post /v1/scenarios/runs/{id}/complete">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">complete</a>(id) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">ScenarioRunView</a></code>
- <code title="post /v1/scenarios/runs/{id}/download_logs">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">download_logs</a>(id) -> BinaryAPIResponse</code>
- <code title="post /v1/scenarios/runs/{id}/score">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">score</a>(id) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">ScenarioRunView</a></code>

## Scorers

Types:

```python
from runloop_api_client.types.scenarios import (
    ScorerCreateResponse,
    ScorerRetrieveResponse,
    ScorerUpdateResponse,
    ScorerListResponse,
)
```

Methods:

- <code title="post /v1/scenarios/scorers">client.scenarios.scorers.<a href="./src/runloop_api_client/resources/scenarios/scorers.py">create</a>(\*\*<a href="src/runloop_api_client/types/scenarios/scorer_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenarios/scorer_create_response.py">ScorerCreateResponse</a></code>
- <code title="get /v1/scenarios/scorers/{id}">client.scenarios.scorers.<a href="./src/runloop_api_client/resources/scenarios/scorers.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/scenarios/scorer_retrieve_response.py">ScorerRetrieveResponse</a></code>
- <code title="post /v1/scenarios/scorers/{id}">client.scenarios.scorers.<a href="./src/runloop_api_client/resources/scenarios/scorers.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/scenarios/scorer_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenarios/scorer_update_response.py">ScorerUpdateResponse</a></code>
- <code title="get /v1/scenarios/scorers">client.scenarios.scorers.<a href="./src/runloop_api_client/resources/scenarios/scorers.py">list</a>(\*\*<a href="src/runloop_api_client/types/scenarios/scorer_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenarios/scorer_list_response.py">SyncScenarioScorersCursorIDPage[ScorerListResponse]</a></code>

# Objects

Types:

```python
from runloop_api_client.types import (
    ObjectCreateParameters,
    ObjectDownloadURLView,
    ObjectListView,
    ObjectView,
)
```

Methods:

- <code title="post /v1/objects">client.objects.<a href="./src/runloop_api_client/resources/objects.py">create</a>(\*\*<a href="src/runloop_api_client/types/object_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/object_view.py">ObjectView</a></code>
- <code title="get /v1/objects/{id}">client.objects.<a href="./src/runloop_api_client/resources/objects.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/object_view.py">ObjectView</a></code>
- <code title="get /v1/objects">client.objects.<a href="./src/runloop_api_client/resources/objects.py">list</a>(\*\*<a href="src/runloop_api_client/types/object_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/object_view.py">SyncObjectsCursorIDPage[ObjectView]</a></code>
- <code title="post /v1/objects/{id}/delete">client.objects.<a href="./src/runloop_api_client/resources/objects.py">delete</a>(id) -> <a href="./src/runloop_api_client/types/object_view.py">ObjectView</a></code>
- <code title="post /v1/objects/{id}/complete">client.objects.<a href="./src/runloop_api_client/resources/objects.py">complete</a>(id) -> <a href="./src/runloop_api_client/types/object_view.py">ObjectView</a></code>
- <code title="get /v1/objects/{id}/download">client.objects.<a href="./src/runloop_api_client/resources/objects.py">download</a>(id, \*\*<a href="src/runloop_api_client/types/object_download_params.py">params</a>) -> <a href="./src/runloop_api_client/types/object_download_url_view.py">ObjectDownloadURLView</a></code>
- <code title="get /v1/objects/list_public">client.objects.<a href="./src/runloop_api_client/resources/objects.py">list_public</a>(\*\*<a href="src/runloop_api_client/types/object_list_public_params.py">params</a>) -> <a href="./src/runloop_api_client/types/object_view.py">SyncObjectsCursorIDPage[ObjectView]</a></code>

# Secrets

Types:

```python
from runloop_api_client.types import (
    SecretCreateParameters,
    SecretListView,
    SecretUpdateParameters,
    SecretView,
)
```

Methods:

- <code title="post /v1/secrets">client.secrets.<a href="./src/runloop_api_client/resources/secrets.py">create</a>(\*\*<a href="src/runloop_api_client/types/secret_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/secret_view.py">SecretView</a></code>
- <code title="get /v1/secrets/{name}">client.secrets.<a href="./src/runloop_api_client/resources/secrets.py">retrieve</a>(name) -> <a href="./src/runloop_api_client/types/secret_view.py">SecretView</a></code>
- <code title="post /v1/secrets/{name}">client.secrets.<a href="./src/runloop_api_client/resources/secrets.py">update</a>(name, \*\*<a href="src/runloop_api_client/types/secret_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/secret_view.py">SecretView</a></code>
- <code title="get /v1/secrets">client.secrets.<a href="./src/runloop_api_client/resources/secrets.py">list</a>(\*\*<a href="src/runloop_api_client/types/secret_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/secret_list_view.py">SecretListView</a></code>
- <code title="post /v1/secrets/{name}/delete">client.secrets.<a href="./src/runloop_api_client/resources/secrets.py">delete</a>(name) -> <a href="./src/runloop_api_client/types/secret_view.py">SecretView</a></code>

# NetworkPolicies

Types:

```python
from runloop_api_client.types import (
    NetworkPolicyCreateParameters,
    NetworkPolicyListView,
    NetworkPolicyUpdateParameters,
    NetworkPolicyView,
)
```

Methods:

- <code title="post /v1/network-policies">client.network_policies.<a href="./src/runloop_api_client/resources/network_policies.py">create</a>(\*\*<a href="src/runloop_api_client/types/network_policy_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/network_policy_view.py">NetworkPolicyView</a></code>
- <code title="get /v1/network-policies/{id}">client.network_policies.<a href="./src/runloop_api_client/resources/network_policies.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/network_policy_view.py">NetworkPolicyView</a></code>
- <code title="post /v1/network-policies/{id}">client.network_policies.<a href="./src/runloop_api_client/resources/network_policies.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/network_policy_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/network_policy_view.py">NetworkPolicyView</a></code>
- <code title="get /v1/network-policies">client.network_policies.<a href="./src/runloop_api_client/resources/network_policies.py">list</a>(\*\*<a href="src/runloop_api_client/types/network_policy_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/network_policy_view.py">SyncNetworkPoliciesCursorIDPage[NetworkPolicyView]</a></code>
- <code title="post /v1/network-policies/{id}/delete">client.network_policies.<a href="./src/runloop_api_client/resources/network_policies.py">delete</a>(id) -> <a href="./src/runloop_api_client/types/network_policy_view.py">NetworkPolicyView</a></code>

# GatewayConfigs

Types:

```python
from runloop_api_client.types import (
    GatewayConfigCreateParameters,
    GatewayConfigListView,
    GatewayConfigUpdateParameters,
    GatewayConfigView,
)
```

Methods:

- <code title="post /v1/gateway-configs">client.gateway_configs.<a href="./src/runloop_api_client/resources/gateway_configs.py">create</a>(\*\*<a href="src/runloop_api_client/types/gateway_config_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/gateway_config_view.py">GatewayConfigView</a></code>
- <code title="get /v1/gateway-configs/{id}">client.gateway_configs.<a href="./src/runloop_api_client/resources/gateway_configs.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/gateway_config_view.py">GatewayConfigView</a></code>
- <code title="post /v1/gateway-configs/{id}">client.gateway_configs.<a href="./src/runloop_api_client/resources/gateway_configs.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/gateway_config_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/gateway_config_view.py">GatewayConfigView</a></code>
- <code title="get /v1/gateway-configs">client.gateway_configs.<a href="./src/runloop_api_client/resources/gateway_configs.py">list</a>(\*\*<a href="src/runloop_api_client/types/gateway_config_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/gateway_config_view.py">SyncGatewayConfigsCursorIDPage[GatewayConfigView]</a></code>
- <code title="post /v1/gateway-configs/{id}/delete">client.gateway_configs.<a href="./src/runloop_api_client/resources/gateway_configs.py">delete</a>(id) -> <a href="./src/runloop_api_client/types/gateway_config_view.py">GatewayConfigView</a></code>

# McpConfigs

Types:

```python
from runloop_api_client.types import (
    McpConfigCreateParameters,
    McpConfigListView,
    McpConfigUpdateParameters,
    McpConfigView,
)
```

Methods:

- <code title="post /v1/mcp-configs">client.mcp_configs.<a href="./src/runloop_api_client/resources/mcp_configs.py">create</a>(\*\*<a href="src/runloop_api_client/types/mcp_config_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/mcp_config_view.py">McpConfigView</a></code>
- <code title="get /v1/mcp-configs/{id}">client.mcp_configs.<a href="./src/runloop_api_client/resources/mcp_configs.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/mcp_config_view.py">McpConfigView</a></code>
- <code title="post /v1/mcp-configs/{id}">client.mcp_configs.<a href="./src/runloop_api_client/resources/mcp_configs.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/mcp_config_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/mcp_config_view.py">McpConfigView</a></code>
- <code title="get /v1/mcp-configs">client.mcp_configs.<a href="./src/runloop_api_client/resources/mcp_configs.py">list</a>(\*\*<a href="src/runloop_api_client/types/mcp_config_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/mcp_config_view.py">SyncMcpConfigsCursorIDPage[McpConfigView]</a></code>
- <code title="post /v1/mcp-configs/{id}/delete">client.mcp_configs.<a href="./src/runloop_api_client/resources/mcp_configs.py">delete</a>(id) -> <a href="./src/runloop_api_client/types/mcp_config_view.py">McpConfigView</a></code>

# Apikeys

Types:

```python
from runloop_api_client.types import APIKeyCreatedView, APIKeyCreateParameters
```

Methods:

- <code title="post /v1/apikeys">client.apikeys.<a href="./src/runloop_api_client/resources/apikeys.py">create</a>(\*\*<a href="src/runloop_api_client/types/apikey_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/api_key_created_view.py">APIKeyCreatedView</a></code>

# RestrictedKeys

Types:

```python
from runloop_api_client.types import (
    RestrictedKeyCreatedView,
    RestrictedKeyCreateParameters,
    ScopeEntryView,
)
```

Methods:

- <code title="post /v1/restricted_keys">client.restricted_keys.<a href="./src/runloop_api_client/resources/restricted_keys.py">create</a>(\*\*<a href="src/runloop_api_client/types/restricted_key_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/restricted_key_created_view.py">RestrictedKeyCreatedView</a></code>
