# load additional Python modules
import socket  

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = "10.0.5.2"

# bind the socket to the port 23456, and connect
server_address = (ip_address, 23456)

sock.connect(server_address)  
print ("connecting to %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

while True:
    data = input("Enter the data to be sent : ")
    sock.sendall(data.encode())
    if(data == 'A')
        print ('connection from', client_address)
        f = open("recv.jpg",'wb')
        
        while (True):       
        # receive data and write it to file
            l = connection.recv(16384)
            print ("Receiving Data")
            if not l:
                break
            f.write(l)
        print ("Receiving Done")
        f.close()

"""f = open ("trans.jpg", "rb")
l = f.read(1024)
while (l):
    sock.send(l)
    l = f.read(1024)"""


# close connection
sock.close()  
