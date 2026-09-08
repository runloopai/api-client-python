# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Optional
from typing_extensions import TypedDict

__all__ = ["AxonUpdateParams"]


class AxonUpdateParams(TypedDict, total=False):
    metadata: Optional[Dict[str, str]]
    """User defined metadata to replace the axon metadata.

    Omit or set to null to leave unchanged, or set to an empty map to clear it.
    """
