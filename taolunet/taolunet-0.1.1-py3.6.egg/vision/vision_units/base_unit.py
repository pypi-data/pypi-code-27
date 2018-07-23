import torch


class BaseUnits(torch.nn.Module):
    def __init__(self, type):
        super(BaseUnits, self).__init__()
        self.type = type
        self.seq = torch.nn.Sequential()
        self.output_shape = ()

    def forward(self, x):
        return self.seq(x)
