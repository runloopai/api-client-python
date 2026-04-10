# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

from __future__ import annotations

import os
import sys
import pkgutil
from typing import get_type_hints
from typing_extensions import override

from sphinx.errors import PycodeError
from sphinx.pycode import ModuleAnalyzer
from sphinx.application import Sphinx
from sphinx.ext.autodoc import Documenter
from sphinx_toolbox.more_autodoc.autotypeddict import TypedDictDocumenter

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


# -- Autodocumenter extensions -----------------------------------------------


def _collect_field_docstrings(cls: type) -> dict[str, list[str]]:
    """Collect field docstrings from cls and all TypedDict ancestors via __orig_bases__."""
    result: dict[str, list[str]] = {}
    # Parents first — child docstrings overwrite via later assignment
    for base in getattr(cls, "__orig_bases__", ()):
        origin = getattr(base, "__origin__", base)
        if isinstance(origin, type) and origin is not cls:
            result.update(_collect_field_docstrings(origin))
    try:
        attr_docs = ModuleAnalyzer.for_module(cls.__module__).find_attr_docs()
        for (_, attr_name), doc_lines in attr_docs.items():
            result[attr_name] = doc_lines
    except PycodeError:
        pass
    return result


class _InheritedDocsTypedDictDocumenter(TypedDictDocumenter):
    """TypedDictDocumenter that collects field docstrings from parent TypedDicts.

    Upstream only scans self.object.__module__ for field docstrings, so
    inherited descriptions are lost. This subclass traverses __orig_bases__.
    Upstream bug: https://github.com/sphinx-doc/sphinx/issues/9290
    Patching sphinx_toolbox 4.1.2.
    """

    @override
    def sort_members(
        self,
        documenters: list[tuple[Documenter, bool]],
        order: str,
    ) -> list[tuple[Documenter, bool]]:
        # Skip TypedDictDocumenter.sort_members (returns [] after adding
        # lines with wrong docstrings). Call ClassDocumenter.sort_members
        # to get the properly sorted documenters list.
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


# -- Dynamic type documentation ----------------------------------------------


def _inject_type_submodules(_app: Sphinx, docname: str, source: list[str]) -> None:
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


def setup(app: Sphinx) -> None:
    app.add_autodocumenter(_InheritedDocsTypedDictDocumenter, override=True)
    app.connect("source-read", _inject_type_submodules)  # pyright: ignore[reportUnknownMemberType]


# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
