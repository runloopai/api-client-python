# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from ..._utils import PropertyInfo
from .signature_help_request_body_param import SignatureHelpRequestBodyParam

__all__ = ["LspGetSignatureHelpParams"]


class LspGetSignatureHelpParams(TypedDict, total=False):
    signature_help_request_body: Required[
        Annotated[SignatureHelpRequestBodyParam, PropertyInfo(alias="signatureHelpRequestBody")]
    ]
