# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable, Optional
from typing_extensions import TypedDict

from .._types import SequenceNotStr
from .shared_params.custom_header import CustomHeader
from .shared_params.auth_mechanism import AuthMechanism

__all__ = ["McpConfigUpdateParams"]


class McpConfigUpdateParams(TypedDict, total=False):
    allowed_tools: Optional[SequenceNotStr[str]]
    """New glob patterns specifying which tools are allowed.

    Examples: ['*'] for all tools, ['github.search_*'] for specific patterns.
    """

    auth_mechanism: Optional[AuthMechanism]
    """
    Defines how the primary credential is applied to requests proxied to the
    upstream.
    """

    custom_headers: Optional[Iterable[CustomHeader]]
    """New list of additional headers.

    Replaces the existing list entirely; use an empty list to clear all custom
    headers. At most 8 entries.
    """

    description: Optional[str]
    """New description for this MCP configuration."""

    endpoint: Optional[str]
    """New target MCP server endpoint URL."""

    name: Optional[str]
    """New name for the McpConfig. Must be unique within your account."""
