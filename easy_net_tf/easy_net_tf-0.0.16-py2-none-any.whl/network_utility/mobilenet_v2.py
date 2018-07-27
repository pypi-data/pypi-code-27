import tensorflow as tf

from network.netword_utility.utility_network import UtilityNetwork


class MobileNetV2:
    def __init__(self,
                 image_in,
                 channels_in,
                 dilatation,
                 filter_size,
                 channels_out,
                 stride=1,
                 add_residuals=False,
                 padding='SAME'):
        """
        :param image_in:
        :param channels_in:
        :param dilatation: if 'None', become MobileNet V1 without output activation
        :param filter_size:
        :param channels_out:
        :param stride:
        :param add_residuals:
        :param padding:
        """

        """
        preprare
        """
        self.channels_in = channels_in
        self.dilatation = dilatation
        self.filter_size = filter_size
        self.channels_out = channels_out
        self.stride = stride
        self.add_residuals = add_residuals
        self.padding = padding

        """
        initialize filter
        """
        self.dilatation_filter, \
        self.convolution_filter, \
        self.compress_filter, \
        self.residuals_filter = self._initialize_variable()

        """
        calculation
        """
        self.feature_map = self._do_calculation(image_in)

    def _initialize_variable(self):
        """
        initialize variable
        :return:
        """

        channel_multiplier = 1

        """
        dilatation_filter
        """
        if self.dilatation is None:  # become MobileNet V1 again
            dilatation_filter = None
            self.dilatation = 1
        else:
            dilatation_filter = UtilityNetwork.initialize_weight(
                [1,
                 1,
                 self.channels_in,
                 self.channels_in * self.dilatation]
            )

        """
        depthwise_filter
        """
        depthwise_filter = UtilityNetwork.initialize_weight(
            [self.filter_size,
             self.filter_size,
             self.channels_in * self.dilatation,
             channel_multiplier]
        )

        """
        compress_filter
        """
        compress_filter = UtilityNetwork.initialize_weight(
            [1,
             1,
             self.channels_in * self.dilatation * channel_multiplier,
             self.channels_out]
        )

        """
        residuals_filter
        """
        if self.add_residuals and self.channels_in != self.channels_out:
            residuals_filter = UtilityNetwork.initialize_weight(
                [1,
                 1,
                 self.channels_in,
                 self.channels_out]
            )
        else:
            residuals_filter = None

        return dilatation_filter, \
               depthwise_filter, \
               compress_filter, \
               residuals_filter

    def _do_calculation(self,
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
            # activation
            dilatation_o = tf.nn.relu6(dilatation_o)

        else:
            dilatation_o = image_in

        """
        depthwise
        """
        convolution_o = tf.nn.depthwise_conv2d(input=dilatation_o,
                                               filter=self.convolution_filter,
                                               strides=[1, self.stride, self.stride, 1],
                                               padding=self.padding)
        # activation
        convolution_o = tf.nn.relu6(convolution_o)

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

        return result

    def get_variable(self):
        """
        :return: filters
        """
        return self.dilatation_filter, \
               self.convolution_filter, \
               self.compress_filter

    def get_feature_map(self):
        """
        :return: image out
        """
        return self.feature_map
