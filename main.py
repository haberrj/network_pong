#!/usr/bin/python3

# Author: Ron Haber
# Date: 22.5.2021
# This is the main script that will be run on the client side for running the game.

import pygame, sys
from pygame.locals import *
import Game.pong_class as pc
import Backend.network as network
import argparse

parser = argparse.ArgumentParser(description="Play pong with yourself or with friends. Add the server IP Address and Port.")
parser.add_argument("-i", "--ip", type=str, required=True, help="The IP address of the server.")
parser.add_argument("-p", "--port", type=int, required=True, help="The Port of the server to access.")

args = parser.parse_args()
ip_address = args.ip
port = args.port

# Available colours for render
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

def OrderUsers(data):
    '''Will order the user positions to be correct based on the received values.
    @param data: A list of lists of the received values from the server.
    @return user1_pos: A list with the position of user 1
    @return user2_pos: A list with the position of user 2
    @return user3_pos: A list with the position of user 3
    @return user4_pos: A list with the position of user 4
    '''
    user1_pos = [0,0]
    user2_pos = [0,0]
    user3_pos = [0,0]
    user4_pos = [0,0]
    for val in data:
        if(val[0] == 1):
            user1_pos[0] = val[1]
            user1_pos[1] = val[2]
        elif(val[0] == 2):
            user2_pos[0] = val[1]
            user2_pos[1] = val[2]
        elif(val[0] == 3):
            user3_pos[0] = val[1]
            user3_pos[1] = val[2]
        else:
            user4_pos[0] = val[1]
            user4_pos[1] = val[2]
    return user1_pos, user2_pos, user3_pos, user4_pos

def main():
    scores = [0,0,0,0]
    ball_pos = [0,0]
    running = True
    n = network.Network(ip_address, port)

    while(n.getP() is None):
        continue
    my_info = n.getP() # This is the received value from the server
    print("Connected to Server!")
    my_user = my_info[0][0]
    print("You are User", my_user)
    my_paddle_pos = my_info[0][1]
    data = my_paddle_pos
    num_users = 1
    game = pc.pong_class() # initialize it as 1 until it gets updated in the loop
    # spawn the ball
    game.spawn_ball(my_info[1])
    
    while(running):
        current_other_users = n.send(data)
        try:
            new_num_users = current_other_users[0][2] + current_other_users[1][2] + current_other_users[2][2] + 1
        except IndexError as e:
            print(e)
            continue
        ball_vel = current_other_users[-1] # It will be the last value
        if(new_num_users != num_users):
            print("A new user has joined.")
            num_users = new_num_users
            game = pc.pong_class()
            game.spawn_ball(ball_vel)
        game.canvas.fill(BLACK)
        pygame.draw.circle(game.canvas, WHITE, [game.WIDTH//2, game.HEIGHT//2], 70, 1)
        sorting_data = [current_other_users[0], current_other_users[1], current_other_users[2], [my_user, my_paddle_pos, 1]]
        user1, user2, user3, user4 = OrderUsers(sorting_data)
        game.game_setup(user1[0], user2[0], user3[0], user4[0])
        game.active_users(user1[1], user2[1], user3[1], user4[1])
        game.gameplay(ball_vel)
        for event in pygame.event.get():
            if(event.type == KEYDOWN):
                game.key_down(event, my_user)
            elif(event.type == KEYUP):
                game.key_up(event, my_user)
            elif(event.type == K_ESCAPE):
                pygame.quit()
                sys.exit()
        my_paddle_pos = game.paddle_pos[my_user - 1]
        data = my_paddle_pos
        pygame.display.flip()
        pygame.display.update()
        game.fps.tick(60)

main()