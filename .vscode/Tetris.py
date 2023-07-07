import pygame
from copy import deepcopy
from random import choice, randrange
import os
import logging

# Create a logger
logger = logging.getLogger('tetris_logger')
logger.setLevel(logging.DEBUG)

# Create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Add ch to logger
logger.addHandler(ch)
logger.debug('debug message')


W, H = 11, 11
TILE = 45
GAME_RES = W * TILE, H * TILE
RES = 800, 750
FPS = 0.5

pygame.init()
pygame.mixer.init()
sc = pygame.display.set_mode(RES)
game_sc = pygame.Surface(GAME_RES)
clock = pygame.time.Clock()

background_music = pygame.mixer.music.load('Victory.mp3')
clear_line_sound = pygame.mixer.Sound('success_sound_effect.mp3')
pygame.mixer.music.play(-1)


# This is the gird of the game on which we are building and playing the game
grid = [pygame.Rect(x * TILE, y * TILE, TILE, TILE) for x in range(W) for y in range(H)]

# storing the history of game scores
highscore_filename = 'highscore.dat'

if not os.path.exists(highscore_filename):
    with open(highscore_filename, 'w') as highscore_file:
        highscore_file.write('0')
        
with open(highscore_filename, 'r') as highscore_file:
    highscore = int(highscore_file.read())

# this is the positions on the grid.
figures_pos = [[(-1,0), (-2,0), (0,0), (1,0)],
               [(0,-1), (-1,-1), (-1,0), (0,0)],
               [(-1,0),(-1,-1), (0,0), (0,-1)],
               [(0,0), (-1,0),(0,1), (-1,-1)],
               [(0,0), (0,-1), (0,1), (-1,-1)],
               [(0,0), (0,-1), (0,1), (1,-1)],
               [(0,0), (0,-1), (0,1), (1,0)]]
# The line of code you provided is a nested list comprehension in Python that constructs pygame.Rect objects 
# for each of the block positions defined in figures_pos, then collects these pygame.Rect objects into separate lists for each figure. 
# It ultimately constructs a list of tetromino figures, where each figure is a list of pygame.Rect objects representing its blocks.
figures= [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
#This line is creating a new rectangle object using the pygame.Rect class from the pygame module. 
figure_rect = pygame.Rect(0, 0, TILE - 2, TILE - 2)
field = [[0 for i in range(W)] for i in range(H)]

bomb_figure=[pygame.Rect(5, 1, 1, 1), pygame.Rect(4, 1, 1, 1), pygame.Rect(5, 2, 1, 1), pygame.Rect(4, 0, 1, 1)]
anim_count, anim_speed, anim_limit = 0, 60, 2000
figure, next_figure =deepcopy(choice(figures)), deepcopy(choice(figures))
logger.debug(f'figure: {figure}')
logger.debug(f'bomb figure: {bomb_figure}')

is_bomb = False

bg = pygame. image. load('space.jpg').convert()
game_bg = pygame.image.load('Earth.jpg').convert()
get_color = lambda : (randrange(30, 256), randrange(30, 256), randrange(30, 256))
font = pygame.font.SysFont('Times New Roman', 90)
color, next_color = get_color(), get_color()
title = font.render('Tetris', True, (179, 0, 255))
title_score = font.render('Score:', True, (0, 255, 251))
score, lines = 0 , 0
scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500 }


logger.debug('initialization of variables complete and going into execution')
# The purpose of this function is to clear a certain radius in the grid to continue the game further 
def explode_bomb(bomb_x, bomb_y, field, bomb_radius=2):
    logger.debug('start explode_bomb function , value of bomb_x:',bomb_x, " value of bomb_y: ", bomb_y)
    # Iterate over each cell in the field.
    for y, row in enumerate(field):
        logger.debug('inside explode_bomb, value of y', y)
        for x, cell in enumerate(row):
            # Calculate the distance from this cell to the bomb.
            distance = ((bomb_x - x) ** 2 + (bomb_y - y) ** 2) ** 0.5
            # If the distance is within the bomb's radius, clear this cell.
            if distance <= bomb_radius:
                field[y][x] = 0  # Or however you represent an empty cell.
    logger.debug('end explode_bomb function')

def check_borders():
    #logger.debug('inside check_borders')
    if figure[i].x <0 or figure[i].x > W-1:
        return False
    elif figure[i].y > H - 1 or field[figure[i].y][figure[i].x]:
        return False
    return True
logger.debug(f'This figure is {figure}')
if figure==bomb_figure:
    logger.debug('is_bomb=True')
    is_bomb=True

while True:
    #logger.debug('starting to perform actions..moving blocks')
    dx, rotate=0, False
    sc.blit(bg, (0,0))
    sc.blit(game_sc, (20,20))
    game_sc.blit(game_bg, (0,0))
    for i in range(lines):
        pygame.time.wait(200)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        if event.type == pygame.KEYDOWN:
            FPS=2
            if event.key == pygame.K_LEFT:
                dx= -1
            elif event.key == pygame.K_RIGHT:
                dx= 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 50
            elif event.key == pygame.K_UP:
                rotate=True
        else:
            FPS=1
    
    figure_old = deepcopy(figure)
    for i in range(len(figure)):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(figure_old)
            break
    if is_bomb==True:
        logger.debug('break1: Inside is_bomb figure_old ', figure_old, ' figure: ', figure)
        explode_bomb(figure_old[0].x, figure_old[0].y, field)
        logger.debug('break2')
        is_bomb = False
    
    anim_count += anim_speed
    #Checking where the block is, checking if has hit the bottom or another block
    if anim_count > anim_limit:
        anim_count = 0
        figure_old = deepcopy(figure)
    #moves the block down by 1 square as long as it is in range
    for i in range(len(figure)):
        figure[i].y += 1
        if not check_borders():
            for i in range(len(figure)):
                field[figure_old[i].y][figure_old[i].x] = color
                if is_bomb==True:
                    logger.debug('break1: Inside is_bomb figure_old ', figure_old, ' figure: ', figure)
                    explode_bomb(figure_old[0].x, figure_old[0].y, field)
                    logger.debug('break2')
                    is_bomb = False

            figure, color = next_figure, next_color
            next_figure, next_color = deepcopy(choice(figures)), get_color()
            anim_limit=2000
            break
#rotate
    center = figure[0]
    figure_old = deepcopy(figure)
    if rotate==True:
        for i in range(len(figure)):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(figure_old)
                break

    line, lines= H - 1, 0
    for row in range(H-1, -1, -1):
        count = 0
        for i in range(W):
            if field[row][i]:
                count+=1
            field[line][i] = field[row][i]
        if count < W:
            line -= 1
        else:
            anim_speed += 3
            lines += 1
            clear_line_sound.play()
    score += scores[lines]

    if score > highscore:
        highscore = score
        with open(highscore_filename, 'w') as highscore_file:
            highscore_file.write(str(highscore))

    highscore_text = font.render('High Score: ' + str(highscore), True, pygame.Color('white'))
    sc.blit(highscore_text, (50, 525))
    


    [pygame.draw.rect(game_sc, (40,40,40), i_rect, 1) for i_rect in grid]

    #draw figure
    for i in range(len(figure)):
       figure_rect.x = figure[i].x * TILE
       figure_rect.y = figure[i].y * TILE
       pygame.draw.rect(game_sc, color, figure_rect)

    for y, raw in enumerate(field):
        for x, col in enumerate(raw):
            if col:
                figure_rect.x, figure_rect.y = x * TILE, y * TILE
                pygame.draw.rect(game_sc, col, figure_rect)

    for i in range(len(next_figure)):
       figure_rect.x = next_figure[i].x * TILE +380
       figure_rect.y = next_figure[i].y * TILE +185
       pygame.draw.rect(sc, next_color, figure_rect)

    
    
    sc.blit(title, (550, 11))
    sc.blit(title_score, (400, 600))
    sc.blit(font.render(str(score), True, pygame.Color('white')), (630, 600))
    
    for i in range(W):
        if field[0][i]:
            field = [[0 for i in range(W)] for i in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for i_rect in grid:
                pygame.draw.rect(game_sc, get_color(), i_rect)
                sc.blit(game_sc, (20,20))
                pygame.display.flip()
                clock.tick(200)
    
    

    pygame.display.flip()
    clock.tick(FPS)
    