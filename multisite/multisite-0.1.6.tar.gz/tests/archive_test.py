import unittest
import os
from .helper import UtilityMethods
import multisite


class ArchiveTest(UtilityMethods):
    def assertExtractedArchiveContents(self, archive_type, extract_method):
        archive_name = '{}-site'.format(archive_type)
        archive_file = 'archives{}{}.{}'.format(
            os.path.sep,
            archive_name,
            archive_type.replace('-', '.')
        )
        extract_method(archive_file, self.workspace)
        self.assertFileContentsEqual(
            os.path.join(self.workspace, archive_name, 'index.md'),
            '# {}/index.md\n\n*as markdown*\n'.format(archive_name)
        )
        self.assertFileContentsEqual(
            os.path.join(self.workspace, archive_name, 'other.html'),
            (
                '<html>\n'
                '    <body>{}/other.html</body>\n'
                '</html>\n'
            ).format(archive_name)
        )

    def test_extract_zip(self):
        self.assertExtractedArchiveContents('zip', multisite.extract_zip)

    def test_extract_tar(self):
        self.assertExtractedArchiveContents('tar', multisite.extract_tarball)

    def test_extract_tar_gz(self):
        self.assertExtractedArchiveContents(
            'tar-gz',
            multisite.extract_tarball
        )

    def test_extract_tar_bz2(self):
        self.assertExtractedArchiveContents(
            'tar-bz2',
            multisite.extract_tarball
        )

    def test_extract_tar_xz(self):
        if multisite.PYTHON3:
            self.assertExtractedArchiveContents(
                'tar-xz',
                multisite.extract_tarball
            )

    def test_import_archive_zip(self):
        self.assertExtractedArchiveContents('zip', multisite.import_archive)

    def test_import_archive_tar(self):
        self.assertExtractedArchiveContents('tar', multisite.import_archive)

    def test_import_archive_tar_xz(self):
        if multisite.PYTHON3:
            self.assertExtractedArchiveContents(
                'tar-xz',
                multisite.import_archive
            )

    def test_import_archive_unknown(self):
        with self.assertRaises(ValueError):
            multisite.import_archive('unsupported.rar', '.')

    def test_add_archive_site(self):
        old_cwd = os.getcwd()
        os.chdir(self.workspace)
        try:
            config_file = 'add_archive_site.json'
            msite = multisite.Multisite(config_file=config_file)
            zip_file = os.path.join('..', 'archives', 'zip-site.zip')
            msite.add_site('zip-site', zip_file, source_type='archive')
            expected = {
                "zip-site": {
                    "name": "zip-site",
                    "source": zip_file,
                    "location": os.path.join('.', "zip-site"),
                    "source_type": "archive",
                    "auto_update": False
                }
            }
            self.assertDictEqual(msite.sites, expected)
        finally:
            os.chdir(old_cwd)


if __name__ == '__main__':
    unittest.main()
