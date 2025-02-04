# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import TypeAlias

from .text_edit import TextEdit

__all__ = ["FormattingResponse"]

FormattingResponse: TypeAlias = List[TextEdit]
