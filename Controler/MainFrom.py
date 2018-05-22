from PyQt5 import QtCore,QtGui,QtWidgets,uic
from PyQt5.QtCore import QBasicTimer
from PyQt5.QtSql import QSqlQueryModel,QSqlDatabase,QSqlQuery
import sys

from PyQt5.QtWidgets import QMessageBox

from Controler.DataConnect.ConectToDatabase import GetNhanVien, create_connection, GetAllNhanVien, GetPhongBan, \
    GetChucVu, TaskNhanVien, getMaChucVu, getMaPhongBan, InsertNhanVien, DeleteNhanVien, UpdateNhanvien
MaNV=20
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
        self.btnThem.clicked.connect(self.ThemMoi)
        self.btnXoa.clicked.connect(self.XoaNhanVien)
        self.btnLuuLai.clicked.connect(self.SuaNhanVien)
        self.MaNV=None
    def ShowListNhanVien(self):
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("DataConnect/DiemDanhDatabse.db")
        db.open()
        query="SELECT MaNV as [Mã NV],Name as [Tên nhân viên],Sex as[Giới Tính],Tuoi as [Tuổi], Address as[Địa chỉ], Email as [Email],PhoneNumber as [Điện thoại],TenChucVu as[Chức vụ],TenPhongBan as [Phòng ban] " \
              "FROM NhanVien,ChucVu,PhongBan " \
              "where Nhanvien.MaChucVu = Chucvu.MaChucVu and Nhanvien.MaPhongBan=PhongBan.MaPhongBan"
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
    def ComboChucVu(self,TenChucVu):
        # Lấy toàn bộ text item của combo box đưa vào mảng
        AllItemsChucVu = [self.txtChucVu.itemText(i) for i in range(self.txtChucVu.count())]

        for item in AllItemsChucVu:
            if(item==TenChucVu):
                Index=AllItemsChucVu.index(item)
                print(Index)
                self.txtChucVu.setCurrentIndex(Index)
    def ComboPhongBan(self,TenPhongBan):
        # Lấy toàn bộ text item của combo box đưa vào mảng
        AllItemsPhongBan = [self.txtPhongBan.itemText(i) for i in range(self.txtPhongBan.count())]

        for item in AllItemsPhongBan:
            if(item==TenPhongBan):
                Index=AllItemsPhongBan.index(item)
                print(Index)
                self.txtPhongBan.setCurrentIndex(Index)
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
        ChucVu=(projectModel.index(row,7)).data()
        PhongBan=(projectModel.index(row,8)).data()


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
        self.ComboChucVu(ChucVu)
        self.ComboPhongBan(PhongBan)
    def ShowQuestion(self):
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Information)
        self.msg.setText("Bạn đã cập nhật thành công thông tin.Bạn có muốn cập nhật lại khuôn mặt   ")
        self.msg.setWindowTitle("Cập nhật khuôn mặt  ")
        self.msg.setStandardButtons(QMessageBox.Yes|QMessageBox.No)
        self.msg.setDefaultButton(QMessageBox.Yes)
        #### Lấy giá trị click lưu vào ret #############################
        ret = self.msg.exec()
        print(str(ret))
        #### nếu ret =16384 hay click vào button yes thì in ra màn hình câu câu thông báo " click yes"
        if(ret == QMessageBox.Yes):
            print("Cập nhật khuôn mặt")
        #### nếu click vào no in ra câu thông báo " click no "
        if  (ret == QMessageBox.No):
            print("Load Lại Form ")
    def CheckForm(self):

        tenNhanVien =self.txtHoTen.text()
        tuoi=self.txtTuoi.value()
        dienthoai=self.txtSoDienThoai.text()
        DiaChi=self.txtDiaChi.text()
        Email=self.txtEmail.text()
        if(tenNhanVien.strip() and tuoi >=18 and dienthoai.strip() and DiaChi.strip() and Email.strip()):
            return 1
        else:
            print("Không đủ điều kiên")
            return 0
    def ClearForm(self):
         self.txtHoTen.setText("")
         self.txtTuoi.setValue(18)
         self.txtSoDienThoai.setText("")
         self.txtDiaChi.setText("")
         self.txtEmail.setText("")
    def ThemMoi(self):
        KiemTra=self.CheckForm()
        if(KiemTra==0):
            print("Bạn Phải nhập đây đủ thông tin ")
        else:
            conn = create_connection('DataConnect/DiemDanhDatabse.db')
            with conn:
                tenNhanVien = self.txtHoTen.text()
                tuoi = self.txtTuoi.value()
                gioitinh=self.txtGioiTinh.currentText()
                dienthoai = self.txtSoDienThoai.text()
                chucvu=self.txtChucVu.currentText()
                MaChucVu=getMaChucVu(conn,chucvu)
                phongban=self.txtPhongBan.currentText()
                MaPhongBan=getMaPhongBan(conn,phongban)
                DiaChi = self.txtDiaChi.text()
                Email = self.txtEmail.text()
                DienThoai=self.txtSoDienThoai.text()
                task=TaskNhanVien(tenNhanVien,gioitinh,tuoi,DiaChi,Email,DienThoai,MaChucVu,MaPhongBan)
                InsertNhanVien(conn,task)
        self.ClearForm()
        self.ShowListNhanVien()
    def XoaNhanVien(self):
        MaNV=self.LbMaNhanVien.text()
        if(MaNV.strip()):
            conn = create_connection('DataConnect/DiemDanhDatabse.db')
            with conn:
                DeleteNhanVien(conn, MaNV)
                self.ClearForm()


        else:
            print("Bạn phải chọn nhân viên cần xóa ")

        self.ShowListNhanVien()
    def SuaNhanVien(self):
        MaNV = self.LbMaNhanVien.text()
        if (MaNV.strip()):
            conn = create_connection('DataConnect/DiemDanhDatabse.db')
            with conn:
                if(self.CheckForm()==1):
                    tenNhanVien = self.txtHoTen.text()
                    tuoi = self.txtTuoi.value()
                    gioitinh = self.txtGioiTinh.currentText()
                    dienthoai = self.txtSoDienThoai.text()
                    chucvu = self.txtChucVu.currentText()
                    MaChucVu = getMaChucVu(conn, chucvu)
                    phongban = self.txtPhongBan.currentText()
                    MaPhongBan = getMaPhongBan(conn, phongban)
                    DiaChi = self.txtDiaChi.text()
                    Email = self.txtEmail.text()
                    DienThoai = self.txtSoDienThoai.text()
                    task = TaskNhanVien(tenNhanVien, gioitinh, tuoi, DiaChi, Email, DienThoai, MaChucVu, MaPhongBan)
                    UpdateNhanvien(conn, MaNV,task)
                    self.ClearForm()
                else:
                    print("Nhập đầy đủ thông tin đi ba")


        else:
            print("Bạn phải chọn nhân viên cần xóa ")

        self.ShowListNhanVien()
if __name__=='__main__':
    import sys;
    app=QtWidgets.QApplication(sys.argv)
    window=MyWindow()
    window.show()
    sys.exit(app.exec())