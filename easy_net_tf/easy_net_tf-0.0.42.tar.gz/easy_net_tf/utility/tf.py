import tensorflow as tf
from tensorflow.python import pywrap_tensorflow

from easy_net_tf.utility.dialog import UtilityDialog


class UtilityTf:
    @staticmethod
    def latest_checkpoint(model_dir=None, initial_dir='', hint=''):
        if model_dir is None:
            import tkinter.filedialog

            model_dir = UtilityDialog.tk_avoid(func=tkinter.filedialog.askdirectory,
                                               hint=hint,
                                               initial_dir=initial_dir)
            if type(model_dir) == tuple:
                model_dir = ''

        return tf.train.latest_checkpoint(model_dir)

    @staticmethod
    def get_variables(checkpoint_path=None):
        if checkpoint_path is None:
            checkpoint_path = UtilityTf.latest_checkpoint(hint='Select model directory')

        reader = pywrap_tensorflow.NewCheckpointReader(checkpoint_path)
        var_to_shape_map = reader.get_variable_to_shape_map()

        result = list()
        for key in var_to_shape_map:
            result.append('%s' % key)
            result.append(reader.get_tensor(key))

        return result


if __name__ == '__main__':
    # path = UtilityTf.latest_checkpoint(hint='hello world')

    variables = UtilityTf.get_variables()

    print(variables)
