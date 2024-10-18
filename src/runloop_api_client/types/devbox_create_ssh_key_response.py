# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.


from .._models import BaseModel

__all__ = ["DevboxCreateSSHKeyResponse"]


class DevboxCreateSSHKeyResponse(BaseModel):
    id: str
    """The id of the Devbox."""

    ssh_private_key: str
    """The ssh private key, in PEM format."""

    url: str
    """The url of the Devbox."""
