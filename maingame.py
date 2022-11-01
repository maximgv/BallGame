from pickle import FALSE, TRUE
import pygame #imports pygame library

import sys #imports sys library

clock = pygame.time.Clock() #clock setup

from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init() # initiates pygame
pygame.mixer.set_num_channels(64)

from pygame.locals import * #imports pygame modules

pygame.init() #used to initiate

pygame.display.set_caption('Ball Adventure') # sets window name

WINDOW_SIZE = (600,400) #sets window size
 
screen = pygame.display.set_mode(WINDOW_SIZE, 0, 32) #INITIALISE WINDOW
display = pygame.Surface((300, 200)) #sets the display size, to be scaled up
 

ball = pygame.image.load('ball.png')            #imports the images for sprites
rock = pygame.image.load('rock.jpg')
TILE_SIZE = rock.get_width()
dirt = pygame.image.load('dirt.jpg')
def load_map(path):                #function to read text file to load the map
    f = open(path + '.txt','r')
    data = f.read()
    f.close()
    data = data.split('\n')
    game_map = []
    for row in data:
        game_map.append(list(row))
    return game_map


global animation_frames
animation_frames = {}

def load_animation(path,frame_durations):
    global animation_frames
    animation_name = path.split('/')[-1]
    animation_frame_data = []
    n = 0
    for frame in frame_durations:                               #loads the different animation frames from 
        animation_frame_id = animation_name + '_' + str(n)
        img_loc = path + '/' + animation_frame_id + '.png'
        animation_image = pygame.image.load(img_loc).convert()
        animation_frames[animation_frame_id] = animation_image.copy()
        for i in range(frame):
            animation_frame_data.append(animation_frame_id)
        n += 1
    return animation_frame_data

def change_action(action_var,frame,new_value):               #animation mechanics - actually makes the animaiton run
    if action_var != new_value:
        action_var = new_value
        frame = 0
    return action_var,frame
        

animations = {}

animations['roll'] = load_animation('ball_anim/roll',[3,3,3,3])     #runs the rolling animation
animations['no'] = load_animation('ball_anim/no',[50,50,50])         #runs the animation for when the ball isnt moving


game_map = load_map('map1')   #loads the first map

jump_sound = pygame.mixer.Sound('jump.wav')          #loads the jump sound effect 

ball_action = 'idle'
player_frame = 0
player_flip = False

pygame.mixer.music.load('music.wav')     #loads and constantly plays the backgrond music 
pygame.mixer.music.play(-1)


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

scroll = [0,0]

ball_rect = pygame.Rect(50, 50, ball.get_width(),ball.get_height())
barl_rect = pygame.Rect(100,100,100,50)   #dimensions of the ball - for collisions 
############## ################## ##########

background_objects = [[0.25,[120,10,70,400]],[0.25,[280,30,40,400]],[0.5,[30,40,40,400]],[0.5,[130,90,100,400]],[0.5,[300,80,120,400]]]
#the objects in the background used for the parallax effect


pygame.display.set_caption('Game')
while True: #the game loop 
    display.fill((146,244,255))


    scroll[0] += (ball_rect.x-scroll[0]-156) /20     #camera movement to follow the ball in x axis 
    scroll[1] += (ball_rect.y-scroll[1]-106) /20    #camera movement to follow the ball in y axis 

    
    pygame.draw.rect(display,(7,80,75),pygame.Rect(0,120,300,80))
    for background_object in background_objects:
        obj_rect = pygame.Rect(background_object[1][0]-scroll[0]*background_object[0],background_object[1][1]-scroll[1]*background_object[0],background_object[1][2],background_object[1][3])
        if background_object[0] == 0.5:
            pygame.draw.rect(display,(14,222,150),obj_rect)
        else:
            pygame.draw.rect(display,(9,91,85),obj_rect)
    
    
    tile_rects = []
    y=0
    for row in game_map:            
        x=0
        for tile in row:                 #displays the tiles from the map text file 
            if tile == '1':
                display.blit(dirt, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if tile == '2':
                display.blit(rock, (x * TILE_SIZE-scroll[0], y * TILE_SIZE-scroll[1]))
            if  tile != '0':
                tile_rects.append(pygame.Rect(x*TILE_SIZE, y*TILE_SIZE,TILE_SIZE, TILE_SIZE))
            x+=1
        y +=1


    ball_movement = [0, 0]        #uses the above mechanics to make the ball move in x and y axis
    if moving_right:
        ball_movement[0] += 2
    if moving_left:
        ball_movement[0] -= 2
    ball_movement[1] += ball_y_momentum
    ball_y_momentum += 0.2
    if ball_y_momentum > 3:
        ball_y_momentum = 3


    if ball_movement[0] == 0:
        ball_action,player_frame = change_action(ball_action,player_frame,'no')        #runs the correlated animation for the ball movement
    if ball_movement[0] > 0:
        player_flip = False
        ball_action,player_frame = change_action(ball_action,player_frame,'roll')
    if ball_movement[0] < 0:
        player_flip = True
        ball_action,player_frame = change_action(ball_action,player_frame,'roll')


    ball_rect, collisions = move(ball_rect, ball_movement, tile_rects)

    if collisions['bottom']:
        ball_y_momentum = 0
        air_timer = 0
    else:
        air_timer += 1

    player_frame += 1

    if player_frame >= len(animations[ball_action]):
        player_frame = 0
    player_img_id = animations[ball_action][player_frame]
    player_img = animation_frames[player_img_id]
    display.blit(pygame.transform.flip(player_img,player_flip,False),(ball_rect.x-scroll[0],ball_rect.y-scroll[1]))

    for event in pygame.event.get(): # event loop
        if event.type == QUIT: # check for window quit
            pygame.quit() # stop pygame
            sys.exit() # stop script
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                moving_right = True
            if event.key == K_LEFT:
                moving_left = True
            if event.key == K_UP:
                if air_timer < 6:
                    jump_sound.play()
                    ball_y_momentum = -5
        if event.type == KEYUP:
            if event.key == K_RIGHT:
                moving_right = False
            if event.key == K_LEFT:
                moving_left = False



    switch = pygame.transform.scale(display, WINDOW_SIZE)  #scales an image
    screen.blit(switch, (0, 0))
    pygame.display.update() #updates the display
    clock.tick(60) #used to maintain the 60 fps
    
