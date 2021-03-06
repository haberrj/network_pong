#!/usr/bin/python3

# Author: Ron Haber
# Date: 22.5.2021
# A class to create the game for use within the network

import pygame
from pygame.locals import *

# Available colours for render
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

class pong_class(object):
    def __init__(self, width=600, height=600, ball_radius=20, pad_width=10, pad_height=100):
        '''Will initialize the game with specific parameters for use within the algorithm.
        @param width: An integer for the width of the game in pixels.
        @param height: An integer for the height of the game in pixels.
        @param ball_radius: An integer for the radius of the ball in pixels.
        @param pad_width: An integer for the width of the paddle in pixels.
        @param pad_height: An integer for the height of the paddle in pixels.
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
        # Setting the availability of the paddles based on the user
        self.paddle_availability = [0, 0, 0, 0]
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
        self.paddle_pos[1] = user2
        self.paddle_pos[2] = user3
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
        if(self.paddle_availability[0] == 1): # user 1
            if ((self.paddle_pos[0][1] > self.HALF_PAD_HEIGHT) and (self.paddle_pos[0][1] < self.HEIGHT - self.HALF_PAD_HEIGHT)):
                self.paddle_pos[0][1] += self.paddle_vel[0]
            elif ((self.paddle_pos[0][1] == self.HALF_PAD_HEIGHT) and (self.paddle_vel[0] > 0)):
                self.paddle_pos[0][1] += self.paddle_vel[0]
            elif ((self.paddle_pos[0][1] == self.HEIGHT - self.HALF_PAD_HEIGHT) and (self.paddle_vel[0] < 0)):
                self.paddle_pos[0][1] += self.paddle_vel[0]
            else: # Stops the paddle from getting stuck at the bottom
                if(self.paddle_pos[0][1] > self.HEIGHT/2):
                    self.paddle_pos[0][1] = self.HEIGHT - self.HALF_PAD_HEIGHT
                else:
                    self.paddle_pos[0][1] = self.HALF_PAD_HEIGHT
            pygame.draw.polygon(self.canvas, GREEN, 
                [[self.paddle_pos[0][0] - self.HALF_PAD_WIDTH, self.paddle_pos[0][1] - self.HALF_PAD_HEIGHT], 
                [self.paddle_pos[0][0] - self.HALF_PAD_WIDTH, self.paddle_pos[0][1] + self.HALF_PAD_HEIGHT], 
                [self.paddle_pos[0][0] + self.HALF_PAD_WIDTH, self.paddle_pos[0][1] + self.HALF_PAD_HEIGHT], 
                [self.paddle_pos[0][0] + self.HALF_PAD_WIDTH, self.paddle_pos[0][1] - self.HALF_PAD_HEIGHT]], 
                0)
        if(self.paddle_availability[1] == 1): # user 2
            if ((self.paddle_pos[1][1] > self.HALF_PAD_HEIGHT) and (self.paddle_pos[1][1] < self.HEIGHT - self.HALF_PAD_HEIGHT)):
                self.paddle_pos[1][1] += self.paddle_vel[1]
            elif ((self.paddle_pos[1][1] == self.HALF_PAD_HEIGHT) and (self.paddle_vel[1] > 0)):
                self.paddle_pos[1][1] += self.paddle_vel[1]
            elif ((self.paddle_pos[1][1] == self.HEIGHT - self.HALF_PAD_HEIGHT) and (self.paddle_vel[1] < 0)):
                self.paddle_pos[1][1] += self.paddle_vel[1]
            else: # Stops the paddle from getting stuck at the bottom
                if(self.paddle_pos[1][1] > self.HEIGHT/2):
                    self.paddle_pos[1][1] = self.HEIGHT - self.HALF_PAD_HEIGHT
                else:
                    self.paddle_pos[1][1] = self.HALF_PAD_HEIGHT
            pygame.draw.polygon(self.canvas, GREEN, 
                [[self.paddle_pos[1][0] - self.HALF_PAD_WIDTH, self.paddle_pos[1][1] - self.HALF_PAD_HEIGHT], 
                [self.paddle_pos[1][0] - self.HALF_PAD_WIDTH, self.paddle_pos[1][1] + self.HALF_PAD_HEIGHT], 
                [self.paddle_pos[1][0] + self.HALF_PAD_WIDTH, self.paddle_pos[1][1] + self.HALF_PAD_HEIGHT], 
                [self.paddle_pos[1][0] + self.HALF_PAD_WIDTH, self.paddle_pos[1][1] - self.HALF_PAD_HEIGHT]], 
                0)
        if(self.paddle_availability[2] == 1): # user 3
            if ((self.paddle_pos[2][0] > self.HALF_PAD_HEIGHT) and (self.paddle_pos[2][0] < self.WIDTH - self.HALF_PAD_HEIGHT)):
                self.paddle_pos[2][0] += self.paddle_vel[2]
            elif ((self.paddle_pos[2][0] == self.HALF_PAD_HEIGHT) and (self.paddle_vel[2] > 0)):
                self.paddle_pos[2][0] += self.paddle_vel[2]
            elif ((self.paddle_pos[2][0] == self.WIDTH - self.HALF_PAD_HEIGHT) and (self.paddle_vel[2] < 0)):
                self.paddle_pos[2][0] += self.paddle_vel[2]
            else: # Stops the paddle from getting stuck at the bottom
                if(self.paddle_pos[2][0] > self.WIDTH/2):
                    self.paddle_pos[2][0] = self.WIDTH - self.HALF_PAD_HEIGHT
                else:
                    self.paddle_pos[2][0] = self.HALF_PAD_HEIGHT
            pygame.draw.polygon(self.canvas, GREEN, 
                [[self.paddle_pos[2][0] - self.HALF_PAD_HEIGHT, self.paddle_pos[2][1] - self.HALF_PAD_WIDTH], 
                [self.paddle_pos[2][0] - self.HALF_PAD_HEIGHT, self.paddle_pos[2][1] + self.HALF_PAD_WIDTH], 
                [self.paddle_pos[2][0] + self.HALF_PAD_HEIGHT, self.paddle_pos[2][1] + self.HALF_PAD_WIDTH], 
                [self.paddle_pos[2][0] + self.HALF_PAD_HEIGHT, self.paddle_pos[2][1] - self.HALF_PAD_WIDTH]], 
                0)
        if(self.paddle_availability[3] == 1): # user 4
            if ((self.paddle_pos[3][0] > self.HALF_PAD_HEIGHT) and (self.paddle_pos[3][0] < self.WIDTH - self.HALF_PAD_HEIGHT)):
                self.paddle_pos[3][0] += self.paddle_vel[3]
            elif ((self.paddle_pos[3][0] == self.HALF_PAD_HEIGHT) and (self.paddle_vel[3] > 0)):
                self.paddle_pos[3][0] += self.paddle_vel[3]
            elif ((self.paddle_pos[3][0] == self.WIDTH - self.HALF_PAD_HEIGHT) and (self.paddle_vel[3] < 0)):
                self.paddle_pos[3][0] += self.paddle_vel[3]
            else: # Stops the paddle from getting stuck at the bottom
                if(self.paddle_pos[3][0] > self.WIDTH/2):
                    self.paddle_pos[3][0] = self.WIDTH - self.HALF_PAD_HEIGHT
                else:
                    self.paddle_pos[3][0] = self.HALF_PAD_HEIGHT
            pygame.draw.polygon(self.canvas, GREEN, 
                [[self.paddle_pos[3][0] - self.HALF_PAD_HEIGHT, self.paddle_pos[3][1] - self.HALF_PAD_WIDTH], 
                [self.paddle_pos[3][0] - self.HALF_PAD_HEIGHT, self.paddle_pos[3][1] + self.HALF_PAD_WIDTH], 
                [self.paddle_pos[3][0] + self.HALF_PAD_HEIGHT, self.paddle_pos[3][1] + self.HALF_PAD_WIDTH], 
                [self.paddle_pos[3][0] + self.HALF_PAD_HEIGHT, self.paddle_pos[3][1] - self.HALF_PAD_WIDTH]], 
                0)

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
        if(self.paddle_availability[0] == 1):
            self.canvas.blit(label_user1, (2*self.PAD_WIDTH, self.HEIGHT/2))    
        if(self.paddle_availability[1] == 1):
            self.canvas.blit(label_user2, (self.WIDTH - 11*self.PAD_WIDTH, self.HEIGHT/2))
        if(self.paddle_availability[2] == 1):
            self.canvas.blit(label_user3, (self.WIDTH/2 - 4*self.PAD_WIDTH, 2*self.PAD_WIDTH))
        if(self.paddle_availability[3] == 1):
            self.canvas.blit(label_user4, (self.WIDTH/2 - 4*self.PAD_WIDTH, self.HEIGHT - 3*self.PAD_WIDTH))

    def determine_walls(self):
        '''Will determine which walls the ball will bounce off of.
        '''
        if(self.paddle_availability[3] == 0): # user 4 not available
            if(int(self.ball_pos[1] >= self.HEIGHT + 1 - self.BALL_RADIUS)): # Bottom wall
                self.ball_vel[1] = -1 * self.ball_vel[1]
        if(self.paddle_availability[2] == 0): # user 3 not available
            if(int(self.ball_pos[1] <= self.BALL_RADIUS)): # Top wall
                self.ball_vel[1] = -1 * self.ball_vel[1]
        if(self.paddle_availability[1] == 0): # user 2 not available
            if((int(self.ball_pos[0] >= self.WIDTH + 1 - self.BALL_RADIUS))): # Right wall
                self.ball_vel[0] = -1 * self.ball_vel[0]
        if(self.paddle_availability[0] == 0): # user 1 not available
            if(int(self.ball_pos[0] <= self.BALL_RADIUS)): # Left wall
                self.ball_vel[0] = -1 * self.ball_vel[0]

    def determine_paddles(self, ball_vel):
        '''Will determine which walls have paddles and which score.
        @param ball_vel: A list containing the velocities of the ball.
        '''
        # Left side
        if(self.paddle_availability[0] == 1): # user 1
            if((int(self.ball_pos[0]) <= self.BALL_RADIUS + self.PAD_WIDTH) and (int(self.ball_pos[1]) in range(int(self.paddle_pos[0][1]) - int(self.HALF_PAD_HEIGHT), int(self.paddle_pos[0][1]) + int(self.HALF_PAD_HEIGHT),1))):
                # Checking if the ball is within the area where the paddle is
                self.ball_vel[0] = -1.1 * self.ball_vel[0] # slightly increase the difficulty by 10%
                self.ball_vel[1] *= 1.1
            elif(int(self.ball_pos[0]) <= self.BALL_RADIUS + self.PAD_WIDTH):
                self.scores[0] += -1 
                self.spawn_ball(ball_vel)
        if(self.paddle_availability[1] == 1): # user 2
            # Right side
            if(int(self.ball_pos[0]) >= self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH) and (int(self.ball_pos[1]) in range(int(self.paddle_pos[1][1]) - int(self.HALF_PAD_HEIGHT),int(self.paddle_pos[1][1]) + int(self.HALF_PAD_HEIGHT),1)):
                self.ball_vel[0] = -1.1 * self.ball_vel[0]
                self.ball_vel[1] *= 1.1
            elif(int(self.ball_pos[0]) >= self.WIDTH + 1 - self.BALL_RADIUS - self.PAD_WIDTH):
                self.scores[1] += -1
                self.spawn_ball(ball_vel)
        if(self.paddle_availability[2] == 1): # user 3
            # Top side 
            if((int(self.ball_pos[1]) <= self.BALL_RADIUS + self.PAD_WIDTH) and (int(self.ball_pos[0]) in range(int(self.paddle_pos[2][0]) - int(self.HALF_PAD_HEIGHT), int(self.paddle_pos[2][0]) + int(self.HALF_PAD_HEIGHT), 1))):
                self.ball_vel[1] = -1.1 * self.ball_vel[1]
                self.ball_vel[0] *= 1.1
            elif(int(self.ball_pos[1]) <= self.BALL_RADIUS + self.PAD_WIDTH):
                self.scores[2] += -1
                self.spawn_ball(ball_vel)
        if(self.paddle_availability[3] == 1): # user 4
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

    def active_users(self, user1, user2, user3, user4):
        '''Will set each user as active or inactive.
        @param active_users: A list of the users' activity value as delivered by the server.
        '''
        self.paddle_availability[0] = user1
        self.paddle_availability[1] = user2
        self.paddle_availability[2] = user3
        self.paddle_availability[3] = user4
