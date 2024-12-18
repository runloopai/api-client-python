# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

__all__ = ["LspGetSignatureHelpParams"]


class LspGetSignatureHelpParams(TypedDict, total=False):
    character: Required[float]

    line: Required[float]

    uri: Required[str]
