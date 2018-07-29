import logging

import torch.nn.functional

losses_logger = logging.getLogger("thelper.losses")


def my_loss(y_input,y_target):
    return torch.nn.functional.nll_loss(y_input,y_target)
