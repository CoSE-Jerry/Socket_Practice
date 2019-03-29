# load additional Python module
import socket
import time

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = "10.0.5.1"
# output hostname, domain name and IP address
print ("working on %s (%s) with %s" % (local_hostname, local_fqdn, ip_address))

# bind the socket to the port 23456
server_address = (ip_address, 23456)  
print ('starting up on %s port %s' % server_address)  
sock.bind(server_address)

# listen for incoming connections (server mode) with one connection at a time
sock.listen(1)

while True:  
    # wait for a connection
    print ('waiting for a connection')
    connection, client_address = sock.accept()

    try:
        # show who connected to us
        print ('connection from', client_address)

        f = open("recv.jpg",'wb')

        while (True):       
        # receive data and write it to file
            l = connection.recv(8192)
            i = 0
            st = time.time()
            while (l):
                i+=1
                f.write(l)
                l = connection.recv(8192)
            print (i)
            print (time.time()-st)
            
                
        f.close()
        
    finally:
        # Clean up the connection
        connection.close()
