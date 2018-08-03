from PIL import Image
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from uuid import uuid4


class MockFilesMixin(object):
    def generate_image(self, **kwargs):
        """
        Create image file
        :param params: dict with image properties
        :return: image object
        """
        width = kwargs.get('width', 100)
        height = kwargs.get('height', width)
        color = kwargs.get('color', 'blue')
        image_format = kwargs.get('format', 'JPEG')
        filename = kwargs.get('filename', '{}{}'.format(uuid4().hex, '.jpg'))
        content_type = "image/{}".format(kwargs.get('content_type', 'jpeg'))

        thumb = Image.new('RGB', (width, height), color)
        thumb_io = BytesIO()
        thumb.save(thumb_io, format=image_format)
        # if you want use UploadedFile instead of SimpleUploadFile
        # pass only thumb_io as file, without getvalue() calling
        return SimpleUploadedFile(filename, thumb_io.getvalue(), content_type)
