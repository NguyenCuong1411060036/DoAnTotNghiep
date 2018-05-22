connection= sqlite3.connect("DiemDanh.db")
# lấy Id lớn nhất có trong database để tiến hành gán id tự động cho hình ảnh chụp được/ đồng bộ hóa giữa hình ảnh và thông tin nhân viên
result = connection.execute("SELECT id FROM NhanVien ORDER BY id DESC limit 1")
values = result.fetchone()
if (values[0] > 0):
    face_id = values[0] + 1
else:
    face_id = 1
print("faceid " + str(face_id))