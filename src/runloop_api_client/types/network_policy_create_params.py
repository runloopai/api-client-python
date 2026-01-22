# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

from .._types import SequenceNotStr

__all__ = ["NetworkPolicyCreateParams"]


class NetworkPolicyCreateParams(TypedDict, total=False):
    name: Required[str]
    """The human-readable name for the NetworkPolicy.

    Must be unique within the account.
    """

    allow_all: Optional[bool]
    """(Optional) If true, all egress traffic is allowed (ALLOW_ALL policy).

    Defaults to false.
    """

    allow_devbox_to_devbox: Optional[bool]
    """
    (Optional) If true, allows traffic between the account's own devboxes via
    tunnels. Defaults to false. If allow_all is true, this is automatically set to
    true.
    """

    allowed_hostnames: Optional[SequenceNotStr[str]]
    """(Optional) DNS-based allow list with wildcard support.

    Examples: ['github.com', '*.npmjs.org'].
    """

    description: Optional[str]
    """Optional description for the NetworkPolicy."""
