"""Secret resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import BaseRequestOptions, LongRequestOptions
from .._client import Runloop
from ..types.secret_view import SecretView


class Secret:
    """Synchronous wrapper around a secret resource.

    Secrets are encrypted key-value pairs that can be securely stored and injected
    into Devboxes as environment variables. This wrapper always operates by its account-scoped
    name, even if it contains an ID from an earlier response. Reads and updates
    select the greatest ID at lookup; deletion removes all selected matches,
    nonatomically. Use ``sdk.secret.from_id(id)`` for exact row operations.

    Example:
        >>> runloop = RunloopSDK()
        >>> secret = runloop.secret.create(
        ...     name="MY_API_KEY",
        ...     value="secret-value",
        ... )
        >>> info = secret.get_info()
        >>> print(f"Secret: {info.name}, ID: {info.id}")
    """

    def __init__(
        self,
        client: Runloop,
        name: str,
        id: str | None = None,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated Runloop client
        :type client: Runloop
        :param name: The literal account-scoped name of the secret
        :type name: str
        :param id: An optional ID captured from the response that constructed this wrapper
        :type id: str | None
        """
        self._client = client
        self._name = name
        self._id = id

    @override
    def __repr__(self) -> str:
        return f"<Secret name={self._name!r}>"

    @property
    def id(self) -> str | None:
        """Return the secret ID.

        :return: Captured response ID, or None. Fetching metadata does not refresh this property.
        :rtype: str | None
        """
        return self._id

    @property
    def name(self) -> str:
        """Return the secret name.

        :return: Literal account-scoped secret name
        :rtype: str
        """
        return self._name

    def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> SecretView:
        """Retrieve the latest secret details from the API.

        Note: The secret value is never returned for security reasons.

        Example:
            >>> info = secret.get_info()
            >>> print(f"Secret: {info.name}, ID: {info.id}, Created: {info.create_time_ms}")

        :param options: Optional request configuration
        :return: API response describing the secret (value not included)
        :rtype: SecretView
        """
        return self._client.secrets.retrieve(
            self._name,
            **options,
        )

    def update(
        self,
        value: str,
        **options: Unpack[LongRequestOptions],
    ) -> SecretView:
        """Update the greatest-ID row matching this name at lookup.

        This wrapper remains name-bound and its captured ID is unchanged.

        Example:
            >>> updated = secret.update("new-secret-value")
            >>> print(f"Updated at: {updated.update_time_ms}")

        :param value: The new secret value (will be encrypted at rest)
        :type value: str
        :param options: Optional request configuration
        :return: Updated secret view
        :rtype: SecretView
        """
        return self._client.secrets.update(
            self._name,
            value=value,
            **options,
        )

    def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> SecretView:
        """Delete every selected row matching this name, nonatomically.

        A concurrent create can survive. This action is irreversible.

        Example:
            >>> secret.delete()

        :param options: Optional long-running request configuration
        :return: API response acknowledging deletion
        :rtype: SecretView
        """
        return self._client.secrets.delete(
            self._name,
            **options,
        )
