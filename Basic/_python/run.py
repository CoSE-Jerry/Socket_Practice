import sys
import socket
import os

# This gets the Qt stuff
import PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *

PORT = 5560
HOST = '192.168.1.100'
UpperStat = [0] * 8
LowerStat = [0] * 8


# This is our window from QtCreator
import ABCD_UI


class Connection(QThread):
    
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))
        while True:
            command = input('Enter your command: ')
            s.send(str.encode(command))
            reply = s.recv(1024)
            print (reply.decode('utf-8'))
        s.close()
        
class PingLower(QThread):
    
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        global LowerStat, LowerReady
        LowerStat = [0] * 8
        for x in range(0, 7):
            hostname = "192.168.1.10" + str(x)
            response = os.system("ping -n 1 -w 1 " + hostname)
            if response == 0:
                LowerStat[x]=1

class PingUpper(QThread):
    
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        global UpperStat, UpperReady
        UpperStat = [0] * 8
        for x in range(0, 7):
            hostname = "192.168.1.20" + str(x)
            response = os.system("ping -n 1 -w 1 " + hostname)
            if response == 0:
                UpperStat[x]=1

# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, ABCD_UI.Ui_Demo):
# access variables inside of the UI's file
    def update(self):
        self.Update_Status.setText("Updating Status...")
        self.Update_Status.setEnabled(False)
        self.LowerStat_Thread = PingLower()
        self.LowerStat_Thread.start()
        self.UpperStat_Thread = PingUpper()
        self.UpperStat_Thread.start()

        self.LowerStat_Thread.finished.connect(lambda: self.UpdateLower())
        self.UpperStat_Thread.finished.connect(lambda: self.UpdateUpper())

    def connect(self):
        try:
            self.Connection_Thread = Connection()
            self.Connection_Thread.start()
        except:
            print("nope")
     
    def UpdateLower(self):
        for x in range(0, 7):
            if(LowerStat[x]==1):
                cmd = "self.Unit_%d_Label.setPixmap(QtGui.QPixmap(\"../_images/Green_button.png\"))"%x
                exec(cmd)
            else:
                cmd = "self.Unit_%d_Label.setPixmap(QtGui.QPixmap(\"../_images/stop-red.png\"))"%x
                exec(cmd)

    def UpdateUpper(self):
        for x in range(0, 7):
            xmod=x+8
            if(UpperStat[x]==1):
                cmd = "self.Unit_%d_Label.setPixmap(QtGui.QPixmap(\"../_images/Green_button.png\"))"%xmod
                exec(cmd)
            else:
                cmd = "self.Unit_%d_Label.setPixmap(QtGui.QPixmap(\"../_images/stop-red.png\"))"%xmod
                exec(cmd)
        self.Update_Status.setText("Update Status")
        self.Update_Status.setEnabled(True)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file
        self.update()
        self.connect()
        self.Update_Status.clicked.connect(lambda: self.update())
        

# I feel better having one of these
def main():
    # a new app instance
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()

    # without this, the script exits immediately.
    sys.exit(app.exec_())




# python bit to figure how who started This
if __name__ == "__main__":
    main()
