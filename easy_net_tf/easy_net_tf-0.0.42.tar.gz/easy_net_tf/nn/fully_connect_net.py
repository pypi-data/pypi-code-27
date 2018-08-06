import numpy
import tensorflow as tf
from easy_net_tf.utility.variable import UtilityVariable


class FullyConnectNet:
    def __init__(self,
                 features_in,
                 nodes_out,
                 nodes_in=0,
                 name=''):

        """

        :param features_in: a Tensor [batch, ?]
        :param nodes_out: output nodes number
        :param nodes_in: effective when the shape of features_in is not available.
        :param name:
        """

        if features_in is None:
            self.nodes_in = nodes_in
        else:
            _, _nodes_in = features_in.shape
            nodes_in = nodes_in if _nodes_in.value is None else _nodes_in.value
            self.nodes_in = nodes_in

        self.nodes_out = nodes_out

        """
        initialize variable
        """
        self.weight, \
        self.bias = self._initialize_variable(nodes_in=nodes_in,
                                              nodes_out=nodes_out,
                                              name=name)

        """
        calculate
        """
        if features_in is None:
            self.features_out = None
        else:
            self.features_out = self._calculate(features_in=features_in)

    @staticmethod
    def _initialize_variable(nodes_in, nodes_out, name=''):
        """

        :param nodes_in: input nodes number
        :param nodes_out: output nodes number
        :return:
        """
        weight = UtilityVariable.initialize_weight([nodes_in, nodes_out],
                                                   name='%s-weight' % name)
        bias = UtilityVariable.initialize_bias([nodes_out],
                                               name='%s-bias' % name)
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

    def get_features(self):
        """

        :return: features
        """
        return self.features_out

    def export_variable(self, sess=None, save_dir=None):
        """

        :return: weight, bias
        """

        if sess is None:
            return self.weight, self.bias
        else:
            weight = None if self.weight is None else sess.run(self.weight)
            bias = None if self.bias is None else sess.run(self.bias)

            if save_dir is not None:
                if weight is not None:
                    shape = '[%d,%d]' % weight.shape
                    numpy.savetxt(fname='%s/fcn-weight-%s.txt' % (save_dir, shape),
                                  X=weight,
                                  header='%s: weight' % FullyConnectNet.__name__,
                                  footer='shape: %s' % shape)

                    numpy.save(file='%s/fcn-weight-%s.npy' % (save_dir, shape),
                               arr=weight)

                if bias is not None:
                    shape = '[%d]' % bias.shape
                    numpy.savetxt(fname='%s/fcn-bias-%s.txt' % (save_dir, shape),
                                  X=bias,
                                  header='%s: bias' % FullyConnectNet.__name__,
                                  footer='shape: %s' % shape)

                    numpy.save(file='%s/fcn-bias-%s.npy' % (save_dir, shape),
                               arr=bias)

            return weight, bias

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
