#!/usr/bin/python3

# Author: Ron Haber
# Date: 22.5.2021
# This script will be server based for communication with users.

import socket, sys, pickle
from _thread import *
from random import randint

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

def threaded_client(conn, player):
    # Will need to figure out what to send for player
    conn.send(pickle.dumps(player))
    reply = ''
    while(True):
        try:
            data = pickle.loads(conn.recv(2048))
            # insert data

            if not data:
                print("Disconnected")
                break
            else:
                if(player == 1):
                    reply = "player1"
                elif(player == 2):
                    reply = "player2"
                elif(player == 3):
                    reply = "player3"
                else:
                    reply = "player4"
                print("Received: ", data)
                print("Sending: ", reply)
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost Connection")
    conn.close()

server = '195.90.200.226' # I have a VPS and this is the IP address for it
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind(server, port)
except socket.error as e:
    print(e)

s.listen()
print("Waiting for connection of client. Server has been started.")

current_player = 0
total = []
lst = []
while(True):
    conn, address = s.accept()
    print("Connected to:", address)
    total.append(address)
    lst.append(conn)
    lst.append(address)
    if(len(total) > 0):
        conn1 = lst[0]
        address1 = lst[1]
        start_new_thread(threaded_client, (conn1, current_player))
        current_player += 1
    if(len(total) > 1):
        conn2 = lst[2]
        address2 = lst[3]
        start_new_thread(threaded_client, (conn1, current_player))
        current_player += 1
    if(len(total) > 2):
        conn3 = lst[4]
        address3 = lst[5]
        start_new_thread(threaded_client, (conn1, current_player))
        current_player += 1
    if(len(total) > 3):
        conn4 = lst[6]
        address4 = lst[7]
        start_new_thread(threaded_client, (conn1, current_player))
        current_player += 1
