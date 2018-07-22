from torchvision.models import vgg16
import torch.nn as nn
import torch


class YOLO(torch.nn.Module):
    def __init__(self):
        super(YOLO, self).__init__()
        self.model = vgg16(True)

        # model = vgg16()
        self.model.classifier = nn.Sequential(
            nn.Linear(512 * 7 * 7, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 4096),
            nn.ReLU(True),
            nn.Dropout(),
            nn.Linear(4096, 1470),
        )

    def forward(self, x):
        x = self.model.features(x)
        x = x.view(x.size(0), -1)
        x = self.model.classifier(x)
        x = x.view(-1, 7, 7, 30)
        return x
