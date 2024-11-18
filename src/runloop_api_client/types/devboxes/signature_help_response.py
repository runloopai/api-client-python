# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from .base_signature import BaseSignature

__all__ = ["SignatureHelpResponse"]


class SignatureHelpResponse(BaseModel):
    signatures: List[BaseSignature]

    active_parameter: Optional[float] = FieldInfo(alias="activeParameter", default=None)

    active_signature: Optional[float] = FieldInfo(alias="activeSignature", default=None)
