# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel

__all__ = ["DevboxCreateSSHKeyResponse"]


class DevboxCreateSSHKeyResponse(BaseModel):
    id: str
    """The ID of the Devbox."""

    ssh_private_key: str
    """The ssh private key, in PEM format."""

    ssh_user: str
    """The Linux user to use for SSH connections to this Devbox."""

    url: str
    """The host url of the Devbox that can be used for SSH."""
