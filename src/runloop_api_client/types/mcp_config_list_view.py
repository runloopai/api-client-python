# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .mcp_config_view import McpConfigView

__all__ = ["McpConfigListView"]


class McpConfigListView(BaseModel):
    """A paginated list of McpConfigs."""

    has_more: bool
    """Whether there are more results available beyond this page."""

    mcp_configs: List[McpConfigView]
    """The list of McpConfigs."""

    total_count: int
    """Total count of McpConfigs that match the query."""
