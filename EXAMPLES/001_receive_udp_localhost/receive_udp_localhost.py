#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3

# How Application receives data over network?


# This module contains info on
# how to work with OS sockets
import socket

# Listen to all IP adresses, that are assigned to the server
# (as server can have multiple network interface cards -> multiple IP adresses)
IP_ON_SERVER_TO_LISTEN = '0.0.0.0'
PORT_ON_SERVER_TO_LISTEN = 9090


# Create a socket,
# which will be a "window" for your Application to the OS kernel
#    - AF_INET - use IPv4
#    - SOCK_DGRAM - use UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Bind IP and Port to a socket
#
# When you open the `Socket` at `OS` level, you need to bind it to:
#    - `IP` adress (as server can have multiple `network interface cards`, 
#       so multiple `IP` adresses. and `App` can listen all of them or just specified ones; 
#       you define it via such bind);
#    - `Port` number (thus `OS` knows to which `App` give received package);
sock.bind((IP_ON_SERVER_TO_LISTEN, PORT_ON_SERVER_TO_LISTEN))

while True:
    # Define received data
    #    - ip - sender's IP adress;
    #    - port - sender's Port number;
    data, (ip, port) = sock.recvfrom(1024)

    print("Sender: {} and Port: {}".format(ip, port))
    print("Received message: {}".format(data))
    print("")
