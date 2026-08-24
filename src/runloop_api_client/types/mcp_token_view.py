# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel

__all__ = ["McpTokenView"]


class McpTokenView(BaseModel):
    token: str
    """The token to send to the MCP hub as a Bearer token in the Authorization header.

    Only accepted for requests originating from the bound Devbox.
    """

    allowed_tools: List[str]
    """Glob patterns for the tools the token permits."""

    devbox_id: str
    """The Devbox the token is bound to."""

    endpoint: str
    """The upstream MCP server endpoint the hub proxies to."""

    mcp_config_id: str
    """The ID of the MCP config the token grants access to."""

    url: str
    """The MCP hub URL the token authenticates against.

    Matches the RL_MCP_URL environment variable inside the Devbox.
    """
