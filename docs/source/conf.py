import os
import sys
sys.path.insert(0, os.path.abspath('../../'))

project = 'Fun Tools'
author = 'Your Name'
release = '1.0.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
]

html_theme = 'alabaster'
