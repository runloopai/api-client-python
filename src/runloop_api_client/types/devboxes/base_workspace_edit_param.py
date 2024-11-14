# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import TypedDict

from .record_string_text_edit_array_param import RecordStringTextEditArrayParam

__all__ = ["BaseWorkspaceEditParam"]


class BaseWorkspaceEditParam(TypedDict, total=False):
    changes: RecordStringTextEditArrayParam
    """Construct a type with a set of properties K of type T"""
