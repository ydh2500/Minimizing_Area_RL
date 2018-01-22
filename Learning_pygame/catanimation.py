# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 18:17:29 2018

@author: user
"""

import pygame, sys
from pygame.locas import *

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
