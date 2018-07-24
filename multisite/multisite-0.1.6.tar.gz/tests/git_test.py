import unittest
import os
import shutil
import tempfile
from .helper import UtilityMethods
import requests
import multisite


class GitTest(UtilityMethods):
    def setUp(self):
        self.old_cwd = os.getcwd()
        self.workspace = tempfile.mkdtemp(dir='tests')
        os.chdir(self.workspace)

    def tearDown(self):
        os.chdir(self.old_cwd)
        shutil.rmtree(self.workspace)

    def test_clone(self):
        url = 'https://github.com/cmccandless/hundredpushups.git'
        site = multisite.Multisite()
        site.add_site(
            name='git-site',
            source=url,
            source_type='git'
        )
        index_url = (
            'https://raw.githubusercontent.com/'
            'cmccandless/hundredpushups/master/index.md'
        )
        expected = requests.get(index_url).text
        self.assertFileContentsEqual(
            'git-site/index.md',
            expected
        )


if __name__ == '__main__':
    unittest.main()
