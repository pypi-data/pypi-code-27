import sys
import os
from unittest.mock import MagicMock as Mock
from setuptools_scm import get_version

# Mocking to make RTD autobuild the documentation.
autodoc_mock_imports = [
		'numpy', 'numpy.testing', 'numpy.random',
		'symengine',
		'jitcxde_common.helpers','jitcxde_common.symbolic'
	]

sys.path.insert(0,os.path.abspath("../examples"))
sys.path.insert(0,os.path.abspath("../jitcsde"))

needs_sphinx = '1.3'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.mathjax',
    'numpydoc',
]

source_suffix = '.rst'

master_doc = 'index'

project = u'JiTCSDE'
copyright = u'2017, Gerrit Ansmann'

release = version = get_version(root='..', relative_to=__file__)

default_role = "any"

add_function_parentheses = True

add_module_names = False

html_theme = 'nature'
pygments_style = 'colorful'
htmlhelp_basename = 'JiTCSDEdoc'

numpydoc_show_class_members = False
autodoc_member_order = 'bysource'

def on_missing_reference(app, env, node, contnode):
	if node['reftype'] == 'any':
		return contnode
	else:
		return None

def setup(app):
	app.connect('missing-reference', on_missing_reference)
