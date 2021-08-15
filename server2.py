#!/usr/bin/env python3 

# Python program to implement server side of chat room.
import socket
import select
import sys
import threading

def get_ip_address():
    #Gets ip address of the machine running the server by asking Google DNS. Man, what can't Google do these days?
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    res = s.getsockname()[0]
    s.close()
    return res

def get_free_port():
    #Generates a random available port to use.
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('', 0))
    addr, port = s.getsockname()
    s.close()
    return port

HOST = get_ip_address()
PORT = get_free_port()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) #Restart the TCP server to allow binding to the ports
server.bind((HOST, PORT))

print("Starting server at IP {0} on port {1}".format(HOST, PORT))

server.listen(100)
clients = []

def clientthread(conn, addr):
    print("Thread started.")
    while True:
        try:
            message = conn.recv(2048)
            if message:
                message_str = message.decode("utf-8")
                """prints the message and address of the
                user who just sent the message on the server
                terminal"""
                print("<" + addr[0] + ">  " + message_str, end='')

                # Calls broadcast function to send message to all
                message_to_send = "<" + addr[0] + ">  " + message_str
                broadcast(message_to_send.encode("utf-8"), conn)

            else:
                """message may have no content if the connection
                is broken, in this case we remove the connection"""
                remove(conn)

        except Exception as e:
            print(e)
            continue

"""Using the below function, we broadcast the message to all
clients who's object is not the same as the one sending
the message """
def broadcast(message, connection):
    for client in clients:
        if client != connection:
            try:
                client.send(message)
            except:
                client.close()

                # if the link is broken, we remove the client
                remove(client)

"""The following function simply removes the object
from the list that was created at the beginning of
the program"""
def remove(connection):
    if connection in clients:
        clients.remove(connection)

while True:
    """Accepts a connection request and stores two parameters,
    conn which is a socket object for that user, and addr
    which contains the IP address of the client that just
    connected"""
    conn, addr = server.accept()

    """Maintains a list of clients for ease of broadcasting
    a message to all available people in the chatroom"""
    clients.append(conn)

    # prints the address of the user that just connected
    print(addr[0] + " connected")

    # creates and individual thread for every user
    # that connects
    threading.Thread(target=clientthread,args=(conn,addr)).start()	

conn.close()
server.close()

