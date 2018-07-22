from taolu.vision.utils.transformers.transformer import Transformer
import torch


class MSETransformer(Transformer):
    def __init__(self, cfg):
        super(MSETransformer, self).__init__(cfg)

    def transform(self, images, labels):
        return torch.Tensor(images), torch.Tensor(labels)
