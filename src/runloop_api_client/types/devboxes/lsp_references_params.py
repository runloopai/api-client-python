# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .references_request_body_param import ReferencesRequestBodyParam

__all__ = ["LspReferencesParams"]


class LspReferencesParams(TypedDict, total=False):
    references_request_body: Required[
        Annotated[ReferencesRequestBodyParam, PropertyInfo(alias="referencesRequestBody")]
    ]
