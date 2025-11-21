"""Agent resource class for asynchronous operations."""

from __future__ import annotations

from typing_extensions import Unpack, override

from ._types import (
    RequestOptions,
)
from .._client import AsyncRunloop
from ..types.agent_view import AgentView


class AsyncAgent:
    """Async wrapper around agent operations."""

    def __init__(
        self,
        client: AsyncRunloop,
        agent_id: str,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated AsyncRunloop client
        :type client: AsyncRunloop
        :param agent_id: Agent identifier returned by the API
        :type agent_id: str
        """
        self._client = client
        self._id = agent_id

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
        **options: Unpack[RequestOptions],
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
