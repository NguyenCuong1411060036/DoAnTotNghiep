from PyQt5.QtWidgets import QMessageBox
from Controler.DataConnect.ConectToDatabase import create_connection, Login, ChangePassWord, CreateAccount
from PyQt5 import QtWidgets,uic
class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('Gui/CreateAccount.ui',self)
        self.txtPassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.txtConfirm.setEchoMode(QtWidgets.QLineEdit.Password)
        self.DataBase = "DataConnect/DiemDanhDatabse.db"
        self.Conn = create_connection(self.DataBase)
        self.setWindowTitle('Tạo mới tài khoản')
        self.btnCancel.clicked.connect(self.ExitApp)
        self.btnCreateAccount.clicked.connect(self.ThemTaiKhoan)
    def ExitApp(self):
        sys.exit()
    def CheckForm(self, Email, Password, Confirm):
        if Email.strip() and Password.strip():
            if Password == Confirm:
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
    def ThemTaiKhoan(self):
        Email = self.txtEmail.text()
        Password = self.txtPassword.text()
        Confirm = self.txtConfirm.text()
        result = self.CheckForm(Email, Password, Confirm)
        if result == 1:
                with self.Conn:
                                KQ = CreateAccount(self.Conn, Email, Password)
                                if KQ == 1:
                                        self.showQMessageBox("Thêm Mới Thành Công")
                                else:
                                        self.ShowWarning("Email Đã Được Đăng kí")
if __name__=='__main__':
    import sys;
    app=QtWidgets.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec())