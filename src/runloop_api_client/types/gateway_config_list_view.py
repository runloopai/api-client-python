# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .gateway_config_view import GatewayConfigView

__all__ = ["GatewayConfigListView"]


class GatewayConfigListView(BaseModel):
    """A paginated list of GatewayConfigs."""

    gateway_configs: List[GatewayConfigView]
    """The list of GatewayConfigs."""

    has_more: bool
    """Whether there are more results available beyond this page."""

    total_count: Optional[int] = None
    """Total count of GatewayConfigs that match the query.

    Deprecated: will be removed in a future breaking change.
    """
