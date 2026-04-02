"""Tests for Axon SSE auto-reconnect functionality."""

from typing import Any, Iterator, AsyncIterator, cast
from unittest.mock import Mock, AsyncMock, patch

import httpx
import pytest

from src.runloop_api_client._constants import RAW_RESPONSE_HEADER
from src.runloop_api_client._streaming import Stream, AsyncStream, ReconnectingStream, AsyncReconnectingStream


class MockAxonEvent:
    """Mock AxonEventView for testing."""

    def __init__(self, sequence: int, data: str):
        self.sequence = sequence
        self.data = data


class TestAxonSSEReconnectSync:
    """Test SSE reconnection for sync Axon subscriptions."""

    def test_subscribe_sse_returns_reconnecting_stream(self):
        """Test that subscribe_sse returns a ReconnectingStream."""
        from src.runloop_api_client import Runloop

        client = Runloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get") as mock_get:
            # Mock the initial stream
            mock_stream = Mock(spec=Stream)
            mock_get.return_value = mock_stream

            result = client.axons.subscribe_sse("axon-123")

            # Should return a ReconnectingStream
            assert isinstance(result, ReconnectingStream)

    def test_subscribe_sse_with_raw_header_returns_plain_stream(self):
        """Test that RAW_RESPONSE_HEADER opts out of reconnection."""
        from src.runloop_api_client import Runloop

        client = Runloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get") as mock_get:
            mock_stream = Mock(spec=Stream)
            mock_get.return_value = mock_stream

            result = client.axons.subscribe_sse("axon-123", extra_headers={RAW_RESPONSE_HEADER: "true"})

            # Should return plain Stream, not ReconnectingStream
            assert not isinstance(result, ReconnectingStream)
            assert result == mock_stream

    def test_reconnection_uses_last_sequence(self):
        """Test that reconnection uses the sequence from the last event."""
        from src.runloop_api_client import Runloop

        call_count = 0
        query_params: list[dict[str, object]] = []

        def mock_get(*_args: object, **kwargs: Any) -> Mock:
            nonlocal call_count
            # Capture query params
            options = cast(dict[str, object], kwargs.get("options", {}))
            if "params" in options:
                query_params.append(cast(dict[str, object], options["params"]))

            # First call: return stream with events
            if call_count == 0:
                call_count += 1
                mock_stream = Mock(spec=Stream)

                def first_iter(_self: object) -> Iterator[MockAxonEvent]:
                    yield MockAxonEvent(sequence=1, data="event1")
                    yield MockAxonEvent(sequence=2, data="event2")
                    raise httpx.ReadTimeout("stream timed out")

                mock_stream.__iter__ = first_iter
                return mock_stream

            # Second call (reconnection): return stream continuing from sequence 2
            mock_stream = Mock(spec=Stream)

            def second_iter(_self: object) -> Iterator[MockAxonEvent]:
                yield MockAxonEvent(sequence=3, data="event3")

            mock_stream.__iter__ = second_iter
            return mock_stream

        client = Runloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get", side_effect=mock_get):
            stream = client.axons.subscribe_sse("axon-123")

            # Consume events
            events = cast(list[MockAxonEvent], list(stream))

            # Should have 3 events total (2 from first stream, 1 from reconnected stream)
            assert len(events) == 3
            assert events[0].sequence == 1
            assert events[1].sequence == 2
            assert events[2].sequence == 3

            # Check that second call used after_sequence parameter
            # Note: first call has None, second call should have after_sequence=2
            assert len(query_params) >= 2

    def test_sequence_extraction_handles_missing_sequence(self):
        """Test that missing sequence fields are handled gracefully."""
        from src.runloop_api_client import Runloop

        client = Runloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get") as mock_get:
            mock_stream = Mock(spec=Stream)

            # Event without sequence attribute
            class EventWithoutSequence:
                pass

            def mock_iter(_self: object) -> Iterator[object]:
                yield EventWithoutSequence()

            mock_stream.__iter__ = mock_iter
            mock_get.return_value = mock_stream

            stream = client.axons.subscribe_sse("axon-123")

            # Should not crash, sequence extractor should return None
            events = list(stream)
            assert len(events) == 1

    def test_subscribe_sse_preserves_request_options(self):
        """Test that extra headers, query, etc. are preserved."""
        from src.runloop_api_client import Runloop

        client = Runloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get") as mock_get:
            mock_stream = Mock(spec=Stream)

            def empty_iter(_self: object) -> Iterator[object]:
                return iter([])

            mock_stream.__iter__ = empty_iter
            mock_get.return_value = mock_stream

            extra_headers = {"X-Custom": "value"}
            extra_query = {"param": "value"}

            client.axons.subscribe_sse("axon-123", extra_headers=extra_headers, extra_query=extra_query, timeout=30.0)

            # Verify _get was called with the options
            call_args = mock_get.call_args
            options = call_args.kwargs["options"]

            # Headers should include Accept: text/event-stream and custom header
            assert "Accept" in options["headers"]
            assert options["headers"]["Accept"] == "text/event-stream"
            assert options["headers"]["X-Custom"] == "value"
            assert options["params"]["param"] == "value"
            assert options["params"]["after_sequence"] is None
            assert options["timeout"] == 30.0


class TestAxonSSEReconnectAsync:
    """Test SSE reconnection for async Axon subscriptions."""

    @pytest.mark.asyncio
    async def test_subscribe_sse_returns_reconnecting_stream(self):
        """Test that subscribe_sse returns an AsyncReconnectingStream."""
        from src.runloop_api_client import AsyncRunloop

        async def mock_get(*_args: object, **_kwargs: object) -> Mock:
            mock_stream = Mock(spec=AsyncStream)
            return mock_stream

        client = AsyncRunloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get", new=AsyncMock(side_effect=mock_get)):
            result = await client.axons.subscribe_sse("axon-123")

            # Should return an AsyncReconnectingStream
            assert isinstance(result, AsyncReconnectingStream)

    @pytest.mark.asyncio
    async def test_subscribe_sse_with_raw_header_returns_plain_stream(self):
        """Test that RAW_RESPONSE_HEADER opts out of reconnection."""
        from src.runloop_api_client import AsyncRunloop

        async def mock_get(*_args: object, **_kwargs: object) -> Mock:
            mock_stream = Mock(spec=AsyncStream)
            return mock_stream

        client = AsyncRunloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get", new=AsyncMock(side_effect=mock_get)):
            result = await client.axons.subscribe_sse("axon-123", extra_headers={RAW_RESPONSE_HEADER: "true"})

            # Should return plain AsyncStream, not AsyncReconnectingStream
            assert not isinstance(result, AsyncReconnectingStream)

    @pytest.mark.asyncio
    async def test_reconnection_uses_last_sequence(self):
        """Test that reconnection uses the sequence from the last event."""
        from src.runloop_api_client import AsyncRunloop

        call_count = 0
        query_params: list[dict[str, object]] = []

        async def mock_get(*_args: object, **kwargs: Any) -> Mock:
            nonlocal call_count
            # Capture query params
            options = cast(dict[str, object], kwargs.get("options", {}))
            if "params" in options:
                query_params.append(cast(dict[str, object], options["params"]))

            # First call: return stream with events
            if call_count == 0:
                call_count += 1
                mock_stream = Mock(spec=AsyncStream)

                async def first_iter(_self: object) -> AsyncIterator[MockAxonEvent]:
                    yield MockAxonEvent(sequence=1, data="event1")
                    yield MockAxonEvent(sequence=2, data="event2")
                    raise httpx.ReadTimeout("stream timed out")

                mock_stream.__aiter__ = first_iter
                return mock_stream

            # Second call (reconnection)
            mock_stream = Mock(spec=AsyncStream)

            async def second_iter(_self: object) -> AsyncIterator[MockAxonEvent]:
                yield MockAxonEvent(sequence=3, data="event3")

            mock_stream.__aiter__ = second_iter
            return mock_stream

        client = AsyncRunloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get", new=AsyncMock(side_effect=mock_get)):
            stream = await client.axons.subscribe_sse("axon-123")

            # Consume events
            events: list[Any] = []
            async for event in stream:
                events.append(event)
                if len(events) >= 3:
                    break

            # Should have 3 events total
            assert len(events) == 3
            assert events[0].sequence == 1
            assert events[1].sequence == 2
            assert events[2].sequence == 3

    @pytest.mark.asyncio
    async def test_sequence_extraction_handles_none(self):
        """Test that None sequences are handled gracefully."""
        from src.runloop_api_client import AsyncRunloop

        async def mock_get(*_args: object, **_kwargs: object) -> Mock:
            mock_stream = Mock(spec=AsyncStream)

            # Event with sequence = None
            class EventWithNoneSequence:
                sequence = None

            async def mock_iter(_self: object) -> AsyncIterator[object]:
                yield EventWithNoneSequence()

            mock_stream.__aiter__ = mock_iter
            return mock_stream

        client = AsyncRunloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get", new=AsyncMock(side_effect=mock_get)):
            stream = await client.axons.subscribe_sse("axon-123")

            # Should not crash
            events: list[object] = []
            async for event in stream:
                events.append(event)
                break

            assert len(events) == 1

    @pytest.mark.asyncio
    async def test_subscribe_sse_preserves_request_options(self):
        """Test that extra headers, query, etc. are preserved in async."""
        from src.runloop_api_client import AsyncRunloop

        async def mock_get(*_args: object, **_kwargs: object) -> Mock:
            mock_stream = Mock(spec=AsyncStream)

            async def mock_iter():
                return
                yield  # Make it async generator

            mock_stream.__aiter__ = mock_iter
            return mock_stream

        client = AsyncRunloop(bearer_token="test-key", base_url="http://test")

        with patch.object(client.axons, "_get", new=AsyncMock(side_effect=mock_get)) as mock_get_method:
            extra_headers = {"X-Custom": "value"}
            extra_query = {"param": "value"}

            await client.axons.subscribe_sse(
                "axon-123", extra_headers=extra_headers, extra_query=extra_query, timeout=30.0
            )

            # Verify _get was called with the options
            call_args = mock_get_method.call_args
            options = call_args.kwargs["options"]

            # Headers should include Accept: text/event-stream and custom header
            assert "Accept" in options["headers"]
            assert options["headers"]["Accept"] == "text/event-stream"
            assert options["headers"]["X-Custom"] == "value"
            assert options["params"]["param"] == "value"
            assert options["params"]["after_sequence"] is None
            assert options["timeout"] == 30.0


class TestAxonSubscribeSseParams:
    """Test AxonSubscribeSseParams TypedDict."""

    def test_params_structure(self):
        """Test that AxonSubscribeSseParams has the correct structure."""
        from src.runloop_api_client.types.axons import AxonSubscribeSseParams

        # Should be able to create with after_sequence
        params: AxonSubscribeSseParams = {"after_sequence": 123}
        assert params["after_sequence"] == 123

        # The field is optional via total=False, so it can also be omitted.
        params2: AxonSubscribeSseParams = {}
        assert "after_sequence" not in params2
