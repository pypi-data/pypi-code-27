class PredictBase():
    '''预测基类
    '''

    def initialize(self):
        '''初始化
        例如：重载PaiFlow.load_model方法
        '''
        pass

    def predict(self, model, to_predict_data) -> object:
        '''预测模型
        参数:
            model: 模型
            to_predict_data: 要预测的数据，list的list列表
        返回值:
            预测结果
        '''
        pass
