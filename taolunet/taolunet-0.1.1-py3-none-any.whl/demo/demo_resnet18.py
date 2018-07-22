import torch
import json
from taolu.vision.jobs.classification import ClassificationJob
from taolu.demo.demo_base import DemoBase

if __name__ == '__main__':
    demo = DemoBase("../vision/base_nets/resnet18.json", "classification")
    demo.go()
