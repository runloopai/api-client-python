"""Agent resource class for asynchronous operations."""

from __future__ import annotations

from typing import Optional
from typing_extensions import Unpack, override

from ._types import (
    BaseRequestOptions,
)
from .._client import AsyncRunloop
from ..types.agent_view import AgentView


class AsyncAgent:
    """Async wrapper around agent operations.

    This class provides an asynchronous interface for interacting with agents,
    including retrieving agent information.

    Example:
        >>> agent = await runloop.agent.create_from_npm(name="my-agent", package_name="@runloop/example-agent")
        >>> info = await agent.get_info()
        >>> print(info.name)
    """

    def __init__(
        self,
        client: AsyncRunloop,
        agent_id: str,
        agent_view: Optional[AgentView] = None,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param agent_id: Agent identifier returned by the API
        :type agent_id: str
        """
        self._client = client
        self._id = agent_id
        self._agent_view = agent_view

    @override
    def __repr__(self) -> str:
        return f"<AsyncAgent id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the agent identifier.

        :return: Unique agent ID
        :rtype: str
        """
        return self._id

    async def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> AgentView:
        """Retrieve the latest agent information.

        :param options: Optional request configuration
        :return: Agent details
        :rtype: AgentView
        """
        return await self._client.agents.retrieve(
            self._id,
            **options,
        )
