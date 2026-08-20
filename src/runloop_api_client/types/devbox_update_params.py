# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["DevboxUpdateParams"]


class DevboxUpdateParams(TypedDict, total=False):
    metadata: Optional[Dict[str, str]]
    """User defined metadata to replace the Devbox metadata.

    Omit to leave unchanged or set to an empty map to clear it.
    """

    name: Optional[str]
    """A user specified name to give the Devbox.

    Omit to leave unchanged or set to an empty string to clear it.
    """
