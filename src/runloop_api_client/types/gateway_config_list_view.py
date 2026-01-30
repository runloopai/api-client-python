# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from .._models import BaseModel
from .gateway_config_view import GatewayConfigView

__all__ = ["GatewayConfigListView"]


class GatewayConfigListView(BaseModel):
    """A paginated list of GatewayConfigs."""

    gateway_configs: List[GatewayConfigView]
    """The list of GatewayConfigs."""

    has_more: bool
    """Whether there are more results available beyond this page."""

    total_count: int
    """Total count of GatewayConfigs that match the query."""
