"""NetworkPolicy resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import BaseRequestOptions, LongRequestOptions, SDKNetworkPolicyUpdateParams
from .._client import AsyncRunloop
from ..types.network_policy_view import NetworkPolicyView


class AsyncNetworkPolicy:
    """Asynchronous wrapper around a network policy resource."""

    def __init__(
        self,
        client: AsyncRunloop,
        network_policy_id: str,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param network_policy_id: NetworkPolicy ID returned by the API
        :type network_policy_id: str
        """
        self._client = client
        self._id = network_policy_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncNetworkPolicy id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the network policy ID.

        :return: Unique network policy ID
        :rtype: str
        """
        return self._id

    async def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> NetworkPolicyView:
        """Retrieve the latest network policy details.

        :param options: Optional request configuration
        :return: API response describing the network policy
        :rtype: NetworkPolicyView
        """
        return await self._client.network_policies.retrieve(
            self._id,
            **options,
        )

    async def update(self, **params: Unpack[SDKNetworkPolicyUpdateParams]) -> NetworkPolicyView:
        """Update the network policy.

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKNetworkPolicyUpdateParams` for available parameters
        :return: Updated network policy view
        :rtype: NetworkPolicyView
        """
        return await self._client.network_policies.update(self._id, **params)

    async def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> NetworkPolicyView:
        """Delete the network policy.

        :param options: Optional long-running request configuration
        :return: API response acknowledging deletion
        :rtype: NetworkPolicyView
        """
        return await self._client.network_policies.delete(
            self._id,
            **options,
        )
