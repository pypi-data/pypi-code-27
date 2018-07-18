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
        PaiFlow.save_model(model)

    @staticmethod
    def save_model(model: object):
        '''保存模型
        参数:
            model: 训练好的模型
        '''
        pickle.dumps(model)

    @staticmethod
    def load_model() -> object:
        '''读取模型'''
        pass

    @staticmethod
    def is_debug():
        '''是否调试模式'''
        return os.getenv('PAIFLOW_RUN') != '1'
