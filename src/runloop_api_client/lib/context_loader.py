from __future__ import annotations

import io
import tarfile
from typing import Callable, Optional, Sequence
from pathlib import Path

from ._ignore import IgnoreMatcher, DockerIgnoreMatcher

TarFilter = Callable[[tarfile.TarInfo], Optional[tarfile.TarInfo]]


def build_docker_context_tar(
    context_root: Path,
    *,
    ignore: IgnoreMatcher | Sequence[str] | None = None,
) -> bytes:
    """Create a .tar.gz of the build context, honoring Docker-style ignore patterns.

    - Treats ``context_root`` as the build context root.
    - Always loads ``.dockerignore`` under ``context_root`` if present.
    - An optional :class:`IgnoreMatcher` may be provided to customise how ignore
      patterns are resolved; when omitted, :class:`DockerIgnoreMatcher` is used.
    """

    context_root = context_root.resolve()

    if ignore is None:
        matcher: IgnoreMatcher = DockerIgnoreMatcher()
    elif isinstance(ignore, IgnoreMatcher):
        matcher = ignore
    else:
        # Treat sequences of pattern strings as additional inline patterns
        # appended after ``.dockerignore`` (if present), mirroring
        # :class:`DockerIgnoreMatcher` semantics.
        matcher = DockerIgnoreMatcher(patterns=list(ignore))

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

    def _wrapped_filter(ti: tarfile.TarInfo) -> Optional[tarfile.TarInfo]:
        # Normalise member names so callers see paths relative to ``root``
        # without a leading ``./``, preserving existing TarFilter semantics and
        # archive layout. This applies to both files and directories.
        if ti.name.startswith("./"):
            ti.name = ti.name[2:]

        if tar_filter is not None:
            return tar_filter(ti)
        return ti

    with tarfile.open(mode="w:gz", fileobj=buf) as tf:
        # Add the root directory recursively in one call, delegating member
        # handling to the wrapped filter above.
        tf.add(root, arcname=".", filter=_wrapped_filter)

    return buf.getvalue()
