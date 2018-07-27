import tensorflow as tf


class UtilityVariable:
    """

    """

    @staticmethod
    def initialize_weight(shape):
        kernel = tf.truncated_normal(shape, stddev=0.1)
        return tf.Variable(kernel)

    @staticmethod
    def initialize_bias(shape):
        initial = tf.constant(0.1, shape=shape)
        return tf.Variable(initial)


