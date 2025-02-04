# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import TypedDict

__all__ = ["BrowserCreateParams"]


class BrowserCreateParams(TypedDict, total=False):
    name: Optional[str]
    """The name to use for the created Devbox with a Browser."""
