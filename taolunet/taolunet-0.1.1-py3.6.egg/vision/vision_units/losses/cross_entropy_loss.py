from .loss import Loss
from torch.nn.functional import cross_entropy


class CrossEntropyLoss(Loss):
    def __init__(self, cfg):
        super(CrossEntropyLoss, self).__init__(cfg)

    def forward(self, pred, target):
        return cross_entropy(pred, target)
