import requests
from django.core.files.uploadedfile import SimpleUploadedFile
from mimetypes import guess_extension
from uuid import uuid4


def get_image_from_url(url, name=None, ext=None):
    """
    Get image source from url and create simple in memory file.
    :param url: url file
    :return: SimpleUploadedFile image object
    """
    req = requests.get(url)
    name = name or uuid4().hex
    content_type = req.headers.get('Content-Type')
    extension = ext or guess_extension(content_type, strict=False) or '.jpg'
    extension = '.{}'.format(extension) if not extension[0] == '.' else extension
    new_image_name = "{name}{ext}".format(name=name, ext=extension)
    image = SimpleUploadedFile(new_image_name, req.content, content_type=content_type)
    return image
