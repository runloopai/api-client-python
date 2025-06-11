# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["SecretUpdateParams"]


class SecretUpdateParams(TypedDict, total=False):
    value: Required[str]
    """The new value for the Secret.

    This will replace the existing value and be encrypted at rest. Example:
    'my-updated-secure-password'
    """
