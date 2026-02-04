"""GatewayConfig resource class for synchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import BaseRequestOptions, LongRequestOptions, SDKGatewayConfigUpdateParams
from .._client import Runloop
from ..types.gateway_config_view import GatewayConfigView


class GatewayConfig:
    """Synchronous wrapper around a gateway config resource.

    Gateway configs define how to proxy API requests through the credential gateway.
    They specify the target endpoint and how credentials should be applied. Use with
    devboxes to securely proxy requests to external APIs without exposing API keys.

    Example:
        >>> runloop = RunloopSDK()
        >>> gateway_config = runloop.gateway_config.create(
        ...     name='my-api-gateway',
        ...     endpoint='https://api.example.com',
        ...     auth_mechanism={'type': 'bearer'},
        ... )
        >>> info = gateway_config.get_info()
        >>> print(f"Gateway Config: {info.name}")
    """

    def __init__(
        self,
        client: Runloop,
        gateway_config_id: str,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated Runloop client
        :type client: Runloop
        :param gateway_config_id: GatewayConfig ID returned by the API
        :type gateway_config_id: str
        """
        self._client = client
        self._id = gateway_config_id

    @override
    def __repr__(self) -> str:
        return f"<GatewayConfig id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the gateway config ID.

        :return: Unique gateway config ID
        :rtype: str
        """
        return self._id

    def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> GatewayConfigView:
        """Retrieve the latest gateway config details.

        Example:
            >>> info = gateway_config.get_info()
            >>> print(f"Gateway Config: {info.name}, endpoint: {info.endpoint}")

        :param options: Optional request configuration
        :return: API response describing the gateway config
        :rtype: GatewayConfigView
        """
        return self._client.gateway_configs.retrieve(
            self._id,
            **options,
        )

    def update(self, **params: Unpack[SDKGatewayConfigUpdateParams]) -> GatewayConfigView:
        """Update the gateway config.

        Example:
            >>> updated = gateway_config.update(
            ...     name='updated-gateway-name',
            ...     description='Updated description',
            ... )

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKGatewayConfigUpdateParams` for available parameters
        :return: Updated gateway config view
        :rtype: GatewayConfigView
        """
        return self._client.gateway_configs.update(self._id, **params)

    def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> GatewayConfigView:
        """Delete the gateway config. This action is irreversible.

        Example:
            >>> gateway_config.delete()

        :param options: Optional long-running request configuration
        :return: API response acknowledging deletion
        :rtype: GatewayConfigView
        """
        return self._client.gateway_configs.delete(
            self._id,
            **options,
        )
