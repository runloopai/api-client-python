# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from .._models import BaseModel

__all__ = ["NetworkPolicyView", "Egress"]


class Egress(BaseModel):
    """The egress rules for this policy."""

    allow_all: bool
    """If true, all egress traffic is allowed and other fields are ignored.

    Used for ALLOW_ALL policies.
    """

    allow_devbox_to_devbox: bool
    """If true, allows traffic between the account's own devboxes via tunnels."""

    allowed_hostnames: List[str]
    """DNS-based allow list with wildcard support.

    Examples: ['github.com', '*.npmjs.org', 'api.openai.com']. Empty list with
    allow_all=false means no network access (DENY_ALL behavior).
    """


class NetworkPolicyView(BaseModel):
    """A NetworkPolicy defines egress network access rules for devboxes.

    Policies can be applied to blueprints, devboxes, and snapshot resumes.
    """

    id: str
    """The unique identifier of the NetworkPolicy."""

    create_time_ms: int
    """The creation time of the NetworkPolicy (Unix timestamp in milliseconds)."""

    egress: Egress
    """The egress rules for this policy."""

    name: str
    """The human-readable name of the NetworkPolicy. Unique per account."""

    update_time_ms: int
    """Last update time of the NetworkPolicy (Unix timestamp in milliseconds)."""

    description: Optional[str] = None
    """Optional description of the NetworkPolicy."""
