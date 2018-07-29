import logging

import numpy as np
import torch.nn
import torch.nn.functional

models_logger = logging.getLogger("thelper.models")


class BaseModel(torch.nn.Module):
    """
    Base class for all models
    """

    def __init__(self,config):
        super(BaseModel,self).__init__()
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    def forward(self,*input):
        """
        Forward pass logic

        :return: Model output
        """
        raise NotImplementedError

    def summary(self):
        """
        Model summary
        """
        model_parameters = filter(lambda p:p.requires_grad,self.parameters())
        params = sum([np.prod(p.size()) for p in model_parameters])
        self.logger.info('Trainable parameters: {}'.format(params))
        self.logger.info(self)


class ExampleModel(BaseModel):
    def __init__(self,config):
        super().__init__(config)
        self.config = config
        self.conv1 = torch.nn.Conv2d(1,10,kernel_size=5)
        self.conv2 = torch.nn.Conv2d(10,20,kernel_size=5)
        self.conv2_drop = torch.nn.Dropout2d()
        self.fc1 = torch.nn.Linear(320,50)
        self.fc2 = torch.nn.Linear(50,10)

    def forward(self,x):
        F = torch.nn.functional
        x = F.relu(F.max_pool2d(self.conv1(x),2))
        x = F.relu(F.max_pool2d(self.conv2_drop(self.conv2(x)),2))
        x = x.view(-1,320)
        x = F.relu(self.fc1(x))
        x = F.dropout(x,training=self.training)
        x = self.fc2(x)
        return F.log_softmax(x,dim=1)
