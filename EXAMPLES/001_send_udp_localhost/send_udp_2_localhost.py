#!/Library/Frameworks/Python.framework/Versions/3.10/bin/python3

# How Application sends data over network?
#
# Application provides following info to the OS kernel, via Socket API:
#    - data which has to be send;
#    - IPv4 or IPv6 to be used;
#    - UPD or TCP to be used
# Once data provided, OS kernel then packages it in necessary form
# to be send over the network

# This module contains info on
# how to work with OS sockets
import socket

DEST_IP = '127.0.0.1'
DEST_PORT = 9090
# Data to be send by your Application
XBS_DATA = b'So was it sent successfully?'

# Create a socket,
# which will be a "window" for your Application to the OS kernel
#    - AF_INET - use IPv4
#    - SOCK_DGRAM - use UDP
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send data to the socket, 
# created above
sock.sendto(XBS_DATA, (DEST_IP, DEST_PORT))
