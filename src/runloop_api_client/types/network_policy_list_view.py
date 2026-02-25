# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel
from .network_policy_view import NetworkPolicyView

__all__ = ["NetworkPolicyListView"]


class NetworkPolicyListView(BaseModel):
    """A list of NetworkPolicies with pagination information."""

    has_more: bool
    """Whether there are more results available."""

    network_policies: List[NetworkPolicyView]
    """The list of NetworkPolicies."""

    total_count: Optional[int] = None
    """Total count of items in this response.

    Deprecated: will be removed in a future breaking change.
    """
