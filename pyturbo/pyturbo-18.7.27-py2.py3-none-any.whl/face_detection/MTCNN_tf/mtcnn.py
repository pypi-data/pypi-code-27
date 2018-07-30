from pyturbo.face_detection.MTCNN_tf import detect_face
import tensorflow as tf
from pyturbo.face_detection.MTCNN_tf.detect_face import PNet, RNet, ONet
import os
import numpy as np
import cv2





class MTCNN:
    minsize = 20
    factor = 0.709
    threshold = [0.6, 0.7, 0.7]

    def __init__(self, model_path, model_names):
        with tf.Graph().as_default():
            sess = tf.Session()
            with sess.as_default():
                with tf.variable_scope('pnet'):
                    data = tf.placeholder(tf.float32, (None, None, None, 3), 'inputs')
                    pnet = PNet({'data': data})
                    pnet.load(os.path.join(model_path, model_names[0]), sess)
                with tf.variable_scope('rnet'):
                    data = tf.placeholder(tf.float32, (None, 24, 24, 3), 'inputs')
                    rnet = RNet({'data': data})
                    rnet.load(os.path.join(model_path, model_names[1]), sess)
                with tf.variable_scope('onet'):
                    data = tf.placeholder(tf.float32, (None, 48, 48, 3), 'inputs')
                    onet = ONet({'data': data})
                    onet.load(os.path.join(model_path, model_names[2]), sess)

                self.pnet, self.rnet, self.onet = detect_face.create_mtcnn(sess)


    def detect_faces(self, image):
        img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if img_gray.ndim == 2:
            img = self.gray2rgb(img_gray)

        bboxes, points = \
        detect_face.detect_face(img, self.minsize, self.pnet, self.rnet, self.onet,
                                self.threshold, self.factor)
        return bboxes, points


    def gray2rgb(self, img):
        h, w = img.shape
        ret = np.empty((h, w, 3), dtype=np.uint8)
        ret[:, :, 0] = ret[:, :, 1] = ret[:, :, 2] = img
        return ret
