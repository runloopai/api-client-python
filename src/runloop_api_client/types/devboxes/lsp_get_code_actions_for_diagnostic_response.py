# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .base_code_action import BaseCodeAction

__all__ = ["LspGetCodeActionsForDiagnosticResponse"]

LspGetCodeActionsForDiagnosticResponse: TypeAlias = List[BaseCodeAction]
