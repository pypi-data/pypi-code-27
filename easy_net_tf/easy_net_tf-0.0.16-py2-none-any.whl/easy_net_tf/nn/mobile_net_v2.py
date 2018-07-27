import tensorflow as tf

from easy_net_tf.utility.variable import UtilityVariable


class MobileNetV2:
    VALID = 'VALID'
    SAME = 'SAME'

    def __init__(self,
                 batch_image,
                 dilate_number,
                 filter_size,
                 channels_out,
                 dilate_active_func,
                 depth_active_func,
                 stride=1,
                 add_residuals=False,
                 add_bias=True,
                 padding='SAME'):
        """
        :param batch_image: a Tensor [batch, height, width, channel]
        :param dilate_number: if 'None', become MobileNet V1 without output activation
        :param filter_size:
        :param channels_out:
        :param dilate_active_func: active function for dilatation.
        :param depth_active_func: active function for depthwise.
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

        if padding == MobileNetV2.VALID:
            height_out = round((height_in - filter_size + 1) / stride)
            width_out = round((width_in - filter_size + 1) / stride)
        elif padding == MobileNetV2.SAME:
            height_out = round(height_in / stride)
            width_out = round(width_in / stride)
        else:
            height_out = 0
            width_out = 0
            print('Error: '
                  '[%s.%s] '
                  'wrong padding mode.' % (MobileNetV2.__name__,
                                           MobileNetV2.__init__.__name__))
        if dilate_number is None:
            self.multi_calculate_dilate = 0
            self.multi_calculate_depth = height_out * width_out * filter_size * filter_size * channels_in
            self.multi_calculate_compress = height_out * width_out * channels_in * channels_out
        else:
            self.multi_calculate_dilate = height_in * width_in * channels_in * dilate_number
            self.multi_calculate_depth = height_out * width_out * filter_size * filter_size * dilate_number
            self.multi_calculate_compress = height_out * width_out * dilate_number * channels_out

        self.channels_in = channels_in
        self.channels_out = channels_out

        self.dilate_number = dilate_number

        self.filter_size = filter_size

        self.dilate_active_func = dilate_active_func
        self.dilate_active_func_name = 'None' \
            if self.dilate_active_func is None \
            else self.dilate_active_func.__name__

        self.depth_active_func = depth_active_func
        self.depth_active_func_name = 'None' \
            if self.depth_active_func is None \
            else self.depth_active_func.__name__

        self.stride = stride
        self.add_residuals = add_residuals
        self.add_bias = add_bias
        self.padding = padding

        """
        initialize filter
        """
        self.dilatation_filter, \
        self.depthwise_filter, \
        self.compress_filter, \
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

        channel_multiplier = 1

        """
        dilatation_filter
        """
        if self.dilate_number is None:
            dilatation_filter = None
            self.dilate_number = self.channels_in
        else:
            dilatation_filter = UtilityVariable.initialize_weight(
                [1,
                 1,
                 self.channels_in,
                 self.dilate_number]
            )

        """
        depthwise_filter
        """
        depthwise_filter = UtilityVariable.initialize_weight(
            [self.filter_size,
             self.filter_size,
             self.dilate_number,
             channel_multiplier]
        )

        """
        compress_filter
        """
        compress_filter = UtilityVariable.initialize_weight(
            [1,
             1,
             self.dilate_number * channel_multiplier,
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

        return dilatation_filter, \
               depthwise_filter, \
               compress_filter, \
               residuals_filter, \
               bias

    def _calculate(self,
                   image_in):
        """
        No activation function applied on output.
        :param image_in:
        :return:
        """

        """
        dilatation
        """
        if self.dilatation_filter is not None:

            dilatation_o = tf.nn.conv2d(input=image_in,
                                        filter=self.dilatation_filter,
                                        strides=[1, 1, 1, 1],
                                        padding='SAME')

            if self.depth_active_func is not None:
                dilatation_o = self.dilate_active_func(dilatation_o)

        else:
            dilatation_o = image_in

        """
        depthwise
        """
        convolution_o = tf.nn.depthwise_conv2d(input=dilatation_o,
                                               filter=self.depthwise_filter,
                                               strides=[1, self.stride, self.stride, 1],
                                               padding=self.padding)
        if self.depth_active_func is not None:
            convolution_o = self.depth_active_func(convolution_o)

        """
        compress
        """
        compress_o = tf.nn.conv2d(input=convolution_o,
                                  filter=self.compress_filter,
                                  strides=[1, 1, 1, 1],
                                  padding='SAME')

        """
        residuals block
        """
        if self.add_residuals is True:
            if self.residuals_filter is not None:
                image_in = tf.nn.conv2d(input=image_in,
                                        filter=self.residuals_filter,
                                        strides=[1, 1, 1, 1],
                                        padding='SAME')

            result = tf.add(compress_o, image_in)
        else:
            result = compress_o

        """
        bias
        """
        if self.bias is not None:
            result += self.bias

        return result

    def get_variable(self):
        """
        :return: filters
        """
        return self.dilatation_filter, \
               self.depthwise_filter, \
               self.compress_filter

    def get_feature_map(self):
        """
        :return: image out
        """
        return self.feature_map

    def export_config(self):
        """
        export config as a list
        :return:
        """
        config = [
            '- MobileNet V2',
            '- filter size: %d' % self.filter_size,
            '- channels in: %d' % self.channels_in,
            '- channels out: %d' % self.channels_out,
            '- dilatation: %d' % self.dilate_number,
            '- dilate active function: %s' % self.dilate_active_func_name,
            '- depth-wise active function: %s' % self.depth_active_func_name,
            '- stride: %d' % self.stride,
            '- add residuals: %s' % self.add_residuals,
            '- add bias: %s' % self.add_bias,
            '- padding: %s ' % self.padding,
            '- multiplicative calculation: ',
            '   - dilatation: %d' % self.multi_calculate_dilate,
            '   - depth-wise: %d' % self.multi_calculate_depth,
            '   - compress: %d' % self.multi_calculate_compress,
            '   - total: %d' % (self.multi_calculate_dilate
                                + self.multi_calculate_depth
                                + self.multi_calculate_compress)
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

    mn = MobileNetV2(batch_image=image_ph,
                     dilate_number=1,
                     filter_size=3,
                     channels_out=15,
                     dilate_active_func=tf.nn.relu6,
                     depth_active_func=tf.nn.leaky_relu,
                     stride=2,
                     add_residuals=False,
                     add_bias=False,
                     padding=MobileNetV2.SAME)

    UtilityFile.list_2_file(Path('test.md'), mn.export_config())
