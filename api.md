# Shared Types

```python
from runloop.types import EmptyRecord, FunctionInvocationDetailView, ProjectLogsView
```

# CodeHandles

Types:

```python
from runloop.types import CodeHandleListView, CodeHandleView
```

Methods:

- <code title="post /v1/code_handles">client.code_handles.<a href="./src/runloop/resources/code_handles.py">create</a>(\*\*<a href="src/runloop/types/code_handle_create_params.py">params</a>) -> <a href="./src/runloop/types/code_handle_view.py">CodeHandleView</a></code>
- <code title="get /v1/code_handles">client.code_handles.<a href="./src/runloop/resources/code_handles.py">list</a>(\*\*<a href="src/runloop/types/code_handle_list_params.py">params</a>) -> <a href="./src/runloop/types/code_handle_list_view.py">CodeHandleListView</a></code>

# Devboxes

Types:

```python
from runloop.types import DevboxExecutionDetailView, DevboxListView, DevboxView
```

Methods:

- <code title="post /v1/devboxes">client.devboxes.<a href="./src/runloop/resources/devboxes/devboxes.py">create</a>(\*\*<a href="src/runloop/types/devbox_create_params.py">params</a>) -> <a href="./src/runloop/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes/{id}">client.devboxes.<a href="./src/runloop/resources/devboxes/devboxes.py">retrieve</a>(id) -> <a href="./src/runloop/types/devbox_view.py">DevboxView</a></code>
- <code title="get /v1/devboxes">client.devboxes.<a href="./src/runloop/resources/devboxes/devboxes.py">list</a>(\*\*<a href="src/runloop/types/devbox_list_params.py">params</a>) -> <a href="./src/runloop/types/devbox_list_view.py">DevboxListView</a></code>
- <code title="post /v1/devboxes/{id}/execute_sync">client.devboxes.<a href="./src/runloop/resources/devboxes/devboxes.py">execute_sync</a>(id) -> <a href="./src/runloop/types/devbox_execution_detail_view.py">DevboxExecutionDetailView</a></code>
- <code title="post /v1/devboxes/{id}/shutdown">client.devboxes.<a href="./src/runloop/resources/devboxes/devboxes.py">shutdown</a>(id) -> <a href="./src/runloop/types/devbox_view.py">DevboxView</a></code>

## Logs

Types:

```python
from runloop.types.devboxes import DevboxLogsListView
```

Methods:

- <code title="get /v1/devboxes/{id}/logs">client.devboxes.logs.<a href="./src/runloop/resources/devboxes/logs.py">list</a>(id) -> <a href="./src/runloop/types/devboxes/devbox_logs_list_view.py">DevboxLogsListView</a></code>

# Functions

Types:

```python
from runloop.types import FunctionListView
```

Methods:

- <code title="get /v1/functions">client.functions.<a href="./src/runloop/resources/functions/functions.py">list</a>() -> <a href="./src/runloop/types/function_list_view.py">FunctionListView</a></code>
- <code title="post /v1/functions/{project_name}/{function_name}/invoke_async">client.functions.<a href="./src/runloop/resources/functions/functions.py">invoke_async</a>(function_name, \*, project_name, \*\*<a href="src/runloop/types/function_invoke_async_params.py">params</a>) -> <a href="./src/runloop/types/shared/function_invocation_detail_view.py">FunctionInvocationDetailView</a></code>
- <code title="post /v1/functions/{project_name}/{function_name}/invoke_sync">client.functions.<a href="./src/runloop/resources/functions/functions.py">invoke_sync</a>(function_name, \*, project_name, \*\*<a href="src/runloop/types/function_invoke_sync_params.py">params</a>) -> <a href="./src/runloop/types/shared/function_invocation_detail_view.py">FunctionInvocationDetailView</a></code>

## Invocations

Types:

```python
from runloop.types.functions import FunctionInvocationListView, KillOperationResponse
```

Methods:

- <code title="get /v1/functions/invocations/{invocationId}">client.functions.invocations.<a href="./src/runloop/resources/functions/invocations/invocations.py">retrieve</a>(invocation_id) -> <a href="./src/runloop/types/shared/function_invocation_detail_view.py">FunctionInvocationDetailView</a></code>
- <code title="get /v1/functions/invocations">client.functions.invocations.<a href="./src/runloop/resources/functions/invocations/invocations.py">list</a>() -> <a href="./src/runloop/types/functions/function_invocation_list_view.py">FunctionInvocationListView</a></code>
- <code title="post /v1/functions/invocations/{invocationId}/kill">client.functions.invocations.<a href="./src/runloop/resources/functions/invocations/invocations.py">kill</a>(invocation_id) -> <a href="./src/runloop/types/functions/kill_operation_response.py">object</a></code>

### Spans

Types:

```python
from runloop.types.functions.invocations import InvocationSpanListView
```

Methods:

- <code title="get /v1/functions/invocations/{invocationId}/spans">client.functions.invocations.spans.<a href="./src/runloop/resources/functions/invocations/spans.py">list</a>(invocation_id) -> <a href="./src/runloop/types/functions/invocations/invocation_span_list_view.py">InvocationSpanListView</a></code>

# Projects

Types:

```python
from runloop.types import ProjectListView
```

Methods:

- <code title="get /v1/projects">client.projects.<a href="./src/runloop/resources/projects/projects.py">list</a>() -> <a href="./src/runloop/types/project_list_view.py">ProjectListView</a></code>

## Logs

Methods:

- <code title="get /v1/projects/{id}/logs">client.projects.logs.<a href="./src/runloop/resources/projects/logs.py">list</a>(id) -> <a href="./src/runloop/types/shared/project_logs_view.py">ProjectLogsView</a></code>
