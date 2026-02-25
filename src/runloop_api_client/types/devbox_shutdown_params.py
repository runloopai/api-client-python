# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

__all__ = ["DevboxShutdownParams"]


class DevboxShutdownParams(TypedDict, total=False):
    force: str
    """If true, force shutdown even if snapshots are in progress. Defaults to false."""
