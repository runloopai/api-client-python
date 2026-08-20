# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from ..._models import BaseModel

__all__ = ["CustomHeader"]


class CustomHeader(BaseModel):
    """
    An additional header applied to upstream requests alongside the primary credential. The value comes from an account secret or a literal string; exactly one of 'secret' and 'value' must be set.
    """

    name: str
    """The header name (e.g., 'DD-APPLICATION-KEY')."""

    secret: Optional[str] = None
    """Account secret providing the header value.

    Accepts a secret name or 'sec*' id on writes; reads always return the 'sec*' id.
    """

    value: Optional[str] = None
    """Literal header value.

    Stored in plaintext and returned by reads - use 'secret' for credentials or
    other sensitive values.
    """
