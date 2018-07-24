import unittest
import os
from .helper import (
    UtilityMethods,
    Contents
)
import multisite


class TestGet(UtilityMethods):
    def test_page_html(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        self.assertEqual(
            msite.page('local-site/other.html', None),
            Contents.HTML
        )

    def test_page_markdown(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        self.assertEqual(msite.page('local-site/index.md', None), Contents.MD)

    def test_page_flexible_extension_html(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        self.assertEqual(msite.page('local-site/other'), Contents.HTML)

    def test_page_flexible_extension_markdown(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        self.assertEqual(msite.page('local-site/index'), Contents.MD)

    def test_not_found_default(self):
        old_cwd = os.getcwd()
        os.chdir(self.workspace)
        try:
            config_file = 'not_found.json'
            msite = multisite.Multisite(config_file)
            status, response = msite.get('/does-not-exist')
            self.assertEqual(status, 404)
            self.assertEqual(response, '404: Page not found')
        finally:
            os.chdir(old_cwd)

    def test_not_found_using_custom_response(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        status, response = msite.get('/does-not-exist')
        self.assertEqual(status, 404)
        self.assertEqual(response, Contents.NOT_FOUND)

    def test_homepage(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        status, response = msite.homepage()
        self.assertEqual(status, 200)
        self.assertEqual(response, Contents.HOMEPAGE)

    def test_homepage_not_found(self):
        old_cwd = os.getcwd()
        os.chdir(self.workspace)
        try:
            config_file = 'homepage-not-found.json'
            msite = multisite.Multisite(config_file)
            status, response = msite.homepage()
            self.assertEqual(status, 404)
            self.assertEqual(response, '404: Page not found')
        finally:
            os.chdir(old_cwd)

    def test_get_root_returns_homepage(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        status, response = msite.get('/')
        self.assertEqual(status, 200)
        self.assertEqual(response, Contents.HOMEPAGE)

    def test_get_subsite_page(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        status, response = msite.get('/local-site/other.html')
        self.assertEqual(status, 200)
        self.assertEqual(response, Contents.HTML)

    def test_get_subsite_page_flexible_extension(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        status, response = msite.get('/local-site/other')
        self.assertEqual(status, 200)
        self.assertEqual(response, Contents.HTML)

    def test_get_subsite_homepage(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        status, response = msite.get('/local-site/')
        self.assertEqual(status, 200)
        self.assertEqual(response, Contents.MD)

    def test_subsite_page_not_found(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file)
        status, response = msite.get('/local-site/does-not-exist')
        self.assertEqual(status, 404)
        self.assertEqual(response, Contents.NOT_FOUND)


if __name__ == '__main__':
    unittest.main()
