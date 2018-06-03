import sqlite3
from sqlite3 import Error
import datetime
def create_connection(db_file):

    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None
def GetAllNhanVien(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM NhanVien")

    rows = cur.fetchall()

    for row in rows:
        print(row)
def GetNhanVien(conn, MaNV):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM NhanVien WHERE MaNV=?", (MaNV,))
    rows = cur.fetchall()
    return rows
def GetLastIDNhanVien(conn):
    cur=conn.cursor();
    cur.execute("SELECT MaNV FROM NhanVien ORDER BY MaNV DESC limit 1")
    result = cur.fetchone();
    return result[0]
def InsertNhanVien(conn,task):
    cur = conn.cursor()
    cmd = "INSERT INTO NhanVien (Name,Sex,Tuoi,Address,Email,PhoneNumber,MaChucVu, MaPhongBan)VALUES (?,?,?,?,?,?,?,?);"
    try:
        cur.execute(cmd, task)
        print("them thanh cong")
        return 1
    except Error as e:
        print(e)
        return 0
def GetPhongBan(conn):
    cur=conn.cursor()
    query="Select * from PhongBan"
    cur.execute(query)
    rows=cur.fetchall()
    return rows
def GetChucVu(conn):
    cur=conn.cursor()
    query="select * from ChucVu"
    cur.execute(query)
    rows=cur.fetchall()
    return rows
def TaskNhanVien(Name,Sex,Tuoi,Address,Email,PhoneNumber,MaChucVu,MaPhongBan):
    Task=(Name,Sex,Tuoi,Address,Email,PhoneNumber,MaChucVu,MaPhongBan)
    return Task
def UpdateNhanvien(conn,MaNv,Task):
    cur=conn.cursor()
    query="UPDATE NhanVien SET Name =?,Sex =?,Tuoi =?,Address = ?,Email = ?,PhoneNumber = ?,MaChucVu = ?, MaPhongBan = ? WHERE MaNV='"+str(MaNv)+"'; "
    try:
        cur.execute(query,Task)
        return 1
    except Error as e:
        print(e)
        return 0
def DeleteNhanVien(conn,MaNv):
    cur=conn.cursor()
    query="DELETE FROM NhanVien WHERE MaNV = ?;"
    try:
        cur.execute(query,(MaNv,))
        return 1
    except Error as e:
        print(e)
        return 0
def getMaChucVu(conn,TenChucVu):
    cur=conn.cursor()
    query="select MaChucVu from ChucVu WHERE TenChucVu like '%"+TenChucVu+"%';"
    cur.execute(query)
    result = cur.fetchone();
    return result[0]
def getMaPhongBan(conn,TenPhongBan):
    cur=conn.cursor()
    query="select MaPhongBan from PhongBan WHERE TenPhongBan like '%"+TenPhongBan+"%';"
    cur.execute(query)
    result = cur.fetchone();
    return result[0]
def InsertDiemDanh(conn,MaNV):
    cur = conn.cursor()
    now = datetime.datetime.now()
    CurentDate = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    CurentTime = str(now.hour) + ":" + str(now.minute) + ":" + str(now.second)
    cmd = "INSERT INTO DiemDanh (Ngay,MaNV,Gio)VALUES ('"+CurentDate+"','"+str(MaNV)+"','"+CurentTime+"');"
    try:
        cur.execute(cmd)
        print("them thanh cong")
        return 1
    except Error as e:
        print(e)
        return 0
def InsertPhongBan(conn,task):
    cur = conn.cursor()
    cmd = "INSERT INTO PhongBan (TenPhongBan,MoTa)VALUES (?,?);"
    try:
        cur.execute(cmd, task)
        print("them thanh cong")
        return 1
    except Error as e:
        print(e)
        return 0
def TaskPhongBan(TenPhong,MoTa):
    Task = (TenPhong,MoTa)
    return Task
def UpdatePhongBan(conn,MaPhongBan,Task):
    cur=conn.cursor()
    query="UPDATE PhongBan SET TenPhongBan = ?,MoTa = ? WHERE MaPhongBan = '"+str(MaPhongBan)+"'; "
    try:
        cur.execute(query,Task)
        return 1
    except Error as e:
        print(e)
        return 0
def InsertChucVu(conn,task):
    cur = conn.cursor()
    cmd = "INSERT INTO ChucVu (TenChucVu,HeSoLuong,PhuCap)VALUES (?,?,?);"
    try:
        cur.execute(cmd, task)
        print("them thanh cong")
        return 1
    except Error as e:
        print(e)
        return 0
def TaskChucVu(TenChucVu,HeSoLuong,PhuCap):
    Task = (TenChucVu,HeSoLuong,PhuCap)
    return Task
def UpdateChucVu(conn,MaChucVu,Task):
    cur=conn.cursor()
    query="UPDATE ChucVu SET TenChucVu = ?,HeSoLuong = ?,PhuCap = ? WHERE MaChucVu = '"+str(MaChucVu)+"'; "
    try:
        cur.execute(query,Task)
        return 1
    except Error as e:
        print(e)
        return 0

def main():
    # create a database connection
    conn = create_connection('DiemDanhDatabse.db')
    task=TaskPhongBan('a','qwsc')
    with conn:
        result = UpdatePhongBan(conn,1,task)
        print(result)
if __name__ == '__main__':
    main()