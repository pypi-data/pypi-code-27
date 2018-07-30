from network.netword_utility.utility_network import UtilityNetwork


class FullyConnectNet:
    def __init__(self,
                 image_in,
                 nodes_in,
                 nodes_out):
        self.weight, self.bias = UtilityNetwork.initialize_variable(nodes_in=nodes_in,
                                                                    nodes_out=nodes_out)
        self.image_out = UtilityNetwork.convolution(image_in=image_in,
                                                    weight=self.weight,
                                                    bias=self.bias)

    def get_variable(self):
        return self.weight, self.bias

    def get_map(self):
        return self.image_out
