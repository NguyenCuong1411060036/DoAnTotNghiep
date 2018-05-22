
import cv2,os
from Controler.DataConnect.ConectToDatabase import GetLastIDNhanVien,create_connection

face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
def loadCam(id):
        if (id == None):
            conn = create_connection('../DataConnect/DiemDanhDatabse.db')
            Id = GetLastIDNhanVien(conn)
            print("Mã nhân viên cuối cùng là " + str(Id))
        vid_cam = cv2.VideoCapture(0)
        face_detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        count = 0
        while(True):
                _, image_frame = vid_cam.read()

                gray = cv2.cvtColor(image_frame, cv2.COLOR_BGR2GRAY)
                faces = face_detector.detectMultiScale(gray, 1.3, 5)
                for (x,y,w,h) in faces:
                    cv2.rectangle(image_frame, (x,y), (x+w,y+h), (255,0,0), 2)

                    count += 1

                    cv2.imwrite("../../DataSet/ImageLibrary/User." + str(id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

                    cv2.imshow('frame', image_frame)

                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                elif count>100:
                    break
        vid_cam.release()
        cv2.destroyAllWindows()
def GetImageLocation(id,path):
    count = 0
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faceSamples = []
    ids = []
    for imagePath in imagePaths:
        # đọc ảnh
        image = cv2.imread(imagePath)
        # Convert ảnh ra mà xám
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # Lấy khuôn mặt xuất hiện trong khung hình
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        # ghi ảnh vào dữ liệu
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            # ghi ảnh khuôn mặt vào dataset
            cv2.imwrite("../../DataSet/ImageLibrary/User." + str(id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
        print(imagePath)
        cv2.imshow('frame', image)


