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
import time
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
        self.fa35 = FaceAligner(self.sp,desiredFaceWidth=48,desiredLeftEye=(0.27, 0.27)) 
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
        #print("load model from disk")
        return loaded_model

    def rect_dlib2opencv(self,d):
        return [d.left(),d.top(),d.right(),d.bottom()] 
    def rect_opencv2dlib(self,rect):
        return dlib.rectangle(rect[0],rect[1],rect[2],rect[3])

    def face_emotion_rect(self,image,rect):
        ts=time.time()
        happy_score=0.5
        #print rect
        d = self.rect_opencv2dlib(rect)
        #print d
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faceAligned = self.fa.align(image,gray,d)
        feature = faceAligned.reshape((48*48)) 
        X = feature.reshape((1,48,48,1))
        #print X
        score=self.model.predict(X)
        #print model.predict(X[0:3,:,:,:])
        #print score
        te=time.time()
        happy_score=score[0][0]
        return happy_score,d,te-ts
    def get_align_face(self,image):
        fal=[]
        dets=self.detector(image,1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for k,d in enumerate(dets):
            faceAligned = self.fa35.align(image, gray, d)
            fal.append(faceAligned)
        return fal
    def face_emotion(self,image):
        ts=time.time()
        sl=[]
        dl=[]
        dets=self.detector(image,1)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        for k,d in enumerate(dets):
            #print d
            #print d.top()
            #print d.left()
            #print d.bottom()
            #print d.right()
            #rect = d
            rect_tmp=[d.left(),d.top(),d.right(),d.bottom()] 
            #dtmp =dlib.rectangle(rect_tmp[0],rect_tmp[1],rect_tmp[2],rect_tmp[3])
            #print dtmp
            #print dtmp.right()
            #faceAligned = self.fa.align(image, gray, rect)
            #feature = faceAligned.reshape((48*48)) 
            ##gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            #X = feature.reshape((1,48,48,1))
            ##print X
            #score=self.model.predict(X)
            score,tc,d=self.face_emotion_rect(image,rect_tmp)
            #print model.predict(X[0:3,:,:,:])
            #print score
            sl.append(score)
            dl.append(d)
        te=time.time()
        return sl,dl,te-ts
    def face_emotion_flat(self,image):
        ts=time.time()
        flag=str(False)
        d=None
        sl,dl,tc=self.face_emotion(image)
        for i in range(0,len(sl)):
            if sl[i]>0.5:
                 flag=str(True)
                 d=dl[i]
                 break
                 #print flag
            #else:
                 #print flag
        te=time.time()
        return flag,d,te-ts

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
        print(fs.face_emotion_rect(image,[91,91,180,181]))

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
    #dirname='/data1/mingmingzhao/data_sets/face_emotion_data/neutral_images_all/origin_images/'
    dirname1='/data1/mingmingzhao/data_sets/face_emotion_data/neutral_images_all/origin_images_api_result/'
   
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
        print(fs.face_emotion_flat(image))
        score,rect,tc=fs.face_emotion(image)
        if len(score):
            if score[0]:
                print score
                print os.path.join(dirname1,f)
                print cv2.imwrite(os.path.join(dirname1,str(score[0])+f),image)
