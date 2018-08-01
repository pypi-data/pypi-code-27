import tensorflow as tf


class UtilityNetwork:
    @staticmethod
    def initialize_weight_variable(shape):
        kernel = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(kernel)

    @staticmethod
    def initialize_bias_variable(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)

    @staticmethod
    def initialize_variable(nodes_in, nodes_out):
        weight = UtilityNetwork.initialize_weight_variable([nodes_in, nodes_out])
        bias = UtilityNetwork.initialize_bias_variable([nodes_out])
        return weight, bias

    @staticmethod
    def matrix_multiply(image_in, weight, bias):
        image_out = tf.matmul(image_in, weight) + bias
        return image_out
