import os
import pickle
from .info_model import InfoModel


class PaiFlow:
    @staticmethod
    def deploy(model: object, info: InfoModel):
        '''发布模型
        参数:
            model: 训练好的模型
            info: 信息
        '''
        pickle.dumps(model)

    @staticmethod
    def is_debug():
        return os.getenv('PAIFLOW_RUN') != '1'
