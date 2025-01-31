# Shared Types

```python
from runloop_api_client.types import AfterIdle, CodeMountParameters, LaunchParameters
```

# Benchmarks

Types:

```python
from runloop_api_client.types import (
    BenchmarkCreateParameters,
    BenchmarkListView,
    BenchmarkRunListView,
    BenchmarkRunView,
    BenchmarkView,
    StartBenchmarkRunParameters,
)
```

Methods:

- <code title="post /v1/benchmarks">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">create</a>(\*\*<a href="src/runloop_api_client/types/benchmark_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_view.py">BenchmarkView</a></code>
- <code title="get /v1/benchmarks/{id}">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_view.py">BenchmarkView</a></code>
- <code title="get /v1/benchmarks">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">list</a>(\*\*<a href="src/runloop_api_client/types/benchmark_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_list_view.py">BenchmarkListView</a></code>
- <code title="post /v1/benchmarks/start_run">client.benchmarks.<a href="./src/runloop_api_client/resources/benchmarks/benchmarks.py">start_run</a>(\*\*<a href="src/runloop_api_client/types/benchmark_start_run_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>

## Runs

Methods:

- <code title="get /v1/benchmarks/runs/{id}">client.benchmarks.runs.<a href="./src/runloop_api_client/resources/benchmarks/runs.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>
- <code title="get /v1/benchmarks/runs">client.benchmarks.runs.<a href="./src/runloop_api_client/resources/benchmarks/runs.py">list</a>(\*\*<a href="src/runloop_api_client/types/benchmarks/run_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/benchmark_run_list_view.py">BenchmarkRunListView</a></code>
- <code title="post /v1/benchmarks/runs/{id}/complete">client.benchmarks.runs.<a href="./src/runloop_api_client/resources/benchmarks/runs.py">complete</a>(id) -> <a href="./src/runloop_api_client/types/benchmark_run_view.py">BenchmarkRunView</a></code>

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
    DevboxDeleteDiskSnapshotResponse,
    DevboxKeepAliveResponse,
    DevboxReadFileContentsResponse,
    DevboxUploadFileResponse,
)
```

Methods:

- <code title="post /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create</a>(\*\*<a href="src/runloop_api_client/types/devbox_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes/{id}">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">list</a>(\*\*<a href="src/runloop_api_client/types/devbox_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">SyncDevboxesCursorIDPage[DevboxView]</a></code>
- <code title="post /v1/devboxes/{id}/create_ssh_key">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create_ssh_key</a>(id) -> <a href="./src/runloop_api_client/types/devbox_create_ssh_key_response.py">DevboxCreateSSHKeyResponse</a></code>
- <code title="post /v1/devboxes/{id}/create_tunnel">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create_tunnel</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_create_tunnel_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_tunnel_view.py">DevboxTunnelView</a></code>
- <code title="post /v1/devboxes/disk_snapshots/{id}/delete">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">delete_disk_snapshot</a>(id) -> <a href="./src/runloop_api_client/types/devbox_delete_disk_snapshot_response.py">object</a></code>
- <code title="post /v1/devboxes/{id}/download_file">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">download_file</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_download_file_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /v1/devboxes/{id}/execute_async">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute_async</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_sync">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute_sync</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/keep_alive">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">keep_alive</a>(id) -> <a href="./src/runloop_api_client/types/devbox_keep_alive_response.py">object</a></code>
- <code title="get /v1/devboxes/disk_snapshots">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">list_disk_snapshots</a>(\*\*<a href="src/runloop_api_client/types/devbox_list_disk_snapshots_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">SyncDiskSnapshotsCursorIDPage[DevboxSnapshotView]</a></code>
- <code title="post /v1/devboxes/{id}/read_file_contents">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">read_file_contents</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_read_file_contents_params.py">params</a>) -> str</code>
- <code title="post /v1/devboxes/{id}/remove_tunnel">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">remove_tunnel</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_remove_tunnel_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_tunnel_view.py">DevboxTunnelView</a></code>
- <code title="post /v1/devboxes/{id}/resume">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">resume</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/shutdown">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">shutdown</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/snapshot_disk">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">snapshot_disk</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_snapshot_disk_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">DevboxSnapshotView</a></code>
- <code title="post /v1/devboxes/{id}/suspend">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">suspend</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/upload_file">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">upload_file</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_upload_file_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_upload_file_response.py">object</a></code>
- <code title="post /v1/devboxes/{id}/write_file_contents">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">write_file_contents</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_write_file_contents_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>

## Browsers

Types:

```python
from runloop_api_client.types.devboxes import BrowserView
```

Methods:

- <code title="post /v1/devboxes/browsers">client.devboxes.browsers.<a href="./src/runloop_api_client/resources/devboxes/browsers.py">create</a>() -> <a href="./src/runloop_api_client/types/devboxes/browser_view.py">BrowserView</a></code>

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
- <code title="post /v1/devboxes/{id}/lsp/code-actions">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">code_actions</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_code_actions_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/code_actions_response.py">object</a></code>
- <code title="post /v1/devboxes/{id}/lsp/diagnostics">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">diagnostics</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_diagnostics_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/diagnostics_response.py">DiagnosticsResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/document-symbols">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">document_symbols</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_document_symbols_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/document_symbol_response.py">object</a></code>
- <code title="post /v1/devboxes/{id}/lsp/file">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">file</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_file_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/file_contents_response.py">FileContentsResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/file-definition">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">file_definition</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_file_definition_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/file_definition_response.py">object</a></code>
- <code title="get /v1/devboxes/{id}/lsp/files">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">files</a>(id) -> <a href="./src/runloop_api_client/types/devboxes/lsp_files_response.py">LspFilesResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/formatting">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">formatting</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_formatting_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/formatting_response.py">object</a></code>
- <code title="post /v1/devboxes/{id}/lsp/get-code-actions-for-diagnostic">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">get_code_actions_for_diagnostic</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_get_code_actions_for_diagnostic_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/lsp_get_code_actions_for_diagnostic_response.py">LspGetCodeActionsForDiagnosticResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/get-code-segment-info">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">get_code_segment_info</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_get_code_segment_info_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/code_segment_info_response.py">CodeSegmentInfoResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/get-signature-help">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">get_signature_help</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_get_signature_help_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/signature_help_response.py">SignatureHelpResponse</a></code>
- <code title="get /v1/devboxes/{id}/lsp/health">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">health</a>(id) -> <a href="./src/runloop_api_client/types/devboxes/health_status_response.py">HealthStatusResponse</a></code>
- <code title="post /v1/devboxes/{id}/lsp/references">client.devboxes.lsp.<a href="./src/runloop_api_client/resources/devboxes/lsp.py">references</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/lsp_references_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devboxes/references_response.py">object</a></code>
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
    ScenarioCreateParameters,
    ScenarioEnvironment,
    ScenarioListView,
    ScenarioRunListView,
    ScenarioRunView,
    ScenarioView,
    ScoringContract,
    ScoringContractResultView,
    ScoringFunction,
    ScoringFunctionResultView,
    StartScenarioRunParameters,
)
```

Methods:

- <code title="post /v1/scenarios">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">create</a>(\*\*<a href="src/runloop_api_client/types/scenario_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_view.py">ScenarioView</a></code>
- <code title="get /v1/scenarios/{id}">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/scenario_view.py">ScenarioView</a></code>
- <code title="get /v1/scenarios">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">list</a>(\*\*<a href="src/runloop_api_client/types/scenario_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_list_view.py">ScenarioListView</a></code>
- <code title="post /v1/scenarios/start_run">client.scenarios.<a href="./src/runloop_api_client/resources/scenarios/scenarios.py">start_run</a>(\*\*<a href="src/runloop_api_client/types/scenario_start_run_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">ScenarioRunView</a></code>

## Runs

Methods:

- <code title="get /v1/scenarios/runs/{id}">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">ScenarioRunView</a></code>
- <code title="get /v1/scenarios/runs">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">list</a>(\*\*<a href="src/runloop_api_client/types/scenarios/run_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/scenario_run_list_view.py">ScenarioRunListView</a></code>
- <code title="post /v1/scenarios/runs/{id}/complete">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">complete</a>(id) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">ScenarioRunView</a></code>
- <code title="post /v1/scenarios/runs/{id}/score">client.scenarios.runs.<a href="./src/runloop_api_client/resources/scenarios/runs.py">score</a>(id) -> <a href="./src/runloop_api_client/types/scenario_run_view.py">ScenarioRunView</a></code>

# Repositories

Types:

```python
from runloop_api_client.types import (
    RepositoryConnectionListView,
    RepositoryConnectionView,
    RepositoryVersionDetails,
    RepositoryVersionListView,
    RepositoryDeleteResponse,
)
```

Methods:

- <code title="post /v1/repositories">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">create</a>(\*\*<a href="src/runloop_api_client/types/repository_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/repository_connection_view.py">RepositoryConnectionView</a></code>
- <code title="get /v1/repositories/{id}">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/repository_connection_view.py">RepositoryConnectionView</a></code>
- <code title="get /v1/repositories">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">list</a>(\*\*<a href="src/runloop_api_client/types/repository_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/repository_connection_view.py">SyncRepositoriesCursorIDPage[RepositoryConnectionView]</a></code>
- <code title="post /v1/repositories/{id}/delete">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">delete</a>(id) -> <a href="./src/runloop_api_client/types/repository_delete_response.py">object</a></code>
- <code title="get /v1/repositories/{id}/versions">client.repositories.<a href="./src/runloop_api_client/resources/repositories.py">versions</a>(id) -> <a href="./src/runloop_api_client/types/repository_version_list_view.py">RepositoryVersionListView</a></code>
