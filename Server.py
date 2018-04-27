import socket
from picamera import PiCamera
from threading import Thread
from time import sleep

host = ''
port = 5560
title = ""
email = ""
interval = 0
duration = 0

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
    global interval, duration, title, email
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        data = conn.recv(1024) # receive the data
        data = data.decode('utf-8')
        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split('-', 5)
        command = dataMessage[0]
        if command == 'CURR':
            reply = title+"-"+str(interval)+"-"+str(duration)+"-"+email
        elif command == 'CAM':
            reply = "got it"
            title = dataMessage[1]
            #interval = dataMessage[2]
            #duration = dataMessage[3]
            #email = dataMessage[4]
            
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
            print('Interval '+str(interval) + ' Duration ' + str(duration))

#Create Class
FiveSecond = Hello5Program()
#Create Thread
FiveSecondThread = Thread(target=FiveSecond.run) 
#Start Thread 
FiveSecondThread.start()

s = setupServer()

while True:
    while True:
        try:
            conn = setupConnection()
            dataTransfer(conn)
        except socket.error as msg:
            print("dead")
        
