import torch
from taolu.vision.base_nets.base_net import BaseNet


class ObjectDetectionJob:
    def __init__(self, cfg, num_classes=None, cuda=False):
        self.num_classes = num_classes
        self.cfg = cfg
        self.cuda = cuda
        self.model = self.build_model()

    def build_model(self):
        model = BaseNet(self.cfg)
        return model.cuda() if self.cuda else model

    def train(self, x, y):


        if self.model.transformer:
            x, y = self.model.transformer.transform(x, y)
        if self.cuda:
            x = x.cuda()
            y = y.cuda()
        output = self.model(x)
        error = self.model.loss(output, y)
        self.model.optim.zero_grad()
        error.backward()
        self.model.optim.step()
        return error
