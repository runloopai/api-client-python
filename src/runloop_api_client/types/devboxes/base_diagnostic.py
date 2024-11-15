# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional

from ..._models import BaseModel
from .base_range import BaseRange
from .diagnostic_severity import DiagnosticSeverity

__all__ = ["BaseDiagnostic"]


class BaseDiagnostic(BaseModel):
    message: str

    range: BaseRange

    code: Union[float, str, None] = None

    severity: Optional[DiagnosticSeverity] = None
    """The diagnostic's severity."""

    source: Optional[str] = None
