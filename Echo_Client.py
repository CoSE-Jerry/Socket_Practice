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
    datas = input("Enter the data to be sent : ")
    sock.sendall(datas.encode())
    if(datas == 'A'):
        '''f = open("recv.jpg",'wb')

        l = sock.recv(1024)
        i=0
        while (l):       
        # receive data and write it to file
            f.write(l)
            l = sock.recv(1024)
            print (i)
            i+=1
        print ("Receiving Done")
        f.close()'''




        with open('recv.jpg', 'wb') as f:
            print('file opened')
            while True:
                print('receiving data...')
                data = sock.recv(1024)
                print('data=%s', (data))
                if not data:
                    break
        # write data to a file
                f.write(data)

f.close()








"""f = open ("trans.jpg", "rb")
l = f.read(1024)
while (l):
    sock.send(l)
    l = f.read(1024)"""


# close connection
sock.close()  
