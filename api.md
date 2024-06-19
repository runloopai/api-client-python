# Shared Types

```python
from runloop.types import FunctionInvocationDetail
```

# CodeHandles

Types:

```python
from runloop.types import CodeHandle, CodeHandleList
```

Methods:

- <code title="post /v1/code_handles">client.code_handles.<a href="./src/runloop/resources/code_handles.py">create</a>(\*\*<a href="src/runloop/types/code_handle_create_params.py">params</a>) -> <a href="./src/runloop/types/code_handle.py">CodeHandle</a></code>
- <code title="get /v1/code_handles">client.code_handles.<a href="./src/runloop/resources/code_handles.py">list</a>(\*\*<a href="src/runloop/types/code_handle_list_params.py">params</a>) -> <a href="./src/runloop/types/code_handle_list.py">CodeHandleList</a></code>

# Devboxes

Types:

```python
from runloop.types import Devbox, DevboxList
```

Methods:

- <code title="post /v1/devboxes">client.devboxes.<a href="./src/runloop/resources/devboxes/devboxes.py">create</a>(\*\*<a href="src/runloop/types/devbox_create_params.py">params</a>) -> <a href="./src/runloop/types/devbox.py">Devbox</a></code>
- <code title="get /v1/devboxes/{id}">client.devboxes.<a href="./src/runloop/resources/devboxes/devboxes.py">retrieve</a>(id) -> <a href="./src/runloop/types/devbox.py">Devbox</a></code>
- <code title="get /v1/devboxes">client.devboxes.<a href="./src/runloop/resources/devboxes/devboxes.py">list</a>(\*\*<a href="src/runloop/types/devbox_list_params.py">params</a>) -> <a href="./src/runloop/types/devbox_list.py">DevboxList</a></code>
- <code title="post /v1/devboxes/{id}/shutdown">client.devboxes.<a href="./src/runloop/resources/devboxes/devboxes.py">shutdown</a>(id) -> <a href="./src/runloop/types/devbox.py">Devbox</a></code>

## Logs

Types:

```python
from runloop.types.devboxes import DevboxLogsList
```

Methods:

- <code title="get /v1/devboxes/{id}/logs">client.devboxes.logs.<a href="./src/runloop/resources/devboxes/logs.py">list</a>(id) -> <a href="./src/runloop/types/devboxes/devbox_logs_list.py">DevboxLogsList</a></code>

# Functions

Types:

```python
from runloop.types import FunctionList
```

Methods:

- <code title="get /v1/functions">client.functions.<a href="./src/runloop/resources/functions/functions.py">list</a>() -> <a href="./src/runloop/types/function_list.py">FunctionList</a></code>
- <code title="post /v1/functions/{projectName}/{functionName}/invoke_async">client.functions.<a href="./src/runloop/resources/functions/functions.py">invoke_async</a>(function_name, \*, project_name, \*\*<a href="src/runloop/types/function_invoke_async_params.py">params</a>) -> <a href="./src/runloop/types/shared/function_invocation_detail.py">FunctionInvocationDetail</a></code>
- <code title="post /v1/functions/{projectName}/{functionName}/invoke_sync">client.functions.<a href="./src/runloop/resources/functions/functions.py">invoke_sync</a>(function_name, \*, project_name, \*\*<a href="src/runloop/types/function_invoke_sync_params.py">params</a>) -> <a href="./src/runloop/types/shared/function_invocation_detail.py">FunctionInvocationDetail</a></code>

## Invocations

Types:

```python
from runloop.types.functions import FunctionInvocationList, KillOperationResponse
```

Methods:

- <code title="get /v1/functions/invocations/{invocationId}">client.functions.invocations.<a href="./src/runloop/resources/functions/invocations/invocations.py">retrieve</a>(invocation_id) -> <a href="./src/runloop/types/shared/function_invocation_detail.py">FunctionInvocationDetail</a></code>
- <code title="get /v1/functions/invocations">client.functions.invocations.<a href="./src/runloop/resources/functions/invocations/invocations.py">list</a>() -> <a href="./src/runloop/types/functions/function_invocation_list.py">FunctionInvocationList</a></code>
- <code title="post /v1/functions/invocations/{invocationId}/kill">client.functions.invocations.<a href="./src/runloop/resources/functions/invocations/invocations.py">kill</a>(invocation_id) -> <a href="./src/runloop/types/functions/kill_operation_response.py">object</a></code>

### Spans

Types:

```python
from runloop.types.functions.invocations import InvocationSpanList
```

Methods:

- <code title="get /v1/functions/invocations/{invocationId}/spans">client.functions.invocations.spans.<a href="./src/runloop/resources/functions/invocations/spans.py">list</a>(invocation_id) -> <a href="./src/runloop/types/functions/invocations/invocation_span_list.py">InvocationSpanList</a></code>

## OpenAPI

Types:

```python
from runloop.types.functions import OpenAPIRetrieveResponse
```

Methods:

- <code title="get /v1/functions/openapi">client.functions.openapi.<a href="./src/runloop/resources/functions/openapi.py">retrieve</a>() -> <a href="./src/runloop/types/functions/openapi_retrieve_response.py">object</a></code>

# Latches

Types:

```python
from runloop.types import EmptyRecord
```

Methods:

- <code title="post /v1/latches/{latchId}">client.latches.<a href="./src/runloop/resources/latches.py">fulfill</a>(latch_id, \*\*<a href="src/runloop/types/latch_fulfill_params.py">params</a>) -> <a href="./src/runloop/types/empty_record.py">object</a></code>

# Projects

Types:

```python
from runloop.types import ProjectList
```

Methods:

- <code title="get /v1/projects">client.projects.<a href="./src/runloop/resources/projects/projects.py">list</a>() -> <a href="./src/runloop/types/project_list.py">ProjectList</a></code>

## Logs

Types:

```python
from runloop.types.projects import ProjectLogs
```

Methods:

- <code title="get /v1/projects/{id}/logs">client.projects.logs.<a href="./src/runloop/resources/projects/logs.py">list</a>(id) -> <a href="./src/runloop/types/projects/project_logs.py">ProjectLogs</a></code>

# Sessions

## Sessions

Types:

```python
from runloop.types.sessions import Session, SessionList
```

Methods:

- <code title="post /v1/sessions/sessions">client.sessions.sessions.<a href="./src/runloop/resources/sessions/sessions/sessions.py">create</a>() -> <a href="./src/runloop/types/sessions/session.py">Session</a></code>
- <code title="get /v1/sessions/sessions">client.sessions.sessions.<a href="./src/runloop/resources/sessions/sessions/sessions.py">list</a>() -> <a href="./src/runloop/types/sessions/session_list.py">SessionList</a></code>

### Kv

Types:

```python
from runloop.types.sessions.sessions import SessionKv
```

Methods:

- <code title="get /v1/sessions/sessions/{sessionId}/kv">client.sessions.sessions.kv.<a href="./src/runloop/resources/sessions/sessions/kv.py">list</a>(session_id, \*\*<a href="src/runloop/types/sessions/sessions/kv_list_params.py">params</a>) -> <a href="./src/runloop/types/sessions/sessions/session_kv.py">SessionKv</a></code>
