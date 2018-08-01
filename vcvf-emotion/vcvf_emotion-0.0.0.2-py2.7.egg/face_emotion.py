# Create first network with keras
from keras.models import Sequential
from keras.layers import Dense
from sklearn.cross_validation import train_test_split
import numpy
from keras.models import model_from_json
from keras.models import Sequential
from keras.layers import Dense
from keras.callbacks import ModelCheckpoint
import numpy as np
from keras import layers
from keras.layers import Input, Dense, Activation, ZeroPadding2D, BatchNormalization, Flatten, Conv2D
from keras.layers import AveragePooling2D, MaxPooling2D, Dropout, GlobalMaxPooling2D, GlobalAveragePooling2D
from keras.models import Model
from keras.preprocessing import image
from keras.utils import layer_utils
from keras.utils.data_utils import get_file
from keras.applications.imagenet_utils import preprocess_input
import matplotlib.pyplot as plt
import numpy
#from load_image_data import get_emotion_data
import sys
import os
import dlib
import glob
try:
    import cPickle as pickle
except ImportError:
    import pickle
import random
import cv2
import datetime as dt
import time
import shutil
import numpy as np
import cv2
import os
from distutils.sysconfig import get_python_lib
import time as tm
from face_utils.facealigner import FaceAligner

'''
class FaceSpecial:
    def __init__(self):
        basedir="./race_models/"
        c2 = open(basedir+'classifier.pickle','rb')
        self.predictor_path = basedir+'shape_predictor_5_face_landmarks.dat'
        self.face_rec_model_path = basedir+'dlib_face_recognition_resnet_model_v1.dat'
        self.classifier=pickle.load(c2)
        self.site_package=get_python_lib()
        self.detector = dlib.get_frontal_face_detector()
        self.sp = dlib.shape_predictor(self.predictor_path)
        self.facerec = dlib.face_recognition_model_v1(self.face_rec_model_path)

    def face_special_from_rect(self,img,dets):
        #dets=detector(img,1)
        yl=[]
        for d in enumerate(dets):
            shape=self.sp(img,d)
            face_descriptor = self.facerec.compute_face_descriptor(img, shape)
            x=face_descriptor
            y_=classifier(x)
            yl.append(y_)
        return yl,shape
    def face_special(self,img):
        dets=self.detector(img,1)
        yl=[]
        for k,d in enumerate(dets):
            print d
            shape=self.sp(img,d)
'''

class face_emotion:
    
    def __init__(self):
        #basedir="./race_models/"
        #basedir="./"
        self.site_package=get_python_lib()
        protofilename=os.path.join(self.site_package,'vcvf_emotion/models/happymodle.json')
        weightfilename=os.path.join(self.site_package,'vcvf_emotion/models/weights.best.hdf5')
        self.model=self.loadmodel(protofilename,weightfilename)
        self.model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
        #self.predictor_path = basedir+'shape_predictor_68_face_landmarks.dat'
        self.predictor_path="landmarks_68.dat"
        url='http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
        self.predictor_path=self.get_model(url,self.predictor_path) 

        self.sp = dlib.shape_predictor(self.predictor_path)
        self.fa = FaceAligner(self.sp,desiredFaceWidth=48) 
        self.detector = dlib.get_frontal_face_detector()
    def get_model(self,url,predictor_path):
        #predictor_path="landmarks_68.dat"
        #url='http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2'
        if not os.path.exists(predictor_path):
            print os.path.exists("%s.bz2"%(predictor_path))
            if not os.path.exists("%s.bz2"%(predictor_path)):
                os.system('wget -O %s.bz2 %s'%(predictor_path,url))   
            os.system('bunzip2 %s.bz2'%(predictor_path))   
        return predictor_path
    

    def loadmodel(self,protofilename,weightfilename):
        yaml_file = open(protofilename, 'r')
        loaded_model_yaml = yaml_file.read()
        yaml_file.close()
        loaded_model = model_from_json(loaded_model_yaml)
        loaded_model.load_weights(weightfilename)
        print("load model from disk")
        return loaded_model

    
    def face_emotion(self,image,rect):
        sl=[]
        dets=self.detector(image,1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for k,d in enumerate(dets):
            print d
            rect = d
            faceAligned = self.fa.align(image, gray, rect)
            feature = faceAligned.reshape((48*48)) 
            #gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            X = feature.reshape((1,48,48,1))
            score=self.model.predict(X)
            #print model.predict(X[0:3,:,:,:])
            print score
            sl.append(score)
        return sl
    def face_emotion_flat(self,image,rect):
        flag=str(False)
        sl=self.face_emotion(image,rect)
        if len(sl)>0:
            if sl[0]>0.5:
                 flag=str(True)
                 print flag
            else:
                 print flag
        return flag

#model = loadmodel("happymodle.json","weights.best.hdf5")
#model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
##loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
#score = model.evaluate(X, Y, verbose=0)
#print "%s: %.2f%%" % (model.metrics_names[1], score[1]*100)
#print X.shape
#print model.predict(X[0:3,:,:,:])
    def test(self):
        fs=face_emotion()
        imf=os.path.join(self.site_package,'vcvf_emotion/test.jpg')
        #imf="test.jpg"
        print(imf)
        image=cv2.imread(imf)
        print(fd.face_emotion(image))

def log2(message,of):
    print(message)
    of.write(message)
def draw_rect(img,savepath,left,top,right,bottom):
    cv2.rectangle(img, (int(left), int(top)), (int(right), int(bottom)), (0, 255, 0), 3)
    #cv2.imwrite(resultsavedir+filename_old,img)
    cv2.imwrite(savepath,img)
    return img

if __name__=="__main__":
    dirname='/data1/mingmingzhao/data_sets/hand_data/test_images/'
    dirname='/data1/mingmingzhao/data_sets/face_emotion_data/neutral_images_all/origin_images/'
    #dirname='/data1/mingmingzhao/data_sets/hand_test_0614_child_1/'
    #dirname='/data1/mingmingzhao/data_sets/no_hand_data/'
    #sess,dg,ci=init()
    #hd3=HandDetector3(int(sys.argv[1]))
    fs=face_emotion()
    #fs.test()
    ci=0 # the count of image
    ch=0 # the count of hand
    ts=0 # avg of time cost
    for f in os.listdir(dirname):
       if f.endswith('.jpg'):
        imf=os.path.join(dirname,f)
        print(imf)
        image=cv2.imread(imf)
        rect=[]
        #sl=fs.face_emotion(image,rect)
        #if len(sl)>0:
        #    if sl[0]>0.5:
        #         print str(True)
        #    else:
        #         print str(False) 
        #print(fs.face_emotion(image,rect))
        print(fs.face_emotion_flat(image,rect))
