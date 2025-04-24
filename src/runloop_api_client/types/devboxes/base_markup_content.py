# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from ..._models import BaseModel

__all__ = ["BaseMarkupContent"]


class BaseMarkupContent(BaseModel):
    kind: str

    value: str
