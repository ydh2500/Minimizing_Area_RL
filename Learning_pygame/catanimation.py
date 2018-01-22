# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:17:29 2018

@author: user
"""

import pygame, sys
from pygame.locals import *

pygame.init()

FPS = 30 # 초당 프레임의 수
fpsClock = pygame.time.Clock()

#윈도우 설정하기
DISPLAYSURF = pygame.display.set_mode((400,300), 0 ,32)
pygame.display.set_caption('Animation')

WHITE = (255, 255, 255)
catImg = pygame.image.load('cat.png')
catx = 10
caty = 10
direction = 'right'

while True: #Game 루프
    DISPLAYSURF.fill(WHITE)
    
    if direction == 'right':
        catx += 5
        if catx == 280:
            direction = 'down'

    elif direction == 'down':
        caty += 5
        if caty == 220:
            direction = 'left'

    elif direction == 'left':
        catx -= 5
        if catx == 10:
            direction = 'up'
            
    elif direction == 'up':
        caty -= 5
        if caty == 10:
            direction = 'right'
            
    DISPLAYSURF.blit(catImg, (catx, caty))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit
            
    pygame.display.update()
    fpsClock.tick(FPS)