import torch
import torch.nn.functional as F
from taolu.vision.vision_units.base_unit import BaseUnits
from taolu.vision.vision_units.losses.yolo_loss import YoloLoss
from taolu.vision.vision_units.losses.mse import MSELoss
from taolu.vision.vision_units.losses.cross_entropy_loss import CrossEntropyLoss
from taolu.vision.vision_units.res_block import ResBlock1, ResBlock2
import taolu.vision.utils.transformers as transformers
import math
import inspect
import json
import os

activation_map = {
    "relu": torch.nn.ReLU(inplace=True),
    "softmax": torch.nn.Softmax()
}

loss_map = {
    "cross_entropy": CrossEntropyLoss,
    "mse": MSELoss,
    "yolo_loss": YoloLoss
}

transformer_map = {
    "cross_entropy_transformer": transformers.cross_entropy_transformer.CrossEntropyTransformer,
    "yolo_loss_transformer": transformers.yolo_transformer.YOLOTransformer,
    "mse_transformer": transformers.mse_transformer.MSETransformer
}


def parse_resblock1(layer, input_shape):
    downsample = layer.get("downsample", False)
    stride = layer.get("stride", 1)
    filters = layer["filters"]
    out_channels = filters
    output_size = int(input_shape[0] / 2) if downsample else input_shape[0]
    output_shape = (output_size, output_size, out_channels)
    unit = BaseUnits(layer['type'])
    resblock = ResBlock1(input_shape[2], out_channels, stride=stride, downsample=downsample)
    unit.seq = resblock
    unit.output_shape = output_shape
    return unit, output_shape


def parse_resblock2(layer, input_shape):
    downsample = layer.get("downsample", False)
    stride = layer.get("stride", 1)
    start_input_channels = layer.get("start_input_channels", int(input_shape[2] / 4))
    output_size = int(input_shape[0] / 2) if downsample else input_shape[0]
    output_shape = (output_size, output_size, start_input_channels * 4)
    unit = BaseUnits(layer['type'])
    resblock = ResBlock2(input_shape[2], start_input_channels, stride=stride, downsample=downsample)
    unit.seq = resblock
    unit.output_shape = output_shape
    return unit, output_shape


def parse_avgpool(layer, input_shape):
    unit = BaseUnits(layer['type'])
    size = layer['size']
    stride = layer.get('stride', 2)
    padding = layer.get("padding", 0)
    output_size = (input_shape[0] - size + 2 * padding) / stride + 1
    output_shape = (output_size, output_size, input_shape[2])
    unit.seq = torch.nn.Sequential(torch.nn.AvgPool2d(size, stride, padding=padding))
    unit.output_shape = output_shape
    return unit, output_shape


def parse_conv2d(layer, input_shape):
    unit_seq = []
    unit = BaseUnits(layer['type'])
    out_channels = layer['filters']
    kernel_size = layer['size']
    stride = layer.get('stride', 1)
    padding = layer.get('padding', 0)
    bias = layer.get("bias", True)
    batch_norm = layer.get('bn', False)
    activation = layer.get('activation', 'relu')
    output_size = (input_shape[0] - kernel_size + 2 * padding) / stride + 1
    output_shape = (output_size, output_size, out_channels)
    unit_seq.append(torch.nn.Conv2d(input_shape[2], out_channels, kernel_size, stride, padding, bias=bias))
    if batch_norm:
        unit_seq.append(torch.nn.BatchNorm2d(output_shape[2]))
    if activation:
        unit_seq.append((activation_map[activation]))
    unit.output_shape = output_shape
    unit.seq = torch.nn.Sequential(*unit_seq)
    return unit, output_shape


def parse_maxpool(layer, input_shape):
    unit = BaseUnits(layer['type'])
    size = layer['size']
    stride = layer.get('stride', 2)
    padding = layer.get("padding", 0)
    output_size = (input_shape[0] - size + 2 * padding) / stride + 1
    output_shape = (output_size, output_size, input_shape[2])
    unit.seq = torch.nn.Sequential(torch.nn.MaxPool2d(size, stride, padding=padding))
    unit.output_shape = output_shape
    return unit, output_shape


def parse_globalavgpool(layer, input_shape):
    unit = BaseUnits(layer['type'])
    unit.seq = torch.nn.Sequential(torch.nn.AvgPool2d(input_shape[0]))
    output_shape = (1, 1, input_shape[2])
    unit.output_shape = output_shape
    return unit, output_shape


def parse_linear(layer, input_shape):
    unit_seq = []
    unit = BaseUnits(layer['type'])
    output = layer['output']
    activation = layer.get('activation', 'relu')
    output_shape = (1, 1, output)
    unit_seq.append(torch.nn.Linear(input_shape[2] * input_shape[0] * input_shape[1], output))
    unit.output_shape = output_shape
    if activation:
        unit_seq.append((activation_map[activation]))
    unit.seq = torch.nn.Sequential(*unit_seq)
    return unit, output_shape


def parse_dropout(layer, input_shape):
    unit = BaseUnits(layer['type'])
    rate = layer.get("rate", 0.5)
    unit.seq = torch.nn.Sequential(torch.nn.Dropout2d(rate))
    unit.output_shape = input_shape
    return unit, input_shape


def parse_optim(optim_cfg, parameters):
    optim_type = optim_cfg.get('optim', 'adam')
    optim_type = optim_type.lower()
    optim = list(filter(lambda x: type(x) is tuple and inspect.isclass(x[1]) and x[1].__name__.lower() == optim_type,
                        inspect.getmembers(torch.optim)))
    if len(optim) > 0:
        return optim[0][1](parameters)
    return torch.optim.Adam(parameters)


def parse_backbone(backbone_cfg, input_shape):
    backbone_net_name = backbone_cfg['name']
    backbone_origin_cfg = json.load(open(os.path.join(os.path.dirname(__file__), backbone_net_name + ".json")))
    backbone_origin_layers_cfg = backbone_origin_cfg['layers']
    remove_indexes = backbone_cfg.get("remove", [0, 0])
    remove_indexes[0] = len(backbone_origin_layers_cfg) + remove_indexes[0] if remove_indexes[0] < 0 else \
        remove_indexes[0]
    remove_indexes[1] = len(backbone_origin_layers_cfg) + remove_indexes[1] if remove_indexes[1] < 0 else \
        remove_indexes[1]
    remove_indexes = list(sorted(remove_indexes))

    del backbone_origin_layers_cfg[remove_indexes[0]:remove_indexes[1] + 1]
    seq, output_shape = parse_layers(backbone_origin_layers_cfg, input_shape)
    unit = BaseUnits(backbone_cfg['type'])
    unit.seq = torch.nn.Sequential(*seq)
    unit.output_shape = output_shape
    return unit, output_shape


def parse_layers(layers_cfg, output_shape):
    seq = []
    for layer in layers_cfg:
        layer_type = layer['type']
        unit, output_shape = eval("parse_" + layer_type + "(layer,output_shape)")
        seq.append(unit)
    return seq, seq[-1].output_shape


class BaseNet(torch.nn.Module):
    def __init__(self, cfg):
        self.loss = None
        super(BaseNet, self).__init__()
        self.seq = []
        in_channels = cfg.get("channels", 3)
        width = cfg['width']
        height = cfg['height']
        output_shape = (height, width, in_channels)
        seq, output_shape = parse_layers(cfg['layers'], output_shape)
        self.seq.extend(seq)
        loss_name = cfg.get("loss", "mse")
        self.loss = loss_map[loss_name](cfg)
        self.seq = torch.nn.Sequential(*self.seq)
        self.optim = parse_optim(cfg, self.seq.parameters())
        self.transformer = transformer_map[loss_name + "_transformer"](cfg)
        self.init_weights()

    def init_weights(self):
        for m in self.seq.modules():
            if isinstance(m, torch.nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2. / n))
            elif isinstance(m, torch.nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def forward(self, x):
        last_unit = None
        for i, unit in enumerate(self.seq.children()):
            if "linear" in unit.type:
                if i > 0 and last_unit.type != "linear":
                    x = x.view(x.size(0), -1)
            x = unit(x)
            last_unit = unit
        x = torch.nn.functional.softmax(x, 1)
        return x

    def cuda(self, device=None):
        self.seq.cuda(device)
        return self

    def cpu(self):
        self.seq.cpu()
        return self
