# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

import os
import sys
import pkgutil
from typing import Any, get_type_hints

# Add the src directory to the path so we can import the package
sys.path.insert(0, os.path.abspath("../src"))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Runloop Python SDK"
copyright = "2025, Runloop"
author = "Runloop"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
    "sphinx.ext.viewcode",
    "sphinx_toolbox.more_autodoc.autotypeddict",
    "sphinx_autodoc_typehints",
    "sphinx_tabs.tabs",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_static_path = ["_static"]
html_favicon = "_static/favicon.png"

# Furo theme options
html_theme_options = {
    "navigation_with_keys": True,
}

# -- Extension configuration -------------------------------------------------

# Autodoc settings
autodoc_default_options = {
    "members": None,
    "member-order": "bysource",
}

autodoc_typehints = "description"
autodoc_typehints_description_target = "documented"


# -- Patches -----------------------------------------------------------------


def _patch_autotypeddict_inherited_docstrings() -> None:
    """Patch autotypeddict to include field docstrings from parent TypedDicts.

    sphinx_toolbox's sort_members only scans self.object.__module__ for field
    docstrings (autotypeddict.py:381-384). SDK TypedDicts like SDKDevboxCreateParams
    inherit fields from types in other modules (e.g. DevboxCreateParams), so those
    descriptions are lost. This patch collects docstrings from the full
    __orig_bases__ chain.

    Upstream bug: https://github.com/sphinx-doc/sphinx/issues/9290
    """
    from sphinx.errors import PycodeError
    from sphinx.pycode import ModuleAnalyzer
    from sphinx_toolbox.more_autodoc.autotypeddict import TypedDictDocumenter

    def _collect_field_docstrings(cls: type) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        visited: set[type] = set()

        def _walk(klass: type) -> None:
            if klass in visited or not hasattr(klass, "__annotations__"):
                return
            visited.add(klass)
            try:
                for (_, fname), doc in ModuleAnalyzer.for_module(klass.__module__).find_attr_docs().items():
                    if fname not in result:
                        result[fname] = doc
            except PycodeError:
                pass
            for base in getattr(klass, "__orig_bases__", []):
                if isinstance(base, type):
                    _walk(base)

        _walk(cls)
        return result

    def _patched_sort_members(
        self: TypedDictDocumenter,
        documenters: list[tuple[Any, bool]],
        order: str,
    ) -> list[tuple[Any, bool]]:
        documenters = super(TypedDictDocumenter, self).sort_members(documenters, order)
        docstrings = _collect_field_docstrings(self.object)

        required_keys: list[str] = []
        optional_keys: list[str] = []
        types = get_type_hints(self.object)

        for d in documenters:
            name = d[0].name.split(".")[-1]
            if name in self.object.__required_keys__:
                required_keys.append(name)
            elif name in self.object.__optional_keys__:
                optional_keys.append(name)

        sourcename = self.get_sourcename()
        if required_keys:
            self.add_line("", sourcename)
            self.add_line(":Required Keys:", sourcename)
            self.document_keys(required_keys, types, docstrings)  # pyright: ignore[reportUnknownMemberType]
            self.add_line("", sourcename)
        if optional_keys:
            self.add_line("", sourcename)
            self.add_line(":Optional Keys:", sourcename)
            self.document_keys(optional_keys, types, docstrings)  # pyright: ignore[reportUnknownMemberType]
            self.add_line("", sourcename)

        return []

    TypedDictDocumenter.sort_members = _patched_sort_members  # type: ignore[assignment]


_patch_autotypeddict_inherited_docstrings()


# -- Dynamic type documentation ----------------------------------------------


def _inject_type_submodules(_app: Any, docname: str, source: list[str]) -> None:
    """Auto-generate automodule directives for all type submodules.

    Replaces the ``.. auto-all-types::`` placeholder in types.rst with
    automodule directives for every submodule in runloop_api_client.types.
    This ensures all types (including file-local helper types like Lifecycle
    and BuildContext) get documented at their actual module path, making
    cross-references resolve without any path rewriting.
    """
    if docname != "api/types":
        return
    import runloop_api_client.types as types_pkg

    directives: list[str] = []
    for _, modname, ispkg in sorted(
        pkgutil.walk_packages(types_pkg.__path__, types_pkg.__name__ + "."),
        key=lambda x: x[1],
    ):
        if ispkg:
            continue
        directives.append(f".. automodule:: {modname}\n   :members:\n   :undoc-members:\n")
    source[0] = source[0].replace(".. auto-all-types::", "\n".join(directives))


def setup(app: Any) -> None:
    app.connect("source-read", _inject_type_submodules)


# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
