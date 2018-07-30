import base64
import binascii
import json
import os

from .signer import Signer
from .pkiexpress_config import PkiExpressConfig


class PadesSigner(Signer):
    __pdf_to_sign_path = None
    __vr_json_path = None
    __overwrite_original_file = False

    def __init__(self, config=None):
        if not config:
            config = PkiExpressConfig()
        super(PadesSigner, self).__init__(config)

    # region set_pdf_to_sign

    def set_pdf_to_sign_from_path(self, path):
        if not os.path.exists(path):
            raise Exception('The provided PDF to be signed was not found')
        self.__pdf_to_sign_path = path

    def set_pdf_to_sign_from_raw(self, content_raw):
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'wb') as file_desc:
            file_desc.write(content_raw)
        self.__pdf_to_sign_path = temp_file_path

    def set_pdf_to_sign_from_base64(self, content_base64):
        try:
            raw = base64.standard_b64decode(str(content_base64))
        except (TypeError, binascii.Error):
            raise Exception('The provided PDF to be signed iw not '
                            'Base64-encoded')
        self.set_pdf_to_sign_from_raw(raw)

    # endregion

    # region set_visual_representation

    def set_visual_representation_file(self, path):
        if not os.path.exists(path):
            raise Exception('The provided visual representation file was not '
                            'found')
        self.__vr_json_path = path

    def set_visual_representation(self, representation):
        try:
            json_str = json.dumps(representation)
        except TypeError:
            raise Exception('The provided visual representation, was not valid')
        temp_file_path = self.create_temp_file()
        with open(temp_file_path, 'w') as file_desc:
            file_desc.write(json_str)
        self.__vr_json_path = temp_file_path

    # endregion

    def sign(self):
        if not self.__pdf_to_sign_path:
            raise Exception('The PDF to be signed was not set')

        if not self.__overwrite_original_file and not self._output_file_path:
            raise Exception('The output destination was not set')

        args = [self.__pdf_to_sign_path]

        # Logic to overwrite original file or use the output file
        if self.__overwrite_original_file:
            args.append('--overwrite')
        else:
            args.append(self._output_file_path)

        # Verify and add common options between signers
        self._verify_and_add_common_options(args)

        if self.__vr_json_path:
            args.append('--visual-rep')
            args.append(self.__vr_json_path)

        # Invoke command with plain text output (to support PKI Express < 1.3
        self._invoke_plain(self.COMMAND_SIGN_PADES, args)

    @property
    def overwrite_original_file(self):
        return self.__overwrite_original_file

    @overwrite_original_file.setter
    def overwrite_original_file(self, value):
        self.__overwrite_original_file = value


__all__ = ['PadesSigner']
