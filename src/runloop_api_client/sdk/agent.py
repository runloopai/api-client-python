"""Agent resource class for synchronous operations."""

from __future__ import annotations

from typing import Optional
from typing_extensions import Unpack, override

from ._types import (
    BaseRequestOptions,
)
from .._client import Runloop
from ..types.agent_view import AgentView


class Agent:
    """Wrapper around synchronous agent operations.

    This class provides a Pythonic interface for interacting with agents,
    including retrieving agent information.

    Example:
        >>> agent = runloop.agent.create_from_npm(name="my-agent", package_name="@runloop/example-agent")
        >>> info = agent.get_info()
        >>> print(info.name)
    """

    def __init__(
        self,
        client: Runloop,
        agent_id: str,
        agent_view: Optional[AgentView] = None,
    ) -> None:
        """Initialize the wrapper.

        :param client: Generated Runloop client
        :type client: Runloop
        :param agent_id: Agent identifier returned by the API
        :type agent_id: str
        """
        self._client = client
        self._id = agent_id
        self._agent_view = agent_view

    @override
    def __repr__(self) -> str:
        return f"<Agent id={self._id!r}>"

    @property
    def id(self) -> str:
        """Return the agent identifier.

        :return: Unique agent ID
        :rtype: str
        """
        return self._id

    def get_info(
        self,
        **options: Unpack[BaseRequestOptions],
    ) -> AgentView:
        """Retrieve the latest agent information.

        :param options: Optional request configuration
        :return: Agent details
        :rtype: AgentView
        """
        return self._client.agents.retrieve(
            self._id,
            **options,
        )
