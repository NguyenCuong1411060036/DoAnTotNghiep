from macpath import expanduser
import cv2, os
import numpy as np
from PIL import Image
from PyQt5 import QtWidgets,uic
from os.path import expanduser
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QFileDialog
from Controler.DataConnect.ConectToDatabase import create_connection, GetLastIDNhanVien
from Controler.MainFrom import MaNV
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('Gui/LayHinhAnh.ui',self)
        self.setWindowTitle('Chỉnh sửa thông tin ')
        self.image = None
        self.StartWebCam()
        self.btnChosseFolder.clicked.connect(self.ChosseImageFile)
        self.btnGetRealTimeFace.setCheckable(True)
        self.btnGetRealTimeFace.toggled.connect(self.face_record)
        self.btnLuuThongTin.clicked.connect(self.training)
        self.face_enable=False
        self.MaNV=MaNV
        self.count=0
        self.ImagePath=None
        self.face_detector = cv2.CascadeClassifier('Face_Recognition/haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
    def ChosseImageFile(self):
        self.ImagePath = QFileDialog.getExistingDirectory(None, 'Select a folder:', expanduser("~"))
        print( self.ImagePath)
        self.GetImageLocation(self.MaNV,self.ImagePath)
    def StartWebCam(self):
        self.video_cam = cv2.VideoCapture(0)
        self.video_cam.set(cv2.CAP_PROP_FRAME_HEIGHT,331)
        self.video_cam.set(cv2.CAP_PROP_FRAME_WIDTH,521)
        self.timer=QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(5)
    def update_frame(self):
        ret,self.image = self.video_cam.read()
        self.image=cv2.flip(self.image,1)
        self.displayImage(self.image,1)
        if (self.face_enable):
            detected_image = self.detect_face(self.image)
            self.displayImage(detected_image,1)
        else:
            self.displayImage(self.image,1)
    def detect_face(self,image_frame):
                gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    self.Chup(gray[y:y+h,x:x+w])

                return image_frame
    def Chup(self,GrayID):
            if (self.MaNV == None):
                conn = create_connection('DataConnect/DiemDanhDatabse.db')
                self.MaNV = GetLastIDNhanVien(conn)
                print("Mã nhân viên cuối cùng là " + str(self.MaNV))
            self.count+=1
            if self.count <=100 :
                cv2.imwrite("../DataSet/ImageLibrary/User." + str(self.MaNV) + '.' + str(self.count) + ".jpg",GrayID)
    def displayImage(self,img,window=1):
        qfromat= QImage.Format_Indexed8
        if len(img.shape)==3:
            if img.shape[2] == 4 :
                qfromat=QImage.Format_RGBA8888
            else:
                qfromat=QImage.Format_RGB888
        outImage=QImage(img,img.shape[1],img.shape[0],img.strides[0],qfromat)
        outImage=outImage.rgbSwapped()
        if window==1:
            self.lbImage.setPixmap(QPixmap.fromImage(outImage))
            self.lbImage.setScaledContents(True)
    def face_record(self,status):
        if status:
            self.btnGetRealTimeFace.setText('Stop')
            self.face_enable=True
        else:
            self.btnGetRealTimeFace.setText('Chup tiep')
            self.face_enable = False
    def getImagesAndLabels(self,path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')

            # PIL image to numpy array
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])

            faces = self.face_detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        return faceSamples, ids
    def training(self):
        path="../DataSet/ImageLibrary"
        faces, ids = self.getImagesAndLabels(path)
        self.recognizer.train(faces, np.array(ids))
        self.recognizer.save('../DataSet/TrainerData/trainer.yml')
        # xoa hinh anh ngay ki training xong
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        for path in imagePaths:
            os.remove(path)
    def GetImageLocation(self,id,path):
        count = 0
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]

        for imagePath in imagePaths:
            # đọc ảnh
            image = cv2.imread(imagePath)
            # Convert ảnh ra mà xám
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # Lấy khuôn mặt xuất hiện trong khung hình
            faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
            # ghi ảnh vào dữ liệu
            for (x, y, w, h) in faces:
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                count += 1
                # ghi ảnh khuôn mặt vào dataset
                cv2.imwrite("../DataSet/ImageLibrary/User." + str(id) + '.' + str(count) + ".jpg",
                            gray[y:y + h, x:x + w])
            print(imagePath)
            cv2.imshow('frame', image)
if __name__=='__main__':
    import sys;
    app=QtWidgets.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec())