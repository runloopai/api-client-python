# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing_extensions import Literal, Required, TypedDict

__all__ = ["ObjectMountParameters"]


class ObjectMountParameters(TypedDict, total=False):
    object_id: Required[str]
    """The ID of the object to write."""

    object_path: Required[str]
    """The path to write the object on the Devbox.

    Use absolute path of object (ie /home/user/object.txt, or directory if archive
    /home/user/archive_dir)
    """

    type: Required[Literal["object_mount"]]
