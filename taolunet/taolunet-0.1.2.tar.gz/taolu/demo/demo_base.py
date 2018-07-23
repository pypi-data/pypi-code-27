import torch
import json
from taolu.vision.jobs.classification import ClassificationJob
from taolu.vision.jobs.object_detection import ObjectDetectionJob
from taolu.vision.utils.cal101_util import load
import numpy as np


class DemoBase:
    def __init__(self, cfg_file, job_type):
        self.cfg = json.load(open(cfg_file))
        self.job_type = job_type
        cuda_available = torch.cuda.is_available()
        if job_type == "classification":
            self.job = ClassificationJob(self.cfg, cuda=cuda_available)
            self.train_X, self.train_y = load((self.job.cfg["width"], self.job.cfg['height']))
        else:
            self.job = ObjectDetectionJob(self.cfg, cuda=cuda_available)
            train_data = np.load("demo_images/obj_detect_data.npz")
            self.train_X = train_data['images'][0:2]
            self.train_y = train_data['boxes'][0:2]

    def go(self):
        for epoch in range(100):
            error = self.job.train(self.train_X, self.train_y)
            print(error)
