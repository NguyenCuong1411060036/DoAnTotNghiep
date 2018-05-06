import sqlite3
from sqlite3 import Error


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

    for row in rows:
        print(row)
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



def main():


    # create a database connection
    conn = create_connection('DiemDanhDatabse.db')
    with conn:
        print("4 .Thêm mới một nhân viên :")
        task=TaskNhanVien("Nguyễn Hữu Cường dsf","Nam","22","Nguyễn văn Quỳ quận 7","nnnnn","0123456789","1","1")
        print(InsertNhanVien(conn,task))
        GetAllNhanVien(conn)

if __name__ == '__main__':
    main()