# Shared Types

```python
from runloop_api_client.types import ProjectLogsView
```

# Account

Types:

```python
from runloop_api_client.types import ResourceSize
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
from runloop_api_client.types import DevboxExecutionDetailView, DevboxListView, DevboxView
```

Methods:

- <code title="post /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">create</a>(\*\*<a href="src/runloop_api_client/types/devbox_create_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes/{id}">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">retrieve</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">list</a>(\*\*<a href="src/runloop_api_client/types/devbox_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_list_view.py">DevboxListView</a></code>
- <code title="post /v1/devboxes/{id}/execute_sync">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">execute_sync</a>(id, \*\*<a href="src/runloop_api_client/types/devbox_execute_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/shutdown">client.devboxes.<a href="./src/runloop_api_client/resources/devboxes/devboxes.py">shutdown</a>(id) -> <a href="./src/runloop_api_client/types/devbox_view.py">DevboxView</a></code>

## Logs

Types:

```python
from runloop_api_client.types.devboxes import DevboxLogsListView
```

Methods:

- <code title="get /v1/devboxes/{id}/logs">client.devboxes.logs.<a href="./src/runloop_api_client/resources/devboxes/logs.py">list</a>(id) -> <a href="./src/runloop_api_client/types/devboxes/devbox_logs_list_view.py">DevboxLogsListView</a></code>

# Functions

Types:

```python
from runloop_api_client.types import (
    FunctionListView,
    FunctionInvokeAsyncResponse,
    FunctionInvokeSyncResponse,
)
```

Methods:

- <code title="get /v1/functions">client.functions.<a href="./src/runloop_api_client/resources/functions/functions.py">list</a>() -> <a href="./src/runloop_api_client/types/function_list_view.py">FunctionListView</a></code>
- <code title="post /v1/functions/{project_name}/{function_name}/invoke_async">client.functions.<a href="./src/runloop_api_client/resources/functions/functions.py">invoke_async</a>(function_name, \*, project_name, \*\*<a href="src/runloop_api_client/types/function_invoke_async_params.py">params</a>) -> <a href="./src/runloop_api_client/types/function_invoke_async_response.py">FunctionInvokeAsyncResponse</a></code>
- <code title="post /v1/functions/{project_name}/{function_name}/invoke_sync">client.functions.<a href="./src/runloop_api_client/resources/functions/functions.py">invoke_sync</a>(function_name, \*, project_name, \*\*<a href="src/runloop_api_client/types/function_invoke_sync_params.py">params</a>) -> <a href="./src/runloop_api_client/types/function_invoke_sync_response.py">FunctionInvokeSyncResponse</a></code>

## Invocations

Types:

```python
from runloop_api_client.types.functions import (
    FunctionInvocationListView,
    KillOperationResponse,
    InvocationRetrieveResponse,
)
```

Methods:

- <code title="get /v1/functions/invocations/{invocationId}">client.functions.invocations.<a href="./src/runloop_api_client/resources/functions/invocations/invocations.py">retrieve</a>(invocation_id) -> <a href="./src/runloop_api_client/types/functions/invocation_retrieve_response.py">InvocationRetrieveResponse</a></code>
- <code title="get /v1/functions/invocations">client.functions.invocations.<a href="./src/runloop_api_client/resources/functions/invocations/invocations.py">list</a>(\*\*<a href="src/runloop_api_client/types/functions/invocation_list_params.py">params</a>) -> <a href="./src/runloop_api_client/types/functions/function_invocation_list_view.py">FunctionInvocationListView</a></code>
- <code title="post /v1/functions/invocations/{invocationId}/kill">client.functions.invocations.<a href="./src/runloop_api_client/resources/functions/invocations/invocations.py">kill</a>(invocation_id) -> <a href="./src/runloop_api_client/types/functions/kill_operation_response.py">object</a></code>

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
