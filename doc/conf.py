#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sphinxbootstrap4theme
import sys
import os

sys.path.insert(0, os.path.abspath('..'))
extensions = ['myasuda.sphinx.erdiagram']

graphviz_output_format = "svg"

source_suffix = '.rst'

master_doc = 'index'

project = 'ER Diagram Manual'
copyright = '2016, myasuda'
author = 'myasuda'

version = '0.0.1'
release = '0.0.1'

language = 'ja'

exclude_patterns = []

pygments_style = 'sphinx'

html_theme = 'sphinxbootstrap4theme'
html_theme_path = [sphinxbootstrap4theme.get_path()]
html_theme_options = {
    'sidebar_right': False,
    'navbar_pages_title': 'Menu',
    'navbar_links': [
        ('GitHub', 'https://github.com/myyasuda/sphinx_erdiagram', True)
    ]
}

#html_static_path = ['_static']
htmlhelp_basename = 'ERDiagramManualdoc'

latex_elements = {}
latex_documents = [
    (master_doc, 'ERDiagramManual.tex', 'ER Diagram Manual Documentation',
     'myasuda', 'manual'),
]

man_pages = [
    (master_doc, 'erdiagrammanual', 'ER Diagram Manual Documentation',
     [author], 1)
]

texinfo_documents = [
    (master_doc, 'ERDiagramManual', 'ER Diagram Manual Documentation',
     author, 'ERDiagramManual', 'One line description of project.',
     'Miscellaneous'),
]