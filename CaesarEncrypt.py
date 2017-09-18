# ==============================================================================================
# Project    = Interface Enkripsi Caesar Pada Arduino Nano Menggunakan Python3 dan Qt5
# Author     = I Wayan Adiyasa
# NIM        = 16/404567/PTK/10984
# Dosen      = Agus Bejo
# ==============================================================================================

import sys
from PyQt5 import QtWidgets,uic
import serial, time

qtCreatorFile = "CaesarEncrypt.ui"
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)
 
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # Set title pada form
        self.setWindowTitle('Enkripsi Caesar with Arduino')

        # Inisialisasi variabel yang akan digunakan
        self.dataTX = bytearray(7)
        self.Enkripsi = bytearray(1)
        self.Key = bytearray(25)

        # Inisialisasi komponent pada file UI
        self.pbConnect.clicked.connect(self.BukaSerial)
        self.pbOpen.clicked.connect(self.BukaPassword)
        self.pbWrite.clicked.connect(self.TulisPassword)

    def BukaSerial(self):
        if self.pbConnect.text()=='Connect':
            #Nama serial "COM7" dapat diganti dengan nama port serial yang lain
            #Baudrate "115200" disesuaikan dengan baudrate yang digunakan pada arduino
            self.ser = serial.Serial("COM7", "115200", timeout=0.2)
            if self.ser.isOpen():
                self.pbConnect.setText('Disconnect')
                self.txtLog.append("Buka Serial Port COM21... OK")
                self.pbOpen.setEnabled(True)
                self.pbWrite.setEnabled(True)
                self.txtPasswordOpen.setEnabled(True)
                self.txtPasswordWrite.setEnabled(True)
                self.numShiftOpen.setEnabled(True)
                self.numShiftWrite.setEnabled(True)
            else:
                self.txtLog.append("Gak bisa buka serial port")
        else:
            if self.ser.isOpen():
                self.ser.close()
                self.pbConnect.setText('Connect')
                self.txtLog.append("Tutup Serial Port COM21... OK")
                self.pbOpen.setEnabled(False)
                self.pbWrite.setEnabled(False)
                self.txtPasswordOpen.setEnabled(False)
                self.txtPasswordWrite.setEnabled(False)
                self.numShiftOpen.setEnabled(False)
                self.numShiftWrite.setEnabled(False)
                
    def BukaPassword(self):
        self.dataTX = bytes(b'Opening')
        self.Enkripsi = bytes(str(self.numShiftOpen.value()).encode())
        self.Key = str(self.txtPasswordOpen.text()).encode()
        self.txtLog.append("===================================================")
        self.txtLog.append("Data dikirim  : ")
        self.txtLog.append("     Status   : " + (self.dataTX).decode())
        self.txtLog.append("     Enkripsi : " + (self.Enkripsi).decode())
        self.txtLog.append("     Password : " + (self.Key).decode())
        self.ser.write(self.dataTX + self.Enkripsi + self.Key)
        time.sleep(1)

        line = ''                                       #Wajib diisi untuk menentukan variabel "line" adalah string
        for xLine in range(0, 7):                       #Jumlah line yang diterima berdasarkan jumlah line yang dikirim arduino
            line += (self.ser.readline()).decode()
        self.txtLog.append(line)                        #Update data pada log di luar for. Di dalam for menyebabkan line akan loncat 1 line (kosong 1 line setiap readline
        time.sleep(1)
        self.ser.close
        
    def TulisPassword(self):
        self.dataTX = bytes(b'Writing')
        self.Enkripsi = bytes(str(self.numShiftOpen.value()).encode())
        self.Key = str(self.txtPasswordOpen.text()).encode()
        self.txtLog.append("===================================================")
        self.txtLog.append("Data dikirim  : ")
        self.txtLog.append("     Status   : " + (self.dataTX).decode())
        self.txtLog.append("     Enkripsi : " + (self.Enkripsi).decode())
        self.txtLog.append("     Password : " + (self.Key).decode())
        self.ser.write(self.dataTX + self.Enkripsi + self.Key)
        time.sleep(1)

        line = ''                                       #Wajib diisi untuk menentukan variabel "line" adalah string
        for xLine in range(0, 7):                       #Jumlah line yang diterima berdasarkan jumlah line yang dikirim arduino
            line += (self.ser.readline()).decode()
        self.txtLog.append(line)                        #Update data pada log di luar for. Di dalam for menyebabkan line akan loncat 1 line (kosong 1 line setiap readline
        time.sleep(1)
        self.ser.close
    

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())
