# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["McpConfigCreateParams"]


class McpConfigCreateParams(TypedDict, total=False):
    allowed_tools: Required[SequenceNotStr[str]]
    """Glob patterns specifying which tools are allowed from this MCP server.

    Examples: ['*'] for all tools, ['github.search_*', 'github.get_*'] for specific
    patterns.
    """

    endpoint: Required[str]
    """The target MCP server endpoint URL (e.g., 'https://mcp.example.com')."""

    name: Required[str]
    """The human-readable name for the McpConfig.

    Must be unique within your account. The first segment before '-' is used as the
    service name for tool routing (e.g., 'github-readonly' uses 'github' as the
    service name).
    """

    description: Optional[str]
    """Optional description for this MCP configuration."""
