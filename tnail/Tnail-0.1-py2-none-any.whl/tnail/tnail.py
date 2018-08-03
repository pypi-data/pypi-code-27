from wand.image import Image
from wand.exceptions import BlobError
from random import randint
import os


def create_thumbnail(file, new_file_name=None,
                     sizes=[(200, 200)]):
    """
    Creates thumbnails of given sizes.

    param file: Image file
    param path: Path where thumbnails will be stored/
                If not given then thumbnails are stored
                in current directory
    param sizes: A list of tuples stating (width, height)
                 of images to be created.
    return: Paths of created thumbnails
    """
    new_file_name = new_file_name or ''.join(
        [str(randint(1, 5)) for i in range(5)]
    )
    try:
        with Image(filename=file) as img:
            _crop_center(img)
            img.format = 'png'
    except BlobError:
        return ("Unable to open image {}: ",
                "No such file or directory".format(file))

    images = []
    for index, size in enumerate(sizes, 1):
        if len(size) == 0:
            size = (50, 50)
        elif len(size) < 2:
            size = (size[0], size[0])
        elif len(size) > 2:
            size = (size[0], size[1])
        with Image(filename=file) as img:
            _crop_center(img)
            file_name = "{}/{}_{}".format(os.getcwd(), new_file_name, index)
            img.sample(size[0], size[1])
            img.format = 'png'
            img.save(filename=file_name)
            images.append(file_name + '.png')
    return images


def _crop_center(image):
    landscape = 1 > (image.width / image.height)
    wh = image.width if landscape else image.height
    image.crop(
        left=int((image.width - wh) / 2),
        top=int((image.height - wh) / 2),
        width=int(wh),
        height=int(wh)
    )
