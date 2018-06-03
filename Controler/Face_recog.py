import cv2
import datetime
from PyQt5 import QtWidgets,uic
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtGui import QImage, QPixmap
from Controler.DataConnect.ConectToDatabase import GetNhanVien, create_connection, InsertDiemDanh
from Controler.MainFrom import MaNV
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('Gui/DiemDanh.ui',self)
        self.setWindowTitle('Chỉnh sửa thông tin ')
        self.image = None
        self.StartWebCam()
        self.Tick()
        self.now = datetime.datetime.now()
        self.ShowCurentDate()
        self.Conn=None
        self.face_enable=True
        self.MaNV=MaNV
        self.count=0
        self.ImagePath=None
        self.face_ID = None
        self.Profile=None
        self.Count=0
        self.face_detector = cv2.CascadeClassifier('Face_Recognition/haarcascade_frontalface_default.xml')
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read('../DataSet/TrainerData/trainer.yml')
    def ShowCurentDate(self):
        Curentdate=str(self.now.day) + "/" + str(self.now.month) + "/" + str(self.now.year)
        self.txtCurentDate.setText(Curentdate)
    def Tick(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_Time)
        self.timer.start(1000)
    def update_Time(self):
        time = QTime.currentTime().toString()
        self.txtCurentTime.setText(time)
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
    def detect_face(self,image_frame):
                gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(image_frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    self.DiemDanh(gray[y:y+h,x:x+w])
                return image_frame
    def DiemDanh(self,GrayID):
        self.MaNV=self.recognizer.predict(GrayID)
        if self.face_ID==None :
            self.face_ID = self.MaNV[0]
            self.completed = 0
            self.default= 50
        else:
            if self.MaNV[0] == self.face_ID:
                self.count+=1
                self.completed += 100 / self.default
            else:
                self.face_ID = self.MaNV[0]
                self.Count = 0
                self.completed = 0


        if self.count >= self.default:
            self.Conn=create_connection('DataConnect/DiemDanhDatabse.db')
            self.Profile=GetNhanVien(self.Conn,self.MaNV[0])
            if self.Profile != None:
                for row in self.Profile:
                    print(row)
                self.txtTen.setText(row[1])
                self.txtPhong.setText(str(row[8]))
                self.txtMaNV.setText(str(row[0]))
                time = QTime.currentTime().toString()
                self.txtTime.setText(time)
                self.progress.setValue(100)
                self.lbWaitting.setText("Xin Cám Ơn")
                with self.Conn:
                    InsertDiemDanh(self.Conn,self.MaNV[0])
                self.face_enable=False
            else:
                self.txtTen.setText("Unknow")
                self.txtPhong.setText("Unknow")
                self.txtMaNV.setText("Unknow")
        self.progress.setValue(self.completed)
        if self.lbWaitting.text() == "Xin Cám Ơn":
            self.ReSet()
    def ReSet(self):
        self.completed2 = 0
        while self.completed2 < 100:
            self.completed2 += 0.0001
            self.progressReset.setValue(self.completed2)
        self.face_ID=None
        self.txtTen.setText("")
        self.txtPhong.setText("")
        self.txtMaNV.setText("")
        self.count=0
        self.txtTime.setText("")
        self.lbWaitting.setText("Chờ xíu")
        self.face_enable=True
        self.progressReset.setValue(0)
if __name__=='__main__':
    import sys;
    app=QtWidgets.QApplication(sys.argv)
    window=MyWindow()
    window.show()
sys.exit(app.exec())