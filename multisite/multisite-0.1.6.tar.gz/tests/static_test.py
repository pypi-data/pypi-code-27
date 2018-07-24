import unittest
import os
from .helper import UtilityMethods, Contents
import multisite


class TestStatic(UtilityMethods):
    def test_make_static(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        msite.make_static(os.path.join(self.workspace, 'html'))
        self.assertFileContentsEqual(
            os.path.join(self.workspace, 'html', 'index.html'),
            Contents.HOMEPAGE
        )
        self.assertFileContentsEqual(
            os.path.join(self.workspace, 'html', '404.html'),
            Contents.NOT_FOUND
        )
        self.assertFileContentsEqual(
            os.path.join(self.workspace, 'html', 'local-site.html'),
            Contents.MD
        )
        self.assertFileContentsEqual(
            os.path.join(self.workspace, 'html', 'local-site', 'other.html'),
            Contents.HTML
        )


if __name__ == '__main__':
    unittest.main()
