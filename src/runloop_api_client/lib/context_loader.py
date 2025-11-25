from __future__ import annotations

import io
import tarfile
from typing import Iterable, Optional, Sequence
from pathlib import Path

from ._ignore import IgnorePattern, compile_ignore, read_ignorefile, iter_included_files


def build_docker_context_tar(
    context_root: Path,
    *,
    ignore: Optional[Sequence[str] | Path | str] = None,
) -> bytes:
    """Create a .tar.gz of the build context, honoring ignore patterns.

    - Treats ``context_root`` as the build context root.
    - Always loads ``.dockerignore`` under ``context_root`` if present.
    - An optional ``ignore`` argument may be provided:

      * If a :class:`pathlib.Path` or string is given, it is treated as an
        additional ignorefile path whose patterns are appended after
        ``.dockerignore``.
      * If a sequence of strings is given, they are treated as inline patterns
        appended after any file-derived patterns.

    Patterns use Docker-style semantics with ``!`` negation and ``**`` support.
    """

    context_root = context_root.resolve()

    all_patterns: list[str] = []

    # 1) Always consider .dockerignore under the context root, if present.
    default_ignorefile = context_root / ".dockerignore"
    all_patterns.extend(read_ignorefile(default_ignorefile))

    # 2) Optional additional ignore source
    if ignore is not None:
        if isinstance(ignore, (str, Path)):
            ignore_path = Path(ignore)
            if not ignore_path.exists():
                raise FileNotFoundError(f"Ignore file does not exist: {ignore_path}")
            all_patterns.extend(read_ignorefile(ignore_path))
        else:
            # Treat as a sequence of raw patterns
            all_patterns.extend(list(ignore))

    compiled: list[IgnorePattern] = compile_ignore(all_patterns)

    buf = io.BytesIO()

    with tarfile.open(mode="w:gz", fileobj=buf) as tf:
        for path in _iter_build_context_files(context_root, patterns=compiled):
            rel = path.relative_to(context_root)
            tf.add(path, arcname=rel.as_posix())

    return buf.getvalue()


def _iter_build_context_files(
    context_root: Path,
    *,
    patterns: Sequence[IgnorePattern],
) -> Iterable[Path]:
    """Yield files to include in the build context, honoring ignore patterns."""

    return iter_included_files(context_root, patterns=patterns)
