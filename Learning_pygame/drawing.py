# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 16:07:01 2018

@author: user
"""

import pygame, sys
from pygame.locals import *  #pygame.locals 안에 있는 걸 워낙 많이 사용한다.

pygame.init() # pygame은 이 명령어를 실행한 이후에야 다른 명령어를 쓸 수 가 있다. initialize 시키는 함수이다. 


# 윈도우 설정하기
DISPLAYSURF = pygame.display.set_mode((400,300), 0, 32)
pygame.display.set_caption('Drawing')

# 색깔 설정하기


BLACK = ( 0, 0, 0)
WHITE = (255,255,255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

#surface 객체상에 그리기
DISPLAYSURF.fill(WHITE)
pygame.draw.polygon(DISPLAYSURF, GREEN, ((146, 0),(281, 196), (291, 106), (236, 277), (56, 277), (0,106)))
pygame.draw.line(DISPLAYSURF, BLUE, (60,60), (120, 60), 4)
pygame.draw.line(DISPLAYSURF, BLUE, (120,60), (60, 120))

pygame.draw.rect(DISPLAYSURF, BLUE, (300, 200, 30, 50))

pixObj = pygame.PixelArray(DISPLAYSURF)
pixObj[380][280] = BLACK
pixObj[382][282] = BLACK
pixObj[384][284] = BLACK
pixObj[386][286] = BLACK
pixObj[388][288] = BLACK
del pixObj

# 게임루프 수행

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    