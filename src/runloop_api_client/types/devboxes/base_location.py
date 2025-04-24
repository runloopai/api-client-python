# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel
from .base_range import BaseRange

__all__ = ["BaseLocation"]


class BaseLocation(BaseModel):
    range: BaseRange

    uri: str
