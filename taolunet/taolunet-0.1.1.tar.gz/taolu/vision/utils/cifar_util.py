import pickle
import numpy as np
import platform


def _load_batch(images):
    X = []
    y = []
    for image in images[b'data'][0:5]:
        r = image[:1024].reshape(32, 32)
        g = image[1024:2048].reshape(32, 32)
        b = image[2048:].reshape(32, 32)
        r = np.resize(r, (224, 224))
        g = np.resize(g, (224, 224))
        b = np.resize(b, (224, 224))
        X.append(np.array([r, g, b]))
    for label in images[b'labels'][0:5]:
        label_y = np.zeros(10)
        label_y[label] = 1
        y.append(label_y)
    return X, y


def load(batch_size=25):
    train_X = []
    train_y = []
    base_path = ""
    plat = platform.platform()
    if "Windows" in plat:
        base_path = "F:/cifar-10-batches-py/"
    else:
        base_path = "/Users/weizuo/Downloads/cifar-10-batches-py/"
    for i in range(1, 6):
        images = pickle.load(open(base_path + "data_batch_" + str(i), "rb"),
                             encoding="bytes")
        X, y = _load_batch(images)
        train_X.extend(X)
        train_y.extend(y)

    images = pickle.load(open(base_path + "test_batch", "rb"), encoding="bytes")
    test_X, test_y = _load_batch(images)

    return np.split(np.array(train_X), 25 / batch_size), \
           np.split(np.array(train_y), 25 / batch_size), \
           np.split(np.array(test_X), 25 / batch_size), \
           np.split(np.array(test_y), 25 / batch_size)
