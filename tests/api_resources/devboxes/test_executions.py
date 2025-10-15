# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast
from unittest.mock import Mock, patch

import httpx
import pytest
from respx import MockRouter

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types import DevboxSendStdInResult, DevboxExecutionDetailView, DevboxAsyncExecutionDetailView
from runloop_api_client._exceptions import APIStatusError, APITimeoutError
from runloop_api_client.lib.polling import PollingConfig, PollingTimeout

# pyright: reportDeprecated=false

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestExecutions:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_retrieve(self, client: Runloop) -> None:
        execution = client.devboxes.executions.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_method_retrieve_with_all_params(self, client: Runloop) -> None:
        execution = client.devboxes.executions.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
            last_n="last_n",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_raw_response_retrieve(self, client: Runloop) -> None:
        response = client.devboxes.executions.with_raw_response.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_streaming_response_retrieve(self, client: Runloop) -> None:
        with client.devboxes.executions.with_streaming_response.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_retrieve(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            client.devboxes.executions.with_raw_response.retrieve(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            client.devboxes.executions.with_raw_response.retrieve(
                execution_id="",
                devbox_id="devbox_id",
            )

    @parametrize
    def test_method_execute_async(self, client: Runloop) -> None:
        execution = client.devboxes.executions.execute_async(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_method_execute_async_with_all_params(self, client: Runloop) -> None:
        execution = client.devboxes.executions.execute_async(
            id="id",
            command="command",
            attach_stdin=True,
            shell_name="shell_name",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_raw_response_execute_async(self, client: Runloop) -> None:
        response = client.devboxes.executions.with_raw_response.execute_async(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_streaming_response_execute_async(self, client: Runloop) -> None:
        with client.devboxes.executions.with_streaming_response.execute_async(
            id="id",
            command="command",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute_async(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.executions.with_raw_response.execute_async(
                id="",
                command="command",
            )

    @parametrize
    def test_method_execute_sync(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            execution = client.devboxes.executions.execute_sync(
                id="id",
                command="command",
            )

        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_method_execute_sync_with_all_params(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            execution = client.devboxes.executions.execute_sync(
                id="id",
                command="command",
                attach_stdin=True,
                shell_name="shell_name",
            )

        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_raw_response_execute_sync(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            response = client.devboxes.executions.with_raw_response.execute_sync(
                id="id",
                command="command",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = response.parse()
        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_streaming_response_execute_sync(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            with client.devboxes.executions.with_streaming_response.execute_sync(
                id="id",
                command="command",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                execution = response.parse()
                assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_execute_sync(self, client: Runloop) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                client.devboxes.executions.with_raw_response.execute_sync(
                    id="",
                    command="command",
                )

    @parametrize
    def test_method_kill(self, client: Runloop) -> None:
        execution = client.devboxes.executions.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_method_kill_with_all_params(self, client: Runloop) -> None:
        execution = client.devboxes.executions.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
            kill_process_group=True,
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_raw_response_kill(self, client: Runloop) -> None:
        response = client.devboxes.executions.with_raw_response.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    def test_streaming_response_kill(self, client: Runloop) -> None:
        with client.devboxes.executions.with_streaming_response.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_kill(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            client.devboxes.executions.with_raw_response.kill(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            client.devboxes.executions.with_raw_response.kill(
                execution_id="",
                devbox_id="devbox_id",
            )

    @parametrize
    def test_method_send_std_in(self, client: Runloop) -> None:
        execution = client.devboxes.executions.send_std_in(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxSendStdInResult, execution, path=["response"])

    @parametrize
    def test_method_send_std_in_with_all_params(self, client: Runloop) -> None:
        execution = client.devboxes.executions.send_std_in(
            execution_id="execution_id",
            devbox_id="devbox_id",
            signal="EOF",
            text="text",
        )
        assert_matches_type(DevboxSendStdInResult, execution, path=["response"])

    @parametrize
    def test_raw_response_send_std_in(self, client: Runloop) -> None:
        response = client.devboxes.executions.with_raw_response.send_std_in(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = response.parse()
        assert_matches_type(DevboxSendStdInResult, execution, path=["response"])

    @parametrize
    def test_streaming_response_send_std_in(self, client: Runloop) -> None:
        with client.devboxes.executions.with_streaming_response.send_std_in(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = response.parse()
            assert_matches_type(DevboxSendStdInResult, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_send_std_in(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            client.devboxes.executions.with_raw_response.send_std_in(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            client.devboxes.executions.with_raw_response.send_std_in(
                execution_id="",
                devbox_id="devbox_id",
            )

    @parametrize
    def test_method_stream_stdout_updates(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/devboxes/devbox_id/executions/execution_id/stream_stdout_updates").mock(
            return_value=httpx.Response(200)
        )
        execution_stream = client.devboxes.executions.stream_stdout_updates(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        execution_stream.response.close()

    @parametrize
    def test_method_stream_stdout_updates_with_all_params(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/devboxes/devbox_id/executions/execution_id/stream_stdout_updates").mock(
            return_value=httpx.Response(200)
        )
        execution_stream = client.devboxes.executions.stream_stdout_updates(
            execution_id="execution_id",
            devbox_id="devbox_id",
            offset="offset",
        )
        execution_stream.response.close()

    @parametrize
    def test_raw_response_stream_stdout_updates(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/devboxes/devbox_id/executions/execution_id/stream_stdout_updates").mock(
            return_value=httpx.Response(200)
        )
        response = client.devboxes.executions.with_raw_response.stream_stdout_updates(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = response.parse()
        stream.close()

    @parametrize
    def test_streaming_response_stream_stdout_updates(self, client: Runloop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/devboxes/devbox_id/executions/execution_id/stream_stdout_updates").mock(
            return_value=httpx.Response(200)
        )
        with client.devboxes.executions.with_streaming_response.stream_stdout_updates(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = response.parse()
            stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_stream_stdout_updates(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            client.devboxes.executions.with_raw_response.stream_stdout_updates(
                execution_id="execution_id",
                devbox_id="",
            )

    @parametrize
    def test_stream_stdout_updates_auto_reconnect_on_timeout(self, client: Runloop) -> None:
        """Verify stream reconnects on timeout using last seen offset (sync)."""

        # Minimal stream stub compatible with ReconnectingStream expectations
        class IteratorStream:
            def __init__(self, items: list[object], exc: Exception | None = None) -> None:
                self._items = list(items)
                self._exc = exc
                self._raised = False
                self.response = httpx.Response(200, request=httpx.Request("GET", "https://example.com"))

            def __iter__(self):
                for item in self._items:
                    yield item
                if self._exc is not None and not self._raised:
                    self._raised = True
                    raise self._exc

            def close(self) -> None:  # called by reconnect wrapper
                pass

        # Items with offsets
        item1 = type("X", (), {"offset": "5"})()
        item2 = type("X", (), {"offset": "9"})()
        item3 = type("X", (), {"offset": "10"})()

        timeout_err = APITimeoutError(request=httpx.Request("GET", "https://example.com"))

        calls: list[str | None] = []

        def fake_get(_path: str, *, options: Any, **_kwargs: Any):
            from typing import Dict

            options_dict: Dict[str, object] = cast(Dict[str, object], options)
            params = cast("dict[str, object]", options_dict.get("params", {}))
            from typing import Optional

            calls.append(cast(Optional[str], params.get("offset")))
            # first call -> yields two items then timeout; second call -> yields one more and completes
            if len(calls) == 1:
                return IteratorStream([item1, item2], timeout_err)
            elif len(calls) == 2:
                return IteratorStream([item3], None)
            raise AssertionError("Unexpected extra call to _get during auto-reconnect test")

        with patch.object(client.devboxes.executions, "_get", side_effect=fake_get):
            stream = client.devboxes.executions.stream_stdout_updates(
                execution_id="execution_id",
                devbox_id="devbox_id",
            )

            seen_offsets: list[str] = []
            for chunk in stream:
                # items are simple objects with an offset attribute
                seen_offsets.append(getattr(chunk, "offset", ""))
            stream.close()

        # Should have retried once using the last known offset
        assert calls[1] is not None
        assert seen_offsets == ["5", "9", "10"]

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            client.devboxes.executions.with_raw_response.stream_stdout_updates(
                execution_id="",
                devbox_id="devbox_id",
            )

    # Polling method tests
    @parametrize
    def test_method_await_completed_success(self, client: Runloop) -> None:
        """Test await_completed with successful polling to completed state"""

        # Mock the wait_for_status calls - first returns running, then completed
        mock_execution_running = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="running",
            stdout="Starting...",
            stderr="",
        )

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Starting...\nFinished!",
            stderr="",
        )

        with patch.object(client.devboxes.executions, "_post") as mock_post:
            mock_post.side_effect = [mock_execution_running, mock_execution_completed]

            result = client.devboxes.executions.await_completed("execution_id", "devbox_id")

            assert result.execution_id == "execution_id"
            assert result.status == "completed"
            assert mock_post.call_count == 2

    @parametrize
    def test_method_await_completed_immediate_success(self, client: Runloop) -> None:
        """Test await_completed when execution is already completed"""

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Already finished!",
            stderr="",
        )

        with patch.object(client.devboxes.executions, "_post") as mock_post:
            mock_post.return_value = mock_execution_completed

            result = client.devboxes.executions.await_completed("execution_id", "devbox_id")

            assert result.execution_id == "execution_id"
            assert result.status == "completed"
            assert mock_post.call_count == 1

    @parametrize
    def test_method_await_completed_timeout_handling(self, client: Runloop) -> None:
        """Test await_completed handles 408 timeouts correctly"""

        # Create a mock 408 response
        mock_response = Mock()
        mock_response.status_code = 408
        mock_408_error = APIStatusError("Request timeout", response=mock_response, body=None)

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Finished after timeout!",
            stderr="",
        )

        with patch.object(client.devboxes.executions, "_post") as mock_post:
            # First call raises 408, second call succeeds
            mock_post.side_effect = [mock_408_error, mock_execution_completed]

            result = client.devboxes.executions.await_completed("execution_id", "devbox_id")

            assert result.execution_id == "execution_id"
            assert result.status == "completed"
            assert mock_post.call_count == 2

    @parametrize
    def test_method_await_completed_other_error(self, client: Runloop) -> None:
        """Test await_completed re-raises non-408 errors"""

        # Create a mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_500_error = APIStatusError("Internal server error", response=mock_response, body=None)

        with patch.object(client.devboxes.executions, "_post") as mock_post:
            mock_post.side_effect = mock_500_error

            with pytest.raises(APIStatusError, match="Internal server error"):
                client.devboxes.executions.await_completed("execution_id", "devbox_id")

    @parametrize
    def test_method_await_completed_with_config(self, client: Runloop) -> None:
        """Test await_completed with custom polling configuration"""

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Finished with config!",
            stderr="",
        )

        config = PollingConfig(interval_seconds=0.1, max_attempts=10)

        with patch.object(client.devboxes.executions, "_post") as mock_post:
            mock_post.return_value = mock_execution_completed

            result = client.devboxes.executions.await_completed("execution_id", "devbox_id", polling_config=config)

            assert result.execution_id == "execution_id"
            assert result.status == "completed"

    @parametrize
    def test_method_await_completed_polling_timeout(self, client: Runloop) -> None:
        """Test await_completed raises PollingTimeout when max attempts exceeded"""

        mock_execution_running = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="running",
            stdout="Still running...",
            stderr="",
        )

        config = PollingConfig(interval_seconds=0.01, max_attempts=2)

        with patch.object(client.devboxes.executions, "_post") as mock_post:
            mock_post.return_value = mock_execution_running

            with pytest.raises(PollingTimeout):
                client.devboxes.executions.await_completed("execution_id", "devbox_id", polling_config=config)

    @parametrize
    def test_method_await_completed_various_statuses(self, client: Runloop) -> None:
        """Test await_completed correctly handles different execution statuses"""

        # Test with queued status first
        mock_execution_queued = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="queued",
            stdout="",
            stderr="",
        )

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Done!",
            stderr="",
        )

        with patch.object(client.devboxes.executions, "_post") as mock_post:
            mock_post.side_effect = [mock_execution_queued, mock_execution_completed]

            result = client.devboxes.executions.await_completed("execution_id", "devbox_id")

            assert result.execution_id == "execution_id"
            assert result.status == "completed"
            assert mock_post.call_count == 2


class TestAsyncExecutions:
    parametrize = pytest.mark.parametrize("async_client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    async def test_method_retrieve(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_method_retrieve_with_all_params(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
            last_n="last_n",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_raw_response_retrieve(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.executions.with_raw_response.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = await response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_streaming_response_retrieve(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.executions.with_streaming_response.retrieve(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = await response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_retrieve(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.retrieve(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.retrieve(
                execution_id="",
                devbox_id="devbox_id",
            )

    @parametrize
    async def test_method_execute_async(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.execute_async(
            id="id",
            command="command",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_method_execute_async_with_all_params(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.execute_async(
            id="id",
            command="command",
            attach_stdin=True,
            shell_name="shell_name",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_raw_response_execute_async(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.executions.with_raw_response.execute_async(
            id="id",
            command="command",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = await response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_streaming_response_execute_async(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.executions.with_streaming_response.execute_async(
            id="id",
            command="command",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = await response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute_async(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.execute_async(
                id="",
                command="command",
            )

    @parametrize
    async def test_method_execute_sync(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            execution = await async_client.devboxes.executions.execute_sync(
                id="id",
                command="command",
            )

        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_method_execute_sync_with_all_params(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            execution = await async_client.devboxes.executions.execute_sync(
                id="id",
                command="command",
                attach_stdin=True,
                shell_name="shell_name",
            )

        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_raw_response_execute_sync(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            response = await async_client.devboxes.executions.with_raw_response.execute_sync(
                id="id",
                command="command",
            )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = await response.parse()
        assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_streaming_response_execute_sync(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            async with async_client.devboxes.executions.with_streaming_response.execute_sync(
                id="id",
                command="command",
            ) as response:
                assert not response.is_closed
                assert response.http_request.headers.get("X-Stainless-Lang") == "python"

                execution = await response.parse()
                assert_matches_type(DevboxExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_execute_sync(self, async_client: AsyncRunloop) -> None:
        with pytest.warns(DeprecationWarning):
            with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
                await async_client.devboxes.executions.with_raw_response.execute_sync(
                    id="",
                    command="command",
                )

    @parametrize
    async def test_method_kill(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_method_kill_with_all_params(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
            kill_process_group=True,
        )
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_raw_response_kill(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.executions.with_raw_response.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = await response.parse()
        assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

    @parametrize
    async def test_streaming_response_kill(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.executions.with_streaming_response.kill(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = await response.parse()
            assert_matches_type(DevboxAsyncExecutionDetailView, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_kill(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.kill(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.kill(
                execution_id="",
                devbox_id="devbox_id",
            )

    @parametrize
    async def test_method_send_std_in(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.send_std_in(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        assert_matches_type(DevboxSendStdInResult, execution, path=["response"])

    @parametrize
    async def test_method_send_std_in_with_all_params(self, async_client: AsyncRunloop) -> None:
        execution = await async_client.devboxes.executions.send_std_in(
            execution_id="execution_id",
            devbox_id="devbox_id",
            signal="EOF",
            text="text",
        )
        assert_matches_type(DevboxSendStdInResult, execution, path=["response"])

    @parametrize
    async def test_raw_response_send_std_in(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.executions.with_raw_response.send_std_in(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        execution = await response.parse()
        assert_matches_type(DevboxSendStdInResult, execution, path=["response"])

    @parametrize
    async def test_streaming_response_send_std_in(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.executions.with_streaming_response.send_std_in(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            execution = await response.parse()
            assert_matches_type(DevboxSendStdInResult, execution, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_send_std_in(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.send_std_in(
                execution_id="execution_id",
                devbox_id="",
            )

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.send_std_in(
                execution_id="",
                devbox_id="devbox_id",
            )

    @parametrize
    async def test_method_stream_stdout_updates(self, async_client: AsyncRunloop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/devboxes/devbox_id/executions/execution_id/stream_stdout_updates").mock(
            return_value=httpx.Response(200)
        )
        execution_stream = await async_client.devboxes.executions.stream_stdout_updates(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )
        await execution_stream.response.aclose()

    @parametrize
    async def test_method_stream_stdout_updates_with_all_params(
        self, async_client: AsyncRunloop, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/v1/devboxes/devbox_id/executions/execution_id/stream_stdout_updates").mock(
            return_value=httpx.Response(200)
        )
        execution_stream = await async_client.devboxes.executions.stream_stdout_updates(
            execution_id="execution_id",
            devbox_id="devbox_id",
            offset="offset",
        )
        await execution_stream.response.aclose()

    @parametrize
    async def test_raw_response_stream_stdout_updates(self, async_client: AsyncRunloop, respx_mock: MockRouter) -> None:
        respx_mock.get("/v1/devboxes/devbox_id/executions/execution_id/stream_stdout_updates").mock(
            return_value=httpx.Response(200)
        )
        response = await async_client.devboxes.executions.with_raw_response.stream_stdout_updates(
            execution_id="execution_id",
            devbox_id="devbox_id",
        )

        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        stream = await response.parse()
        await stream.close()

    @parametrize
    async def test_streaming_response_stream_stdout_updates(
        self, async_client: AsyncRunloop, respx_mock: MockRouter
    ) -> None:
        respx_mock.get("/v1/devboxes/devbox_id/executions/execution_id/stream_stdout_updates").mock(
            return_value=httpx.Response(200)
        )
        async with async_client.devboxes.executions.with_streaming_response.stream_stdout_updates(
            execution_id="execution_id",
            devbox_id="devbox_id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            stream = await response.parse()
            await stream.close()

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_stream_stdout_updates(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `devbox_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.stream_stdout_updates(
                execution_id="execution_id",
                devbox_id="",
            )

    @parametrize
    async def test_stream_stdout_updates_auto_reconnect_on_timeout(self, async_client: AsyncRunloop) -> None:
        """Verify stream reconnects on timeout using last seen offset (async)."""

        class AsyncIteratorStream:
            def __init__(self, items: list[object], exc: Exception | None = None) -> None:
                self._items = list(items)
                self._exc = exc
                self._raised = False
                self.response = httpx.Response(200, request=httpx.Request("GET", "https://example.com"))

            def __aiter__(self):
                self._iter = iter(self._items)
                return self

            async def __anext__(self):
                try:
                    return next(self._iter)
                except StopIteration:
                    if self._exc is not None and not self._raised:
                        self._raised = True
                        raise self._exc from None
                    raise StopAsyncIteration from None

            async def close(self) -> None:
                pass

        item1 = type("X", (), {"offset": "5"})()
        item2 = type("X", (), {"offset": "9"})()
        item3 = type("X", (), {"offset": "10"})()

        timeout_err = APITimeoutError(request=httpx.Request("GET", "https://example.com"))

        calls: list[str | None] = []

        async def fake_get(_path: str, *, options: Any, **_kwargs: Any):
            from typing import Dict

            options_dict: Dict[str, object] = cast(Dict[str, object], options)
            params = cast("dict[str, object]", options_dict.get("params", {}))
            from typing import Optional

            calls.append(cast(Optional[str], params.get("offset")))
            if len(calls) == 1:
                return AsyncIteratorStream([item1, item2], timeout_err)
            elif len(calls) == 2:
                return AsyncIteratorStream([item3], None)
            raise AssertionError("Unexpected extra call to _get during auto-reconnect test")

        with patch.object(async_client.devboxes.executions, "_get", side_effect=fake_get):
            stream = await async_client.devboxes.executions.stream_stdout_updates(
                execution_id="execution_id",
                devbox_id="devbox_id",
            )

            seen_offsets: list[str] = []
            async for chunk in stream:
                seen_offsets.append(getattr(chunk, "offset", ""))
            await stream.close()

        assert calls[1] is not None
        assert seen_offsets == ["5", "9", "10"]

        with pytest.raises(ValueError, match=r"Expected a non-empty value for `execution_id` but received ''"):
            await async_client.devboxes.executions.with_raw_response.stream_stdout_updates(
                execution_id="",
                devbox_id="devbox_id",
            )

    # Async polling method tests
    @parametrize
    async def test_method_await_completed_success(self, async_client: AsyncRunloop) -> None:
        """Test await_completed with successful polling to completed state"""

        # Mock the wait_for_status calls - first returns running, then completed
        mock_execution_running = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="running",
            stdout="Starting...",
            stderr="",
        )

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Starting...\nFinished!",
            stderr="",
        )

        with patch.object(async_client.devboxes.executions, "_post") as mock_post:
            mock_post.side_effect = [mock_execution_running, mock_execution_completed]

            result = await async_client.devboxes.executions.await_completed("execution_id", devbox_id="devbox_id")

            assert result.execution_id == "execution_id"
            assert result.status == "completed"
            assert mock_post.call_count == 2

    @parametrize
    async def test_method_await_completed_immediate_success(self, async_client: AsyncRunloop) -> None:
        """Test await_completed when execution is already completed"""

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Already finished!",
            stderr="",
        )

        with patch.object(async_client.devboxes.executions, "_post") as mock_post:
            mock_post.return_value = mock_execution_completed

            result = await async_client.devboxes.executions.await_completed("execution_id", devbox_id="devbox_id")

            assert result.execution_id == "execution_id"
            assert result.status == "completed"
            assert mock_post.call_count == 1

    @parametrize
    async def test_method_await_completed_timeout_handling(self, async_client: AsyncRunloop) -> None:
        """Test await_completed handles 408 timeouts correctly"""

        # Create a mock 408 response
        mock_response = Mock()
        mock_response.status_code = 408
        mock_408_error = APITimeoutError(request=mock_response.request)

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Finished after timeout!",
            stderr="",
        )

        with patch.object(async_client.devboxes.executions, "_post") as mock_post:
            # First call raises 408, second call succeeds
            mock_post.side_effect = [mock_408_error, mock_execution_completed]

            result = await async_client.devboxes.executions.await_completed("execution_id", devbox_id="devbox_id")

            assert result.execution_id == "execution_id"
            assert result.status == "completed"
            assert mock_post.call_count == 2

    @parametrize
    async def test_method_await_completed_other_error(self, async_client: AsyncRunloop) -> None:
        """Test await_completed re-raises non-408 errors"""

        # Create a mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_500_error = APIStatusError("Internal server error", response=mock_response, body=None)

        with patch.object(async_client.devboxes.executions, "_post") as mock_post:
            mock_post.side_effect = mock_500_error

            with pytest.raises(APIStatusError, match="Internal server error"):
                await async_client.devboxes.executions.await_completed("execution_id", devbox_id="devbox_id")

    @parametrize
    async def test_method_await_completed_with_config(self, async_client: AsyncRunloop) -> None:
        """Test await_completed with custom polling configuration"""

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Finished with config!",
            stderr="",
        )

        config = PollingConfig(interval_seconds=0.1, max_attempts=10)

        with patch.object(async_client.devboxes.executions, "_post") as mock_post:
            mock_post.return_value = mock_execution_completed

            result = await async_client.devboxes.executions.await_completed(
                "execution_id", devbox_id="devbox_id", polling_config=config
            )

            assert result.execution_id == "execution_id"
            assert result.status == "completed"

    @parametrize
    async def test_method_await_completed_polling_timeout(self, async_client: AsyncRunloop) -> None:
        """Test await_completed raises PollingTimeout when max attempts exceeded"""

        mock_execution_running = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="running",
            stdout="Still running...",
            stderr="",
        )

        config = PollingConfig(interval_seconds=0.01, max_attempts=2)

        with patch.object(async_client.devboxes.executions, "_post") as mock_post:
            mock_post.return_value = mock_execution_running

            with pytest.raises(PollingTimeout):
                await async_client.devboxes.executions.await_completed(
                    "execution_id", devbox_id="devbox_id", polling_config=config
                )

    @parametrize
    async def test_method_await_completed_various_statuses(self, async_client: AsyncRunloop) -> None:
        """Test await_completed correctly handles different execution statuses"""

        # Test with queued status first
        mock_execution_queued = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="queued",
            stdout="",
            stderr="",
        )

        mock_execution_completed = DevboxAsyncExecutionDetailView(
            devbox_id="devbox_id",
            execution_id="execution_id",
            status="completed",
            stdout="Done!",
            stderr="",
        )

        with patch.object(async_client.devboxes.executions, "_post") as mock_post:
            mock_post.side_effect = [mock_execution_queued, mock_execution_completed]

            result = await async_client.devboxes.executions.await_completed("execution_id", devbox_id="devbox_id")

            assert result.execution_id == "execution_id"
            assert result.status == "completed"
            assert mock_post.call_count == 2
