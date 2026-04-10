# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

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


def _inject_type_submodules(app, docname, source):
    """Auto-generate automodule directives for all type submodules.

    Replaces the ``.. auto-all-types::`` placeholder in types.rst with
    automodule directives for every submodule in runloop_api_client.types.
    This ensures all types (including file-local helper types like Lifecycle
    and BuildContext) get documented at their actual module path, making
    cross-references resolve without any path rewriting.
    """
    if docname != "api/types":
        return
    import pkgutil

    import runloop_api_client.types as types_pkg

    directives = []
    for _, modname, ispkg in sorted(
        pkgutil.walk_packages(types_pkg.__path__, types_pkg.__name__ + "."),
        key=lambda x: x[1],
    ):
        if ispkg:
            continue
        directives.append(
            f".. automodule:: {modname}\n"
            f"   :members:\n"
            f"   :undoc-members:\n"
        )
    source[0] = source[0].replace(".. auto-all-types::", "\n".join(directives))


def setup(app):
    app.connect("source-read", _inject_type_submodules)


# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
}
