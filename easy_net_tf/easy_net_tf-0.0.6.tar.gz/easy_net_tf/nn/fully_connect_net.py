import tensorflow as tf
from easy_net_tf.utility.variable import UtilityVariable


class FullyConnectNet:
    def __init__(self,
                 features_in,
                 nodes_in,
                 nodes_out):

        """

        :param features_in:
        :param nodes_in: input nodes number
        :param nodes_out: output nodes number
        """

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
