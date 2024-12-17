# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import TypeAlias

from ..._models import BaseModel
from .base_markup_content import BaseMarkupContent
from .base_parameter_information import BaseParameterInformation

__all__ = ["BaseSignature", "Documentation"]

Documentation: TypeAlias = Union[str, BaseMarkupContent]


class BaseSignature(BaseModel):
    label: str

    documentation: Optional[Documentation] = None

    parameters: Optional[List[BaseParameterInformation]] = None
