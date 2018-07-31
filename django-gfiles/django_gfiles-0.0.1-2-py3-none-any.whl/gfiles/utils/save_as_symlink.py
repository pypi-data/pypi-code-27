import os
import tempfile
from django.core.files import File
from django.conf import settings

def save_as_symlink(abs_pth, name, generic_file_obj):
    """ Takes a :class:`gfiles.models.GenericFiles` object and saves a symlink of the file to the absolute path
     (abs_pth).

    :param abs_pth: path to the file to symlink to
    :param name: Name to save to the file as
    :param generic_file_obj: :class:`gfiles.models.GenericFiles` object

    :returns: updated :class:`gfiles.models.GenericFiles` object with symlink

    """
    tf = tempfile.NamedTemporaryFile(delete=False)

    # first create link to empty file
    file_data_obj.data_file.save(name, File(open(tf.name)))

    fpth = os.path.join(settings.MEDIA_ROOT, generic_file_obj.data_file.name)
    os.remove(fpth)
    os.symlink(abs_pth, fpth)
    file_data_obj.save()
    tf.close()

    return generic_file_obj