"""Tests for Devbox streaming functionality.

Tests streaming setup, thread spawning, concurrent operations, and the
streaming group management.
"""

from __future__ import annotations

import time
import threading
from types import SimpleNamespace
from unittest.mock import Mock

from tests.sdk.conftest import THREAD_STARTUP_DELAY
from runloop_api_client.sdk import Devbox
from runloop_api_client._streaming import Stream
from runloop_api_client.sdk.execution import _StreamingGroup
from runloop_api_client.types.devboxes.execution_update_chunk import ExecutionUpdateChunk

# Legacy alias for backward compatibility
SHORT_SLEEP = THREAD_STARTUP_DELAY


class TestDevboxStreaming:
    """Tests for Devbox streaming methods."""

    def test_start_streaming_no_callbacks(self, mock_client: Mock) -> None:
        """Test _start_streaming returns None when no callbacks."""
        devbox = Devbox(mock_client, "dev_123")
        result = devbox._start_streaming("exec_123", stdout=None, stderr=None, output=None)
        assert result is None

    def test_start_streaming_stdout_only(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _start_streaming with stdout callback only."""
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream

        devbox = Devbox(mock_client, "dev_123")
        stdout_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=stdout_calls.append, stderr=None, output=None)

        assert result is not None
        assert isinstance(result, _StreamingGroup)
        assert len(result._threads) == 1
        mock_client.devboxes.executions.stream_stdout_updates.assert_called_once()

    def test_start_streaming_stderr_only(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _start_streaming with stderr callback only."""
        mock_client.devboxes.executions.stream_stderr_updates.return_value = mock_stream

        devbox = Devbox(mock_client, "dev_123")
        stderr_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=None, stderr=stderr_calls.append, output=None)

        assert result is not None
        assert isinstance(result, _StreamingGroup)
        assert len(result._threads) == 1
        mock_client.devboxes.executions.stream_stderr_updates.assert_called_once()

    def test_start_streaming_output_only(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _start_streaming with output callback only."""
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream
        mock_client.devboxes.executions.stream_stderr_updates.return_value = mock_stream

        devbox = Devbox(mock_client, "dev_123")
        output_calls: list[str] = []
        result = devbox._start_streaming("exec_123", stdout=None, stderr=None, output=output_calls.append)

        assert result is not None
        assert isinstance(result, _StreamingGroup)
        assert len(result._threads) == 2  # Both stdout and stderr streams

    def test_start_streaming_all_callbacks(self, mock_client: Mock, mock_stream: Mock) -> None:
        """Test _start_streaming with all callbacks."""
        mock_client.devboxes.executions.stream_stdout_updates.return_value = mock_stream
        mock_client.devboxes.executions.stream_stderr_updates.return_value = mock_stream

        devbox = Devbox(mock_client, "dev_123")
        stdout_calls: list[str] = []
        stderr_calls: list[str] = []
        output_calls: list[str] = []
        result = devbox._start_streaming(
            "exec_123",
            stdout=stdout_calls.append,
            stderr=stderr_calls.append,
            output=output_calls.append,
        )

        assert result is not None
        assert isinstance(result, _StreamingGroup)
        assert len(result._threads) == 2  # Both stdout and stderr streams

    def test_spawn_stream_thread(
        self, mock_client: Mock, mock_stream: Mock, thread_cleanup: tuple[list[threading.Thread], list[threading.Event]]
    ) -> None:
        """Test _spawn_stream_thread creates and starts thread."""
        mock_stream.__iter__ = Mock(
            return_value=iter(
                [
                    SimpleNamespace(output="line 1"),
                    SimpleNamespace(output="line 2"),
                ]
            )
        )
        mock_stream.__enter__ = Mock(return_value=mock_stream)
        mock_stream.__exit__ = Mock(return_value=None)

        devbox = Devbox(mock_client, "dev_123")
        stop_event = threading.Event()
        calls: list[str] = []

        def stream_factory() -> Stream[ExecutionUpdateChunk]:
            return mock_stream

        thread = devbox._spawn_stream_thread(
            name="test",
            stream_factory=stream_factory,
            callbacks=[calls.append],
            stop_event=stop_event,
        )

        # Register thread and stop event for automatic cleanup
        threads, stop_events = thread_cleanup
        threads.append(thread)
        stop_events.append(stop_event)

        assert isinstance(thread, threading.Thread)
        # Give thread time to start
        time.sleep(SHORT_SLEEP)
        # Thread may have already finished if stream is short
        if thread.is_alive():
            stop_event.set()
            thread.join(timeout=1.0)
        assert not thread.is_alive()

    def test_spawn_stream_thread_stop_event(
        self, mock_client: Mock, mock_stream: Mock, thread_cleanup: tuple[list[threading.Thread], list[threading.Event]]
    ) -> None:
        """Test _spawn_stream_thread respects stop event."""
        mock_stream.__iter__ = Mock(
            return_value=iter(
                [
                    SimpleNamespace(output="line 1"),
                    SimpleNamespace(output="line 2"),
                ]
            )
        )
        mock_stream.__enter__ = Mock(return_value=mock_stream)
        mock_stream.__exit__ = Mock(return_value=None)

        devbox = Devbox(mock_client, "dev_123")
        stop_event = threading.Event()
        calls: list[str] = []

        def stream_factory() -> Stream[ExecutionUpdateChunk]:
            return mock_stream

        thread = devbox._spawn_stream_thread(
            name="test",
            stream_factory=stream_factory,
            callbacks=[calls.append],
            stop_event=stop_event,
        )

        # Register thread and stop event for automatic cleanup
        threads, stop_events = thread_cleanup
        threads.append(thread)
        stop_events.append(stop_event)

        stop_event.set()
        thread.join(timeout=1.0)
        assert not thread.is_alive()
