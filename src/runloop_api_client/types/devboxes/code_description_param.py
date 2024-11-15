# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, TypedDict

from .u_ri import URi

__all__ = ["CodeDescriptionParam"]


class CodeDescriptionParam(TypedDict, total=False):
    href: Required[URi]
    """An URI to open with more information about the diagnostic error."""
