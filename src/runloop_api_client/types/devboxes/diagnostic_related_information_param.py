# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypeAlias, TypedDict

from .location_param import LocationParam

__all__ = ["DiagnosticRelatedInformationParam"]


class DiagnosticRelatedInformationParamTyped(TypedDict, total=False):
    location: Required[LocationParam]
    """The location of this related diagnostic information."""

    message: Required[str]
    """The message of this related diagnostic information."""


DiagnosticRelatedInformationParam: TypeAlias = Union[DiagnosticRelatedInformationParamTyped, Dict[str, object]]
