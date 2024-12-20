# Shared Types

```python
from runloop_api_client.types import (
    AfterIdle,
    FunctionInvocationExecutionDetailView,
    LaunchParameters,
    ProjectLogsView,
)
```

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
- <code title="get /v1/blueprints">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">list</a>(\*\*<a href="src/runloop_api_client/types/blueprint_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_list_view.py">BlueprintListView</a></code>
- <code title="get /v1/blueprints/{id}/logs">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">logs</a>(id) -> <a href="./src/runloop_api_client/types/blueprint_build_logs_list_view.py">BlueprintBuildLogsListView</a></code>
- <code title="post /v1/blueprints/preview">client.blueprints.<a href="./src/runloop_api_client/resources/blueprints.py">preview</a>(\*\*<a href="src/runloop_api_client/types/blueprint_preview_params.py">params</a>) -> <a href="./src/runloop_api_client/types/blueprint_preview_view.py">BlueprintPreviewView</a></code>

# Code

Types:

```python
from runloop_api_client.types import CodeMountParameters
```

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
    DevboxKeepAliveResponse,
    DevboxReadFileContentsResponse,
    DevboxUploadFileResponse,
)
```

Methods:

- <code title="post /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create</a>(\*\*<a href="src/runloop_api_client/types/devbox_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes/{id}">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">list</a>(\*\*<a href="src/runloop_api_client/types/devbox_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_list_view.py">DevboxListView</a></code>
- <code title="post /v1/devboxes/{id}/create_ssh_key">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create_ssh_key</a>(id) -> <a href="./src/runloop_api_client/types/devbox_create_ssh_key_response.py">DevboxCreateSSHKeyResponse</a></code>
- <code title="post /v1/devboxes/{id}/create_tunnel">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create_tunnel</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_create_tunnel_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_tunnel_view.py">DevboxTunnelView</a></code>
- <code title="get /v1/devboxes/disk_snapshots">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">disk_snapshots</a>(\*\*<a href="src/runloop_api_client/types/devbox_disk_snapshots_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_list_view.py">DevboxSnapshotListView</a></code>
- <code title="post /v1/devboxes/{id}/download_file">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">download_file</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_download_file_params.py">params</a>) -> BinaryAPIResponse</code>
- <code title="post /v1/devboxes/{id}/execute_async">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute_async</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_sync">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute_sync</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/keep_alive">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">keep_alive</a>(id) -> <a href="./src/runloop_api_client/types/devbox_keep_alive_response.py">object</a></code>
- <code title="post /v1/devboxes/{id}/read_file_contents">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">read_file_contents</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_read_file_contents_params.py">params</a>) -> str</code>
- <code title="post /v1/devboxes/{id}/resume">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">resume</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/shutdown">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">shutdown</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/snapshot_disk">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">snapshot_disk</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_snapshot_disk_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_snapshot_view.py">DevboxSnapshotView</a></code>
- <code title="post /v1/devboxes/{id}/suspend">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">suspend</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="post /v1/devboxes/{id}/upload_file">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">upload_file</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_upload_file_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_upload_file_response.py">object</a></code>
- <code title="post /v1/devboxes/{id}/write_file">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">write_file</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_write_file_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>

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

- <code title="get /v1/devboxes/{id}/executions/{execution_id}">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">retrieve</a>(execution_id, \*, id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_retrieve_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_async">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">execute_async</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_execute_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/execute_sync">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">execute_sync</a>(id, \*\*<a href="src/runloop_api_client/types/devboxes/execution_execute_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/executions/{execution_id}/kill">client.devboxes.executions.<a href="./src/runloop_api_client/resources/devboxes/executions.py">kill</a>(execution_id, \*, id) -> <a href="./src/runloop_api_client/types/devbox_async_execution_detail_view.py">DevboxAsyncExecutionDetailView</a></code>

# Functions

Types:

```python
from runloop_api_client.types import FunctionListView
```

Methods:

- <code title="get /v1/functions">client.functions.<a href="./src/runloop_api_client/resources/functions/functions.py">list</a>() -> <a href="./src/runloop_api_client/types/function_list_view.py">FunctionListView</a></code>
- <code title="post /v1/functions/{project_name}/{function_name}/invoke_async">client.functions.<a href="./src/runloop_api_client/resources/functions/functions.py">invoke_async</a>(function_name, \*, project_name, \*\*<a href="src/runloop_api_client/types/function_invoke_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/shared/function_invocation_execution_detail_view.py">FunctionInvocationExecutionDetailView</a></code>
- <code title="post /v1/functions/{project_name}/{function_name}/invoke_sync">client.functions.<a href="./src/runloop_api_client/resources/functions/functions.py">invoke_sync</a>(function_name, \*, project_name, \*\*<a href="src/runloop_api_client/types/function_invoke_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/shared/function_invocation_execution_detail_view.py">FunctionInvocationExecutionDetailView</a></code>

## Invocations

Types:

```python
from runloop_api_client.types.functions import FunctionInvocationListView, KillOperationResponse
```

Methods:

- <code title="get /v1/functions/invocations/{invocationId}">client.functions.invocations.<a href="./src/runloop_api_client/resources/functions/invocations.py">retrieve</a>(invocation_id) -> <a href="./src/runloop_api_client/types/shared/function_invocation_execution_detail_view.py">FunctionInvocationExecutionDetailView</a></code>
- <code title="get /v1/functions/invocations">client.functions.invocations.<a href="./src/runloop_api_client/resources/functions/invocations.py">list</a>(\*\*<a href="src/runloop_api_client/types/functions/invocation_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/functions/function_invocation_list_view.py">FunctionInvocationListView</a></code>
- <code title="post /v1/functions/invocations/{invocationId}/kill">client.functions.invocations.<a href="./src/runloop_api_client/resources/functions/invocations.py">kill</a>(invocation_id) -> <a href="./src/runloop_api_client/types/functions/kill_operation_response.py">object</a></code>

# Projects

Types:

```python
from runloop_api_client.types import ProjectListView
```

Methods:

- <code title="get /v1/projects">client.projects.<a href="./src/runloop_api_client/resources/projects/projects.py">list</a>() -> <a href="./src/runloop_api_client/types/project_list_view.py">ProjectListView</a></code>

## Logs

Methods:

- <code title="get /v1/projects/{id}/logs">client.projects.logs.<a href="./src/runloop_api_client/resources/projects/logs.py">list</a>(id) -> <a href="./src/runloop_api_client/types/shared/project_logs_view.py">ProjectLogsView</a></code>
