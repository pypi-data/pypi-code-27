import numpy as np
import cv2
from matplotlib import pyplot as plt
from os.path import splitext
import micral_harmonic_core

def showTimeline(dict_input):
     
    def getKey(item):
        return -item[1]
    
    r = []
    for k,v in dict_input.items():
        if 'harmonicity' in v:
            r.append([k,v['harmonicity']])
    
    r = sorted(r, key=getKey)
    print(r)
    
    minVal = r[-1][1]
    maxVal = r[0][1]
    border = 5
    sizeLine = 60
    sizeImage = 256
    nbImages = len(r)
    w = int(border + nbImages/2 * (sizeImage + border) - border/2 + border + sizeImage/2)
    h = int(border + sizeImage + sizeLine + sizeImage + border)
    img_output = np.empty((h,w,3), dtype = np.uint8)
    img_output.fill(255)
    
    cv2.line(img_output, (0,h//2), (w-1,h//2), (0,0,0), border//2)
    
    for i in range(nbImages):
        x = int(border + i/2 * (border + sizeImage))
        y = int(border + i%2 * (sizeImage + sizeLine))
        
        if i%2==0:
            y1 = y + sizeImage
        else:
            y1 = y
        x2 = np.clip(int(w-w/(maxVal-minVal)*(r[i][1]-minVal)-1), 0, w-1)
        cv2.line(img_output, (x+sizeImage//2,y1), (x2,h//2), (0,0,0), border//2, lineType=cv2.LINE_AA)
        cv2.line(img_output, (x2,h//2-sizeLine//6), (x2,h//2+sizeLine//6), (255,0,0), border//2)
        
        img = cv2.imread(r[i][0], cv2.IMREAD_GRAYSCALE)
        img = cv2.resize(img, (sizeImage, sizeImage), interpolation=cv2.INTER_AREA)
        img = cv2.applyColorMap(np.clip(img, 0, 255).astype('uint8'), cv2.COLORMAP_RAINBOW)
        img_output[y:y+sizeImage,x:x+sizeImage] = img
        
    cv2.imwrite("out.png", img_output)
    img_output = cv2.cvtColor( img_output, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("out_gray.png", img_output)

def harmonicMeasurement(images, plot, plotTimeline):
    output_dict = micral_harmonic_core.harmonicMeasurementCore(images, plot, plotTimeline)
    output_final = []
    
    if output_dict == None or len(output_dict) == 0:
        return output_dict
    
    for k,v in output_dict.items():
        if plot and 'process' in v:
            plt.figure(figsize=(10,5))
            
            if 'spectrum1d' in v['process']:
                spec = v['process']['spectrum1d']
                plt.plot(spec)
                maxSpec = spec.max()
            else:
                maxSpec = 1
            if 'left' in v['process']:
                left = v['process']['left']
                plt.plot([left,left], [0,maxSpec])
            if 'right' in v['process']:
                right = v['process']['right']
                plt.plot([right,right], [0,maxSpec])
            if 'limit' in v['process']:
                limit = v['process']['limit']
                plt.plot([0, len(spec)-1], [limit,limit])
            
            plt.title('Spectrum')    
            plt.savefig(splitext(k)[0] + "_harmonic_details.png")
            plt.close()
        if 'harmonicity' in v:
            output_final.append(v['harmonicity'])
        else:
            output_final.append(-1)
    
    if len(output_dict)>1 and plotTimeline:
        showTimeline(output_dict)
    
    if len(output_final) == 0:
        return None
    elif len(output_final) == 1:
        return output_final[0]
    else:
        return output_final