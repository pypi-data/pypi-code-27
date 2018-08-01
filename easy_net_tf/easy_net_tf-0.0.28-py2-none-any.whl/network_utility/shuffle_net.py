import tensorflow as tf

from network.netword_utility.utility_network import UtilityNetwork


class ShuffleNet:
    def __init__(self,
                 image_in,
                 channels_in,
                 filter_size,
                 channels_out,
                 padding='SAME'):

    @staticmethod
    def initialize_variable(channels_in,
                            filter_size,
                            channels_out):
        point_wise_filter = UtilityNetwork.initialize_weight([1, 1, ])
