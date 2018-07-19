import os
import pickle
from .info_model import InfoModel


class PaiFlow:

    @staticmethod
    def get_model_folder():
        folder = os.path.expanduser('~/paiflow_models')
        if not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

    @staticmethod
    def deploy(model: object, info: InfoModel):
        '''发布模型
        参数:
            model: 训练好的模型
            info: 信息
        '''
        PaiFlow.save_model(model, PaiFlow.get_model_folder())

    @staticmethod
    def save_model(model: object, folder: str):
        '''保存模型
        参数:
            model: 训练好的模型,
            folder: 保存的目录
        '''
        pickle.dumps(model)

    @staticmethod
    def load_model(folder: str) -> object:
        '''读取模型
        参数:
            folder: 获取模型的目录
        '''
        pass

    @staticmethod
    def is_debug():
        '''是否调试模式'''
        return os.getenv('PAIFLOW_RUN') != '1'
