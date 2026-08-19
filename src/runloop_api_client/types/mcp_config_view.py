# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .shared.custom_header import CustomHeader

__all__ = ["McpConfigView"]


class McpConfigView(BaseModel):
    """
    An McpConfig defines a configuration for connecting to an upstream MCP (Model Context Protocol) server. It specifies the target endpoint and which tools are allowed.
    """

    id: str
    """The unique identifier of the McpConfig."""

    allowed_tools: List[str]
    """
    Glob patterns specifying which tools are allowed from this MCP server (e.g.,
    ['github.search_*', 'github.get_*'] or ['*'] for all tools).
    """

    create_time_ms: int
    """Creation time of the McpConfig (Unix timestamp in milliseconds)."""

    endpoint: str
    """The target MCP server endpoint URL (e.g., 'https://mcp.example.com')."""

    name: str
    """The human-readable name of the McpConfig. Unique per account."""

    custom_headers: Optional[List[CustomHeader]] = None
    """Additional headers applied to upstream requests after the credential.

    Secret-backed entries reference the secret by 'sec\\__' id; values are never
    returned.
    """

    description: Optional[str] = None
    """Optional description for this MCP configuration."""
