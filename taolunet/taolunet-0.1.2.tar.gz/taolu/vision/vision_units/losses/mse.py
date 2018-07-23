from .loss import Loss
from torch.nn.functional import mse_loss


class MSELoss(Loss):
    def __init__(self, cfg):
        super(MSELoss, self).__init__(cfg)

    def forward(self, pred, target):
        return mse_loss(pred, target)
