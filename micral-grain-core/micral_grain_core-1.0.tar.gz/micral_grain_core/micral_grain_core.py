import cv2
import numpy as np

import micral_utils

def printIm(img, plotFull, plotDetails, plotNum):
    img = np.uint8((img - img.min())/(img.max()-img.min()) * 255.0)
    img = cv2.resize(img, (512,512))
    output_dict = dict()
    if plotFull or plotDetails:
        output_dict['id'] = plotNum
    if plotFull:
        output_dict['full'] = np.clip(img, 0, 255).astype('uint8')
    if plotDetails is not None and plotDetails is not False:
        length = int(np.sqrt(np.square(plotDetails[0]-plotDetails[2]) + np.square(plotDetails[1]-plotDetails[3])))
        img_out = np.empty(length, dtype=np.uint8)
        for i in range(length):
            x = int(plotDetails[0] + i/length * (plotDetails[2]-plotDetails[0]))
            y = int(plotDetails[1] + i/length * (plotDetails[3]-plotDetails[1]))
            img_out[i] = np.uint8(img[y,x])
        output_dict['details'] = img_out
    return img, plotNum+1, output_dict

def grainSeparatorProcessor(img_ori, name, plot, plotFull, plotDetails):
    
    image_dict = dict()
    
    if img_ori.shape == (0,0):
        return image_dict
    
    img_ori = cv2.cvtColor(img_ori, cv2.COLOR_BGR2RGB)
    img_ori = cv2.resize(img_ori, (512,512))
    img = cv2.cvtColor(img_ori, cv2.COLOR_RGB2GRAY)
    
    image_dict['process'] = dict()
    
    if plotDetails is not None and plotDetails is not False:
        if isinstance(plotDetails,list) and len(plotDetails) == 4:
            plotDetails = list(plotDetails)
        else:
            plotDetails = [-1]*4
        for i, val in enumerate([128,256,128+256,256]):
            if plotDetails[i] < 0:
                plotDetails[i] = val
        img_out = img_ori.copy()
        cv2.line(img_out,(plotDetails[0],plotDetails[1]),(plotDetails[2],plotDetails[3]),(255,0,0), 5)
        image_dict['process']['preprocess'] = dict(id=0, details=img_out)
    
    
    plotNum = 1
    img, plotNum, image_dict['process']['input'] = printIm(img, plotFull, plotDetails, plotNum)
    
    img = np.sqrt(np.square(cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)) + np.square(cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)))
    img, plotNum, image_dict['process']['derivate'] = printIm(img, plotFull, plotDetails, plotNum)
    
    img = cv2.medianBlur(img, 51)
    img, plotNum, image_dict['process']['median'] = printIm(img, plotFull, plotDetails, plotNum)
    
    img = cv2.blur(img,(101,101))
    img, plotNum, image_dict['process']['average'] = printIm(img, plotFull, plotDetails, plotNum)
    
    th, img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)
    img, plotNum, image_dict['process']['threshold'] = printIm(img, plotFull, plotDetails, plotNum)
    
    unique, counts = np.unique(img, return_counts=True)
    
    if plot:
        alpha = 0.4
        image_dict['overlay'] = cv2.addWeighted(cv2.cvtColor(img, cv2.COLOR_GRAY2RGB), alpha, img_ori, 1 - alpha, 0)
    
    if len(counts) < 2:
        image_dict['coarse'] = unique[0]/255 * 100.0
    else:
        image_dict['coarse'] = counts[0]/(counts[0]+counts[1])*100.0
    
    image_dict['ultrafine'] = 100-image_dict['coarse']
    
    if image_dict['ultrafine'] != 0:
        image_dict['ratio'] = image_dict['coarse'] / image_dict['ultrafine']
        
    return image_dict
    
def grainSeparatorCore(images, plot, plotFull, plotDetails):
    if not isinstance(images,list):
        images = [images]
    output = dict()
    for numImage, image in enumerate(images):
        try:
            if isinstance(image, str):
                data = cv2.imread(image)
                name = image
            else:
                data = image
                name = "unknown_image" + str(numImage)
            output[name] = grainSeparatorProcessor(data, name, plot, plotFull, plotDetails)
        except Exception as e:
            print("image " + name + " raise : " + e.__doc__)
    return micral_utils.removeEmptyDict(output)