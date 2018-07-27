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
                 add_residuals=False,
                 add_bias=True,
                 padding='SAME'):
        """
        :param batch_image:
        :param filter_size:
        :param channels_out:
        :param stride:
        :param add_residuals:
        :param add_bias: True: add; False: not add
        :param padding:
        """

        """
        prepare
        """
        _, height_in, width_in, channels_in = batch_image.shape
        height_in = height_in.value
        width_in = width_in.value
        channels_in = channels_in.value

        if padding == CNN.SAME:
            height_out = round(height_in / stride)
            width_out = round(width_in / stride)
        elif padding == CNN.VALID:
            height_out = round((height_in - filter_size + 1) / stride)
            width_out = round((width_in - filter_size + 1) / stride)
        else:
            height_out = 0
            width_out = 0
            print('Error: '
                  '[%s.%s] '
                  'wrong padding mode.' % (CNN.__name__,
                                           CNN.__init__.__name__))

        self.multi_calculate_conv = height_out * width_out * filter_size * filter_size * channels_in * channels_out

        if add_residuals \
                and (stride != 1
                     or padding is not CNN.SAME):
            add_residuals = False
            print('Error: '
                  '[%s.%s] '
                  'if adding residuals, '
                  'be sure stride = 1 and padding = MobileNetV2.SAME' % (CNN.__name__,
                                                                         CNN.__init__.__name__))
        if add_residuals and channels_in != channels_out:
            self.multi_calculate_residuals = height_in * width_out * channels_in * channels_out
        else:
            self.multi_calculate_residuals = 0

        self.channels_in = channels_in
        self.filter_size = filter_size
        self.channels_out = channels_out
        self.stride = stride
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
        config = [
            '- CNN',
            '- filter size: %d' % self.filter_size,
            '- channels out: %d' % self.channels_out,
            '- stride: %d' % self.stride,
            '- add residuals: %s' % self.add_residuals,
            '- add bias: %s' % self.add_bias,
            '- padding: %s' % self.padding,
            '- multiplicative calculation: %d' % (self.multi_calculate_conv + self.multi_calculate_residuals),
            '   - convolution: %d' % self.multi_calculate_conv,
            '   - residuals: %d' % self.multi_calculate_residuals
        ]
        return config


if __name__ == '__main__':
    from easy_net_tf.utility.file import UtilityFile
    import tensorflow as tf
    import numpy
    from pathlib import Path

    image = numpy.array([[[[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
                          [[1, 1, 1], [1, 1, 1], [1, 1, 1], [1, 1, 1]]]],
                        dtype=numpy.float32)

    image_ph = tf.placeholder(dtype=tf.float32, shape=[None, 5, 4, 3])

    mn = CNN(batch_image=image_ph,
             filter_size=2,
             channels_out=6,
             stride=1,
             add_residuals=True,
             add_bias=True,
             padding=CNN.SAME)

    UtilityFile.list_2_file(Path('test-cnn.md'), mn.export_config())
