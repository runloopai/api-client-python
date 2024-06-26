# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Required, Annotated, TypedDict

from .._utils import PropertyInfo

__all__ = ["FunctionInvokeAsyncParams", "RunloopMeta"]


class FunctionInvokeAsyncParams(TypedDict, total=False):
    project_name: Required[str]

    request: Required[object]
    """Json of the request"""

    runloop_meta: Annotated[RunloopMeta, PropertyInfo(alias="runloopMeta")]


class RunloopMeta(TypedDict, total=False):
    session_id: str
    """Json of the request"""
