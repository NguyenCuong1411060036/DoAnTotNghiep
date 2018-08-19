from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel

from Controler.DataConnect.ConectToDatabase import create_connection, Login, GetNhanVien
from PyQt5 import QtWidgets, uic

from Controler.Export_CSV import Export_DiemDanh


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        uic.loadUi('Gui/BaoCaoDiemDanh.ui', self)
        self.TableNhanVien.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.TableNhanVien.clicked.connect(self.GetNhanVienFromTable)
        self.ShowListNhanVien()
        self.txtStartDate.setDate(QDate.currentDate())
        self.txtEndDate.setDate(QDate.currentDate())
        self.txtMaNV.setDisabled(True)
        self.disabled = self.txtHoTen.setDisabled(True)
        self.btnXuatBaoCao.clicked.connect(self.file_save)
        self.DataBase = "DataConnect/DiemDanhDatabse.db"
        self.Conn = create_connection(self.DataBase)

    def ShowListNhanVien(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("DataConnect/DiemDanhDatabse.db")
        db.open()
        query = "SELECT MaNV as [Mã NV],Name as [Tên nhân viên],Sex as[Giới Tính],Tuoi as [Tuổi], Address as[Địa chỉ], Email as [Email],PhoneNumber as [Điện thoại],TenChucVu as[Chức vụ],TenPhongBan as [Phòng ban] " \
                "FROM NhanVien,ChucVu,PhongBan " \
                "where Nhanvien.MaChucVu = Chucvu.MaChucVu and Nhanvien.MaPhongBan=PhongBan.MaPhongBan"
        projectModel = QSqlQueryModel()
        projectModel.setQuery(
            query,
            db)
        self.TableNhanVien.setModel(projectModel)
        self.TableNhanVien.show()

    def GetNhanVienFromTable(self, index):
        projectModel = self.TableNhanVien.model()
        row = index.row()
        MaNV = (projectModel.index(row, 0)).data()
        TenNhanVien = (projectModel.index(row, 1)).data()
        self.txtMaNV.setText(str(MaNV))
        self.txtHoTen.setText(str(TenNhanVien))

    def file_save(self):
        TenNhanVien = self.txtHoTen.text()
        MaNV = self.txtMaNV.text()
        StartDate = self.txtStartDate.date()
        print(QDate.month(StartDate))
        startDate = str(QDate.day(StartDate)) + "/" + str(QDate.month(StartDate)) + "/" + str(QDate.year(StartDate))
        print(startDate)
        EndDate = self.txtEndDate.date()
        endDate = str(QDate.day(EndDate)) + "/" + str(QDate.month(EndDate)) + "/" + str(QDate.year(EndDate))
        print(endDate)
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', str(TenNhanVien) + "_" + (MaNV), "csv")
        print(name)
        file = open(name[0] + "." + name[1], 'w+')
        Export_DiemDanh(MaNV, startDate, endDate, file)
        file.close()


if __name__ == '__main__':
    import sys;

    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec())
