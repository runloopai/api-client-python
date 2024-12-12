# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Union
from typing_extensions import Required, TypedDict

from .base_range_param import BaseRangeParam
from .diagnostic_severity import DiagnosticSeverity

__all__ = ["BaseDiagnosticParam"]


class BaseDiagnosticParam(TypedDict, total=False):
    message: Required[str]

    range: Required[BaseRangeParam]

    code: Union[float, str]

    severity: DiagnosticSeverity
    """The diagnostic's severity."""

    source: str
