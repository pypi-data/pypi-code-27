import numpy as np
import platform
import os
from scipy import misc


def load(target_size):
    X = []
    y = []
    plat = platform.platform()
    if "Windows" in plat:
        base_path = "F:/101_ObjectCategories/"
    else:
        base_path = "/Users/weizuo/Downloads/101_ObjectCategories/"
    labels = {}
    cates = os.listdir(base_path)
    for cate in cates[0:2]:
        if ".DS_Store" in cate:
            continue
        if cate in labels:
            index = labels[cate]
        else:
            index = len(labels)
            labels[cate] = index
        label_y = np.zeros(101)
        label_y[index] = 1
        images_dir = os.path.join(base_path, cate)
        for image_file in os.listdir(images_dir):
            image_data = misc.imread(os.path.join(images_dir, image_file))
            image_data = np.resize(image_data, (3, target_size[0],target_size[1]))
            X.append(image_data)
            y.append(label_y)
    return np.array(X[0:6]), np.array(y[0:6])
