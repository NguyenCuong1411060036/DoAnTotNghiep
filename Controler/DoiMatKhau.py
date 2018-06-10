from PyQt5.QtWidgets import QMessageBox

from Controler.DataConnect.ConectToDatabase import create_connection, Login, ChangePassWord
from PyQt5 import QtWidgets,uic
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('Gui/ChangePass.ui',self)
        self.DataBase = "DataConnect/DiemDanhDatabse.db"
        self.Conn = create_connection(self.DataBase)
        self.setWindowTitle('Đổi Mật Khẩu')
        self.txtOldPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtNewPass.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtConfirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.btnChangePass.clicked.connect(self.DoiPass)
        self.btnCancel.clicked.connect(self.ExitApp)
        self.Email=self.ReadFileSecc()
        self.txtEmail.setText(self.Email)
    def ExitApp(self):
        sys.exit()
    def ReadFileSecc(self):
        f = open("LoginSec.txt", "r")
        if f.mode == 'r':
            self.Email = f.read()
        print(self.Email)
        return self.Email
    def CheckForm(self,OldPass,NewPass,Confirm):
        if OldPass.strip() and NewPass.strip():
            if NewPass == Confirm:
                return 1
            else:
                self.ShowWarning("Xác Nhận Mật Khẩu Không Chính Xác !!!")
                return 0
        else:
            self.ShowWarning("Vui Lòng Nhập Đầy Đủ Thông tin")
            return 0
    def showQMessageBox(self, Mes):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(str(Mes))
        self.msg.setWindowTitle("Thông Báo")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()
        ret = self.msg.exec()
        if (ret == QMessageBox.Ok):
            self.ExitApp()
    def ShowWarning(self, Mes):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(str(Mes))
        self.msg.setWindowTitle("Cảnh Báo")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()
    def DoiPass(self):
        Email=self.txtEmail.text()
        OldPass = self.txtOldPass.text()
        NewPass = self.txtNewPass.text()
        Confirm = self.txtConfirm.text()
        result = self.CheckForm(OldPass,NewPass,Confirm)
        CheckPass =Login(self.Conn,self.Email,OldPass)
        if result == 1:
            if CheckPass == 1:
                Conn = create_connection('DataConnect/DiemDanhDatabse.db')
                with Conn:
                    KQ= ChangePassWord(Conn,Email,NewPass)
                    if KQ == 1:
                        self.showQMessageBox("Đổi Mật Khẩu Thành Công")
                    else:
                        self.ShowWarning("Thay Đổi Thất Bại")
            else:
                self.ShowWarning("Password Không Chính xác !!!")
if __name__=='__main__':
    import sys;
    app=QtWidgets.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec())