from __future__ import annotations

from typing import Mapping

import httpx

from .._types import Timeout, NotGiven, not_given
from .._client import AsyncRunloop
from .async_devbox import AsyncDevboxClient
from .async_snapshot import AsyncSnapshotClient
from .async_blueprint import AsyncBlueprintClient
from .async_storage_object import AsyncStorageObjectClient


class AsyncRunloopSDK:
    """
    High-level asynchronous entry point for the Runloop SDK.

    The generated async REST client remains available via the ``api`` attribute.
    Higher-level helpers will be introduced incrementally.
    """

    api: AsyncRunloop
    devbox: AsyncDevboxClient
    blueprint: AsyncBlueprintClient
    snapshot: AsyncSnapshotClient
    storage_object: AsyncStorageObjectClient

    def __init__(
        self,
        *,
        client: AsyncRunloop | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int | None = None,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.AsyncClient | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """
        Create an asynchronous Runloop SDK instance.

        Arguments mirror :class:`runloop_api_client.AsyncRunloop`.
        """
        if client is None:
            runloop_kwargs: dict[str, object] = {
                "bearer_token": bearer_token,
                "base_url": base_url,
                "timeout": timeout,
                "default_headers": default_headers,
                "default_query": default_query,
                "http_client": http_client,
                "_strict_response_validation": _strict_response_validation,
            }
            if max_retries is not None:
                runloop_kwargs["max_retries"] = max_retries

            self.api = AsyncRunloop(**runloop_kwargs)
            self._owns_client = True
        else:
            self.api = client
            self._owns_client = False

        self.devbox = AsyncDevboxClient(self.api)
        self.blueprint = AsyncBlueprintClient(self.api, self.devbox)
        self.snapshot = AsyncSnapshotClient(self.api, self.devbox)
        self.storage_object = AsyncStorageObjectClient(self.api)

    async def aclose(self) -> None:
        """Close the underlying async HTTP client."""
        if self._owns_client:
            await self.api.close()

    async def __aenter__(self) -> "AsyncRunloopSDK":
        return self

    async def __aexit__(self, *_exc_info: object) -> None:
        await self.aclose()
