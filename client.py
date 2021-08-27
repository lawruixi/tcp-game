#!/usr/bin/env python3 

# Python program to implement client side 
import socket
import sys
import threading
def valid_ip(address):
    l = address.split(".")
    if(len(l) != 4): return False

    try:
        for i in l:
            if(int(i) < 0 or int(i) > 255):
                return False
    except:
        return False
    return True
def valid_port(port):
    return port > 1024 and port < 65536

print("Welcome to the Arena!!!")
while(True):
    try:
        host = input("Enter host IP address: ").strip()
        port = int(input("Enter port number (1024-65535): ").strip())
        print("HOST: " + host)
        print("PORT: " + str(port))
        if(host == "" or port == ""):
            print("Connection cancelled.")
            sys.exit(0)
        if(not valid_ip(host) or not valid_port(port)):
            print("Invalid IP address / port number.")
            continue
        break
    except: 
        continue
    
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
HOST = host
PORT = port
server.connect((HOST, PORT))
 
print("Successfully connected! \n")

def send_msg():
    while True:
        message = sys.stdin.readline()
        server.send(message.encode("utf-8"))
        sys.stdout.write("<You> ")
        sys.stdout.write(message)
        sys.stdout.flush()
def recv_msg():
    while True:
        message = server.recv(2048)
        if(message != b""):
            print(message.decode("utf-8"))

threading.Thread(target=send_msg).start()  
threading.Thread(target=recv_msg).start()
