import tensorflow as tf

from easy_net_tf.utility.variable import UtilityVariable


class CNN:
    def __init__(self,
                 image_in,
                 channels_in,
                 filter_size,
                 channels_out,
                 stride,
                 add_residuals=False,
                 add_bias=True,
                 padding='SAME'):
        """
        :param image_in:
        :param channels_in:
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
        self.feature_map = self._calculate(image_in)

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
                   image):
        """
        No activation function applied on output.
        :param image:
        :return:
        """

        """
        convolution
        """
        convolution_o = tf.nn.conv2d(input=image,
                                     filter=self.convolution_filter,
                                     strides=[1, self.stride, self.stride, 1],
                                     padding=self.padding)

        """
        residuals block
        """
        if self.add_residuals is True:
            if self.residuals_filter is not None:
                image = tf.nn.conv2d(input=image,
                                     filter=self.residuals_filter,
                                     strides=[1, 1, 1, 1],
                                     padding='SAME')

            map_out = tf.add(convolution_o, image)
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
