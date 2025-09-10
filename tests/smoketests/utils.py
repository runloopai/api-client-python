import os
import time
from typing import Any, Mapping

from runloop_api_client import Runloop


def unique_name(prefix: str) -> str:
    return f"{prefix}-{int(time.time() * 1000)}"


THIRTY_SECOND_TIMEOUT = 30


def make_client(**overrides: Mapping[str, Any]) -> Runloop:
    """Create a Runloop client from local src with sane defaults.

    Read RUNLOOP_BASE_URL and RUNLOOP_API_KEY from environment.
    """

    base_url = os.getenv("RUNLOOP_BASE_URL")
    bearer_token = os.getenv("RUNLOOP_API_KEY")

    # Default values similar to TS smoketests
    kwargs: dict[str, Any] = {
        "base_url": base_url,
        "bearer_token": bearer_token,
        "timeout": 120.0,
        "max_retries": 1,
    }
    if overrides:
        kwargs.update(dict(overrides))

    return Runloop(**kwargs)
