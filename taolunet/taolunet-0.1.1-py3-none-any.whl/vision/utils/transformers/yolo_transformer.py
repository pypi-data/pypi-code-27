import torch
from .transformer import Transformer
import cv2
import numpy as np


class YOLOTransformer(Transformer):
    def __init__(self, cfg):
        super(YOLOTransformer, self).__init__(cfg)

    def transform(self, images, boxes):
        new_images = []
        new_boxes = []
        for i in range(len(images)):
            origin_size = [images[i].shape[0], images[i].shape[1]]
            image = cv2.resize(images[i], (self.cfg['height'], self.cfg['width']))
            box = boxes[i]
            if box.shape[0] == 0:
                continue
            if image.shape[0] != 3:
                image = image.transpose(2, 0, 1)
            new_images.append(image)
            box[:, 1] = box[:, 1] / origin_size[1] * self.cfg['width']
            box[:, 2] = box[:, 2] / origin_size[0] * self.cfg['height']
            box[:, 3] = box[:, 3] / origin_size[1] * self.cfg['width']
            box[:, 4] = box[:, 4] / origin_size[0] * self.cfg['height']
            new_boxes.append(self.encoder(box[:, 1:], box[:, 0]))
        return torch.Tensor(new_images), torch.Tensor(new_boxes)

    def encoder(self, boxes, labels):
        '''
        boxes (tensor) [[x1,y1,x2,y2],[]]
        labels (tensor) [...]
        return 7x7x30
        '''
        target = np.zeros((self.cfg['C'], self.cfg['C'], self.cfg['B'] * 5 + self.cfg['num_classes']))
        cell_size = 1. / self.cfg['C'] * self.cfg['height']
        wh = boxes[:, 2:] - boxes[:, :2]
        cxcy = (boxes[:, 2:] + boxes[:, :2]) / 2
        for i in range(cxcy.shape[0]):
            cxcy_sample = cxcy[i]
            ij = np.ceil(cxcy_sample / cell_size) - 1  #
            for b in range(self.cfg['B']):
                target[int(ij[1]), int(ij[0]), b * 5 + 4] = 1
            target[int(ij[1]), int(ij[0]), int(labels[i]) + self.cfg['B'] * 5] = 1
            xy = ij * cell_size
            delta_xy = (cxcy_sample - xy) / cell_size
            target[int(ij[1]), int(ij[0]), 2:4] = wh[i]
            target[int(ij[1]), int(ij[0]), :2] = delta_xy
            target[int(ij[1]), int(ij[0]), 7:9] = wh[i]
            target[int(ij[1]), int(ij[0]), 5:7] = delta_xy
        return target
