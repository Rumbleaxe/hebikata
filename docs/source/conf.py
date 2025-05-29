# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
sys.path.insert(0, os.path.abspath('../app'))  # Adjust path to your source code

project = 'hebikata'
copyright = '2025, Ioannis Lazaridis'
author = 'Ioannis Lazaridis'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ['sphinx.ext.autodoc',        # Core autodoc extension
    'sphinx.ext.napoleon',       # Support for Google/NumPy style docstrings
    'sphinx.ext.viewcode',       # Add links to source code
    'sphinx.ext.autosectionlabel' # Optional: reference sections by name
    ]

templates_path = ['_templates']
exclude_patterns = []


# Optional: autodoc settings
autodoc_member_order = 'bysource'  # Document members in source order
autodoc_typehints = 'description'  # Show type hints in description

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output


html_theme = 'sphinx_rtd_theme'  # Popular, clean theme; install via pip if needed
html_static_path = ['_static']
