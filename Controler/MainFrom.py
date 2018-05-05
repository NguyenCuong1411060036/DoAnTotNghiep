from PyQt5 import QtCore,QtGui,QtWidgets,uic
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery
import sys

from Controler.DataConnect.ConectToDatabase import GetNhanVien, create_connection, GetAllNhanVien, GetPhongBan, \
    GetChucVu


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('Gui/ChinhSuaThongTin.ui',self)
        self.setWindowTitle('Chỉnh sửa thông tin ')
        self.TableNhanVien.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ShowListNhanVien()
        self.LoadPhongBan()
        self.LoadChucVu()
        self.TableNhanVien.clicked.connect(self.GetNhanVienFromTable)


    def ShowListNhanVien(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("DataConnect/DiemDanhDatabse.db")
        db.open()
        query="SELECT MaNV as [Mã NV],Name as [Tên nhân viên],Sex as[Giới Tính],Tuoi as [Tuổi], Address as[Địa chỉ], Email as [Email],PhoneNumber as [Điện thoại],MaChucVu as[Chức vụ],MaPhongBan as [Phòng ban] FROM NhanVien"
        projectModel = QSqlQueryModel()
        projectModel.setQuery(
            query,
            db)
        self.TableNhanVien.setModel(projectModel)
        self.TableNhanVien.show()

    def LoadPhongBan(self):
        conn=create_connection("DataConnect/DiemDanhDatabse.db")
        rows =GetPhongBan(conn)
        self.txtPhongBan.clear()
        for row in rows:

            self.txtPhongBan.addItem(row[1])
    def LoadChucVu(self):
        conn = create_connection("DataConnect/DiemDanhDatabse.db")
        rows = GetChucVu(conn)
        self.txtChucVu.clear()
        for row in rows:
            self.txtChucVu.addItem(row[1])

    def GetNhanVienFromTable(self,index):
        projectModel=self.TableNhanVien.model()
        row=index.row()
        MaNV = (projectModel.index(row, 0)).data()
        TenNhanVien = (projectModel.index(row, 1)).data()
        GioiTinh = (projectModel.index(row, 2)).data()
        Tuoi=(projectModel.index(row,3)).data()
        DiaChi=(projectModel.index(row,4)).data()
        Email=(projectModel.index(row,5)).data()
        DienThoai=(projectModel.index(row,6)).data()

        self.LbMaNhanVien.setText(str(MaNV))
        self.txtHoTen.setText(str(TenNhanVien))
        if (GioiTinh == "Nữ"):
            self.txtGioiTinh.setCurrentIndex(1)
        else:
            self.txtGioiTinh.setCurrentIndex(0)
        self.txtTuoi.setValue(int(Tuoi))
        self.txtDiaChi.setText(str(DiaChi))
        self.txtEmail.setText(str(Email))
        self.txtSoDienThoai.setText(str(DienThoai))

if __name__=='__main__':
    import sys;
    app=QtWidgets.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    conn=create_connection('DataConnect/DiemDanhDatabse.db')
    GetNhanVien(conn,3)

    sys.exit(app.exec())