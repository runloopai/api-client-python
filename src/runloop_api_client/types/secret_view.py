# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["SecretView"]


class SecretView(BaseModel):
    """
    A Secret represents a key-value pair that can be securely stored and used in Devboxes as environment variables.
    """

    id: str
    """The unique identifier of the Secret."""

    create_time_ms: int
    """Creation time of the Secret (Unix timestamp in milliseconds)."""

    name: str
    """The globally unique name of the Secret.

    Used as the environment variable name in Devboxes.
    """

    update_time_ms: int
    """Last update time of the Secret (Unix timestamp in milliseconds)."""
