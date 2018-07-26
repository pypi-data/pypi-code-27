import cv2
import os

# base_dir = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(base_dir,'Face_cascade.xml')
path = os.path.join(os.getcwd(), 'Face_cascade.xml')
print(path)

class FaceExtract:

    def detect_faces(self,img_path):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_dir,'Face_cascade.xml')
        print(file_path)
        FACE_CASCADE = cv2.CascadeClassifier(file_path)
        image = cv2.imread(img_path)
        image_grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faces = FACE_CASCADE.detectMultiScale(image_grey, scaleFactor=1.16, minNeighbors=5, minSize=(25, 25), flags=0)

        for x, y, w, h in faces:
            sub_img = image[y - 10:y + h + 10, x - 10:x + w + 10]
            cv2.imshow("Faces Found", sub_img)
            cv2.waitKey(0)


