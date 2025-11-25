from pathlib import Path

from runloop_api_client.lib._ignore import (
    IgnorePattern,
    is_ignored,
    path_match,
    compile_ignore,
    read_ignorefile,
)
from runloop_api_client.lib.context_loader import _iter_build_context_files


def test_segment_match_basic_globs():
    patterns = compile_ignore(["*.log", "foo?", "[ab].txt"])
    pat_glob, pat_q, pat_class = patterns

    assert path_match(pat_glob, "app.log", is_dir=False)
    assert not path_match(pat_glob, "app.txt", is_dir=False)
    assert path_match(pat_q, "fooa", is_dir=False)
    assert not path_match(pat_q, "fooba", is_dir=False)
    assert path_match(pat_class, "a.txt", is_dir=False)
    assert not path_match(pat_class, "c.txt", is_dir=False)


def test_path_match_anchored_and_unanchored():
    pat = IgnorePattern(pattern="foo/bar.txt", negated=False, directory_only=False, anchored=True)
    assert path_match(pat, "foo/bar.txt", is_dir=False)
    assert not path_match(pat, "a/foo/bar.txt", is_dir=False)

    pat_unanchored = IgnorePattern(pattern="foo/bar.txt", negated=False, directory_only=False, anchored=False)
    assert path_match(pat_unanchored, "a/foo/bar.txt", is_dir=False)
    assert path_match(pat_unanchored, "foo/bar.txt", is_dir=False)


def test_path_match_double_star():
    pat = IgnorePattern(pattern="**/*.log", negated=False, directory_only=False, anchored=False)
    assert path_match(pat, "app.log", is_dir=False)
    assert path_match(pat, "a/b/app.log", is_dir=False)
    assert not path_match(pat, "a/b/app.txt", is_dir=False)


def test_is_ignored_last_match_wins():
    patterns = compile_ignore(["*.log", "!keep.log"])
    assert is_ignored("foo.log", is_dir=False, patterns=patterns)
    assert not is_ignored("keep.log", is_dir=False, patterns=patterns)


def test_read_ignorefile_basic(tmp_path: Path):
    dockerignore = tmp_path / ".dockerignore"
    dockerignore.write_bytes(b"\xef\xbb\xbf# comment line\n*.log  \n!keep.log\nbuild/\n")

    patterns = read_ignorefile(dockerignore)
    assert patterns == ["*.log", "!keep.log", "build"]


def test_iter_build_context_files_respects_dockerignore(tmp_path: Path):
    # Layout:
    #   foo.txt
    #   app.log
    #   build/ignored.txt
    root = tmp_path
    (root / "foo.txt").write_text("ok", encoding="utf-8")
    (root / "app.log").write_text("ignored", encoding="utf-8")
    build_dir = root / "build"
    build_dir.mkdir()
    (build_dir / "ignored.txt").write_text("ignored", encoding="utf-8")

    dockerignore = root / ".dockerignore"
    dockerignore.write_text("*.log\nbuild/\n", encoding="utf-8")

    compiled = compile_ignore(read_ignorefile(dockerignore))
    files = {p.relative_to(root).as_posix() for p in _iter_build_context_files(root, patterns=compiled)}
    assert "foo.txt" in files
    assert "app.log" not in files
    assert "build/ignored.txt" not in files


def test_is_ignored_folder_exclusion_cannot_be_reincluded() -> None:
    """Folder exclusion followed by file inclusion should still exclude.

    Mirrors Docker behavior exercised in moby's TestPatternMatchesFolderExclusions
    style tests: a directory excluded by a pattern like ``docs`` cannot have
    children re-included by a later ``!docs/README.md`` pattern.
    """

    patterns = compile_ignore(["docs", "!docs/README.md"])
    # The file under docs remains ignored overall.
    assert is_ignored("docs/README.md", is_dir=False, patterns=patterns)


def test_compile_ignore_directory_only_and_files() -> None:
    patterns = compile_ignore(["build/", "*.log"])

    build_pat, log_pat = patterns
    assert build_pat.directory_only
    assert not log_pat.directory_only

    # Directory-only pattern does not directly match files at that path.
    assert not path_match(build_pat, "build", is_dir=False)
    assert path_match(build_pat, "build", is_dir=True)

    # But files under the directory are ignored via ancestor directory match.
    assert is_ignored("build/output.bin", is_dir=False, patterns=patterns)
    # Log files are ignored everywhere.
    assert is_ignored("app.log", is_dir=False, patterns=patterns)
    assert is_ignored("subdir/app.log", is_dir=False, patterns=patterns)


def test_double_star_matching_variants() -> None:
    patterns = compile_ignore(["**", "dir/**", "**/file", "**/*.txt"])

    any_pat, dir_pat, file_pat, txt_pat = patterns

    # '**' matches everything.
    assert path_match(any_pat, "file", is_dir=False)
    assert path_match(any_pat, "dir/file", is_dir=False)

    # 'dir/**' matches anything under dir.
    assert path_match(dir_pat, "dir/file", is_dir=False)
    assert path_match(dir_pat, "dir/sub/file", is_dir=False)
    assert not path_match(dir_pat, "other/file", is_dir=False)

    # '**/file' matches at any depth.
    assert path_match(file_pat, "file", is_dir=False)
    assert path_match(file_pat, "dir/file", is_dir=False)
    assert path_match(file_pat, "a/b/file", is_dir=False)

    # '**/*.txt' matches text files at any depth.
    assert path_match(txt_pat, "file.txt", is_dir=False)
    assert path_match(txt_pat, "dir/file.txt", is_dir=False)
    assert not path_match(txt_pat, "dir/file.log", is_dir=False)


def test_iter_build_context_files_respects_directory_pruning(tmp_path: Path) -> None:
    """Directories excluded by patterns are not traversed, even with negation."""

    root = tmp_path
    docs = root / "docs"
    docs.mkdir()
    (docs / "README.md").write_text("keep?", encoding="utf-8")

    ignorefile = root / ".dockerignore"
    # Attempt to re-include a file under an ignored directory.
    ignorefile.write_text("docs/\n!docs/README.md\n", encoding="utf-8")

    compiled = compile_ignore(read_ignorefile(ignorefile))
    files = {p.relative_to(root).as_posix() for p in _iter_build_context_files(root, patterns=compiled)}

    # README.md should not appear because the parent directory is pruned.
    assert "docs/README.md" not in files
