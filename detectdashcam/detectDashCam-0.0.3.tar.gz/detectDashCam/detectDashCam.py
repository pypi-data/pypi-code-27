import numpy as np
import cv2
import argparse

# parser = argparse.ArgumentParser(description='Detecting if a video is DashCam Video.')
# parser.add_argument('video', help='Path to input video')

# args = parser.parse_args()

def detect(video):
    cap = cv2.VideoCapture(video)
    fgbg = cv2.createBackgroundSubtractorMOG2()

    resTrue = 0
    resFalse = 0

    while(1):
        try :
            ret, frame = cap.read()
            fgmask = fgbg.apply(frame)
            # print len(fgmask)
            # print len(fgmask[0])
            cropped = fgmask[ int(len(fgmask)*0.8):int(len(fgmask)*1.0), 0:int(len(fgmask[0]))]
            white = cv2.countNonZero(cropped)*1.0/(len(cropped)*len(cropped[0]))
            # print white
            if white<0.1:
                print "Yes !"
                resTrue += 1
            else:
                print "No  !"
                resFalse += 1
            # cv2.imshow('frame',fgmask)
            cv2.imshow('cropped',cropped)
            k = cv2.waitKey(30) & 0xff
            if k == 27:
                break
        except:
            break

    print (resTrue*1.0/(resTrue + resFalse))

    if (resTrue*1.0/(resTrue + resFalse))>0.7:
        print "YES ! DashCam Video"
    else:
        print "NOT a DashCam Video"

    cap.release()
    cv2.destroyAllWindows()

# detect(args.video)