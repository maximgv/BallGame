from pickle import FALSE, TRUE
import pygame #imports pygame library

import sys #imports sys library

clock = pygame.time.Clock() #clock setup

from pygame.locals import * #imports pygame modules

pygame.init() #used to initiate

pygame.display.set_caption('Ball Adventure') # sets window name

WINDOW_SIZE = (600,400) #sets window size
 
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) #INITIALISE WINDOW
display = pygame.Surface((300, 200))
 

ball = pygame.image.load('ball.png')
rock = pygame.image.load('rock.jpg')
TILE_SIZE = rock.get_width()
dirt = pygame.image.load('dirt.jpg')
game_map = [['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','2','2','2','2','2','0','0','0','0','0','0','0'],
            ['0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0'],
            ['2','2','0','0','0','0','0','0','0','0','0','0','0','0','0','0','0','2','2'],
            ['1','1','2','2','2','2','2','2','2','2','2','2','2','2','2','2','2','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1'],
            ['1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1','1']]

def collision_test(rect, tiles):       # collision testing
    hit_list = []
    for tile in tiles:
        if rect.colliderect(tile):
            hit_list.append(tile)
    return hit_list

def move(rect, movement, tiles):
    collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}    #the collision mechanics
    rect.x += movement[0]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[0] > 0:
            rect.right = tile.left
            collision_types['right'] = True
        elif movement[0] < 0:
            rect.left = tile.right
            collision_types['left'] = True
    rect.y += movement[1]
    hit_list = collision_test(rect, tiles)
    for tile in hit_list:
        if movement[1] > 0:
            rect.bottom = tile.top
            collision_types['bottom'] = True
        elif movement[1] < 0:
            rect.top = tile.bottom
            collision_types['top'] = True
    return rect, collision_types

moving_right = False
moving_left = False
ismoving = False 
ball_location = [50,50]
ball_y_momentum = 0 
air_timer = 0
ball_rect = pygame.Rect(50, 50, ball.get_width(),ball.get_height())
barl_rect = pygame.Rect(100,100,100,50)
############## ################## ##########



while True: #the game loop 
    display.fill((146,244,255))

    y=0
    tile_rects = []
    for row in game_map:            
        x=0
        for tile in row:                 #displays the tiles from the map
            if tile == '1':
                display.blit(dirt, (x * TILE_SIZE, y * TILE_SIZE))
            if tile == '2':
                display.blit(rock, (x * TILE_SIZE, y * TILE_SIZE))
            if  tile != '0':
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE,TILE_SIZE, TILE_SIZE))

            x+=1
        y +=1


    #display.blit(ball, ball_location) #displays the ball



    ball_movement = [0, 0]         #code for ball movement
    if moving_right:
        ball_movement[0] += 2
    if moving_left:
        ball_movement[0] -= 2
    ball_movement[1] += ball_y_momentum
    ball_y_momentum += 0.2
    if ball_y_momentum > 3:
        ball_y_momentum = 3

    ball_rect, collisions = move(ball_rect, ball_movement, tile_rects)

    if collisions['bottom']:
        player_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1


    display.blit(ball, (ball_rect.x, ball_rect.y))


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

    





    switch = pygame.transform.scale(display, WINDOW_SIZE)  #scales an image
    screen.blit(switch, (0, 0))
    pygame.display.update() #updates the display
    clock.tick(60) #used to maintain the 60 fps
    