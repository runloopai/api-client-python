# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Union, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel
from .base_markup_content import BaseMarkupContent

__all__ = ["BaseParameterInformation", "Documentation"]

Documentation: TypeAlias = Union[str, BaseMarkupContent]


class BaseParameterInformation(BaseModel):
    label: str

    documentation: Optional[Documentation] = None
