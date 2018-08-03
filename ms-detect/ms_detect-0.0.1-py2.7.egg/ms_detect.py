import cognitive_face as CF
import json
import numpy as np
def ms_face_detect(img_url):
    #KEY = 'subscription key'  # Replace with a valid Subscription Key here.
    #KEY = '74bc910571cd4785991d003b30c2a783'
    KEY = '6a78402ab44140aba9e2014e0c7263ea'
    CF.Key.set(KEY)
    #https://eastasia.api.cognitive.microsoft.com/face/v1.0
    #BASE_URL = 'https://westus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL
    BASE_URL = 'https://eastasia.api.cognitive.microsoft.com/face/v1.0'
    CF.BaseUrl.set(BASE_URL)
    #img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
    try:
        result = CF.face.detect(img_url)
    except Exception as e:
        print e
        return ms_face_detect(img_url)
 
    #print(result)
    cc=0
    rects=[]
    for re in result:
        #{u'faceId': u'4076f1f6-3461-4c8b-9113-647e17230d85', u'faceRectangle': {u'width': 101, u'top': 67, u'height': 101, u'left': 137}}
        cc+=1
        #np.array((0,0,faces[0][0],faces[0][1])) 
        #print cc
        rer=re[u'faceRectangle']
        #print rer[u'width']
        #print rer[u'top']
        #print rer[u'height']
        #print rer[u'left']
        #dic=json.loads(re)
        #print dic
        rects.append(np.array((rer[u'left'],rer[u'top'],rer[u'width'],rer[u'height'])))
    return rects
img_url = 'https://raw.githubusercontent.com/Microsoft/Cognitive-Face-Windows/master/Data/detection1.jpg'
img_url = '/data1/mingmingzhao/label/data_sets_teacher_1w/47017613_1510574400_out-video-jzc70f41fa6f7145b4b66738f81f082b65_f_1510574403268_t_1510575931221.flv_0001.jpg'
print(ms_face_detect(img_url))
