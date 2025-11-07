from __future__ import annotations

from typing import Mapping

import httpx

from .devbox import DevboxClient
from .._types import Timeout, NotGiven, not_given
from .._client import Runloop
from .snapshot import SnapshotClient
from .blueprint import BlueprintClient
from .storage_object import StorageObjectClient


class RunloopSDK:
    """
    High-level synchronous entry point for the Runloop SDK.

    This thin wrapper exposes the generated REST client via the ``api`` attribute.
    Higher-level object-oriented helpers will be layered on top incrementally.
    """

    api: Runloop
    devbox: DevboxClient
    blueprint: BlueprintClient
    snapshot: SnapshotClient
    storage_object: StorageObjectClient

    def __init__(
        self,
        *,
        client: Runloop | None = None,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int | None = None,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        http_client: httpx.Client | None = None,
        _strict_response_validation: bool = False,
    ) -> None:
        """
        Create a synchronous Runloop SDK instance.

        Arguments mirror :class:`runloop_api_client.Runloop`. Additional high-level helpers
        are exposed as attributes on this class as they're implemented.
        """
        if client is None:
            runloop_kwargs: dict[str, object] = {
                "bearer_token": bearer_token,
                "base_url": base_url,
                "timeout": timeout,
                "max_retries": max_retries,
                "default_headers": default_headers,
                "default_query": default_query,
                "http_client": http_client,
                "_strict_response_validation": _strict_response_validation,
            }

            self.api = Runloop(**runloop_kwargs)
            self._owns_client = True
        else:
            self.api = client
            self._owns_client = False

        self.devbox = DevboxClient(self.api)
        self.blueprint = BlueprintClient(self.api, self.devbox)
        self.snapshot = SnapshotClient(self.api, self.devbox)
        self.storage_object = StorageObjectClient(self.api)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        if self._owns_client:
            self.api.close()

    def __enter__(self) -> "RunloopSDK":
        return self

    def __exit__(self, *_exc_info: object) -> None:
        self.close()
