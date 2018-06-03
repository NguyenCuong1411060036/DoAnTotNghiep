from PyQt5.QtWidgets import QMessageBox
from Controler.DataConnect.ConectToDatabase import GetNhanVien, create_connection, InsertPhongBan, TaskPhongBan, \
    UpdatePhongBan
from PyQt5 import QtWidgets,uic
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
import sys
from PyQt5 import uic, QtWidgets, QtCore
from PyQt5.QtWidgets import QDialog

def main():
    app = QtWidgets.QApplication(sys.argv)
    myWindow = MyWindowClass()
    myWindow.show()
    app.exec_()

main_dialog = uic.loadUiType("Gui/QuanLyChucVu.ui")[0]

TestQDialog = uic.loadUiType("Gui/QuanLyPhongBan.ui")[0]

class QDialogClass(QtWidgets.QMainWindow, TestQDialog):
    def __init__(self, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setWindowTitle('Quản Lý Phòng Ban')
        self.TablePhongBan.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ShowListPhongBan()
        self.DataBase = "DataConnect/DiemDanhDatabse.db"
        self.Conn = create_connection(self.DataBase)
        self.btnThemPhong.clicked.connect(self.ThemPhongBan)
        self.btnCapNhat.clicked.connect(self.SuaPhongBan)

    def ShowListPhongBan(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("DataConnect/DiemDanhDatabse.db")
        db.open()
        query = "select MaPhongBan as [Mã Phòng Ban] , TenPhongBan as [Tên Phòng Ban], MoTa as [Mô tả ] from PhongBan"
        projectModel = QSqlQueryModel()
        projectModel.setQuery(
            query,
            db)
        self.TablePhongBan.setModel(projectModel)
        self.TablePhongBan.show()
        self.TablePhongBan.clicked.connect(self.GetPhongBanFromTable)

    def GetPhongBanFromTable(self, index):
        projectModel = self.TablePhongBan.model()
        row = index.row()
        MaPhongBan = (projectModel.index(row, 0)).data()
        TenPhongBan = (projectModel.index(row, 1)).data()
        MoTa = (projectModel.index(row, 2)).data()
        self.txtMaPhongBan.setText(str(MaPhongBan))
        self.txtTenPhongban.setText(str(TenPhongBan))
        self.txtMoTa.clear()
        self.txtMoTa.appendPlainText(str(MoTa))

    def ThemPhongBan(self):
        Check = self.CheckForm()
        if Check == 1:
            TenPhong = self.txtTenPhongban.text()
            MoTa = self.txtMoTa.toPlainText()
            with self.Conn:

                task = TaskPhongBan(str(TenPhong), str(MoTa))
                Result = InsertPhongBan(self.Conn, task)
                if Result == 0:
                    mes = "Tên Phòng ban đã tồn tại "
                    self.ShowWarning(mes)
                    self.txtTenPhongban.setText("")
                else:
                    mes = "Đã thêm thành công"
                    self.showQMessageBox(mes)
                    self.ClearFrom()

        else:
            self.ShowWarning("Vui lòng nhập đầy đủ thông tin")

        self.ShowListPhongBan()

    def CheckForm(self):

        tenPhongBan = self.txtTenPhongban.text()
        MoTa = self.txtMoTa.toPlainText()

        if (tenPhongBan.strip() and MoTa.strip()):
            return 1
        else:
            return 0

    def ClearFrom(self):
        self.txtMaPhongBan.setText("")
        self.txtTenPhongban.setText("")
        self.txtMoTa.clear()

    def ShowWarning(self, Mes):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(str(Mes))
        self.msg.setWindowTitle("Cảnh Báo")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()

    def showQMessageBox(self, Mes):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(str(Mes))
        self.msg.setWindowTitle("Thông Báo")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()

    def SuaPhongBan(self):
        MaPhongBan = self.txtMaPhongBan.text()
        if (MaPhongBan.strip()):
            TenPhong = self.txtTenPhongban.text()
            MoTa = self.txtMoTa.toPlainText()
            with self.Conn:
                task = TaskPhongBan(str(TenPhong), str(MoTa))
                Result = UpdatePhongBan(self.Conn, MaPhongBan, task)
                if Result == 0:
                    mes = "Tên Phòng ban đã tồn tại "
                    self.ShowWarning(mes)
                    self.txtTenPhongban.setText("")
                else:
                    mes = "Đã Cập nhật  thành công"
                    self.showQMessageBox(mes)
                    self.ClearFrom()

        else:
            self.ShowWarning("Vui lòng nhập đầy đủ thông tin")
        self.ShowListPhongBan()

class MyWindowClass(QtWidgets.QMainWindow, main_dialog):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.btnThemChucVu.clicked.connect(self.dialog)

    def dialog(self):
        app = QtWidgets.QApplication(sys.argv)
        dialog = QDialog()
        dialog.ui = QDialogClass()
        dialog.ui.setupUi(dialog)
        dialog.exec_()

if __name__ == "__main__":
    main()