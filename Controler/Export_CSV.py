import csv
import os
import this
from macpath import expanduser

from PyQt5 import QtWidgets
from PyQt5.uic.properties import QtWidgets

Ngay= None
from Controler.DataConnect.ConectToDatabase import create_connection
def ExportCSV():
    conn  = create_connection("DataConnect/DiemDanhDatabse.db")
    conn.text_factory = str ## my current (failed) attempt to resolve this
    cur = conn.cursor()
    data = cur.execute("select * from DiemDanh")

    f = open("Report.csv", "w+")
    for row in data :
        numberCol = len(row)
        indexCol = 0
        for col in row:
            indexCol +=1
            if indexCol == numberCol:
                f.write(str(col) + "\n")
            else:
                f.write(str(col) + ",")

def Export_DiemDanh(MaNV,StartDate,EndDate,file):
    conn = create_connection("DataConnect/DiemDanhDatabse.db")
    conn.text_factory = str  ## my current (failed) attempt to resolve this
    cur = conn.cursor()
    data = cur.execute("select Ngay,Gio from DiemDanh where MaNV="+str(MaNV)+" and Ngay >= '"+str(StartDate)+"' and Ngay <= '"+str(EndDate)+"'")
    file.write("Date,In,Out,In,Out,In,Out,In,Out,In,Out,In,Out,In,Out,In,Out,In,Out,In,Out\n")
    index =0
    for row in data:
        if index == 0 :
            this.Ngay = row[0]
            file.write(str(this.Ngay) + ",")
            index +=1
        else:
            GetTimeViaDay(row,file)

def GetTimeViaDay(row,file):
    if row[0] == this.Ngay:
        file.write(row[1]+",")
    else:
        file.write("\n")
        this.Ngay = row[0]
        file.write(str(this.Ngay) + ",")
def file_save():
    name = QtWidgets.QFileDialog.getSaveFileName( 'Save File', '', "csv")

    file = open(name[0] + "." + name[1] , 'w+')
    text = "abc"
    file.write(text)
    file.close()










