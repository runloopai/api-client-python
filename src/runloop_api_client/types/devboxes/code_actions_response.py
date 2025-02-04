# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union
from typing_extensions import TypeAlias

from .base_command import BaseCommand
from .base_code_action import BaseCodeAction

__all__ = ["CodeActionsResponse", "CodeActionsResponseItem"]

CodeActionsResponseItem: TypeAlias = Union[BaseCodeAction, BaseCommand]

CodeActionsResponse: TypeAlias = List[CodeActionsResponseItem]
