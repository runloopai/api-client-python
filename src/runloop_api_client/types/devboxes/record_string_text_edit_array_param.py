# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Iterable
from typing_extensions import TypeAlias

from .text_edit_param import TextEditParam

__all__ = ["RecordStringTextEditArrayParam"]

RecordStringTextEditArrayParam: TypeAlias = Dict[str, Iterable[TextEditParam]]
