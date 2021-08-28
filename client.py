#!/usr/bin/env python3 

# Python program to implement client side 
import socket
import sys
import os
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
    try:
        return int(port) > 1024 and int(port) < 65536;
    except:
        return False;

def valid_option(option):
    valid_dict = {"1": True,
            "2": True,
            "3": True
            }
    return valid_dict.get(option, False);

print("=" * 45);
print("Welcome to the Arena!!!")
print("=" * 45);
print("Select Option:")
print("1. Single Player (Experimental)");
print("2. Multiplayer");
print("3. Exit");

option = input();
while(not valid_option(option)):
    print("Invalid option.")
    option = input();

if(option == "3"):
    sys.exit(0)

if(option == "2"):
    while(True):
        try:
            host = input("Enter host IP address: ").strip()
            port = input("Enter port number (1024-65535): ").strip()
            if(host == "" or port == ""):
                print("Connection cancelled.")
                sys.exit(0)
            if(not valid_ip(host) or not valid_port(port)):
                print("Invalid IP address / port number.")
                continue
            break
        except Exception as e: 
            print(e)
            continue
        
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = host
    PORT = int(port)
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
            if(message == b"!TERMINATE"):
                print("Disconnected from server.")
                os._exit(0)
            elif(message != b""):
                print(message.decode("utf-8"))

    threading.Thread(target=send_msg).start()  
    threading.Thread(target=recv_msg).start()

