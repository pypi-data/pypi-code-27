import tensorflow as tf
from easy_net_tf.utility.variable import UtilityVariable


class FullyConnectNet:
    def __init__(self,
                 features_in,
                 nodes_out,
                 nodes_in=0):

        """

        :param features_in: a Tensor [batch, ?]
        :param nodes_out: output nodes number
        :param nodes_in: effective when the shape of features_in is not available.
        """

        _, _nodes_in = features_in.shape
        nodes_in = nodes_in if _nodes_in.value is None else _nodes_in.value
        self.nodes_in = nodes_in
        self.nodes_out = nodes_out

        """
        initialize variable
        """
        self.weight, \
        self.bias = self._initialize_variable(nodes_in=nodes_in,
                                              nodes_out=nodes_out)

        """
        calculate
        """
        self.features_out = self._calculate(features_in=features_in)

    @staticmethod
    def _initialize_variable(nodes_in, nodes_out):
        """

        :param nodes_in: input nodes number
        :param nodes_out: output nodes number
        :return:
        """
        weight = UtilityVariable.initialize_weight([nodes_in, nodes_out])
        bias = UtilityVariable.initialize_bias([nodes_out])
        return weight, bias

    def _calculate(self, features_in):
        """

        :param features_in:
        :return: features
        """
        if self.bias is None:
            features_out = tf.matmul(features_in, self.weight)
        else:
            features_out = tf.matmul(features_in, self.weight) + self.bias
        return features_out

    def get_variable(self):
        """

        :return: weight, bias
        """
        return self.weight, self.bias

    def get_features(self):
        """

        :return: features
        """
        return self.features_out

    def export_config(self):
        """
        export config as a list
        :return:
        """
        config = [
            '- Fully Connect Net',
            '- nodes in: %d' % self.nodes_in,
            '- nodes out: %d' % self.nodes_out,
            '- multiplicative calculation: %d' % (self.nodes_in * self.nodes_out),
            ''
        ]
        return config


if __name__ == '__main__':
    from easy_net_tf.utility.file import UtilityFile
    import numpy
    from pathlib import Path

    image = numpy.array([[[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]]],
                        dtype=numpy.float32)

    image_ph = tf.placeholder(dtype=tf.float32, shape=[None, 60])

    fcn = FullyConnectNet(features_in=image_ph,
                          nodes_out=30)

    UtilityFile.list_2_file(Path('test-fcn.md'), fcn.export_config())
