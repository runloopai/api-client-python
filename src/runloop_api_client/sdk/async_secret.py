"""Secret resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import BaseRequestOptions, LongRequestOptions
from .._client import AsyncRunloop
from ..types.secret_view import SecretView


class AsyncSecret:
    """Asynchronous wrapper around a secret resource.

    Secrets are encrypted key-value pairs that can be securely stored and injected
    into Devboxes as environment variables. Secrets are identified by their globally
    unique name.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> secret = await runloop.secret.create(
        ...     name="MY_API_KEY",
        ...     value="secret-value",
        ... )
        >>> info = await secret.get_info()
        >>> print(f"Secret: {info.name}, ID: {info.id}")
    """

    def __init__(
        self,
        client: AsyncRunloop,
        name: str,
        id: str | None = None,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param name: The globally unique name of the secret
        :type name: str
        :param id: The secret ID (optional, may not be known until get_info is called)
        :type id: str | None
        """
        self._client = client
        self._name = name
        self._id = id

    @override
    def __repr__(self) -> str:
        return f"<AsyncSecret name={self._name!r}>"

    @property
    def id(self) -> str | None:
        """Return the secret ID.

        :return: Secret ID, or None if not yet fetched from API
        :rtype: str | None
        """
        return self._id

    @property
    def name(self) -> str:
        """Return the secret name.

        :return: Globally unique secret name
        :rtype: str
        """
        return self._name

    async def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> SecretView:
        """Retrieve the latest secret details from the API.

        Note: The secret value is never returned for security reasons.

        Example:
            >>> info = await secret.get_info()
            >>> print(f"Secret: {info.name}, ID: {info.id}, Created: {info.create_time_ms}")

        :param options: Optional request configuration
        :return: API response describing the secret (value not included)
        :rtype: SecretView
        """
        return await self._client.secrets.retrieve(
            self._name,
            **options,
        )

    async def update(
        self,
        value: str,
        **options: Unpack[LongRequestOptions],
    ) -> SecretView:
        """Update this secret's value.

        Example:
            >>> updated = await secret.update("new-secret-value")
            >>> print(f"Updated at: {updated.update_time_ms}")

        :param value: The new secret value (will be encrypted at rest)
        :type value: str
        :param options: Optional request configuration
        :return: Updated secret view
        :rtype: SecretView
        """
        return await self._client.secrets.update(
            self._name,
            value=value,
            **options,
        )

    async def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> SecretView:
        """Delete this secret. This action is irreversible.

        Example:
            >>> await secret.delete()

        :param options: Optional long-running request configuration
        :return: API response acknowledging deletion
        :rtype: SecretView
        """
        return await self._client.secrets.delete(
            self._name,
            **options,
        )
