# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List

from ..._models import BaseModel
from .base_diagnostic import BaseDiagnostic

__all__ = ["DiagnosticsResponse"]


class DiagnosticsResponse(BaseModel):
    diagnostics: List[BaseDiagnostic]

    uri: str
