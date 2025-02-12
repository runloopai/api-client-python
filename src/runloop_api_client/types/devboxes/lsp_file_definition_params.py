# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .file_definition_request_body_param import FileDefinitionRequestBodyParam

__all__ = ["LspFileDefinitionParams"]


class LspFileDefinitionParams(TypedDict, total=False):
    file_definition_request_body: Required[
        Annotated[FileDefinitionRequestBodyParam, PropertyInfo(alias="fileDefinitionRequestBody")]
    ]
