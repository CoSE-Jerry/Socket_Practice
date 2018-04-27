import socket
from picamera import PiCamera
from threading import Thread
import time

host = ''
port = 5560
global interval = 0
global duration = 0

def setupServer():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Socket created.")
    try:
        s.bind((host, port))
    except socket.error as msg:
        print(msg)
    print("Socket bind comlete.")
    return s

def setupConnection():
    s.listen(1) # Allows one connection at a time.
    conn, address = s.accept()
    return conn

def CALL():
    reply = "CONNECTED"
    return reply

def dataTransfer(conn):
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        data = conn.recv(1024) # receive the data
        data = data.decode('utf-8')
        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split('-', 1)
        command = dataMessage[0]
        if command == 'CAM':
            interval = dataMessage[1]
            duration = dataMessage[2]
            reply = 'Interval '+str(interval) + ' Duration ' + str(duration)
            reply = 'Unknown Command'
            
        else:
            reply = 'Unknown Command'
            
        # Send the reply back to the client
        conn.sendall(str.encode(reply))
        print("Data has been sent!")
    conn.close()
class Hello5Program:  
    def __init__(self):
        self._running = True

    def terminate(self):  
        self._running = False  

    def run(self):
        global interval, duration
        while self._running:
            sleep(2)
            print("test")

#Create Class
FiveSecond = Hello5Program()
#Create Thread
FiveSecondThread = Thread(target=FiveSecond.run) 
#Start Thread 
FiveSecondThread.start()

s = setupServer()

while True:
    conn = setupConnection()
    dataTransfer(conn)
