from __future__ import print_function

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

import numpy as np
import tables
import matplotlib.pyplot as plt

from faster_particles.larcvdata.larcvdata_generator import LarcvGenerator
from faster_particles.demo_ppn import get_filelist

# Accelerate *if all input sizes are same*
torch.backends.cudnn.benchmark = True

def get_conv(is_3d):
    if is_3d:
        return nn.Conv3d, nn.ConvTranspose3d, nn.BatchNorm3d
    else:
        return nn.Conv2d, nn.ConvTranspose2d, nn.BatchNorm2d

def padding(kernel, stride, input_size):
    if input_size[-1] % stride == 0:
        p = max(kernel - stride, 0)
    else:
        p = max(kernel - (input_size[-1] % stride), 0)
    p1 = p // 2
    p2 = p - p1
    return (p1, p2,) * (len(input_size) - 2)


class ResNetModule(nn.Module):
    def __init__(self, is_3d, num_inputs, num_outputs, kernel=3, stride=1):
        super(ResNetModule, self).__init__()
        self.fn_conv, self.fn_conv_transpose, self.batch_norm = get_conv(is_3d)
        self.kernel, self.stride = kernel, stride

        # Shortcut path
        self.use_shortcut = (num_outputs != num_inputs or stride != 1)
        self.shortcut = self.fn_conv(
            in_channels = num_inputs,
            out_channels = num_outputs,
            kernel_size = 1,
            stride      = stride,
            padding     = 0
        )
        self.shortcut_bn = self.batch_norm(num_features = num_outputs)

        # residual path
        self.residual1 = self.fn_conv(
            in_channels = num_inputs,
            out_channels = num_outputs,
            kernel_size = kernel,
            stride      = stride,
            padding     = 0
        )
        self.residual1_bn = self.batch_norm(num_features = num_outputs)

        self.residual2 = self.fn_conv(
            in_channels = num_outputs,
            out_channels = num_outputs,
            kernel_size = kernel,
            stride      = 1,
            padding     = 0
        )
        self.residual2_bn = self.batch_norm(num_features = num_outputs)

    def forward(self, input_tensor):
        if not self.use_shortcut:
            shortcut = input_tensor
        else:
            shortcut = F.pad(input_tensor, padding(self.shortcut.kernel_size[0], self.shortcut.stride[0], input_tensor.size()), mode='replicate')
            shortcut = self.shortcut(shortcut)
            shortcut = self.shortcut_bn(shortcut)
	# FIXME padding value
	residual = F.pad(input_tensor, padding(self.residual1.kernel_size[0], self.residual1.stride[0], input_tensor.size()), mode='replicate')
        residual = self.residual1(residual)
        residual = self.residual1_bn(residual)
        residual = F.pad(residual, padding(self.residual2.kernel_size[0], self.residual2.stride[0], residual.size()), mode='replicate')
        residual = self.residual2(residual)
        residual = self.residual2_bn(residual)
        return F.relu(shortcut + residual)


class DoubleResnet(nn.Module):
    def __init__(self, is_3d, num_inputs, num_outputs, kernel=3, stride=1):
        super(DoubleResnet, self).__init__()

        self.resnet1 = ResNetModule(
            is_3d = is_3d,
            num_inputs = num_inputs,
            num_outputs = num_outputs,
            kernel = kernel,
            stride = stride
        )
        self.resnet2 = ResNetModule(
            is_3d = is_3d,
            num_inputs = num_outputs,
            num_outputs = num_outputs,
            kernel = kernel,
            stride = 1
        )

    def forward(self, input_tensor):
        resnet = self.resnet1(input_tensor)
        resnet = self.resnet2(resnet)
        return resnet


class UResNet(nn.Module):
    def __init__(self, is_3d, num_inputs=1, num_strides=3, base_num_outputs=16, num_classes=3):
        super(UResNet, self).__init__()
        # Parameters
        self.fn_conv, self.fn_conv_transpose, self.batch_norm = get_conv(is_3d)
        self.is_3d = is_3d
        self.conv_feature_map = {}
        self.base_num_outputs = base_num_outputs
        self._num_strides = num_strides
        self.num_inputs = num_inputs  # number of channels of input image
        self.num_classes = num_classes

        # Define layers
        self.conv1 = self.fn_conv(
            in_channels = self.num_inputs,
            out_channels = self.base_num_outputs,
            kernel_size = 7,
            stride = 1,
            padding = 0 # FIXME 'same' in tensorflow
        )
        self.conv1_bn = self.batch_norm(num_features=self.base_num_outputs)

        # Encoding steps
        self.double_resnet = nn.ModuleList()
        current_num_outputs = self.base_num_outputs
        for step in xrange(self._num_strides):
            self.double_resnet.append(DoubleResnet(
                is_3d = self.is_3d,
                num_inputs = current_num_outputs,
                num_outputs = current_num_outputs * 2,
                kernel = 3,
                stride = 2
            ))
            current_num_outputs *= 2

        # Decoding steps
        self.decode_conv = nn.ModuleList()
        self.decode_conv_bn = nn.ModuleList()
        self.decode_double_resnet = nn.ModuleList()
        for step in xrange(self._num_strides):
            self.decode_conv.append(self.fn_conv_transpose(
                in_channels = current_num_outputs,
                out_channels = current_num_outputs / 2,
                kernel_size = 3,
                stride = 2,
                padding=1,
                output_padding=1
            ))
            self.decode_conv_bn.append(self.batch_norm(num_features=current_num_outputs / 2))
            self.decode_double_resnet.append(DoubleResnet(
                is_3d = self.is_3d,
                num_inputs = current_num_outputs,
                num_outputs = current_num_outputs / 2,
                kernel = 3,
                stride = 1
            ))
            current_num_outputs /= 2

        self.conv2 = self.fn_conv(
            in_channels = current_num_outputs,
            out_channels = self.base_num_outputs,
            padding = 0,
            kernel_size = 7,
            stride = 1
        )
        self.conv2_bn = self.batch_norm(num_features=current_num_outputs)
        self.conv3 = self.fn_conv(
            in_channels = self.base_num_outputs,
            out_channels = self.num_classes,
            padding = 0,
            kernel_size = 3,
            stride = 1
        )
        self.conv3_bn = self.batch_norm(num_features=self.num_classes)

    def forward(self, input):
        net = F.pad(input, padding(self.conv1.kernel_size[0], self.conv1.stride[0], input.size()), mode='replicate')
        net = F.relu(self.conv1_bn(self.conv1(net)))
        self.conv_feature_map[net.size()[1]] = net
        # Encoding steps
        for step in xrange(self._num_strides):
            net = self.double_resnet[step](net)
            self.conv_feature_map[net.size()[1]] = net
        # Decoding steps
        for step in xrange(self._num_strides):
            num_outputs = net.size()[1] / 2
            decode_layer = self.decode_conv[step]
            net = F.relu(self.decode_conv_bn[step](decode_layer(net)))
            net = torch.cat((net, self.conv_feature_map[net.size()[1]]), dim=1)
            net = self.decode_double_resnet[step](net)
        # Final conv layers
        net = F.pad(net, padding(self.conv2.kernel_size[0], self.conv2.stride[0], net.size()), mode='replicate')
        net = F.relu(self.conv2_bn(self.conv2(net)))
        net = F.pad(net, padding(self.conv3.kernel_size[0], self.conv3.stride[0], net.size()), mode='replicate')
        net = self.conv3_bn(self.conv3(net))
        return net

def dataloader_hdf5(i, f, N=192, batch_size=1):
    num_img = len(f.root.data)
    print("loading data ", i)
    i = i % num_img
    data = f.root.data[i].reshape((batch_size, 1, N, N, N))
    label = f.root.label[i].astype(int).reshape((batch_size, N, N, N))
    return torch.from_numpy(data).cuda(), torch.from_numpy(label).cuda()

def train_uresnet(cfg):
    cuda = torch.device("cuda:0")
    net = UResNet(cfg.DATA_3D).cuda()
    print(net)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(net.parameters(), lr=cfg.LEARNING_RATE)
    generator = LarcvGenerator(cfg, ioname="train", filelist=get_filelist(cfg.DATA))

    for i in range(cfg.MAX_STEPS): # use with torch.no_grad() for test network
        #inputs, label = dataloader(i)
        blob = generator.forward()
        
        print("step ", i)
        optimizer.zero_grad()
        predictions = net(inputs)
        loss = criterion(predictions, label)
        loss.backward()
        optimizer.step()

        print(loss.item())

if __name__ == '__main__':
    class MyCfg:
        IMAGE_SIZE = 192
        BATCH_SIZE = 1


    train_uresnet(MyCfg())

    #f = tables.open_file('sample3d.hdf5','r')
    #f.close()
