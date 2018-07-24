import unittest
import os
from .helper import UtilityMethods
import multisite


class TestLocal(UtilityMethods):
    def test_add_local_site(self):
        config_file = os.path.join(self.workspace, 'add_local_site.json')
        msite = multisite.Multisite(config_file=config_file)
        msite.add_site('local', 'local-site', source_type='local')
        expected = {
            "local": {
                "name": "local",
                "source": "local-site",
                "location": "local-site",
                "source_type": "local",
                "auto_update": False
            }
        }
        self.assertDictEqual(msite.sites, expected)

    def test_existing_config_file(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file=config_file)
        expected = {
            "local-site": {
                "name": "local-site",
                "source": "local-site/",
                "location": "local-site/",
                "source_type": "local",
                "auto_update": False
            }
        }
        self.assertDictEqual(msite.sites, expected)

    def test_bad_directory_path(self):
        config_file = os.path.join('configs', 'local.json')
        msite = multisite.Multisite(config_file=config_file)
        with self.assertRaises(OSError):
            msite.add_site(
                'bad-dir',
                os.path.join('archives', 'zip-site.zip'),
                source_type='local'
            )


if __name__ == '__main__':
    unittest.main()
