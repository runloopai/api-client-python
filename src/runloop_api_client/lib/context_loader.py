from __future__ import annotations

import io
import tarfile
from typing import Callable, Iterable, Optional, Sequence
from pathlib import Path

from ._ignore import IgnoreMatcher, IgnorePattern, DockerIgnoreMatcher, iter_included_files

TarFilter = Callable[[tarfile.TarInfo], Optional[tarfile.TarInfo]]


def build_docker_context_tar(
    context_root: Path,
    *,
    ignore: Optional[IgnoreMatcher] = None,
) -> bytes:
    """Create a .tar.gz of the build context, honoring Docker-style ignore patterns.

    - Treats ``context_root`` as the build context root.
    - Always loads ``.dockerignore`` under ``context_root`` if present.
    - An optional :class:`IgnoreMatcher` may be provided to customise how ignore
      patterns are resolved; when omitted, :class:`DockerIgnoreMatcher` is used.
    """

    context_root = context_root.resolve()

    matcher: IgnoreMatcher = ignore or DockerIgnoreMatcher()

    buf = io.BytesIO()

    with tarfile.open(mode="w:gz", fileobj=buf) as tf:
        for path in matcher.iter_paths(context_root):
            rel = path.relative_to(context_root)
            tf.add(path, arcname=rel.as_posix())

    return buf.getvalue()


def build_directory_tar(
    root: Path,
    *,
    tar_filter: TarFilter | None = None,
) -> bytes:
    """Create a .tar.gz archive containing all files under ``root``.

    No ignore semantics are applied by default; callers may pass a tar filter
    compatible with :meth:`tarfile.TarFile.add` to modify or exclude members.
    """

    root = root.resolve()
    buf = io.BytesIO()
    with tarfile.open(mode="w:gz", fileobj=buf) as tf:
        for file_path in root.rglob("*"):
            if not file_path.is_file():
                continue
            rel = file_path.relative_to(root)
            tf.add(file_path, arcname=rel.as_posix(), filter=tar_filter)
    return buf.getvalue()


def _iter_build_context_files(
    context_root: Path,
    *,
    patterns: Sequence[IgnorePattern],
) -> Iterable[Path]:
    """Yield files to include in the build context, honoring ignore patterns."""

    return iter_included_files(context_root, patterns=patterns)
