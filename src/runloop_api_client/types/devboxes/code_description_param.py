# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, Union
from typing_extensions import Required, TypeAlias, TypedDict

from .u_ri import URi

__all__ = ["CodeDescriptionParam"]


class CodeDescriptionParamTyped(TypedDict, total=False):
    href: Required[URi]
    """An URI to open with more information about the diagnostic error."""


CodeDescriptionParam: TypeAlias = Union[CodeDescriptionParamTyped, Dict[str, object]]
