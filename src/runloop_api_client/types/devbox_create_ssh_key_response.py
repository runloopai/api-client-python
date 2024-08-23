# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Optional

from .._models import BaseModel

__all__ = ["DevboxCreateSSHKeyResponse"]


class DevboxCreateSSHKeyResponse(BaseModel):
    id: Optional[str] = None
    """The id of the Devbox."""

    ssh_private_key: Optional[str] = None
    """The ssh private key, in PEM format."""

    url: Optional[str] = None
    """The url of the Devbox."""
