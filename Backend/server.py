#!/usr/bin/python3

# Author: Ron Haber
# Date: 22.5.2021
# This script will be server based for communication with users.

import socket, sys, pickle
from _thread import *
import random

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

def threaded_client(conn, player):
    # Will need to figure out what to send for player
    conn.send(pickle.dumps([players[player], ball_vel]))
    reply = ''
    while(True):
        try:
            data = pickle.loads(conn.recv(2048))
            players[player][1] = data # The position of the player
            players[player][2] = 1
            if not data:
                print("Disconnected")
                break
            else:
                if(player == 0): # user1
                    reply = [players[1], players[2], players[3], ball_vel]
                elif(player == 1): # user2
                    reply = [players[0], players[2], players[3], ball_vel]
                elif(player == 2): # user3 
                    reply = [players[0], players[1], players[3], ball_vel]
                else: # user4
                    reply = [players[0], players[1], players[2], ball_vel]
                print("Received: ", data)
                # print("Sending: ", reply)
            conn.sendall(pickle.dumps(reply))
        except:
            break
    print("Lost Connection")
    conn.close()

server = '195.90.200.226' # I have a VPS and this is the IP address for it
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen()
print("Waiting for connection of client. Server has been started.")

# This will be the initial position of every paddle.
# Each array is broken up as [user_num, paddle position, connected]
ball_vel = [random.randrange(2,4), random.randrange(1,3)]
players = [[1, [4, 300], 0], [2, [596, 300], 0], [3, [300, 4], 0], [4, [300, 596], 0]]


current_player = 0
total = []
lst = []
while(True):
    conn, address = s.accept()
    print("Connected to:", address)
    total.append(address)
    lst.append(conn)
    lst.append(address)
    ball_vel = [random.randrange(2,4), random.randrange(1,3)]
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1
    # print(len(total))
    # if(len(total) > 0):
    #     conn1 = lst[0]
    #     address1 = lst[1]
    #     start_new_thread(threaded_client, (conn1, current_player))
    #     current_player += 1
    # if(len(total) > 1):
    #     conn2 = lst[2]
    #     address2 = lst[3]
    #     start_new_thread(threaded_client, (conn2, current_player))
    #     current_player += 1
    # if(len(total) > 2):
    #     conn3 = lst[4]
    #     address3 = lst[5]
    #     start_new_thread(threaded_client, (conn3, current_player))
    #     current_player += 1
    # if(len(total) > 3):
    #     conn4 = lst[6]
    #     address4 = lst[7]
    #     start_new_thread(threaded_client, (conn4, current_player))
    #     current_player += 1