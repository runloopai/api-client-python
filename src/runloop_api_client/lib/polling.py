import time
from typing import Any, TypeVar, Callable, Optional
from dataclasses import dataclass

T = TypeVar("T")


@dataclass
class PollingConfig:
    """Configuration for polling behavior"""

    interval_seconds: float = 1.0
    max_attempts: int = 120
    timeout_seconds: Optional[float] = None


class PollingTimeout(Exception):
    """Raised when polling exceeds max attempts or timeout"""

    def __init__(self, message: str, last_value: Any):
        self.last_value = last_value
        super().__init__(f"{message}. Last retrieved value: {last_value}")


def poll_until(
    retriever: Callable[[], T],
    is_terminal: Callable[[T], bool],
    config: Optional[PollingConfig] = None,
    on_error: Optional[Callable[[Exception], T]] = None,
) -> T:
    """
    Poll until a condition is met or timeout/max attempts are reached.

    Args:
        retriever: Callable that returns the object to check
        is_terminal: Callable that returns True when polling should stop
        config: Optional polling configuration
        on_error: Optional error handler that can return a value to continue polling
                 or re-raise the exception to stop polling

    Returns:
        The final state of the polled object

    Raises:
        PollingTimeout: When max attempts or timeout is reached
    """
    if config is None:
        config = PollingConfig()

    attempts = 0
    start_time = time.time()
    last_result = None

    while True:
        try:
            last_result = retriever()
        except Exception as e:
            if on_error is not None:
                last_result = on_error(e)
            else:
                raise

        if is_terminal(last_result):
            return last_result

        attempts += 1
        if attempts >= config.max_attempts:
            raise PollingTimeout(f"Exceeded maximum attempts ({config.max_attempts})", last_result)

        if config.timeout_seconds is not None:
            elapsed = time.time() - start_time
            if elapsed >= config.timeout_seconds:
                raise PollingTimeout(f"Exceeded timeout of {config.timeout_seconds} seconds", last_result)

        time.sleep(config.interval_seconds)
