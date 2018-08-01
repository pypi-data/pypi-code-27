import tensorflow as tf
from easy_net_tf.utility.variable import UtilityVariable


class CNN:
    VALID = 'VALID'
    SAME = 'SAME'

    def __init__(self,
                 batch_image,
                 filter_size,
                 channels_out,
                 stride,
                 channels_in=0,
                 add_residuals=False,
                 add_bias=True,
                 padding='SAME'):
        """
        :param batch_image:
        :param filter_size:
        :param channels_out:
        :param stride:
        :param channels_in: effective when the shape of batch_image is not available.
        :param add_residuals:
        :param add_bias: True: add; False: not add
        :param padding:
        """

        """
        prepare
        """
        _, _height_in, _width_in, _channels_in = batch_image.shape
        self.height_in = _height_in.value
        self.width_in = _width_in.value
        self.channels_in = channels_in if _channels_in.value is None else _channels_in.value

        assert self.channels_in != 0, '[%s,%s] ' \
                                      'channels_in should be set, ' \
                                      'when the shape of batch_image is not sure.' % (CNN.__name__,
                                                                                      CNN.__init__.__name__)

        self.filter_size = filter_size
        self.channels_out = channels_out
        self.stride = stride

        if add_residuals \
                and (stride != 1
                     or padding is not CNN.SAME):
            add_residuals = False
            print('Error: '
                  '[%s.%s] '
                  'if adding residuals, '
                  'be sure stride = 1 and padding = MobileNetV2.SAME' % (CNN.__name__,
                                                                         CNN.__init__.__name__))
        self.add_residuals = add_residuals
        self.add_bias = add_bias
        self.padding = padding

        """
        initialize filter
        """
        self.convolution_filter, \
        self.residuals_filter, \
        self.bias = self._initialize_variable()

        """
        calculation
        """
        self.feature_map = self._calculate(batch_image)

    def _initialize_variable(self):
        """
        initialize variable
        :return:
        """

        """
        filter
        """
        convolution_filter = UtilityVariable.initialize_weight(
            [self.filter_size,
             self.filter_size,
             self.channels_in,
             self.channels_out]
        )

        """
        residuals_filter
        """
        if self.add_residuals and self.channels_in != self.channels_out:
            residuals_filter = UtilityVariable.initialize_weight(
                [1,
                 1,
                 self.channels_in,
                 self.channels_out]
            )
        else:
            residuals_filter = None

        """
        bias
        """
        if self.add_bias:
            bias = UtilityVariable.initialize_bias([self.channels_out])
        else:
            bias = None

        return convolution_filter, residuals_filter, bias

    def _calculate(self,
                   batch_image):
        """
        No activation function applied on output.
        :param batch_image:
        :return:
        """

        """
        convolution
        """
        convolution_o = tf.nn.conv2d(input=batch_image,
                                     filter=self.convolution_filter,
                                     strides=[1, self.stride, self.stride, 1],
                                     padding=self.padding)

        """
        residuals block
        """
        if self.add_residuals is True:
            if self.residuals_filter is not None:
                batch_image = tf.nn.conv2d(input=batch_image,
                                           filter=self.residuals_filter,
                                           strides=[1, 1, 1, 1],
                                           padding='SAME')

            map_out = tf.add(convolution_o, batch_image)
        else:
            map_out = convolution_o

        """
        bias
        """
        if self.bias is not None:
            map_out += self.bias

        return map_out

    def _count_multiplication(self):
        if self.height_in is None or self.width_in is None:
            return -1, -1

        else:
            if self.padding == CNN.SAME:
                height_out = round(self.height_in / self.stride)
                width_out = round(self.width_in / self.stride)
            elif self.padding == CNN.VALID:
                height_out = round((self.height_in - self.filter_size + 1) / self.stride)
                width_out = round((self.width_in - self.filter_size + 1) / self.stride)
            else:
                height_out = 0
                width_out = 0
                print('Error: '
                      '[%s.%s] '
                      'wrong padding mode.' % (CNN.__name__,
                                               CNN.__init__.__name__))

            convolution = height_out * width_out * self.filter_size * self.filter_size * self.channels_in * self.channels_out

            if self.add_residuals and self.channels_in != self.channels_out:
                residuals = self.height_in * width_out * self.channels_in * self.channels_out
            else:
                residuals = 0

            return convolution, residuals

    def get_variable(self):
        """
        :return:
        """
        return self.convolution_filter, \
               self.residuals_filter, \
               self.bias

    def get_feature_map(self):
        """
        :return:
        """
        return self.feature_map

    def export_config(self):

        multiplication_convolution, \
        multiplication_residuals = self._count_multiplication()

        config = [
            '- CNN',
            '- filter size: %d' % self.filter_size,
            '- channels in: %d' % self.channels_in,
            '- channels out: %d' % self.channels_out,
            '- stride: %d' % self.stride,
            '- add residuals: %s' % self.add_residuals,
            '- add bias: %s' % self.add_bias,
            '- padding: %s' % self.padding,
            '- multiplicative calculation: %d' % (multiplication_convolution + multiplication_residuals),
            '   - convolution: %d' % multiplication_convolution,
            '   - residuals: %d' % multiplication_residuals,
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

    image_ph = tf.placeholder(dtype=tf.float32, shape=[None, None, None, None])

    mn = CNN(batch_image=image_ph,
             filter_size=2,
             channels_out=6,
             stride=1,
             channels_in=3,
             add_residuals=True,
             add_bias=True,
             padding=CNN.SAME)

    UtilityFile.list_2_file(Path('test-cnn.md'), mn.export_config())
