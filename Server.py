import socket
import thread
from picamera import PiCamera

host = ''
port = 5560
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
    # A big loop that sends/receives data until told not to.
    while True:
        # Receive the data
        data = conn.recv(1024) # receive the data
        data = data.decode('utf-8')
        # Split the data such that you separate the command
        # from the rest of the data.
        dataMessage = data.split('-', 2)
        command = dataMessage[0]
        if command == 'CAM':
            interval = dataMessage[1]
            duration = dataMessage[2]
            reply = 'Interval '+str(interval) + ' Duration ' + str(duration)
            
        else:
            reply = 'Unknown Command'
            
        # Send the reply back to the client
        conn.sendall(str.encode(reply))
        print("Data has been sent!")
    conn.close()

def socket_connect( threadName):
    s = setupServer()
    while True:
        conn = setupConnection()
        dataTransfer(conn)

thread.start_new_thread( socket_connect, "Thread_1" )

