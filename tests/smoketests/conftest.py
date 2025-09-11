from __future__ import annotations

from typing import Iterator

import pytest
from _pytest.fixtures import FixtureRequest  # pyright: ignore[reportPrivateImportUsage]

from runloop_api_client import Runloop

from .utils import make_client, make_async_client_adapter

"""
This file is used to create a client fixture for the tests.
It makes it possible to run the tests with both sync and async clients.
"""


@pytest.fixture(scope="module", params=["sync", "async"], ids=["sync-client", "async-client"])
def client(request: FixtureRequest) -> Iterator[Runloop]:
    if request.param == "sync":
        c: Runloop = make_client()
        try:
            yield c
        finally:
            try:
                # Runloop supports close()
                c.close()
            except Exception:
                pass
    else:
        c: Runloop = make_async_client_adapter()
        try:
            yield c
        finally:
            try:
                c.close()
            except Exception:
                pass
