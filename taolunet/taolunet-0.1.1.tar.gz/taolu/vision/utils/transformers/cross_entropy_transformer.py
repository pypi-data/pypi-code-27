from taolu.vision.utils.transformers.transformer import Transformer
import torch


class CrossEntropyTransformer(Transformer):
    def __init__(self, cfg):
        super(CrossEntropyTransformer, self).__init__(cfg)

    def transform(self, images, labels):
        images = torch.Tensor(images)
        labels = torch.Tensor(labels)
        labels = labels.to(dtype=torch.long)
        return images, torch.argmax(labels, 1)
