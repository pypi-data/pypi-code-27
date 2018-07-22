import torch


class ResBlock1(torch.nn.Module):
    def __init__(self, input_channels, output_channels, stride=1, downsample=False):
        super(ResBlock1, self).__init__()
        self.conv1 = torch.nn.Conv2d(input_channels, output_channels, 3, bias=False, padding=1, stride=stride)
        self.bn1 = torch.nn.BatchNorm2d(output_channels)
        self.relu = torch.nn.ReLU(inplace=True)
        self.conv2 = torch.nn.Conv2d(output_channels, output_channels, 3, bias=False, padding=1)
        self.bn2 = torch.nn.BatchNorm2d(output_channels)
        self.downsample = torch.nn.Sequential(
            torch.nn.Conv2d(input_channels, output_channels, kernel_size=1, stride=stride, bias=False),
            torch.nn.BatchNorm2d(output_channels)) if downsample else None
        self.stride = stride

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        if self.downsample is not None:
            residual = self.downsample(x)
        out += residual
        out = self.relu(out)
        return out


class ResBlock2(torch.nn.Module):
    def __init__(self, input_channels, start_input_channels, stride=1, downsample=False):
        super(ResBlock2, self).__init__()
        self.conv1 = torch.nn.Conv2d(input_channels, start_input_channels, kernel_size=1, bias=False)
        self.bn1 = torch.nn.BatchNorm2d(start_input_channels)
        self.conv2 = torch.nn.Conv2d(start_input_channels, start_input_channels, kernel_size=3, stride=stride,
                                     padding=1, bias=False)
        self.bn2 = torch.nn.BatchNorm2d(start_input_channels)
        self.conv3 = torch.nn.Conv2d(start_input_channels, start_input_channels * 4, kernel_size=1, bias=False)
        self.bn3 = torch.nn.BatchNorm2d(start_input_channels * 4)
        self.relu = torch.nn.ReLU(inplace=True)
        self.downsample = torch.nn.Sequential(
            torch.nn.Conv2d(input_channels, start_input_channels * 4, kernel_size=1, stride=stride, bias=False),
            torch.nn.BatchNorm2d(start_input_channels * 4)) if downsample else None
        self.stride = stride

    def forward(self, x):
        residual = x
        out = self.conv1(x)
        out = self.bn1(out)
        out = self.relu(out)
        out = self.conv2(out)
        out = self.bn2(out)
        out = self.relu(out)
        out = self.conv3(out)
        out = self.bn3(out)
        if self.downsample is not None:
            residual = self.downsample(x)
        out += residual
        out = self.relu(out)
        return out
