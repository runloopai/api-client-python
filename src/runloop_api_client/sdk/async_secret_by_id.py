"""Exact-ID Secret operations, separate from legacy name selectors."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import BaseRequestOptions, LongRequestOptions
from .._client import AsyncRunloop
from ..types.secret_view import SecretView


class AsyncSecretById:
    """An exact Secret row, obtained with ``sdk.secret.from_id(id)``.

    Construction makes no request. The ID never changes, but another writer can
    change the value. Requests retain the generated client's retry policy and are
    not exactly-once operations. Use ``get_info()`` for the name and metadata;
    values are never returned.
    """

    def __init__(self, client: AsyncRunloop, id: str) -> None:
        self._client = client
        self._id = id

    @override
    def __repr__(self) -> str:
        return f"<AsyncSecretById id={self._id!r}>"

    @property
    def id(self) -> str:
        """The exact row ID, not a name or an immutable value-version identifier."""
        return self._id

    async def get_info(self, **options: Unpack[BaseRequestOptions]) -> SecretView:
        """Retrieve this row's metadata. Missing IDs never fall back to names."""
        return await self._client.secrets.retrieve_by_id(self._id, **options)

    async def update(self, value: str, **options: Unpack[LongRequestOptions]) -> SecretView:
        """Replace this row's value, without changing running devbox environments or issued tokens."""
        return await self._client.secrets.update_by_id(self._id, value=value, **options)

    async def delete(self, **options: Unpack[LongRequestOptions]) -> SecretView:
        """Delete only this row. Name readers may then see an older same-name row."""
        return await self._client.secrets.delete_by_id(self._id, **options)
