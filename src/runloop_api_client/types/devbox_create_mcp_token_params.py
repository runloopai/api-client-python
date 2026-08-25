# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["DevboxCreateMcpTokenParams"]


class DevboxCreateMcpTokenParams(TypedDict, total=False):
    mcp_config: Required[str]
    """The MCP config to use. Can be an MCP config ID (mcp_xxx) or name."""

    secret: Required[str]
    """The secret containing the MCP server credential. Can be a secret ID or name."""
