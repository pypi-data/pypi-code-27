import os
from glob import glob
from itertools import product

from helper import unittest, PillowTestCase

from PIL import Image


_TGA_DIR = os.path.join("Tests", "images", "tga")
_TGA_DIR_COMMON = os.path.join(_TGA_DIR, "common")


class TestFileTga(PillowTestCase):

    _MODES = ("L", "P", "RGB", "RGBA")
    _ORIGINS = ("tl", "bl")

    _ORIGIN_TO_ORIENTATION = {
        "tl": 1,
        "bl": -1
    }

    def test_sanity(self):
        for mode in self._MODES:
            png_paths = glob(
                os.path.join(
                    _TGA_DIR_COMMON, "*x*_{}.png".format(mode.lower())))

            for png_path in png_paths:
                reference_im = Image.open(png_path)
                self.assertEqual(reference_im.mode, mode)

                path_no_ext = os.path.splitext(png_path)[0]
                for origin, rle in product(self._ORIGINS, (True, False)):
                    tga_path = "{}_{}_{}.tga".format(
                        path_no_ext, origin, "rle" if rle else "raw")

                    original_im = Image.open(tga_path)
                    if rle:
                        self.assertEqual(
                            original_im.info["compression"], "tga_rle")
                    self.assertEqual(
                        original_im.info["orientation"],
                        self._ORIGIN_TO_ORIENTATION[origin])
                    if mode == "P":
                        self.assertEqual(
                            original_im.getpalette(),
                            reference_im.getpalette())

                    self.assert_image_equal(original_im, reference_im)

                    # Generate a new test name every time so the
                    # test will not fail with permission error
                    # on Windows.
                    test_file = self.tempfile("temp.tga")

                    original_im.save(test_file, rle=rle)
                    saved_im = Image.open(test_file)
                    if rle:
                        self.assertEqual(
                            saved_im.info["compression"],
                            original_im.info["compression"])
                    self.assertEqual(
                        saved_im.info["orientation"],
                        original_im.info["orientation"])
                    if mode == "P":
                        self.assertEqual(
                            saved_im.getpalette(),
                            original_im.getpalette())

                    self.assert_image_equal(saved_im, original_im)

    def test_id_field(self):
        # tga file with id field
        test_file = "Tests/images/tga_id_field.tga"

        # Act
        im = Image.open(test_file)

        # Assert
        self.assertEqual(im.size, (100, 100))

    def test_id_field_rle(self):
        # tga file with id field
        test_file = "Tests/images/rgb32rle.tga"

        # Act
        im = Image.open(test_file)

        # Assert
        self.assertEqual(im.size, (199, 199))

    def test_save(self):
        test_file = "Tests/images/tga_id_field.tga"
        im = Image.open(test_file)

        test_file = self.tempfile("temp.tga")

        # Save
        im.save(test_file)
        test_im = Image.open(test_file)
        self.assertEqual(test_im.size, (100, 100))

        # RGBA save
        im.convert("RGBA").save(test_file)
        test_im = Image.open(test_file)
        self.assertEqual(test_im.size, (100, 100))

    def test_save_rle(self):
        test_file = "Tests/images/rgb32rle.tga"
        im = Image.open(test_file)

        test_file = self.tempfile("temp.tga")

        # Save
        im.save(test_file)
        test_im = Image.open(test_file)
        self.assertEqual(test_im.size, (199, 199))

        # RGBA save
        im.convert("RGBA").save(test_file)
        test_im = Image.open(test_file)
        self.assertEqual(test_im.size, (199, 199))

    def test_save_l_transparency(self):
        # There are 559 transparent pixels in la.tga.
        num_transparent = 559

        in_file = "Tests/images/la.tga"
        im = Image.open(in_file)
        self.assertEqual(im.mode, "LA")
        self.assertEqual(
            im.getchannel("A").getcolors()[0][0], num_transparent)

        test_file = self.tempfile("temp.tga")
        im.save(test_file)

        test_im = Image.open(test_file)
        self.assertEqual(test_im.mode, "LA")
        self.assertEqual(
            test_im.getchannel("A").getcolors()[0][0], num_transparent)

        self.assert_image_equal(im, test_im)


if __name__ == '__main__':
    unittest.main()
