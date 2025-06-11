# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SecretCreateParams"]


class SecretCreateParams(TypedDict, total=False):
    name: Required[str]
    """The globally unique name for the Secret.

    Must be a valid environment variable name (alphanumeric and underscores only).
    Example: 'DATABASE_PASSWORD'
    """

    value: Required[str]
    """The value to store for this Secret.

    This will be encrypted at rest and made available as an environment variable in
    Devboxes. Example: 'my-secure-password'
    """
