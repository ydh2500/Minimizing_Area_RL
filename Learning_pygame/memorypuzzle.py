# Memory Puzzle

import random, pygame, sys
from pygame.locals import *

FPS = 30
WINDOWIDTH = 640 # 윈도우의 너비 (픽셀단위)
WINDOWHEIGHT = 480 # 윈도우의 높이 (픽셀단위)
REVEALSPEED = 8 # 상자가 보였다가 가려지는 속도
BOXSIZE = 40 # 상자의 너비와 높이 (픽셀단위)
GAPSIZE = 10 # 상자 사이의 간격 (픽셀단위)
BOARDWIDTH = 10 # 아이콘 가로 줄 수
BOARDHEIGHT = 7 # 아이콘 세로 줄 수
assert (BOARDWIDTH * BOARDHEIGHT) % 2 == 0, 'Board needs to have an even number of boxxes for pairs of matches.'
# assert 문은 즉각 검사이며, assert를 통과하지 못하면 프로그램은 멈춘다.
XMARGIN = int((WINDOWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 2)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#           R    G    B
GRAY    = (100, 100, 100)
NAVYBLUE= ( 60,  60, 100)
WHITE   = (255, 255, 255)
RED     = (255,   0,   0)
GREEN   = (  0, 255,   0)
BLUE    = (  0,   0, 255)
YELLOW  = (255, 255,   0)
ORANGE  = (255, 128,   0)
PURPLE  = (255,   0, 255)
CYAN    = (  0, 255, 255)

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALLSHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALLCOLORS) * len(ALLSHAPES) * 2 >= BOARDWIDTH * BOARDHEIGHT, \
    "Board is too big for the number of shapes/colors defined."

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWIDTH, WINDOWHEIGHT))

    mousex = 0 # 마우스 이벤트 발생 시 x좌표
    mousey = 0 # 마우스 이벤트 발생 시 y좌표
    pygame.display.set_caption("Memory Game")

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(False)

    firstSection = None # 첫 번째 상자를 클릭했을 때, (x,y)를 저장
    DISPLAYSURF.fill(BGCOLOR)
    startGameAnimation(mainBoard)

    while True: #게임루프
        mouseClicked = False

        DISPLAYSURF.fill(BGCOLOR) #윈도우를 그린다.
        drawBoard(mainBoard, revealedBoxes)