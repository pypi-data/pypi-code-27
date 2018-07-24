import unittest
import os
import tempfile
import shutil


class UtilityMethods(unittest.TestCase):
    def setUp(self):
        self.old_cwd = os.getcwd()
        os.chdir('tests')
        self.workspace = tempfile.mkdtemp(dir='.')

    def tearDown(self):
        shutil.rmtree(self.workspace)
        os.chdir(self.old_cwd)

    def assertFileContentsEqual(self, filepath, expected):
        with open(filepath) as f:
            self.assertEqual(f.read(), expected)


class Contents(object):
    MD = """<h1>local-site/index.md</h1>
<p><em>as markdown</em></p>
"""
    HTML = """<html>
    <body>local-site/other.html</body>
</html>
"""
    NOT_FOUND = """<h1>404</h1>
<p>Page not found</p>
"""
    HOMEPAGE = """<h1>homepage</h1>
<p>Try other URLs!</p>
"""