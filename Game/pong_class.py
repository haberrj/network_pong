#!/usr/bin/python3

# Author: Ron Haber
# Date: 22.5.2021
# A class to create the game for use within the network

import random
import pygame, sys
from pygame.locals import *

# Available colours for render
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

class pong_class(object):
    def __init__(self, width=600, height=600, ball_radius=20, pad_width=10, pad_height=100, num_of_users=2):
        '''Will initialize the game with specific parameters for use within the algorithm.
        @param width: An integer for the width of the game in pixels.
        @param height: An integer for the height of the game in pixels.
        @param ball_radius: An integer for the radius of the ball in pixels.
        @param pad_width: An integer for the width of the paddle in pixels.
        @param pad_height: An integer for the height of the paddle in pixels.
        @param num_of_users: An integer for the desired number of users (1-4).
        '''
        pygame.init()
        self.fps = pygame.time.Clock()
        # User defined values
        self.WIDTH = width
        self.HEIGHT = height
        self.BALL_RADIUS = ball_radius
        self.PAD_WIDTH = pad_width
        self.PAD_HEIGHT = pad_height
        self.HALF_PAD_WIDTH = self.PAD_WIDTH/2 # I will reverse PAD WIDTH and HEIGHT for users 3 and 4
        self.HALF_PAD_HEIGHT = self.PAD_HEIGHT/2
        if(type(num_of_users) != int):
            raise TypeError("num_of_users is expected to be an if integer type.")
        elif(num_of_users < 1 or num_of_users > 4):
            raise ValueError("num_of_users must be an integer between 1 and 4.")
        else:
            self.num_of_users = num_of_users
        # Other needed class values
        self.ball_pos = [0,0]
        self.ball_vel = [0,0]
        # Setting values for multiple paddles regardless of users
        self.paddle_vel = [0, 0, 0, 0]
        # Setting the paddle positions
        self.paddle_pos = [[0,0], [0,0], [0,0], [0,0]] # 1 is left, 2 is right, 3 is up, 4 is down
        # need to come up with a scoring system. It might be out of scope due to time restrictions so for now scores will be negative (i.e. loser based)
        self.scores = [0, 0, 0, 0] # Even if the last 2 values are not required it doesn't use much memory
        # Drawing elements
        self.canvas = pygame.display.set_mode((self.WIDTH, self.HEIGHT), 0, 32)
        pygame.display.set_caption('Network Based Pong')
        self.canvas.fill(BLACK)
        pygame.draw.circle(self.canvas, WHITE, [self.WIDTH//2, self.HEIGHT//2], 70, 1)

    def game_setup(self, user1, user2, user3, user4):
        '''Will setup the initial starting positions of each paddle if they exist based on the input.
        Once paddles are setup, the ball will be spawned.
        @param user1: A list with the position of user 1
        @param user2: A list with the position of user 2
        @param user3: A list with the position of user 3
        @param user4: A list with the position of user 4
        @param ball_vel: A list with the x and y velocities of the ball to be initialized
        '''
        self.paddle_pos[0] = user1 # Paddle 1 will always be initialized
        if(self.num_of_users > 1): # Cascading if statements since as the number is increased all other users are required
            self.paddle_pos[1] = user2
            if(self.num_of_users > 2):
                self.paddle_pos[2] = user3
                if(self.num_of_users == 4):
                    self.paddle_pos[3] = user4
    
    def spawn_ball(self, ball_vel):
        '''Will spawn the ball based on the position received from the server.
        @param ball_vel: A list of the velocities of the ball as outlined by the server.
        '''
        self.ball_vel = ball_vel
        self.ball_pos = [self.WIDTH/2, self.HEIGHT/2]

    def update_paddle_pos(self):
        '''This will update the paddle positions so that they are continuously updated and remain on screen.
        There is a difference between users 1 & 2 and users 3 & 4 since due to the nature of moving horizontally
        or vertically.
        '''
        counter = 0
        for paddle_i in self.paddle_pos:
            if(counter + 1 > self.num_of_users):
                break
            if(counter < 2): # for users 1 & 2
                if ((paddle_i[1] > self.HALF_PAD_HEIGHT) and (paddle_i[1] < self.HEIGHT - self.HALF_PAD_HEIGHT)):
                    paddle_i[1] += self.paddle_vel[counter]
                elif ((paddle_i[1] == self.HALF_PAD_HEIGHT) and (self.paddle_vel[counter] > 0)):
                    paddle_i[1] += self.paddle_vel[counter]
                elif ((paddle_i[1] == self.HEIGHT - self.HALF_PAD_HEIGHT) and (self.paddle_vel[counter] < 0)):
                    paddle_i[1] += self.paddle_vel[counter]
                else: # Stops the paddle from getting stuck at the bottom
                    if(paddle_i[1] > self.HEIGHT/2):
                        paddle_i[1] = self.HEIGHT - self.HALF_PAD_HEIGHT
                    else:
                        paddle_i[1] = self.HALF_PAD_HEIGHT
                pygame.draw.polygon(self.canvas, GREEN, 
                    [[paddle_i[0] - self.HALF_PAD_WIDTH, paddle_i[1] - self.HALF_PAD_HEIGHT], 
                    [paddle_i[0] - self.HALF_PAD_WIDTH, paddle_i[1] + self.HALF_PAD_HEIGHT], 
                    [paddle_i[0] + self.HALF_PAD_WIDTH, paddle_i[1] + self.HALF_PAD_HEIGHT], 
                    [paddle_i[0] + self.HALF_PAD_WIDTH, paddle_i[1] - self.HALF_PAD_HEIGHT]], 
                    0)
            else: # for users 3 & 4
                if ((paddle_i[0] > self.HALF_PAD_HEIGHT) and (paddle_i[0] < self.WIDTH - self.HALF_PAD_HEIGHT)):
                    paddle_i[0] += self.paddle_vel[counter]
                elif ((paddle_i[0] == self.HALF_PAD_HEIGHT) and (self.paddle_vel[counter] > 0)):
                    paddle_i[0] += self.paddle_vel[counter]
                elif ((paddle_i[0] == self.WIDTH - self.HALF_PAD_HEIGHT) and (self.paddle_vel[counter] < 0)):
                    paddle_i[0] += self.paddle_vel[counter]
                else: # Stops the paddle from getting stuck at the bottom
                    if(paddle_i[0] > self.WIDTH/2):
                        paddle_i[0] = self.WIDTH - self.HALF_PAD_HEIGHT
                    else:
                        paddle_i[0] = self.HALF_PAD_HEIGHT
                pygame.draw.polygon(self.canvas, GREEN, 
                    [[paddle_i[0] - self.HALF_PAD_HEIGHT, paddle_i[1] - self.HALF_PAD_WIDTH], 
                    [paddle_i[0] - self.HALF_PAD_HEIGHT, paddle_i[1] + self.HALF_PAD_WIDTH], 
                    [paddle_i[0] + self.HALF_PAD_HEIGHT, paddle_i[1] + self.HALF_PAD_WIDTH], 
                    [paddle_i[0] + self.HALF_PAD_HEIGHT, paddle_i[1] - self.HALF_PAD_WIDTH]], 
                    0)
            counter += 1

    def update_scores(self):
        '''Will update the score variables and draw the scores on the field based on
        the number participants in the game.
        '''
        system_font = pygame.font.SysFont("Comic Sans MS", 20) # Hope you guys like it ;)
        label_user1 = system_font.render("User 1 Score " + str(self.scores[0]), 1, YELLOW)
        label_user2 = system_font.render("User 2 Score " + str(self.scores[1]), 1, YELLOW)
        label_user3 = system_font.render("User 3 Score " + str(self.scores[2]), 1, YELLOW)
        label_user4 = system_font.render("User 4 Score " + str(self.scores[3]), 1, YELLOW)
        # Draw the scores on the board
        self.canvas.blit(label_user1, (2*self.PAD_WIDTH, self.HEIGHT/2))    
        if(self.num_of_users > 1):
            self.canvas.blit(label_user2, (self.WIDTH - 11*self.PAD_WIDTH, self.HEIGHT/2))
            if(self.num_of_users > 2):
                self.canvas.blit(label_user3, (self.WIDTH/2 - 4*self.PAD_WIDTH, 2*self.PAD_WIDTH))
                if(self.num_of_users > 3):
                    self.canvas.blit(label_user4, (self.WIDTH/2 - 4*self.PAD_WIDTH, self.HEIGHT - 3*self.PAD_WIDTH))

    def determine_walls(self):
        '''Will determine which walls the ball will bounce off of.
        '''
        # Check if less than 4 players, since with 4 players theres no walls
        if(self.num_of_users == 4):
            return
        elif(self.num_of_users < 4):
            if(int(self.ball_pos[1] >= self.HEIGHT + 1 - self.BALL_RADIUS)): # Bottom wall
                self.ball_vel[1] = -1 * self.ball_vel[1]
            if(self.num_of_users < 3):
                if(int(self.ball_pos[1] <= self.BALL_RADIUS)): # Top wall
                    self.ball_vel[1] = -1 * self.ball_vel[1]
                if(self.num_of_users < 2):
                    if((int(self.ball_pos[0] >= self.WIDTH + 1 - self.BALL_RADIUS))): # Right wall
                        self.ball_vel[0] = -1 * self.ball_vel[0]

    def determine_paddles(self, ball_vel):
        '''Will determine which walls have paddles and which score.
        @param ball_vel: A list containing the velocities of the ball.
        '''
        # Left side
        if((int(self.ball_pos[0]) <= self.BALL_RADIUS + self.PAD_WIDTH) and (int(self.ball_pos[1]) in range(int(self.paddle_pos[0][1]) - int(self.HALF_PAD_HEIGHT), int(self.paddle_pos[0][1]) + int(self.HALF_PAD_HEIGHT),1))):
            # Checking if the ball is within the area where the paddle is
            self.ball_vel[0] = -1.1 * self.ball_vel[0] # slightly increase the difficulty by 10%
            self.ball_vel[1] *= 1.1
        elif(int(self.ball_pos[0]) <= self.BALL_RADIUS + self.PAD_WIDTH):
            self.scores[0] += -1 
            self.spawn_ball(ball_vel)
        if(self.num_of_users > 1):
            # Right side
            if(int(self.ball_pos[0]) >= self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH) and (int(self.ball_pos[1]) in range(int(self.paddle_pos[1][1]) - int(self.HALF_PAD_HEIGHT),int(self.paddle_pos[1][1]) + int(self.HALF_PAD_HEIGHT),1)):
                self.ball_vel[0] = -1.1 * self.ball_vel[0]
                self.ball_vel[1] *= 1.1
            elif(int(self.ball_pos[0]) >= self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH):
                self.scores[1] += -1
                self.spawn_ball(ball_vel)
            if(self.num_of_users > 2):
                # Top side 
                if((int(self.ball_pos[1]) <= self.BALL_RADIUS + self.PAD_WIDTH) and (int(self.ball_pos[0]) in range(int(self.paddle_pos[2][0]) - int(self.HALF_PAD_HEIGHT), int(self.paddle_pos[2][0]) + int(self.HALF_PAD_HEIGHT), 1))):
                    self.ball_vel[1] = -1.1 * self.ball_vel[1]
                    self.ball_vel[0] *= 1.1
                elif(int(self.ball_pos[1]) <= self.BALL_RADIUS + self.PAD_WIDTH):
                    self.scores[2] += -1
                    self.spawn_ball(ball_vel)
                if(self.num_of_users > 3):
                    # Bottom side
                    if((int(self.ball_pos[1]) >= self.HEIGHT + 1 - self.BALL_RADIUS - self.PAD_WIDTH) and (int(self.ball_pos[0]) in range(int(self.paddle_pos[3][0]) - int(self.HALF_PAD_HEIGHT), int(self.paddle_pos[3][0]) + int(self.HALF_PAD_HEIGHT), 1))):
                        self.ball_vel[1] = -1.1 * self.ball_vel[1]
                        self.ball_vel[0] *= 1.1
                    elif(int(self.ball_pos[1]) >= self.HEIGHT + 1 - self.BALL_RADIUS - self.PAD_WIDTH):
                        self.scores[3] += -1
                        self.spawn_ball(ball_vel)

    def gameplay(self, ball_vel):
        '''Will draw the game on the screen and execute the game itself.
        @param ball_vel: A list containing the velocities of the ball sent from the server.
        '''
        self.update_paddle_pos()
        # Update the ball position
        self.ball_pos[0] += int(self.ball_vel[0])
        self.ball_pos[1] += int(self.ball_vel[1])
        pygame.draw.circle(self.canvas, RED, self.ball_pos, 20, 0)
        # Determine which sides are walls
        self.determine_walls()
        # Determine when the ball has hit a paddle
        self.determine_paddles(ball_vel)
        # Update the scores
        self.update_scores()

    def key_down(self, event, user):
        '''Will determine what happens when specific keys are pressed.
        Will need to be changed to incorporate networked systems but for
        now will remain local.
        User 1 = W & S
        User 2 = UP & DOWN
        User 3 = A & D
        User 4 = RIGHT & LEFT
        @param event: The key event captured.
        @param user: An integer representing the actual user.
        '''
        if(user < 3): # for user input 1 or 2
            if(event.key == K_UP):
                self.paddle_vel[user-1] = -8
            elif(event.key == K_DOWN):
                self.paddle_vel[user-1] = 8
        else:
            if(event.key == K_LEFT):
                self.paddle_vel[user-1] = -8
            elif(event.key == K_RIGHT):
                self.paddle_vel[user-1] = 8
    
    def key_up(self, event, user):
        '''Will determine what happens when the specific keys are released.
        Will need to be changed later to incorporate networking but will work
        for now for local purposes.
        @param event: The key event captured.
        @param user: An integer representing the actual user.
        '''
        if(event.key in (K_UP, K_DOWN)):
            self.paddle_vel[user-1] = 0
        elif(event.key in (K_LEFT, K_RIGHT)):
            self.paddle_vel[user-1] = 0