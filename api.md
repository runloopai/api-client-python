# Shared Types

```python
from runloop_api_client.types import AfterIdle, CodeMountParameters, LaunchParameters
```

# Benchmarks

Types:

```python
from runloop_api_client.types import (
    BenchmarkCreateParameters,
    BenchmarkRunListView,
    BenchmarkRunView,
    BenchmarkView,
    ScenarioDefinitionListView,
    StartBenchmarkRunParameters,
)
```

Methods:

- <code title="post /v1/benchmarks">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">create</a>(\*\*<a href="src/runloop_api_client/types/benchmark_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">BenchmarkView</a></code>
- <code title="get /v1/benchmarks/{id}">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_view.py">BenchmarkView</a></code>
- <code title="post /v1/benchmarks/{id}">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/benchmark_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">BenchmarkView</a></code>
- <code title="get /v1/benchmarks">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">list</a>(\*\*<a href="src/runloop_api_client/types/benchmark_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">SyncBenchmarksCursorIDPage[BenchmarkView]</a></code>
- <code title="get /v1/benchmarks/{id}/definitions">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">definitions</a>(id, \*\*<a href="src/runloop_api_client/types/benchmark_definitions_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_definition_list_view.py">ScenarioDefinitionListView</a></code>
- <code title="get /v1/benchmarks/list_public">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">list_public</a>(\*\*<a href="src/runloop_api_client/types/benchmark_list_public_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">SyncBenchmarksCursorIDPage[BenchmarkView]</a></code>
- <code title="post /v1/benchmarks/start_run">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">start_run</a>(\*\*<a href="src/runloop_api_client/types/benchmark_start_run_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>

## Runs

Methods:

- <code title="get /v1/benchmarks/runs/{id}">client.benchmarks.runs.<a href="./src/runloop_api_client/resources/benchmarks/runs.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>
- <code title="get /v1/benchmarks/runs">client.benchmarks.runs.<a href="./src/runloop_api_client/resources/benchmarks/runs.py">list</a>(\*\*<a href="src/runloop_api_client/types/benchmarks/run_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">SyncBenchmarkRunsCursorIDPage[BenchmarkRunView]</a></code>
- <code title="post /v1/benchmarks/runs/{id}/cancel">client.benchmarks.runs.<a href="./src/runloop_api_client/resources/benchmarks/runs.py">cancel</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>
- <code title="post /v1/benchmarks/runs/{id}/complete">client.benchmarks.runs.<a href="./src/runloop_api_client/resources/benchmarks/runs.py">complete</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>
- <code title="get /v1/benchmarks/runs/{id}/scenario_runs">client.benchmarks.runs.<a href="./src/runloop_api_client/resources/benchmarks/runs.py">list_scenario_runs</a>(id, \*\*<a href="src/runloop_api_client/types/benchmarks/run_list_scenario_runs_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">SyncBenchmarkRunsCursorIDPage[ScenarioRunView]</a></code>

# Blueprints

Types:

```python
from runloop_api_client.types import (
    BlueprintBuildLog,
    BlueprintBuildLogsListView,
    BlueprintBuildParameters,
    BlueprintListView,
    BlueprintPreviewView,
    BlueprintView,
)
```

Methods:

- <code title="post /v1/blueprints">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">create</a>(\*\*<a href="src/runloop_api_client/types/blueprint_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_view.py">BlueprintView</a></code>
- <code title="get /v1/blueprints/{id}">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/blueprint_view.py">BlueprintView</a></code>
- <code title="get /v1/blueprints">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">list</a>(\*\*<a href="src/runloop_api_client/types/blueprint_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_view.py">SyncBlueprintsCursorIDPage[BlueprintView]</a></code>
- <code title="post /v1/blueprints/{id}/delete">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">delete</a>(id) -> object</code>
- <code title="get /v1/blueprints/{id}/logs">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">logs</a>(id) -> <a href="./src/runloop_api_client/types/blueprint_build_logs_list_view.py">BlueprintBuildLogsListView</a></code>
- <code title="post /v1/blueprints/preview">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">preview</a>(\*\*<a href="src/runloop_api_client/types/blueprint_preview_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_preview_view.py">BlueprintPreviewView</a></code>

# Devboxes

Types:

```python
from runloop_api_client.types import (
    DevboxAsyncExecutionDetailView,
    DevboxExecutionDetailView,
    DevboxListView,
    DevboxSnapshotListView,
    DevboxSnapshotView,
    DevboxTunnelView,
    DevboxView,
    DevboxCreateSSHKeyResponse,
    DevboxReadFileContentsResponse,
)
```

Methods:

- <code title="post /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create</a>(\*\*<a href="src/runloop_api_client/types/devbox_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes/{id}">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">list</a>(\*\*<a href="src/runloop_api_client/types/devbox_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">SyncDevboxesCursorIDPage[DevboxView]</a></code>
- <code title="post /v1/devboxes/{id}/create_ssh_key">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create_ssh_key</a>(id) -> <a href="./src/runloop_api_client/types/devbox_create_ssh_key_response.py">DevboxCreateSSHKeyResponse</a></code>
- <code title="post /v1/devboxes/{id}/create_tunnel">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create_tunnel</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_create_tunnel_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_tunnel_view.py">DevboxTunnelView</a></code>
- <code title="post /v1/devboxes/disk_snapshots/{id}/delete">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">delete_disk_snapshot</a>(id) -> object</code>
- <code title="post /v1/devboxes/{id}/download_file">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">download_file</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_download_file_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /v1/devboxes/{id}/execute_async">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute_async</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_sync">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute_sync</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/keep_alive">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">keep_alive</a>(id) -> object</code>
- <code title="get /v1/devboxes/disk_snapshots">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">list_disk_snapshots</a>(\*\*<a href="src/runloop_api_client/types/devbox_list_disk_snapshots_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView]</a></code>
- <code title="post /v1/devboxes/{id}/read_file_contents">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">read_file_contents</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_read_file_contents_params.py">params</a>) -> str</code>
- <code title="post /v1/devboxes/{id}/remove_tunnel">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">remove_tunnel</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_remove_tunnel_params.py">params</a>) -> object</code>
- <code title="post /v1/devboxes/{id}/resume">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">resume</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/shutdown">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">shutdown</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/snapshot_disk">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">snapshot_disk</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_snapshot_disk_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">DevboxSnapshotView</a></code>
- <code title="post /v1/devboxes/{id}/snapshot_disk_async">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">snapshot_disk_async</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_snapshot_disk_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">DevboxSnapshotView</a></code>
- <code title="post /v1/devboxes/{id}/suspend">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">suspend</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/upload_file">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">upload_file</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_upload_file_params.py">params</a>) -> object</code>
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

## Browsers

Types:

```python
from runloop_api_client.types.devboxes import BrowserView
```

Methods:

- <code title="post /v1/devboxes/browsers">client.devboxes.browsers.<a href="./src/runloop_api_client/resources/devboxes/browsers.py">create</a>(\*\*<a href="src/runloop_api_client/types/devboxes/browser_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/browser_view.py">BrowserView</a></code>
- <code title="get /v1/devboxes/browsers/{id}">client.devboxes.browsers.<a href="./src/runloop_api_client/resources/devboxes/browsers.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/devboxes/browser_view.py">BrowserView</a></code>

## Computers

Types:

```python
from runloop_api_client.types.devboxes import (
    ComputerView,
    ComputerKeyboardInteractionResponse,
    ComputerMouseInteractionResponse,
    ComputerScreenInteractionResponse,
)
```

Methods:

- <code title="post /v1/devboxes/computers">client.devboxes.computers.<a href="./src/runloop_api_client/resources/devboxes/computers.py">create</a>(\*\*<a href="src/runloop_api_client/types/devboxes/computer_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/computer_view.py">ComputerView</a></code>
- <code title="get /v1/devboxes/computers/{id}">client.devboxes.computers.<a href="./src/runloop_api_client/resources/devboxes/computers.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/devboxes/computer_view.py">ComputerView</a></code>
- <code title="post /v1/devboxes/computers/{id}/keyboard_interaction">client.devboxes.computers.<a href="./src/runloop_api_client/resources/devboxes/computers.py">keyboard_interaction</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/computer_keyboard_interaction_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/computer_keyboard_interaction_response.py">ComputerKeyboardInteractionResponse</a></code>
- <code title="post /v1/devboxes/computers/{id}/mouse_interaction">client.devboxes.computers.<a href="./src/runloop_api_client/resources/devboxes/computers.py">mouse_interaction</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/computer_mouse_interaction_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/computer_mouse_interaction_response.py">ComputerMouseInteractionResponse</a></code>
- <code title="post /v1/devboxes/computers/{id}/screen_interaction">client.devboxes.computers.<a href="./src/runloop_api_client/resources/devboxes/computers.py">screen_interaction</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/computer_screen_interaction_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/computer_screen_interaction_response.py">ComputerScreenInteractionResponse</a></code>

## Lsp

Types:

```python
from runloop_api_client.types.devboxes import (
    BaseCodeAction,
    BaseCommand,
    BaseDiagnostic,
    BaseLocation,
    BaseMarkupContent,
    BaseParameterInformation,
    BaseRange,
    BaseSignature,
    BaseWorkspaceEdit,
    CodeActionApplicationResult,
    CodeActionContext,
    CodeActionKind,
    CodeActionsForDiagnosticRequestBody,
    CodeActionsRequestBody,
    CodeActionsResponse,
    CodeActionTriggerKind,
    CodeDescription,
    CodeSegmentInfoRequestBody,
    CodeSegmentInfoResponse,
    Diagnostic,
    DiagnosticRelatedInformation,
    DiagnosticSeverity,
    DiagnosticsResponse,
    DiagnosticTag,
    DocumentSymbol,
    DocumentSymbolResponse,
    DocumentUri,
    FileContentsResponse,
    FileDefinitionRequestBody,
    FileDefinitionResponse,
    FilePath,
    FileRequestBody,
    FileUri,
    FormattingResponse,
    HealthStatusResponse,
    Integer,
    Location,
    LSpAny,
    Position,
    Range,
    RecordStringTextEditArray,
    ReferencesRequestBody,
    ReferencesResponse,
    SetWatchDirectoryRequestBody,
    SignatureHelpRequestBody,
    SignatureHelpResponse,
    SymbolKind,
    SymbolTag,
    SymbolType,
    TextEdit,
    Uinteger,
    URi,
    WatchedFileResponse,
    LspFilesResponse,
    LspGetCodeActionsForDiagnosticResponse,
    LspSetWatchDirectoryResponse,
)
```

Methods:

- <code title="post /v1/devboxes/{id}/lsp/apply-code-action">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">apply_code_action</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_apply_code_action_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/code_action_application_result.py">CodeActionApplicationResult</a></code>
- <code title="post /v1/devboxes/{id}/lsp/code-actions">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">code_actions</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_code_actions_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/code_actions_response.py">CodeActionsResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/diagnostics">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">diagnostics</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_diagnostics_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/diagnostics_response.py">DiagnosticsResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/document-symbols">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">document_symbols</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_document_symbols_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/document_symbol_response.py">DocumentSymbolResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/file">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">file</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_file_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/file_contents_response.py">FileContentsResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/file-definition">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">file_definition</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_file_definition_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/file_definition_response.py">FileDefinitionResponse</a></code>
- <code title="get /v1/devboxes/{id}/lsp/files">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">files</a>(id) -> <a href="./src/runloop_api_client/types/devboxes/lsp_files_response.py">LspFilesResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/formatting">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">formatting</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_formatting_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/formatting_response.py">FormattingResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/get-code-actions-for-diagnostic">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">get_code_actions_for_diagnostic</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_get_code_actions_for_diagnostic_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/lsp_get_code_actions_for_diagnostic_response.py">LspGetCodeActionsForDiagnosticResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/get-code-segment-info">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">get_code_segment_info</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_get_code_segment_info_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/code_segment_info_response.py">CodeSegmentInfoResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/get-signature-help">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">get_signature_help</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_get_signature_help_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/signature_help_response.py">SignatureHelpResponse</a></code>
- <code title="get /v1/devboxes/{id}/lsp/health">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">health</a>(id) -> <a href="./src/runloop_api_client/types/devboxes/health_status_response.py">HealthStatusResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/references">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">references</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_references_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/references_response.py">ReferencesResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/set-watch-directory">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">set_watch_directory</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_set_watch_directory_params.py">params</a>) -> str</code>

## Logs

Types:

```python
from runloop_api_client.types.devboxes import DevboxLogsListView
```

Methods:

- <code title="get /v1/devboxes/{id}/logs">client.devboxes.logs.<a href="./src/runloop_api_client/resources/devboxes/logs.py">list</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/log_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/devbox_logs_list_view.py">DevboxLogsListView</a></code>

## Executions

Methods:

- <code title="get /v1/devboxes/{devbox_id}/executions/{execution_id}">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">retrieve</a>(execution_id, \*, devbox_id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_retrieve_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_async">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">execute_async</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_execute_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_sync">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">execute_sync</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_execute_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{devbox_id}/executions/{execution_id}/kill">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">kill</a>(execution_id, \*, devbox_id) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>

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
    ScorerValidateResponse,
)
```

Methods:

- <code title="post /v1/scenarios/scorers">client.scenarios.scorers.<a href="./src/runloop_api_client/resources/scenarios/scorers.py">create</a>(\*\*<a href="src/runloop_api_client/types/scenarios/scorer_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenarios/scorer_create_response.py">ScorerCreateResponse</a></code>
- <code title="get /v1/scenarios/scorers/{id}">client.scenarios.scorers.<a href="./src/runloop_api_client/resources/scenarios/scorers.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/scenarios/scorer_retrieve_response.py">ScorerRetrieveResponse</a></code>
- <code title="post /v1/scenarios/scorers/{id}">client.scenarios.scorers.<a href="./src/runloop_api_client/resources/scenarios/scorers.py">update</a>(id, \*\*<a href="src/runloop_api_client/types/scenarios/scorer_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenarios/scorer_update_response.py">ScorerUpdateResponse</a></code>
- <code title="get /v1/scenarios/scorers">client.scenarios.scorers.<a href="./src/runloop_api_client/resources/scenarios/scorers.py">list</a>(\*\*<a href="src/runloop_api_client/types/scenarios/scorer_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenarios/scorer_list_response.py">SyncScenarioScorersCursorIDPage[ScorerListResponse]</a></code>
- <code title="post /v1/scenarios/scorers/{id}/validate">client.scenarios.scorers.<a href="./src/runloop_api_client/resources/scenarios/scorers.py">validate</a>(id, \*\*<a href="src/runloop_api_client/types/scenarios/scorer_validate_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenarios/scorer_validate_response.py">ScorerValidateResponse</a></code>

# Repositories

Types:

```python
from runloop_api_client.types import (
    RepositoryConnectionListView,
    RepositoryConnectionView,
    RepositoryInspectionDetails,
    RepositoryInspectionListView,
    RepositoryManifestView,
)
```

Methods:

- <code title="post /v1/repositories">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">create</a>(\*\*<a href="src/runloop_api_client/types/repository_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/repository_connection_view.py">RepositoryConnectionView</a></code>
- <code title="get /v1/repositories/{id}">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/repository_connection_view.py">RepositoryConnectionView</a></code>
- <code title="get /v1/repositories">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">list</a>(\*\*<a href="src/runloop_api_client/types/repository_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/repository_connection_view.py">SyncRepositoriesCursorIDPage[RepositoryConnectionView]</a></code>
- <code title="post /v1/repositories/{id}/delete">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">delete</a>(id) -> object</code>
- <code title="get /v1/repositories/{id}/inspections">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">list_inspections</a>(id) -> <a href="./src/runloop_api_client/types/repository_inspection_list_view.py">RepositoryInspectionListView</a></code>
- <code title="post /v1/repositories/{id}/refresh">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">refresh</a>(id, \*\*<a href="src/runloop_api_client/types/repository_refresh_params.py">params</a>) -> object</code>

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
- <code title="post /v1/secrets/{name}">client.secrets.<a href="./src/runloop_api_client/resources/secrets.py">update</a>(name, \*\*<a href="src/runloop_api_client/types/secret_update_params.py">params</a>) -> <a href="./src/runloop_api_client/types/secret_view.py">SecretView</a></code>
- <code title="get /v1/secrets">client.secrets.<a href="./src/runloop_api_client/resources/secrets.py">list</a>() -> <a href="./src/runloop_api_client/types/secret_list_view.py">SecretListView</a></code>
- <code title="post /v1/secrets/{name}/delete">client.secrets.<a href="./src/runloop_api_client/resources/secrets.py">delete</a>(name) -> <a href="./src/runloop_api_client/types/secret_view.py">SecretView</a></code>
