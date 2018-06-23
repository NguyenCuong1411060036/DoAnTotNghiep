import os
from macpath import expanduser

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
import cv2
from Controler.face_properties import face_detector, face_enable
MaNV=None
def ChosseImageFile(MaNV):
    ImagePath = QFileDialog.getExistingDirectory(None, 'Select a folder:', expanduser("~"))
    print(ImagePath)
    GetImageLocation(MaNV,ImagePath)
def GetImageLocation(id,path):
    count = 0
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        # đọc ảnh
        image = cv2.imread(imagePath)
        # Convert ảnh ra mà xám
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Lấy khuôn mặt xuất hiện trong khung hình
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        # ghi ảnh vào dữ liệu
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            # ghi ảnh khuôn mặt vào dataset
            cv2.imwrite("Face_Recognition/DataSet/ImageLibrary/User." + str(id) + '.' + str(count) + ".jpg",
                        gray[y:y + h, x:x + w])
        print(imagePath)
        cv2.imshow('frame', image)
def StartWebCam():
    video_cam = cv2.VideoCapture(0)
    video_cam.set(cv2.CAP_PROP_FRAME_HEIGHT,331)
    video_cam.set(cv2.CAP_PROP_FRAME_WIDTH,521)
    timer=QTimer()
   # timer.timeout.connect(update_frame)
    timer.start(5)
def update_frame(video_cam):
    ret,image = video_cam.read()
    image=cv2.flip(image,1)
    displayImage(image,1)
    if (face_enable):
        detected_image = detect_face(image)
        displayImage(detected_image,1)
    else:
        displayImage(image,1)
def detect_face(self,image_frame):
            gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
            faces = face_detector.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.imwrite("Face_Recognition/DataSet/ImageLibrary/User." + str(MaNV) + '.' + str(self.count) + ".jpg",
                            gray[y:y + h, x:x + w])
            return image_frame
def displayImage(img,lbImage,window=1):
        qfromat= QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2] == 4 :
                qfromat=QImage.Format_RGBA8888
            else:
                qfromat=QImage.Format_RGB888
        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qfromat)
        outImage=outImage.rgbSwapped()
        if window==1:
            lbImage.setPixmap(QPixmap.fromImage(outImage))
            lbImage.setScaledContents(True)
def face_record(status):
    if status:
        face_enable=True
    else:
        face_enable = False

def main():
    StartWebCam()

if __name__ == '__main__':
    main()