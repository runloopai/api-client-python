# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

from .._types import SequenceNotStr

__all__ = ["McpConfigUpdateParams"]


class McpConfigUpdateParams(TypedDict, total=False):
    allowed_tools: Optional[SequenceNotStr[str]]
    """New glob patterns specifying which tools are allowed.

    Examples: ['*'] for all tools, ['github.search_*'] for specific patterns.
    """

    description: Optional[str]
    """New description for this MCP configuration."""

    endpoint: Optional[str]
    """New target MCP server endpoint URL."""

    name: Optional[str]
    """New name for the McpConfig. Must be unique within your account."""
