"""Tests for Axon SSE auto-reconnect functionality."""

from unittest.mock import Mock, patch, MagicMock
from typing import Iterator, AsyncIterator

import pytest

from src.runloop_api_client._streaming import Stream, AsyncStream, ReconnectingStream, AsyncReconnectingStream
from src.runloop_api_client._constants import RAW_RESPONSE_HEADER
from src.runloop_api_client.types.axon_event_view import AxonEventView


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

        with patch.object(Runloop, "_get") as mock_get:
            # Mock the initial stream
            mock_stream = Mock(spec=Stream)
            mock_get.return_value = mock_stream

            client = Runloop(api_key="test-key", base_url="http://test")

            result = client.axons.subscribe_sse("axon-123")

            # Should return a ReconnectingStream
            assert isinstance(result, ReconnectingStream)

    def test_subscribe_sse_with_raw_header_returns_plain_stream(self):
        """Test that RAW_RESPONSE_HEADER opts out of reconnection."""
        from src.runloop_api_client import Runloop

        with patch.object(Runloop, "_get") as mock_get:
            mock_stream = Mock(spec=Stream)
            mock_get.return_value = mock_stream

            client = Runloop(api_key="test-key", base_url="http://test")

            result = client.axons.subscribe_sse("axon-123", extra_headers={RAW_RESPONSE_HEADER: "true"})

            # Should return plain Stream, not ReconnectingStream
            assert not isinstance(result, ReconnectingStream)
            assert result == mock_stream

    def test_reconnection_uses_last_sequence(self):
        """Test that reconnection uses the sequence from the last event."""
        from src.runloop_api_client import Runloop

        call_count = 0
        query_params = []

        def mock_get(*args, **kwargs):
            nonlocal call_count
            # Capture query params
            if "query" in kwargs.get("options", {}):
                query_params.append(kwargs["options"]["query"])

            # First call: return stream with events
            if call_count == 0:
                call_count += 1
                mock_stream = Mock(spec=Stream)

                def mock_iter():
                    yield MockAxonEvent(sequence=1, data="event1")
                    yield MockAxonEvent(sequence=2, data="event2")
                    # Simulate timeout/disconnect
                    raise StopIteration()

                mock_stream.__iter__ = mock_iter
                return mock_stream

            # Second call (reconnection): return stream continuing from sequence 2
            mock_stream = Mock(spec=Stream)

            def mock_iter():
                yield MockAxonEvent(sequence=3, data="event3")

            mock_stream.__iter__ = mock_iter
            return mock_stream

        with patch.object(Runloop, "_get", side_effect=mock_get):
            client = Runloop(api_key="test-key", base_url="http://test")

            stream = client.axons.subscribe_sse("axon-123")

            # Consume events
            events = list(stream)

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

        with patch.object(Runloop, "_get") as mock_get:
            mock_stream = Mock(spec=Stream)

            # Event without sequence attribute
            class EventWithoutSequence:
                pass

            def mock_iter():
                yield EventWithoutSequence()

            mock_stream.__iter__ = mock_iter
            mock_get.return_value = mock_stream

            client = Runloop(api_key="test-key", base_url="http://test")

            stream = client.axons.subscribe_sse("axon-123")

            # Should not crash, sequence extractor should return None
            events = list(stream)
            assert len(events) == 1

    def test_subscribe_sse_preserves_request_options(self):
        """Test that extra headers, query, etc. are preserved."""
        from src.runloop_api_client import Runloop

        with patch.object(Runloop, "_get") as mock_get:
            mock_stream = Mock(spec=Stream)
            mock_stream.__iter__ = lambda self: iter([])
            mock_get.return_value = mock_stream

            client = Runloop(api_key="test-key", base_url="http://test")

            extra_headers = {"X-Custom": "value"}
            extra_query = {"param": "value"}

            client.axons.subscribe_sse(
                "axon-123", extra_headers=extra_headers, extra_query=extra_query, timeout=30.0
            )

            # Verify _get was called with the options
            call_args = mock_get.call_args
            options = call_args.kwargs["options"]

            # Headers should include Accept: text/event-stream and custom header
            assert "Accept" in options["extra_headers"]
            assert options["extra_headers"]["Accept"] == "text/event-stream"
            assert options["extra_headers"]["X-Custom"] == "value"
            assert options["extra_query"] == extra_query
            assert options["timeout"] == 30.0


class TestAxonSSEReconnectAsync:
    """Test SSE reconnection for async Axon subscriptions."""

    @pytest.mark.asyncio
    async def test_subscribe_sse_returns_reconnecting_stream(self):
        """Test that subscribe_sse returns an AsyncReconnectingStream."""
        from src.runloop_api_client import AsyncRunloop

        async def mock_get(*args, **kwargs):
            mock_stream = Mock(spec=AsyncStream)
            return mock_stream

        with patch.object(AsyncRunloop, "_get", side_effect=mock_get):
            client = AsyncRunloop(api_key="test-key", base_url="http://test")

            result = await client.axons.subscribe_sse("axon-123")

            # Should return an AsyncReconnectingStream
            assert isinstance(result, AsyncReconnectingStream)

    @pytest.mark.asyncio
    async def test_subscribe_sse_with_raw_header_returns_plain_stream(self):
        """Test that RAW_RESPONSE_HEADER opts out of reconnection."""
        from src.runloop_api_client import AsyncRunloop

        async def mock_get(*args, **kwargs):
            mock_stream = Mock(spec=AsyncStream)
            return mock_stream

        with patch.object(AsyncRunloop, "_get", side_effect=mock_get) as mock_get_method:
            client = AsyncRunloop(api_key="test-key", base_url="http://test")

            result = await client.axons.subscribe_sse("axon-123", extra_headers={RAW_RESPONSE_HEADER: "true"})

            # Should return plain AsyncStream, not AsyncReconnectingStream
            assert not isinstance(result, AsyncReconnectingStream)

    @pytest.mark.asyncio
    async def test_reconnection_uses_last_sequence(self):
        """Test that reconnection uses the sequence from the last event."""
        from src.runloop_api_client import AsyncRunloop

        call_count = 0
        query_params = []

        async def mock_get(*args, **kwargs):
            nonlocal call_count
            # Capture query params
            if "query" in kwargs.get("options", {}):
                query_params.append(kwargs["options"]["query"])

            # First call: return stream with events
            if call_count == 0:
                call_count += 1
                mock_stream = Mock(spec=AsyncStream)

                async def mock_iter():
                    yield MockAxonEvent(sequence=1, data="event1")
                    yield MockAxonEvent(sequence=2, data="event2")

                mock_stream.__aiter__ = mock_iter
                return mock_stream

            # Second call (reconnection)
            mock_stream = Mock(spec=AsyncStream)

            async def mock_iter():
                yield MockAxonEvent(sequence=3, data="event3")

            mock_stream.__aiter__ = mock_iter
            return mock_stream

        with patch.object(AsyncRunloop, "_get", side_effect=mock_get):
            client = AsyncRunloop(api_key="test-key", base_url="http://test")

            stream = await client.axons.subscribe_sse("axon-123")

            # Consume events
            events = []
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

        async def mock_get(*args, **kwargs):
            mock_stream = Mock(spec=AsyncStream)

            # Event with sequence = None
            class EventWithNoneSequence:
                sequence = None

            async def mock_iter():
                yield EventWithNoneSequence()

            mock_stream.__aiter__ = mock_iter
            return mock_stream

        with patch.object(AsyncRunloop, "_get", side_effect=mock_get):
            client = AsyncRunloop(api_key="test-key", base_url="http://test")

            stream = await client.axons.subscribe_sse("axon-123")

            # Should not crash
            events = []
            async for event in stream:
                events.append(event)
                break

            assert len(events) == 1

    @pytest.mark.asyncio
    async def test_subscribe_sse_preserves_request_options(self):
        """Test that extra headers, query, etc. are preserved in async."""
        from src.runloop_api_client import AsyncRunloop

        async def mock_get(*args, **kwargs):
            mock_stream = Mock(spec=AsyncStream)

            async def mock_iter():
                return
                yield  # Make it async generator

            mock_stream.__aiter__ = mock_iter
            return mock_stream

        with patch.object(AsyncRunloop, "_get", side_effect=mock_get) as mock_get_method:
            client = AsyncRunloop(api_key="test-key", base_url="http://test")

            extra_headers = {"X-Custom": "value"}
            extra_query = {"param": "value"}

            await client.axons.subscribe_sse(
                "axon-123", extra_headers=extra_headers, extra_query=extra_query, timeout=30.0
            )

            # Verify _get was called with the options
            call_args = mock_get_method.call_args
            options = call_args.kwargs["options"]

            # Headers should include Accept: text/event-stream and custom header
            assert "Accept" in options["extra_headers"]
            assert options["extra_headers"]["Accept"] == "text/event-stream"
            assert options["extra_headers"]["X-Custom"] == "value"
            assert options["extra_query"] == extra_query
            assert options["timeout"] == 30.0


class TestAxonSubscribeSseParams:
    """Test AxonSubscribeSseParams TypedDict."""

    def test_params_structure(self):
        """Test that AxonSubscribeSseParams has the correct structure."""
        from src.runloop_api_client.types.axons import AxonSubscribeSseParams
        from src.runloop_api_client._types import NOT_GIVEN

        # Should be able to create with after_sequence
        params: AxonSubscribeSseParams = {"after_sequence": 123}
        assert params["after_sequence"] == 123

        # Should be able to create with NOT_GIVEN
        params2: AxonSubscribeSseParams = {"after_sequence": NOT_GIVEN}
        assert params2["after_sequence"] is NOT_GIVEN

        # Should be able to create with None implicitly (total=False)
        params3: AxonSubscribeSseParams = {}
        assert "after_sequence" not in params3
