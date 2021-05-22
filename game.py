#!/usr/bin/python3

# Author: Ron Haber
# Date: 22.5.2021
# This will help to build the requirements for the game itself.

import random
import pygame, sys
from pygame.locals import *

# Write all of this as a class to make it cleaner

pygame.init()
fps = pygame.time.Clock()

# Avaiable colours for render
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Game variables/settings
WIDTH = 600
HEIGHT = 600
BALL_RADIUS = 20
PAD_WIDTH = 10
PAD_HEIGHT = 100
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
ball_pos = [0,0]
ball_vel = [0,0]
paddle1_vel = 0 # Will eventually add player 3 and 4
paddle2_vel = 0
l_score = 0
r_score = 0
u_score = 0
d_score = 0

# Display declarations
window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
pygame.display.set_caption('Network Based Pong')

def spawn_ball(side):
    '''Will spawn the ball on a given side. [up=0, down=1, right=2, left=3]
    @param side: An integer between 0 and 3 which will choose the spawn
                of the ball.
    '''
    global ball_pos, ball_vel
    ball_pos = [WIDTH/2, HEIGHT/2]
    horz = random.randrange(2,4)
    vert = random.randrange(1,3)

    if(side == 0): # up
        ball_vel = [vert, -1 * horz]
    elif(side == 1): # down
        ball_vel = [-1 * vert, -1 * horz]
    elif(side == 3): # right
        ball_vel = [horz, -1 * vert]
    else: # left
        ball_vel = [-1 * horz, -1 * vert]

def init():
    '''Will initialize the game.
    '''
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel, l_score, r_score, u_score, d_score
    global score1, score2
    paddle1_pos = [HALF_PAD_WIDTH - 1, HEIGHT/2]
    paddle2_pos = [WIDTH + 1 - HALF_PAD_WIDTH, HEIGHT/2]
    l_score = 0
    r_score = 0
    u_score = 0
    d_score = 0
    spawn_ball(random.randrange(0,4))

def draw_game(canvas):
    '''Will draw the game on the screen.
    @param canvas: The pygame object that was defined.
    '''
    global paddle1_pos, paddle2_pos, ball_pos, ball_vel, l_score, r_score

    canvas.fill(BLACK)
    pygame.draw.line(canvas, WHITE, [WIDTH/2, 0], [WIDTH/2, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1)
    pygame.draw.line(canvas, WHITE, [WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1)
    pygame.draw.circle(canvas, WHITE, [WIDTH//2, HEIGHT//2], 70, 1)

    # Updates the paddle's vertical position and keeps the paddle on the screen
    # Maybe create a function to do this for each available paddle

    if ((paddle1_pos[1] > HALF_PAD_HEIGHT) and (paddle1_pos[1] < HEIGHT - HALF_PAD_HEIGHT)):
        paddle1_pos[1] += paddle1_vel
    elif ((paddle1_pos[1] == HALF_PAD_HEIGHT) and (paddle1_vel > 0)):
        paddle1_pos[1] += paddle1_vel
    elif ((paddle1_pos[1] == HEIGHT - HALF_PAD_HEIGHT) and (paddle1_vel < 0)):
        paddle1_pos[1] += paddle1_vel
    else: # Stops the paddle from getting stuck at the bottom
        if(paddle1_pos[1] > HEIGHT/2):
            paddle1_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        else:
            paddle1_pos[1] = HALF_PAD_HEIGHT

    if ((paddle2_pos[1] > HALF_PAD_HEIGHT) and (paddle2_pos[1] < HEIGHT - HALF_PAD_HEIGHT)):
        paddle2_pos[1] += paddle2_vel
    elif ((paddle2_pos[1] == HALF_PAD_HEIGHT) and (paddle2_vel > 0)):
        paddle2_pos[1] += paddle2_vel
    elif ((paddle2_pos[1] == HEIGHT - HALF_PAD_HEIGHT) and (paddle2_vel < 0)):
        paddle2_pos[1] += paddle2_vel
    else: # Stops the paddle from getting stuck at the bottom
        if(paddle2_pos[1] > HEIGHT/2):
            paddle2_pos[1] = HEIGHT - HALF_PAD_HEIGHT
        else:
            paddle2_pos[1] = HALF_PAD_HEIGHT
    
    # Update the ball position
    ball_pos[0] += int(ball_vel[0])
    ball_pos[1] += int(ball_vel[1])

    # Update all components
    pygame.draw.circle(canvas, RED, ball_pos, 20, 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT], [paddle1_pos[0] - HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] + HALF_PAD_HEIGHT], [paddle1_pos[0] + HALF_PAD_WIDTH, paddle1_pos[1] - HALF_PAD_HEIGHT]], 0)
    pygame.draw.polygon(canvas, GREEN, [[paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT], [paddle2_pos[0] - HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] + HALF_PAD_HEIGHT], [paddle2_pos[0] + HALF_PAD_WIDTH, paddle2_pos[1] - HALF_PAD_HEIGHT]], 0)

    # Check the ball collisions on the walls without players
    if (int(ball_pos[1]) <= BALL_RADIUS):
        ball_vel[1] = - ball_vel[1]
    if (int(ball_pos[1]) >= HEIGHT + 1 - BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]

    # Check the ball collisions on the gutters and user paddles
    # Make a function to do this for every side
    try:
        if(int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH) and (int(ball_pos[1]) in range(int(paddle1_pos[1]) - int(HALF_PAD_HEIGHT),int(paddle1_pos[1]) + int(HALF_PAD_HEIGHT),1)):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        elif(int(ball_pos[0]) <= BALL_RADIUS + PAD_WIDTH):
            r_score += 1
            spawn_ball(2)
    except TypeError:
        print("Error in paddle 1")
        print(int(ball_pos[0]))
        print(ball_pos[1])
        print(paddle1_pos[1])
        sys.exit()
    try:
        if(int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH) and (int(ball_pos[1]) in range(int(paddle2_pos[1]) - int(HALF_PAD_HEIGHT),int(paddle2_pos[1]) + int(HALF_PAD_HEIGHT),1)):
            ball_vel[0] = -ball_vel[0]
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        elif int(ball_pos[0]) >= WIDTH + 1 - BALL_RADIUS - PAD_WIDTH:
            l_score += 1
            spawn_ball(3)
    except TypeError:
        print("Error in paddle 2")
        print(int(ball_pos[0]))
        print(ball_pos[1])
        print(paddle2_pos[1])
        sys.exit()
    
    # Update the scores
    game_font1 = pygame.font.SysFont("Comic Sans MS", 20) # def not Comic Sans
    label1 = game_font1.render("Score "+str(l_score), 1, (255,255,0))
    canvas.blit(label1, (50,20))

    game_font2 = pygame.font.SysFont("Comic Sans MS", 20)
    label2 = game_font2.render("Score "+str(r_score), 1, (255,255,0))
    canvas.blit(label2, (470, 20))  

#keydown handler
# This will be changed to match to individual computers
def keydown(event):
    global paddle1_vel, paddle2_vel
    
    if event.key == K_UP:
        paddle2_vel = -8
    elif event.key == K_DOWN:
        paddle2_vel = 8
    elif event.key == K_w:
        paddle1_vel = -8
    elif event.key == K_s:
        paddle1_vel = 8

#keyup handler
def keyup(event):
    global paddle1_vel, paddle2_vel
    
    if event.key in (K_w, K_s):
        paddle1_vel = 0
    elif event.key in (K_UP, K_DOWN):
        paddle2_vel = 0

init()

# main
while(True):
    draw_game(window)
    for event in pygame.event.get():
        if(event.type == KEYDOWN):
            keydown(event)
        elif(event.type == KEYUP):
            keyup(event)
        elif(event.type == QUIT):
            pygame.quit()
            sys.exit()
    pygame.display.update()
    fps.tick(60)