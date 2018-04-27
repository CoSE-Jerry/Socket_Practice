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

UpperStat = [0] * 8
LowerStat = [0] * 8
UpperConn = [1] * 8
LowerConn = [1] * 8
title=""


# This is our window from QtCreator
import ABCD_UI


class ConnectionUpdate(QThread):
    
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):

        for x in range(0, 7):
            if(LowerStat[x]==1):
                HOST="192.168.1.10"+str(x)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((HOST,PORT))
            s.send(str.encode("CURR"))
            reply = s.recv(1024)
            print (reply.decode('utf-8'))
            s.close()
        except:
            print("nope")

class PingConnection(QThread):
    
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        global LowerConn,Upperconn
        for x in range(0, 7):
            if(LowerStat[x]==1):
                HOST="192.168.1.10"+str(x)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect((HOST,PORT))
                    s.close()
                    print("connection successful" + HOST)
                except:
                    LowerConn[x]=0
                    print("connection failed" + HOST)
        for x in range(0, 7):
            if(UpperStat[x]==1):
                HOST="192.168.1.20"+str(x)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    s.connect((HOST,PORT))
                    s.close()
                    print("connection successful" + HOST)
                except:
                    LowerConn[x]=0
                    print("connection failed" + HOST)
        
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
    def IST_Edit(self):
        global title
        title = self.IST_Editor.text()
        print(title)
        
    def IST_Change(self):
        
        self.ICI_spinBox.setEnabled(True)
        if(len(self.IST_Editor.text())==0):
            self.ICI_spinBox.setEnabled(False)
            self.ISD_spinBox.setEnabled(False)

    def Update(self):
        self.Update_Status.setText("Updating Status...")
        self.Update_Status.setEnabled(False)
        self.LowerStat_Thread = PingLower()
        self.LowerStat_Thread.start()
        self.UpperStat_Thread = PingUpper()
        self.UpperStat_Thread.start()

        self.LowerStat_Thread.finished.connect(lambda: self.UpdateLower())
        self.UpperStat_Thread.finished.connect(lambda: self.UpdateUpper())
        

    def ConnectUpdate(self):
        try:
            self.Connection_Thread = ConnectionUpdate()
            self.Connection_Thread.start()
            self.Connection_Thread.finished.connect(lambda: self.ConnectionTest())
        except:
            print("nope")
            
    def ConnectionTest(self):
        self.Ping_Connection_Thread = PingConnection()
        self.Ping_Connection_Thread.start()
        self.Ping_Connection_Thread.finished.connect(lambda: self.ConnectionUIUpdate())
     
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
        self.IST_Editor.setEnabled(True)
        self.ConnectUpdate()

    def ConnectionUIUpdate(self):
        for x in range(0, 7):
            if(LowerConn[x]==0):
                cmd = "self.Unit_%d_Label.setEnabled(False)"%x
                exec(cmd)

    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self) # gets defined in the UI file
        self.Update()
        self.Update_Status.clicked.connect(lambda: self.Update())
        self.IST_Editor.editingFinished.connect(lambda: self.IST_Edit())
        self.IST_Editor.textChanged.connect(lambda: self.IST_Change())
        

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
