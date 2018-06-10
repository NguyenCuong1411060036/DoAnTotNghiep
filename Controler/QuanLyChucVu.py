from PyQt5.QtWidgets import QMessageBox
from Controler.DataConnect.ConectToDatabase import GetNhanVien, create_connection, InsertChucVu, TaskChucVu, \
    UpdateChucVu
from PyQt5 import QtWidgets,uic
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel
class MyWindow(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        #self.resize(300, 200)
        uic.loadUi('Gui/QuanLyChucVu.ui', self)
        self.setWindowTitle('Quản Lý Chức Vụ')
        self.TableChucVu.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ShowListChucVu()
        self.txtMaChucVu.setText("")
        self.DataBase="DataConnect/DiemDanhDatabse.db"
        self.Conn=create_connection(self.DataBase)
        self.btnThemChucVu.clicked.connect(self.ThemChucVu)
        self.btnSuaChucVu.clicked.connect(self.SuaChucVu)
    def ShowListChucVu(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("DataConnect/DiemDanhDatabse.db")
        db.open()
        query = "select MaChucVu as [Mã Chức Vụ], TenChucVu as [Tên Chức Vụ] , HeSoLuong as [Hệ Số Lương], PhuCap as [Phụ Cấp Chức Vụ ]from ChucVu"
        projectModel = QSqlQueryModel()
        projectModel.setQuery(
            query,
            db)
        self.TableChucVu.setModel(projectModel)
        self.TableChucVu.show()
        self.TableChucVu.clicked.connect(self.GetChucVuFromTable)
    def GetChucVuFromTable(self, index):
        projectModel = self.TableChucVu.model()
        row = index.row()
        MaChucVu = (projectModel.index(row, 0)).data()
        TenChucVu = (projectModel.index(row, 1)).data()
        HeSoLuong = (projectModel.index(row, 2)).data()
        PhuCap = (projectModel.index(row, 3)).data()
        self.txtMaChucVu.setText(str(MaChucVu))
        self.txtTenChucVu.setText(str(TenChucVu))
        self.txtHeSoLuong.setValue(HeSoLuong)
        self.txtPhuCap.setValue(PhuCap)
    def CheckForm(self):

        TenChucVu =self.txtTenChucVu.text()
        if (TenChucVu.strip()):
            return 1
        else:
            return 0
    def showQMessageBox(self,Mes):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText(str(Mes))
        self.msg.setWindowTitle("Thông Báo")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()
    def ThemChucVu(self):
        Check = self.CheckForm()

        if Check == 1:
            TenChucVu = self.txtTenChucVu.text()
            HeSoLuong= self.txtHeSoLuong.value()
            PhuCap = self.txtPhuCap.value()
            with self.Conn:

                task = TaskChucVu(str(TenChucVu),HeSoLuong, PhuCap)
                Result = InsertChucVu(self.Conn, task)
                if Result == 0:
                    mes = "Tên Chức Vụ đã tồn tại "
                    self.ShowWarning(mes)
                    self.txtTenChucVu.setText("")
                else:
                    mes = "Đã thêm thành công"
                    self.showQMessageBox(mes)
                    self.ClearFrom()

        else:
            self.ShowWarning("Vui lòng nhập đầy đủ thông tin")

        self.ShowListChucVu()

    def ShowWarning(self, Mes):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Warning)
        self.msg.setText(str(Mes))
        self.msg.setWindowTitle("Cảnh Báo")
        self.msg.setStandardButtons(QMessageBox.Ok)
        self.msg.show()
    def ClearFrom(self):
        self.txtMaChucVu.setText("")
        self.txtTenChucVu.setText("")

    def SuaChucVu(self):
        Check = self.CheckForm()
        MaChucVu = self.txtMaChucVu.text()
        if MaChucVu.strip() :
            if Check == 1:

                TenChucVu = self.txtTenChucVu.text()
                HeSoLuong = self.txtHeSoLuong.value()
                PhuCap = self.txtPhuCap.value()
                with self.Conn:

                    task = TaskChucVu(str(TenChucVu), HeSoLuong, PhuCap)
                    Result = UpdateChucVu(self.Conn, MaChucVu,task)
                    if Result == 0:
                        mes = "Tên Chức Vụ đã tồn tại "
                        self.ShowWarning(mes)
                        self.txtTenChucVu.setText("")
                    else:
                        mes = "Đã Cập nhật  thành công"
                        self.showQMessageBox(mes)
                        self.ClearFrom()
            else:
                self.ShowWarning("Vui lòng nhập đầy đủ thông tin")
            self.ShowListChucVu()
        else:
            self.ShowWarning("Vui Lòng chọn Chức vụ cần cập nhật !!!")


if __name__ == '__main__':
    import sys;

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())