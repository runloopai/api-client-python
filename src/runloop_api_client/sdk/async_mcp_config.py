"""McpConfig resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import BaseRequestOptions, LongRequestOptions, SDKMcpConfigUpdateParams
from .._client import AsyncRunloop
from ..types.mcp_config_view import McpConfigView


class AsyncMcpConfig:
    """Asynchronous wrapper around an MCP config resource.

    MCP configs define how to connect to upstream MCP (Model Context Protocol) servers.
    They specify the target endpoint and which tools are allowed. Use with devboxes to
    securely connect to MCP servers.

    Example:
        >>> runloop = AsyncRunloopSDK()
        >>> mcp_config = await runloop.mcp_config.create(
        ...     name="my-mcp-server",
        ...     endpoint="https://mcp.example.com",
        ...     allowed_tools=["*"],
        ... )
        >>> info = await mcp_config.get_info()
        >>> print(f"MCP Config: {info.name}")
    """

    def __init__(
        self,
        client: AsyncRunloop,
        mcp_config_id: str,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param mcp_config_id: McpConfig ID returned by the API
        :type mcp_config_id: str
        """
        self._client = client
        self._id = mcp_config_id

    @override
    def __repr__(self) -> str:
        return f"<AsyncMcpConfig id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the MCP config ID.

        :return: Unique MCP config ID
        :rtype: str
        """
        return self._id

    async def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> McpConfigView:
        """Retrieve the latest MCP config details.

        Example:
            >>> info = await mcp_config.get_info()
            >>> print(f"MCP Config: {info.name}, endpoint: {info.endpoint}")

        :param options: Optional request configuration
        :return: API response describing the MCP config
        :rtype: McpConfigView
        """
        return await self._client.mcp_configs.retrieve(
            self._id,
            **options,
        )

    async def update(self, **params: Unpack[SDKMcpConfigUpdateParams]) -> McpConfigView:
        """Update the MCP config.

        Example:
            >>> updated = await mcp_config.update(
            ...     name="updated-mcp-name",
            ...     description="Updated description",
            ... )

        :param params: See :typeddict:`~runloop_api_client.sdk._types.SDKMcpConfigUpdateParams` for available parameters
        :return: Updated MCP config view
        :rtype: McpConfigView
        """
        return await self._client.mcp_configs.update(self._id, **params)

    async def delete(
        self,
        **options: Unpack[LongRequestOptions],
    ) -> McpConfigView:
        """Delete the MCP config. This action is irreversible.

        Example:
            >>> await mcp_config.delete()

        :param options: Optional long-running request configuration
        :return: API response acknowledging deletion
        :rtype: McpConfigView
        """
        return await self._client.mcp_configs.delete(
            self._id,
            **options,
        )
