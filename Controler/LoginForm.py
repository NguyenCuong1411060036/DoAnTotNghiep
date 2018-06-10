from subprocess import Popen
from PyQt5.QtWidgets import QMessageBox
from Controler.DataConnect.ConectToDatabase import create_connection,Login
from PyQt5 import QtWidgets,uic
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('Gui/Login.ui',self)
        self.DataBase = "DataConnect/DiemDanhDatabse.db"
        self.Conn = create_connection(self.DataBase)
        self.setWindowTitle('Đăng nhập')
        self.txtPassWord.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnHuy.clicked.connect(self.ExitApp)
        self.btnDangNhap.clicked.connect(self.DangNhap)
    def ExitApp(self):
        sys.exit()
    def DangNhap(self):
        Email= self.txtUsername.text()
        Pass= self.txtPassWord.text()
        result = Login(self.Conn,Email,Pass)
        if result ==1 :
            self.CreateFile(Email)
            Popen('python MainFrom.py')
        else:
            self.ShowWarning("Email hoặc Password Không chính xác !!!")
    def ShowWarning(self, Mes):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(str(Mes))
        self.msg.setWindowTitle("Cảnh Báo")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()
    def CreateFile(self,Email):
        f = open("LoginSec.txt", "w+")
        f.write(Email)
        f.close()

if __name__=='__main__':
    import sys;
    app=QtWidgets.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec())