from typing import Any
from unittest.mock import Mock, patch

import pytest

from src.runloop_api_client.lib.polling import PollingConfig, PollingTimeout, poll_until


class TestPollingConfig:
    """Test PollingConfig dataclass"""

    def test_default_config(self):
        config = PollingConfig()
        assert config.interval_seconds == 1.0
        assert config.max_attempts == 120
        assert config.timeout_seconds is None

    def test_custom_config(self):
        config = PollingConfig(interval_seconds=0.5, max_attempts=10, timeout_seconds=30.0)
        assert config.interval_seconds == 0.5
        assert config.max_attempts == 10
        assert config.timeout_seconds == 30.0


class TestPollingTimeout:
    """Test PollingTimeout exception"""

    def test_polling_timeout_initialization(self):
        last_value = {"status": "running"}
        exception = PollingTimeout("Test message", last_value)

        assert exception.last_value == last_value
        assert "Test message" in str(exception)
        assert "Last retrieved value: {'status': 'running'}" in str(exception)


class TestPollUntil:
    """Test poll_until function"""

    def test_immediate_success(self):
        """Test when condition is met on first attempt"""
        retriever = Mock(return_value="completed")
        is_terminal = Mock(return_value=True)

        result = poll_until(retriever, is_terminal)

        assert result == "completed"
        assert retriever.call_count == 1
        assert is_terminal.call_count == 1
        is_terminal.assert_called_with("completed")

    def test_success_after_multiple_attempts(self):
        """Test when condition is met after several attempts"""
        values = ["pending", "running", "completed"]
        retriever = Mock(side_effect=values)
        is_terminal = Mock(side_effect=[False, False, True])

        with patch("time.sleep") as mock_sleep:
            result = poll_until(retriever, is_terminal)

        assert result == "completed"
        assert retriever.call_count == 3
        assert is_terminal.call_count == 3
        assert mock_sleep.call_count == 2  # Should sleep between attempts

    def test_custom_config_interval(self):
        """Test with custom polling interval"""
        retriever = Mock(side_effect=["pending", "completed"])
        is_terminal = Mock(side_effect=[False, True])
        config = PollingConfig(interval_seconds=0.1)

        with patch("time.sleep") as mock_sleep:
            result = poll_until(retriever, is_terminal, config)

        assert result == "completed"
        mock_sleep.assert_called_with(0.1)

    def test_max_attempts_exceeded(self):
        """Test when max attempts is exceeded"""
        retriever = Mock(return_value="still_running")
        is_terminal = Mock(return_value=False)
        config = PollingConfig(max_attempts=3, interval_seconds=0.01)

        with patch("time.sleep"):
            with pytest.raises(PollingTimeout) as exc_info:
                poll_until(retriever, is_terminal, config)

        assert "Exceeded maximum attempts (3)" in str(exc_info.value)
        assert exc_info.value.last_value == "still_running"
        assert retriever.call_count == 3

    def test_timeout_exceeded(self):
        """Test when timeout is exceeded"""
        retriever = Mock(return_value="still_running")
        is_terminal = Mock(return_value=False)
        config = PollingConfig(timeout_seconds=0.1, interval_seconds=0.01)

        # Mock time.time to simulate timeout
        start_time = 1000.0
        with patch("time.time", side_effect=[start_time, start_time + 0.05, start_time + 0.15]):
            with patch("time.sleep"):
                with pytest.raises(PollingTimeout) as exc_info:
                    poll_until(retriever, is_terminal, config)

        assert "Exceeded timeout of 0.1 seconds" in str(exc_info.value)
        assert exc_info.value.last_value == "still_running"

    def test_error_without_handler(self):
        """Test that exceptions are re-raised when no error handler is provided"""
        retriever = Mock(side_effect=ValueError("Test error"))
        is_terminal = Mock(return_value=False)

        with pytest.raises(ValueError, match="Test error"):
            poll_until(retriever, is_terminal)

    def test_error_with_handler_continue(self):
        """Test error handler that allows polling to continue"""
        retriever = Mock(side_effect=[ValueError("Test error"), "recovered"])
        is_terminal = Mock(side_effect=[False, True])

        def error_handler(_: Exception) -> str:
            return "error_handled"

        with patch("time.sleep"):
            result = poll_until(retriever, is_terminal, on_error=error_handler)

        assert result == "recovered"
        assert retriever.call_count == 2
        assert is_terminal.call_count == 2

    def test_error_with_handler_reraise(self):
        """Test error handler that re-raises the exception"""
        retriever = Mock(side_effect=ValueError("Test error"))
        is_terminal = Mock(return_value=False)

        def error_handler(e: Exception) -> None:
            raise e

        with pytest.raises(ValueError, match="Test error"):
            poll_until(retriever, is_terminal, on_error=error_handler)

    def test_error_handler_return_terminal_value(self):
        """Test error handler that returns a terminal value"""
        retriever = Mock(side_effect=ValueError("Test error"))
        is_terminal = Mock(side_effect=[True])  # Terminal condition met on error handler return

        def error_handler(_: Exception) -> str:
            return "error_terminal"

        result = poll_until(retriever, is_terminal, on_error=error_handler)

        assert result == "error_terminal"
        assert retriever.call_count == 1
        assert is_terminal.call_count == 1

    def test_multiple_errors_with_handler(self):
        """Test multiple errors with handler"""
        retriever = Mock(side_effect=[ValueError("Error 1"), RuntimeError("Error 2"), "success"])
        is_terminal = Mock(side_effect=[False, False, True])

        error_count = 0

        def error_handler(_: Exception) -> str:
            nonlocal error_count
            error_count += 1
            return f"handled_error_{error_count}"

        with patch("time.sleep"):
            result = poll_until(retriever, is_terminal, on_error=error_handler)

        assert result == "success"
        assert error_count == 2
        assert retriever.call_count == 3

    def test_none_values_handling(self):
        """Test handling of None values"""
        retriever = Mock(side_effect=[None, None, "final"])
        is_terminal = Mock(side_effect=[False, False, True])

        with patch("time.sleep"):
            result = poll_until(retriever, is_terminal)

        assert result == "final"
        assert retriever.call_count == 3

    def test_complex_object_polling(self):
        """Test polling with complex objects"""

        class Status:
            def __init__(self, state: str, progress: int):
                self.state = state
                self.progress = progress

        statuses = [Status("starting", 0), Status("running", 50), Status("completed", 100)]

        retriever = Mock(side_effect=statuses)
        is_terminal = Mock(side_effect=[False, False, True])

        with patch("time.sleep"):
            result = poll_until(retriever, is_terminal)

        assert result.state == "completed"
        assert result.progress == 100

    def test_zero_max_attempts(self):
        """Test with zero max attempts"""
        retriever = Mock(return_value="value")
        is_terminal = Mock(return_value=False)
        config = PollingConfig(max_attempts=0)

        with pytest.raises(PollingTimeout) as exc_info:
            poll_until(retriever, is_terminal, config)

        assert "Exceeded maximum attempts (0)" in str(exc_info.value)
        assert retriever.call_count == 1  # Retriever is called once, then attempts check happens

    def test_negative_interval(self):
        """Test with negative interval (should still work)"""
        retriever = Mock(side_effect=["first", "second"])
        is_terminal = Mock(side_effect=[False, True])
        config = PollingConfig(interval_seconds=-0.1)

        with patch("time.sleep") as mock_sleep:
            result = poll_until(retriever, is_terminal, config)

        assert result == "second"
        mock_sleep.assert_called_with(-0.1)

    def test_both_timeout_and_max_attempts(self):
        """Test when both timeout and max_attempts are set"""
        retriever = Mock(return_value="still_running")
        is_terminal = Mock(return_value=False)
        config = PollingConfig(max_attempts=5, timeout_seconds=0.1, interval_seconds=0.01)

        # Mock time to hit timeout before max_attempts
        start_time = 1000.0
        with patch("time.time", side_effect=[start_time, start_time + 0.05, start_time + 0.15]):
            with patch("time.sleep"):
                with pytest.raises(PollingTimeout) as exc_info:
                    poll_until(retriever, is_terminal, config)

        # Should hit timeout first
        assert "Exceeded timeout of 0.1 seconds" in str(exc_info.value)
        assert retriever.call_count == 2  # Called twice before timeout

    def test_terminal_condition_changes(self):
        """Test when terminal condition logic changes during polling"""
        retriever = Mock(side_effect=["value1", "value2", "value3"])

        call_count = 0

        def dynamic_terminal(_: Any) -> bool:
            nonlocal call_count
            call_count += 1
            # First two calls return False, third returns True
            return call_count >= 3

        with patch("time.sleep"):
            result = poll_until(retriever, dynamic_terminal)

        assert result == "value3"
        assert retriever.call_count == 3
