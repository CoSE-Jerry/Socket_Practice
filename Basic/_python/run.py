# always seem to need this
import sys
import socket
 
# This gets the Qt stuff
import PyQt5
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
 
# This is our window from QtCreator
import ABCD_UI

class Camera(QThread):
    
    def __init__(self):
        QThread.__init__(self)

    def __del__(self):
        self._running = False

    def run(self):
        HOST = '192.168.1.25'
        PORT = 5560
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST,PORT))

        while True:
            command = input('Enter your command: ')
            s.send(str.encode(command))
            reply = s.recv(1024)
            print (reply.decode('utf-8'))
        s.close()
 
# create class for our Raspberry Pi GUI
class MainWindow(QMainWindow, ABCD_UI.Ui_Demo):
 # access variables inside of the UI's file
 def __init__(self):
     super(self.__class__, self).__init__()
     self.setupUi(self) # gets defined in the UI file
     self.Camera_Thread = Camera()
     self.Camera_Thread.start();
 
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
