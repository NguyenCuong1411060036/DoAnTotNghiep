import sys
from PyQt5 import QtWidgets, QtCore

from Controler.Export_CSV import Export_DiemDanh


class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 500, 300)
        self.setWindowTitle("PyQT tuts!")
        self.file_save()
    def file_save(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File','',"csv")
        print(name)
        file = open(name[0]+"."+name[1], 'w+')
        Export_DiemDanh(20, "28/5/2018", "3/6/2018",file)
        file.close()

def run():
    app = QtWidgets.QApplication(sys.argv)
    GUI = Window()
    sys.exit(app.exec_())


run()