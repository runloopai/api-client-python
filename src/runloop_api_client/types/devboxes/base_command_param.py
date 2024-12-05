# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Iterable
from typing_extensions import Required, TypedDict

__all__ = ["BaseCommandParam"]


class BaseCommandParam(TypedDict, total=False):
    command: Required[str]

    title: Required[str]

    arguments: Iterable[object]
