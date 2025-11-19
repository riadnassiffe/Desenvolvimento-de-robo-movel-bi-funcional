# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys
import subprocess
subprocess.call('doxygen Doxyfile.in', shell=True)
sys.path.insert(0, os.path.abspath('../../../Cliente'))
#sys.path.append(os.path.abspath('../../../Servidor/'))
# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Desenvolvimento de robo bifuncional'
copyright = '2025, IFC'
author = 'IFC'
release = '2.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx_rtd_theme',
    'sphinx.ext.graphviz',
    'breathe',
    'sphinx.ext.imgmath', 
    'sphinx.ext.todo',
        ]

breathe_projects = {"myproject": os.path.abspath("doc_out/xml/"),}
breathe_default_project = "myproject"
templates_path = ['_templates']
exclude_patterns = []

language = 'pt'

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
