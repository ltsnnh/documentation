# Configuration file for the Sphinx documentation builder.

# -- Project information -----------------------------------------------------

project = 'Ltsnnh Documentation'
copyright = '2025, Ltsnnh'
author = 'Ltsnnh'

release = '1.0'
version = ''

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'myst_parser',
]

myst_enable_extensions = [
    'linkify',
    'substitution',
    'deflist',
]

intersphinx_mapping = {
    'python': ('https://docs.python.org/3/', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}
intersphinx_disabled_domains = ['std']

templates_path = ['_templates']

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

# -- Options for Epub output -------------------------------------------------

epub_show_urls = 'footnote'
