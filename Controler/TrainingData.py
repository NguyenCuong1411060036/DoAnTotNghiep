import cv2, os
import numpy as np
from PIL import Image
recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("Face_Recognition/haarcascade_frontalface_default.xml");
def getImagesAndLabels():
    path="Face_Recognition/DataSet/ImageLibrary"
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids = []
    print(len(imagePaths))
    if len(imagePaths) > 0 :
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')

            # PIL image to numpy array
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])

            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:

                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
            return faceSamples,ids
    else:
        return 0
if getImagesAndLabels() != 0 :
    faces,ids = getImagesAndLabels()
    recognizer.train(faces, np.array(ids))
    recognizer.write('Face_Recognition/DataSet/TrainerData/trainer.yml')
else:
    print("There is no immage in library")
print(getImagesAndLabels())
