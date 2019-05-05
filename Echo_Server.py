# load additional Python module
import socket

# create TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# retrieve local hostname
local_hostname = socket.gethostname()

# get fully qualified hostname
local_fqdn = socket.getfqdn()

# get the according IP address
ip_address = "10.0.5.2"
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

    while True:
        CMD = connection.recv(1024).decode("utf-8")
        
        if not CMD:
            break
        if(CMD=='A'):
            print("got A")
        elif(CMD=='Q'):
            break
        else:
            print(CMD)
    connection.close()
    if(CMD=='Q'):
        break

    """try:
        # show who connected to us
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
        
        
    finally:
        # Clean up the connection
        connection.close()"""
