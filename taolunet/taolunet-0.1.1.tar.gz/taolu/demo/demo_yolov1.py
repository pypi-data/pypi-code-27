from taolu.vision.vision_units.losses.yolo_loss import YoloLoss
import torch
import taolu.demo.demo_images
import numpy as np
import cv2
from taolu.demo.yolo_temp import YOLO
from taolu.vision.vision_units.losses.yolo_loss import YoloLoss


def encoder(boxes, labels):
    '''
    boxes (tensor) [[x1,y1,x2,y2],[]]
    labels (tensor) [...]
    return 7x7x30
    '''
    # boxes = torch.Tensor(boxes)
    # labels = torch.Tensor(labels)
    target = np.zeros((7, 7, 30))
    cell_size = 1. / 7 * 224
    wh = boxes[:, 2:] - boxes[:, :2]
    cxcy = (boxes[:, 2:] + boxes[:, :2]) / 2
    for i in range(cxcy.shape[0]):
        cxcy_sample = cxcy[i]
        ij = np.ceil(cxcy_sample / cell_size) - 1  #
        target[int(ij[1]), int(ij[0]), 4] = 1
        target[int(ij[1]), int(ij[0]), 9] = 1
        target[int(ij[1]), int(ij[0]), int(labels[i]) + 9] = 1
        xy = ij * cell_size  # 匹配到的网格的左上角相对坐标
        delta_xy = (cxcy_sample - xy) / cell_size
        target[int(ij[1]), int(ij[0]), 2:4] = wh[i]
        target[int(ij[1]), int(ij[0]), :2] = delta_xy
        target[int(ij[1]), int(ij[0]), 7:9] = wh[i]
        target[int(ij[1]), int(ij[0]), 5:7] = delta_xy
    return target


def translate_image(images, boxes):
    new_images = []
    new_boxes = []
    images[0].transpose(2, 0, 1)
    for i in range(len(images)):
        image = cv2.resize(images[i], (224, 224))
        box = boxes[i]
        if box.shape[0] == 0:
            continue
        new_images.append(image.transpose(2, 0, 1))
        box[:, 0] = box[:, 0] - 80
        box[:, 1:] = box[:, 1:] / 640 * 224
        new_boxes.append(encoder(box[:, 1:], box[:, 0]))

    return new_images, torch.Tensor(new_boxes)


if __name__ == '__main__':
    train_data = np.load("demo_images/obj_detect_data.npz")
    loss_fun = YoloLoss()
    images, boxes = translate_image(train_data['images'], train_data['boxes'])
    cuda_available = torch.cuda.is_available()
    yolo = YOLO()
    if cuda_available:
        yolo.cuda()
    optimizer = torch.optim.Adam(yolo.parameters())
    for i in range(100):
        input = torch.autograd.Variable(torch.Tensor(images[0:2]))
        label = torch.autograd.Variable(torch.Tensor(boxes[0:2]))
        if cuda_available:
            input = input.cuda()
            label = label.cuda()
        pred = yolo(input)
        error = loss_fun(pred, label)
        optimizer.zero_grad()
        error.backward()
        optimizer.step()
        print(error)
