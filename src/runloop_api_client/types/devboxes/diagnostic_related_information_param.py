# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .location_param import LocationParam

__all__ = ["DiagnosticRelatedInformationParam"]


class DiagnosticRelatedInformationParam(TypedDict, total=False):
    location: Required[LocationParam]
    """The location of this related diagnostic information."""

    message: Required[str]
    """The message of this related diagnostic information."""
