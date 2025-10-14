# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["ExecutionRetrieveParams"]


class ExecutionRetrieveParams(TypedDict, total=False):
    devbox_id: Required[str]

    last_n: str
    """Last n lines of standard error / standard out to return (default: 100)"""
