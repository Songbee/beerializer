#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import pkg_resources

#: If extensions (or modules to document with autodoc) are in another directory,
#: add these directories to sys.path here. If the directory is relative to the
#: documentation root, use os.path.abspath to make it absolute.
sys.path.insert(0, os.path.abspath('..'))

# -- General configuration --

needs_sphinx = '1.2'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.viewcode',
]

#: Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# source_suffix = ['.rst']

#: The master toctree document.
master_doc = 'index'

# General information about the project.
project = 'Beerializer'
# copyright = ''
author = 'Songbee Team'

try:
    release = pkg_resources.get_distribution('beerializer').version
except pkg_resources.DistributionNotFound:
    print('Beerializer must be installed to build the documentation.')
    print('Install from source using `pip install -e .` in a virtualenv.')
    sys.exit(1)

if 'dev' in release:
    release = ''.join(release.partition('dev')[:2])

version = '.'.join(release.split('.')[:2])

#: List of patterns, relative to source directory, that match files and
#: directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

#: The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'
highlight_language = 'python3'

#: If true, keep warnings as "system message" paragraphs in the built documents.
# keep_warnings = False

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

html_theme = 'alabaster'
# html_title = 'Beerializer vX.Y.Z'
html_short_title = "Beerializer"
html_logo = "_static/logo.png"
html_show_copyright = False
# html_favicon = None
html_static_path = ['_static']
# html_extra_path = []
htmlhelp_basename = 'Beerializerdoc'
html_sidebars = {
    'index': [
        'sidebarintro.html',
        'searchbox.html',
        'copybutton.html',
    ],
    '**': [
        'localtoc.html',
        'sourcelink.html',
        'searchbox.html',
        'copybutton.html',
    ]
}


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'Beerializer.tex', 'Beerializer Documentation',
     author, 'manual'),
]

#: The name of an image file (relative to this directory) to place at the top of
#: the title page.
# latex_logo = None

#: For "manual" documents, if this is true, then toplevel headings are parts,
#: not chapters.
# latex_use_parts = False

#: If true, show page references after internal links.
# latex_show_pagerefs = False

#: If true, show URL addresses after external links.
# latex_show_urls = False

#: Documents to append as an appendix to all manuals.
# latex_appendices = []

#: If false, no module index is generated.
# latex_domain_indices = True


# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {'https://docs.python.org/': None}
