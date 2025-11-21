import io
import os
import tarfile
from typing import Iterable, Optional
from pathlib import Path, PurePosixPath
from dataclasses import dataclass

## This file has helper methods to get a docker context tarball from a given context root.
##
## It includes a small, self-contained implementation of Docker's `.dockerignore`
## semantics. The goal is to be very close to Docker's behavior without depending
## on Docker's own Python libraries.


def build_docker_context_tar(
    context_root: Path,
    *,
    dockerignore: Optional[Path] = None,
) -> bytes:
    """Create a .tar.gz of the Docker build context, respecting .dockerignore for use with object store.

    Generally you shouldn't need to pass in .dockerignore directly; just let the function find it for you.
    - Treats ``context_root`` as the Docker build context root.
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


@dataclass(frozen=True)
class _DockerignorePattern:
    """Single parsed .dockerignore pattern.

    Attributes:
        pattern: The normalized pattern text with escapes processed and leading
            '/' / trailing '/' removed. Always uses POSIX '/' separators.
        negated: True if this is a negation pattern starting with '!'.
        directory_only: True if the original pattern ended with '/' and should
            apply only to directories and their descendants.
        anchored: True if the original pattern started with '/' and is anchored
            to the context root. Non-anchored patterns may match at any depth.
    """

    pattern: str
    negated: bool
    directory_only: bool
    anchored: bool


def _unescape_pattern(text: str) -> str:
    """Unescape backslash-escaped characters in a pattern string."""
    result: list[str] = []
    i = 0
    while i < len(text):
        if text[i] == "\\" and i + 1 < len(text):
            # Backslash escapes the next character
            result.append(text[i + 1])
            i += 2
        else:
            result.append(text[i])
            i += 1
    return "".join(result)


def _find_first_non_space(text: str) -> int:
    """Find the index of the first non-space character, skipping escaped spaces."""
    i = 0
    while i < len(text) and text[i] == " ":
        i += 1

    # Check if we stopped at an escaped space
    if i < len(text) and text[i] == "\\" and i + 1 < len(text) and text[i + 1] == " ":
        return i

    return i  # Either first non-space char or len(text)


def _strip_trailing_whitespace(text: str) -> str:
    """Strip trailing whitespace unless it's escaped."""
    while text and text[-1] in " \t":
        if len(text) >= 2 and text[-2] == "\\":
            # Trailing space is escaped, keep it
            break
        text = text[:-1]
    return text


def _load_dockerignore_patterns(
    dockerignore_path: Optional[Path],
) -> list[_DockerignorePattern]:
    """Parse .dockerignore into a list of structured patterns.

    Parsing rules mirror Docker's behavior as described in the official docs:

    - Empty lines are ignored.
    - Lines starting with unescaped ``#`` (after optional leading spaces) are
      treated as comments and ignored.
    - A leading ``!`` (after optional leading spaces) negates the pattern.
      A leading ``\\!`` is treated as a literal ``!``.
    - A leading ``#`` can be escaped as ``\\#`` to be treated as part of the
      pattern.
    - Leading and trailing spaces are significant if escaped with a backslash.
    """
    if dockerignore_path is None or not dockerignore_path.exists():
        return []

    patterns: list[_DockerignorePattern] = []
    for line in dockerignore_path.read_text(encoding="utf-8").splitlines():
        # Strip trailing newline/carriage return, but preserve escaped trailing spaces
        line = line.rstrip("\n\r")
        if not line:
            continue

        # Find first non-space character (handles escaped spaces)
        start_idx = _find_first_non_space(line)
        if start_idx >= len(line):
            # Line is entirely whitespace
            continue

        # Check for comment: first non-space char is unescaped '#'
        first_char = line[start_idx]
        if first_char == "#" and (start_idx == 0 or line[start_idx - 1] != "\\"):
            continue

        # Check for negation: first non-space char is unescaped '!'
        negated = False
        if first_char == "!" and (start_idx == 0 or line[start_idx - 1] != "\\"):
            negated = True
            start_idx += 1
            if start_idx >= len(line):
                # Bare "!" after optional spaces is ignored
                continue

        # Extract pattern part (everything after negation marker)
        pattern_raw = line[start_idx:]
        pattern_raw = _strip_trailing_whitespace(pattern_raw)
        pattern = _unescape_pattern(pattern_raw)

        if not pattern:
            # Nothing meaningful left after processing
            continue

        # Extract anchored and directory-only flags
        anchored = pattern.startswith("/")
        if anchored:
            pattern = pattern.lstrip("/")

        directory_only = pattern.endswith("/")
        if directory_only:
            pattern = pattern.rstrip("/")

        if not pattern:
            # A line that is effectively "/" or similar after processing
            continue

        patterns.append(
            _DockerignorePattern(
                pattern=PurePosixPath(pattern).as_posix(),
                negated=negated,
                directory_only=directory_only,
                anchored=anchored,
            )
        )

    return patterns


def _segment_match(pattern_segment: str, path_segment: str) -> bool:
    """Match a single path segment against a glob pattern segment.

    Supports:
    - ``*``: any sequence of characters except ``/``.
    - ``?``: any single character except ``/``.
    - ``[]``: character classes, excluding ``/``.
    """
    import re

    escaped = ""
    i = 0
    while i < len(pattern_segment):
        ch = pattern_segment[i]
        if ch == "*":
            escaped += "[^/]*"
        elif ch == "?":
            escaped += "[^/]"
        elif ch == "[":
            # Copy character class as-is until closing ']'.
            j = i + 1
            while j < len(pattern_segment) and pattern_segment[j] != "]":
                j += 1
            if j < len(pattern_segment):
                escaped += pattern_segment[i : j + 1]
                i = j
            else:
                # Unterminated '['; treat it literally.
                escaped += re.escape(ch)
        else:
            escaped += re.escape(ch)
        i += 1

    regex = re.compile(rf"^{escaped}$")
    return regex.match(path_segment) is not None


def _match_parts_recursive(pattern_parts: list[str], path_parts: list[str]) -> bool:
    """Recursive helper implementing ``**`` segment semantics."""

    if not pattern_parts:
        return not path_parts

    if pattern_parts[0] == "**":
        # '**' matches zero or more segments.
        for i in range(len(path_parts) + 1):
            if _match_parts_recursive(pattern_parts[1:], path_parts[i:]):
                return True
        return False

    if not path_parts:
        return False

    if not _segment_match(pattern_parts[0], path_parts[0]):
        return False

    return _match_parts_recursive(pattern_parts[1:], path_parts[1:])


def _path_match(pattern: _DockerignorePattern, relpath: str, is_dir: bool) -> bool:
    """Return True if ``relpath`` matches a parsed .dockerignore pattern."""

    relpath_posix = PurePosixPath(relpath).as_posix()
    path_parts = PurePosixPath(relpath_posix).parts
    pattern_parts = PurePosixPath(pattern.pattern).parts

    # Directory-only patterns never directly match files here; the effect on
    # descendants is enforced by directory pruning in the traversal.
    if pattern.directory_only and not is_dir:
        return False

    # Anchored patterns must match starting at the context root; otherwise we
    # allow them to match at any depth.
    if pattern.anchored:
        return _match_parts_recursive(list(pattern_parts), list(path_parts))

    for start in range(len(path_parts)):
        if _match_parts_recursive(list(pattern_parts), list(path_parts[start:])):
            return True
    return False


def _is_ignored(relpath: str, is_dir: bool, patterns: list[_DockerignorePattern]) -> bool:
    """Apply .dockerignore patterns with 'last match wins' semantics.

    Examples::

        *.log
        !important.log

    excludes all ``.log`` files except ``important.log``. Patterns are applied
    in order, and the last matching pattern determines inclusion.
    """

    included = True  # include by default
    for pat in patterns:
        if _path_match(pat, relpath, is_dir=is_dir):
            included = pat.negated
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

    # Walk the tree with directory pruning. We mirror Docker's behavior where
    # excluded parent directories prevent re-including children, even with
    # negation patterns.
    for root, dirs, files in os.walk(context_root):
        root_path = Path(root)

        # Prune ignored directories in-place so their contents are never visited.
        for name in list(dirs):
            dir_path = root_path / name
            rel_dir = dir_path.relative_to(context_root).as_posix()
            if _is_ignored(rel_dir, is_dir=True, patterns=patterns):
                dirs.remove(name)

        # Yield non-ignored files.
        for name in files:
            file_path = root_path / name
            rel_file = file_path.relative_to(context_root).as_posix()
            if _is_ignored(rel_file, is_dir=False, patterns=patterns):
                continue
            yield file_path
