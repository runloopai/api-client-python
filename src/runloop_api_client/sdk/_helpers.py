"""SDK helper types and utility functions."""

from __future__ import annotations

from typing import Any, Dict, Type, Mapping, TypeVar
from pathlib import Path

from ..types.object_create_params import ContentType

_CONTENT_TYPE_MAP: Dict[str, ContentType] = {
    ".txt": "text",
    ".html": "text",
    ".css": "text",
    ".js": "text",
    ".json": "text",
    ".xml": "text",
    ".yaml": "text",
    ".yml": "text",
    ".md": "text",
    ".csv": "text",
    ".gz": "gzip",
    ".tar": "tar",
    ".tgz": "tgz",
    ".tar.gz": "tgz",
}


def detect_content_type(name: str) -> ContentType:
    lower = name.lower()
    if lower.endswith(".tar.gz") or lower.endswith(".tgz"):
        return "tgz"
    ext = Path(lower).suffix
    return _CONTENT_TYPE_MAP.get(ext, "unspecified")


T = TypeVar("T")


def filter_params(params: Mapping[str, Any], type_filter: Type[T]) -> T:
    """Filter params dict to only include keys defined in the given TypedDict type.

    Args:
        params: Dictionary or TypedDict of parameters to filter
        type_filter: TypedDict class to filter against

    Returns:
        Filtered dictionary matching the TypedDict structure
    """
    return {k: v for k, v in params.items() if k in type_filter.__annotations__}  # type: ignore[return-value]
