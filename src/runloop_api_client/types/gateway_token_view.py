# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from .._models import BaseModel
from .shared.auth_mechanism import AuthMechanism

__all__ = ["GatewayTokenView"]


class GatewayTokenView(BaseModel):
    token: str
    """The token to send to the gateway as a Bearer token in the Authorization header.

    Only accepted for requests originating from the bound Devbox.
    """

    auth_mechanism: AuthMechanism
    """How the gateway applies the credential to proxied requests."""

    devbox_id: str
    """The Devbox the token is bound to."""

    endpoint: str
    """The target API endpoint the gateway proxies to."""

    gateway_config_id: str
    """The ID of the gateway config the token proxies through."""

    url: str
    """The gateway URL to send requests to.

    Matches the value of the &#123;prefix&#125;\\__URL environment variable inside the
    Devbox.
    """
