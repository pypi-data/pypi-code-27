# -*- coding: utf-8 -*-
from common.config_ops import load_config
from deepcrf.model import GraphDeepCRFModel
import os
import sys

merge_entity = set(["LOC", "TIME"])

def load_model():
    config_path = os.path.join(os.getcwd(), os.path.dirname(__file__), "ner.json")
    model_path = os.path.join(os.getcwd(), os.path.dirname(__file__), "ner.pb")
    config = load_config(config_path)
    config.temp_path = os.path.join(os.getcwd(), os.path.dirname(__file__), "resources")
    return GraphDeepCRFModel(model_path, config, None)
model = load_model()

def get_char_list(texts):
    docs = []
    for text in texts:
        docs.append([c for c in text])
    return docs

def analysis(texts):
    rets = model.predict(get_char_list(texts))
    for ret in rets:
        print(extract(ret))

def extract(pairs):
    words = []
    word = ""
    index = 0
    start = 0
    end = 0
    last_label = ""
    for p in pairs:
        ch = p[0]
        tag = p[1]
        if tag.startswith("B"):
            if end == index and last_label in merge_entity and tag.split("-")[1] == last_label:
                word = words[-1][0] + ch
                start = words[-1][2]
                words.remove(words[-1])
            else:
                start = index
                word = ch
        elif tag.startswith("M"):
            word += ch
        elif tag.startswith("E"):
            word += ch
            last_label = tag.split("-")[1]
            end = start + len(word)
            words.append((word, last_label, start, end))
            word = ""
        elif tag.startswith("S"):
            if end == index and last_label in merge_entity and tag.split("-")[1] == last_label:
                word = words[-1][0] + ch
                start = words[-1][2]
                end = start + 1
                last_label = tag.split("-")[1]
                words.remove(words[-1])
                words.append((word, last_label, start, end))
            else:
                last_label = tag.split("-")[1]
                end = start + 1
                words.append((ch, last_label, start, end))
            word = ""
        index += 1
    return words

