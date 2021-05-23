#!/usr/bin/python3

# Author: Ron Haber
# Date: 22.5.2021
# This script will be server based for communication with users.

import socket, pickle
from _thread import *
import random, argparse

parser = argparse.ArgumentParser(description="The server script for the pong game. Add the server IP Address and Port.")
parser.add_argument("-i", "--ip", type=str, required=True, help="The IP address of the server.")
parser.add_argument("-p", "--port", type=int, required=True, help="The Port of the server to access.")

args = parser.parse_args()
server = args.ip
port = args.port

def threaded_client(conn, player):
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
                elif(player == 3): # user4
                    reply = [players[0], players[1], players[2], ball_vel]
                else:
                    reply = '' # Will prevent a 5th player from joining the game
                print("Received from Player", player, ":", data)
                print("Sending to Player", player, ':', reply)
            conn.sendall(pickle.dumps(reply))
        except:
            break
    players[player] = default_players[player] # resets the player for the rest
    print("Lost Connection to Client: ", player + 1)
    conn.close()

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
default_players = [[1, [4, 300], 0], [2, [596, 300], 0], [3, [300, 4], 0], [4, [300, 596], 0]]
connected_players = [0, 0, 0, 0]

current_player = 0
total = []
lst = []
while(True):
    conn, address = s.accept()
    print("Connected to:", address)
    ball_vel = [random.randrange(2,4), random.randrange(1,3)]
    start_new_thread(threaded_client, (conn, current_player))
    current_player += 1