from pickle import FALSE, TRUE
import pygame #imports pygame library

import sys #imports sys library

clock = pygame.time.Clock() #clock setup

from pygame.locals import * #imports pygame modules

pygame.init() #used to initiate

pygame.display.set_caption('Ball Adventure') # sets window name

WINDOW_SIZE = (400,400) #sets window size
 
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) #INITIALISE WINDOW
 
background = pygame.image.load('backg.jpg')
ball = pygame.image.load('ball.png')
moving_right = False
moving_left = False
ismoving = False 
ball_location = [50,50]
ball_y_momentum = 0 
ball_rect = pygame.Rect(ball_location[0],ball_location[1],ball.get_width(),ball.get_height())
barl_rect = pygame.Rect(100,100,100,50)
############## ################## ##########



while True: #the game loop 
    screen.fill((0,0,0))


    screen.blit(background, (0,0)) #displays the background image
    screen.blit(ball, ball_location) #displays the ball

    if ball_location[1] > WINDOW_SIZE[1]-ball.get_height(): #
        ball_y_momentum = -ball_y_momentum
    else:
        ball_y_momentum += 0.2


    ball_location[1] += ball_y_momentum
    if moving_right == TRUE:
        ball_location[0] += 4
    if moving_left == TRUE:
        ball_location[0] -= 4

    ball_rect.x = ball_location[0]
    ball_rect.y = ball_location[1]

    if ball_rect.colliderect(barl_rect):
        pygame.draw.rect(screen, (255,0,0), barl_rect)
    else:
        pygame.draw.rect(screen, (0,0,0), barl_rect)

    for event in pygame.event.get(): #event loop
        if event.type == QUIT: #checks whether the window has been quit
            pygame.quit() # stops pygame
            sys.exit() # stops sys script
        if event.type == KEYDOWN:
            ismoving = True
            if event.key == K_RIGHT:
                moving_right = TRUE
            if event.key == K_LEFT:
                moving_left = TRUE
        if event.type == KEYUP:
            ismoving = False
            if event.key == K_RIGHT:
                moving_right = FALSE
            if event.key == K_LEFT:
                moving_left = FALSE




    pygame.display.update() #updates the display
    clock.tick(60) #used to maintain the 60 fps
    
