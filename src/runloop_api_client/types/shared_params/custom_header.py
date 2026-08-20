# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Optional
from typing_extensions import Required, TypedDict

__all__ = ["CustomHeader"]


class CustomHeader(TypedDict, total=False):
    """
    An additional header applied to upstream requests alongside the primary credential. The value comes from an account secret or a literal string; exactly one of 'secret' and 'value' must be set.
    """

    name: Required[str]
    """The header name (e.g., 'DD-APPLICATION-KEY')."""

    secret: Optional[str]
    """Account secret providing the header value.

    Accepts a secret name or 'sec*' id on writes; reads always return the 'sec*' id.
    """

    value: Optional[str]
    """Literal header value.

    Stored in plaintext and returned by reads - use 'secret' for credentials or
    other sensitive values.
    """
