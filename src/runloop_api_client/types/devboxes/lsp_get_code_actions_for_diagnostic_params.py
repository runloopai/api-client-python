# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .base_diagnostic_param import BaseDiagnosticParam

__all__ = ["LspGetCodeActionsForDiagnosticParams"]


class LspGetCodeActionsForDiagnosticParams(TypedDict, total=False):
    diagnostic: Required[BaseDiagnosticParam]

    uri: Required[str]
