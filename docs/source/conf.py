"""Configure the local Sphinx documentation build."""

from importlib.metadata import version as distribution_version

project = 'AWS CDK Static Site'
author = 'Dagitali LLC'
project_copyright = '2026, Dagitali LLC'
release = distribution_version('aws-cdk-static-site')
version = release

globals()['copyright'] = project_copyright

extensions = [
    'sphinx_rtd_theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

root_doc = 'index'
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']
autodoc_default_options = {
    'member-order': 'bysource',
    'show-inheritance': True,
}
autodoc_typehints = 'signature'
napoleon_google_docstring = False
napoleon_numpy_docstring = True

html_theme = 'sphinx_rtd_theme'
html_title = f'{project} {release}'
html_theme_options = {'navigation_depth': 3}
