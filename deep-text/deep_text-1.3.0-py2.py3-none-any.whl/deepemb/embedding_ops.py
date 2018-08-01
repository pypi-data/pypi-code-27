# -*- coding=utf-8 -*-
from deeplm import GraphDeepLMModel
from common.config_ops import load_deep_lm_config


def load_lm_char_layer():
    config = load_deep_lm_config("lm_char_model/lm_config.json")
    model = GraphDeepLMModel("lm_char_model/lm-114000.pb", config)
    return model


model = load_lm_char_layer()
text = ["距离拼多多纳斯达克上市还有不到12个小时"]
ret = model.fluency(text)
print(ret)
