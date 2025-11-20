import io
import tarfile
from typing import Iterable, Optional
from pathlib import Path, PurePosixPath

## This file has helper methods to get a docker context tarball from a given context root.


def _load_dockerignore_patterns(
    dockerignore_path: Optional[Path],
) -> list[tuple[bool, str]]:
    """Parse .dockerignore contents into a list of (is_negated, pattern).

    Notes:
    - Empty lines and comments are ignored.
    - Lines starting with '!' are negation patterns.
    """
    if dockerignore_path is None or not dockerignore_path.exists():
        return []

    patterns: list[tuple[bool, str]] = []
    for raw_line in dockerignore_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue

        is_negated = line.startswith("!")
        if is_negated:
            line = line[1:].strip()
            if not line:
                continue

        patterns.append((is_negated, line))

    return patterns


def _match_dockerignore_pattern(relpath: str, pattern: str) -> bool:
    """Return True if relpath matches a single .dockerignore pattern.

    This is a small, pragmatic approximation of Docker's matching rules:
    - Patterns ending with '/' are treated as directory-only.
    - Patterns without '/' match basenames anywhere in the tree.
    - Other patterns match against the full relative path.
    """
    from fnmatch import fnmatch

    relpath_posix = PurePosixPath(relpath).as_posix()

    directory_only = pattern.endswith("/")
    if directory_only:
        pattern = pattern.rstrip("/")

    if "/" not in pattern:
        # Match against basename anywhere in the tree
        name = PurePosixPath(relpath_posix).name
        matched = fnmatch(name, pattern)
    else:
        # Match against the full relative path
        matched = fnmatch(relpath_posix, pattern)

    if directory_only:
        # Directory-only pattern matches the directory itself or anything under it
        return matched and (relpath_posix == pattern or relpath_posix.startswith(f"{pattern}/"))

    return matched


def _is_ignored(relpath: str, patterns: list[tuple[bool, str]]) -> bool:
    """Apply .dockerignore patterns with 'last match wins' semantics."""

    included = True  # include by default
    for is_negated, pat in patterns:
        if _match_dockerignore_pattern(relpath, pat):
            # Negated patterns flip back to included, normal patterns exclude.
            included = is_negated
    return not included


def _iter_build_context_files(
    context_root: Path,
    *,
    dockerignore_path: Optional[Path] = None,
) -> Iterable[Path]:
    """Yield files to include in the build context, honoring .dockerignore.

    This hand-rolls .dockerignore parsing and matching instead of relying on the
    Docker SDK to avoid pulling in the docker Python dependency.
    It approximates Docker's behavior.
    """
    if not context_root.is_dir():
        raise ValueError(f"context_root must be a directory, got: {context_root}")

    if dockerignore_path is None:
        candidate = context_root / ".dockerignore"
        dockerignore_path = candidate if candidate.exists() else None

    patterns = _load_dockerignore_patterns(dockerignore_path)

    # Walk the tree and apply ignore rules. We mirror the "include by default"
    # behavior and apply patterns in order, with last match winning.
    for path in context_root.rglob("*"):
        if path.is_dir():
            # Docker's context is file-based; directories are implicit.
            continue

        rel = path.relative_to(context_root).as_posix()

        if _is_ignored(rel, patterns):
            continue

        yield path


def build_docker_context_tar(
    context_root: Path,
    *,
    dockerignore: Optional[Path] = None,
) -> bytes:
    """Create a .tar.gz of the Docker build context, respecting .dockerignore.

    - Treats ``context_root`` as the Docker build context root.
    - Determines the .dockerignore path as:
        * explicit ``dockerignore`` argument if provided
        * otherwise ``context_root / \".dockerignore\"`` if it exists
    """
    context_root = context_root.resolve()

    # Resolve dockerignore path according to the requested behavior
    if dockerignore is not None:
        dockerignore_path = dockerignore.resolve()
    else:
        dockerignore_path = context_root / ".dockerignore"

    buf = io.BytesIO()

    with tarfile.open(mode="w:gz", fileobj=buf) as tf:
        for path in _iter_build_context_files(
            context_root,
            dockerignore_path=dockerignore_path if dockerignore_path.exists() else None,
        ):
            rel = path.relative_to(context_root)
            tf.add(path, arcname=rel.as_posix())

    return buf.getvalue()
