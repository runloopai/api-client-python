# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List
from typing_extensions import TypeAlias

from .text_edit import TextEdit

__all__ = ["RecordStringTextEditArray"]

RecordStringTextEditArray: TypeAlias = Dict[str, List[TextEdit]]
