import pygame
import random
import sys
from pygame.mixer import *
from Piece import *
from pygame.locals import *

# pretty UI
class P_UI:
    """docstring for P_UI"""
    # Tetris_Background
    black = (10, 10, 10)
    black_2 = (26, 26, 26)
    white = (255, 255, 255)
    grey = (35, 35, 35)
    grey_2 = (55, 55, 55)

    t_background = black_2
    backcolor = white
    # Piece_color
    cyan = (69, 206, 204)
    blue = (64, 111, 249)
    orange = (253, 189, 53)
    yellow = (246, 227, 90)
    green = (98, 190, 68)
    pink = (242, 64, 235)
    red = (225, 13, 27)

    # PIECES =                  {1: I,    2: J,    3: L,     4: O,      5: S,     6:T,     7:Z}
    COLORS = { 0: t_background, 1: cyan, 2: blue, 3: orange, 4: yellow, 5: green, 6: pink, 7:red, 8:grey_2}
    # width
    WIDTH = 500
    # height
    HEIGHT = 500
    # font_path , font = I LOVE U 
    path = "./materials/font/Iloveu.ttf"
    SPEED = 500
    SPEED_DOWN = 40

    drop_path = "./materials/sound/tok.wav"
    ssg_path = "./materials/sound/ssg.mp3"
    game_over_path = "./materials/sound/game_over.wav"
    delete3_path = "./materials/sound/dorrrru.wav"
    pause_path = "./materials/sound/didong.wav"
    hold_path = "./materials/sound/cutting.wav"
    cash_path = "./materials/sound/cash.wav"
    base_path = "./materials/sound/base.wav" 
    move_path = "./materials/sound/deb.wav"
    delete4_path = "./materials/sound/super_weapon.wav"
    delete_path = "./materials/sound/pop.flac"

class Mino:

    def __init__(self, piece_name=0):
        if piece_name:
            self.piece_name = piece_name
        else:
            self.piece_name = random.randrange(1, 8)
        self.rotation = 0
        self.array2d = Piece.PIECES[self.piece_name][self.rotation]
        self.color = P_UI.COLORS[self.piece_name]

    def __iter__(self):
        for row in self.array2d:
            yield row

    def rotate(self, clockwise=True):
        self.rotation = (self.rotation + 1) % 4 if clockwise else \
                        (self.rotation - 1) % 4
        self.array2d = Piece.PIECES[self.piece_name][self.rotation]

class Board:
    COLLIDE_EVENT = {'no_error': 0, 'right_wall': 1, 'left_wall': 2,
                     'bottom': 3, 'overlap': 4}

    def __init__(self, screen):
        self.screen = screen
        self.t_width = 10
        self.t_height = 25
        self.block_size = 20
        self.board = []
        self.next_1 = random.randrange(1, 8)
        self.next_2 = random.randrange(1, 8)
        self.next_3 = random.randrange(1, 8)
        self.mino_size_row_and_col = Piece.TETRIMINO_SIZE
        self.holding = False
        self.holding_block = None
        self.holding_count = False
        self.score = 0
        self.level = 0
        self.goal = 0

        for _ in range(self.t_height):
            self.board.append([0] * self.t_width)
        self.generate_piece()

    def generate_piece(self):
        self.piece = Mino(self.next_1)
        self.piece_num = self. next_1
        self.next_1 = self.next_2
        self.next_2 = self.next_3
        self.next_3 = random.randrange(1, 8)
        self.holding_count = False

        self.piece_x, self.piece_y = 3, 0

    def tetris_location(self, x, y): 
        return self.block_size*(x+7), self.block_size*(y-2)

    def absorb_piece(self):
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    self.board[y+self.piece_y][x+self.piece_x] = block
        self.generate_piece()

    def _block_collide_with_board(self, x, y):
        if x < 0:
            return Board.COLLIDE_EVENT['left_wall']
        elif x >= self.t_width:
            return Board.COLLIDE_EVENT['right_wall']
        elif y >= self.t_height:
            return Board.COLLIDE_EVENT['bottom']
        elif self.board[y][x]:
            return Board.COLLIDE_EVENT['overlap']
        return Board.COLLIDE_EVENT['no_error']

    def collide_with_board(self, dx, dy):
        """Check if piece (offset dx, dy) collides with board"""
        for y, row in enumerate(self.piece):
            for x, block in enumerate(row):
                if block:
                    collide = self._block_collide_with_board(x=x+dx, y=y+dy)
                    if collide:
                        return collide
        return Board.COLLIDE_EVENT['no_error']

    def _can_move_piece(self, dx, dy):
        dx_ = self.piece_x + dx
        dy_ = self.piece_y + dy
        if self.collide_with_board(dx=dx_, dy=dy_):
            return False
        else : return True

    def _can_drop_piece(self):
        return self._can_move_piece(dx=0, dy=1)

    def _try_rotate_piece(self, clockwise=True):
        self.piece.rotate(clockwise)
        collide = self.collide_with_board(dx=self.piece_x, dy=self.piece_y)
        if not collide:
            pass
        elif collide == Board.COLLIDE_EVENT['left_wall']:
            if self._can_move_piece(dx=1, dy=0):
                self.move_piece(dx=1, dy=0)
            elif self._can_move_piece(dx=2, dy=0):
                self.move_piece(dx=2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        elif collide == Board.COLLIDE_EVENT['right_wall']:
            if self._can_move_piece(dx=-1, dy=0):
                self.move_piece(dx=-1, dy=0)
            elif self._can_move_piece(dx=-2, dy=0):
                self.move_piece(dx=-2, dy=0)
            else:
                self.piece.rotate(not clockwise)
        else:
            self.piece.rotate(not clockwise)

    def move_piece(self, dx, dy):
        if self._can_move_piece(dx, dy):
            self.piece_x += dx
            self.piece_y += dy

    def drop_piece(self):
        if self._can_drop_piece():
            self.move_piece(dx=0, dy=1)
        else:
            self.absorb_piece()
            self.delete_lines()
    def rotate_piece(self, clockwise=True):
        self._try_rotate_piece(clockwise)

    def full_drop_piece(self):
        while self._can_drop_piece():
            self.drop_piece()
        self.score += self.level * 5
        self.drop_piece()


    def score_up(self, rline):
        if self.score > 500000 :
            self.score = 500000
        else :
            self.score += (10 + rline * rline * 20)
        if self.score >= self.goal : 
            self.level += 1
            P_UI.SPEED -= (P_UI.SPEED_DOWN * self.level)
            if P_UI.SPEED < 80: P_UI.SPEED = 80
            self.set_timer(P_UI.SPEED)

        self.goal = 280 + self.level * self.level * self.level * 20

    def set_timer(self,timer):
        pygame.time.set_timer(Tetris.DROP_EVENT, timer)
    def _delete_line(self, y):
        for y in reversed(range(1, y+1)):
            self.board[y] = list(self.board[y-1])

    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        for y in remove:
            self._delete_line(y)
        self.score_up(len(remove))

    def hold_block(self):
        if not self.holding_count :
            self.holding_count = True

            if self.holding :
                self.piece_xce, self.holding_block = self.holding_block, self.piece
                self.piece_x, self.piece_y = 3, 1
            else :
                self.holding_block = self.piece
                self.holding = True
                self.generate_piece()

        else :
            pass
    def game_over(self):
        result = sum(self.board[0]) > 0 or sum(self.board[1]) > 0
        return result


    # def lowest(self, array2d):
    #     x = self.piece_x
    #     y = self.piece_y
    #     for i in range(4):
    #         for j in range(4):
    #             if array2d[i][j] != 0:
    #                 if (y + i + 1) > 20:
    #                     return True
    #                 elif self.board[x + j][y + i + 1] != 0 and\
    #                      self.board[x + j][y + i + 1] != 8:
    #                     return True
    # def draw_ghost(self, array2d):

    #     tx, ty = self.piece_x, self.piece_y
    #     while not self.lowest(array2d):
    #         ty += 1

    #     for i in range(4):
    #         for j in range(4):
    #             if array2d[i][j] != 0:
    #                 self.board[tx + j][ty + i] = 8  

    def draw_blocks(self, array2d, dx=0, dy=0, board=0):
        # if not board :
        #    self. draw_ghost(array2d.array2d)
        for y, row in enumerate(array2d):
            y += dy
            if y >= 2 and y < self.t_height:
                for x, block in enumerate(row):
                    x += dx
                    x_pix, y_pix = self.tetris_location(x, y)
                    if block:
                        # match block and color
                        color = P_UI.COLORS [block]
                        # draw block
                        pygame.draw.rect(self.screen, color,
                                         (  x_pix, y_pix,
                                            self.block_size,
                                            self.block_size))
                    # Board
                    if board :
                        pygame.draw.rect(self.screen, P_UI.grey,
                        (  x_pix, y_pix,
                            self.block_size,
                            self.block_size), 1)


    def draw_static_block(self, next_name, dx, dy, size):
        next_block = Piece.PIECES[next_name][0]
        for x in range(self.mino_size_row_and_col):
            for y in range(self.mino_size_row_and_col):
                if next_block[x][y] != 0:
                    x_pix = dx + size * y
                    y_pix = dy + size * x
                    pygame.draw.rect(
                        self.screen,
                        P_UI.COLORS[next_block[x][y]],
                        Rect( x_pix, y_pix,
                          size, size)
                    )
                    pygame.draw.rect(self.screen, P_UI.backcolor,
                     (  x_pix, y_pix,
                        size-2,
                        size-2), 1)

     

    def draw_board(self):
        x_pix, y_pix = self.tetris_location(0, 0)
        x_end = x_pix + self.t_width * self.block_size
        y_end = y_pix + self.t_height * self.block_size
        self.screen.fill(P_UI.backcolor)       
        pygame.draw.circle(self.screen, P_UI.grey_2, (x_pix, y_end), 6, 0)
        pygame.draw.circle(self.screen, P_UI.grey_2, (x_end, y_end), 6, 0)
        
        pygame.draw.rect(self.screen,
                    P_UI.grey_2,
                    Rect(x_pix, y_pix + self.block_size, 
                    self.t_width * self.block_size, (self.t_height-1) * self.block_size),13)        
        pygame.draw.rect(self.screen,
                    P_UI.t_background,
                    Rect(x_pix, y_pix + self.block_size, 
                    self.t_width * self.block_size, (self.t_height-1) * self.block_size))

        

        font0 = pygame.font.Font(P_UI.path, 25)
        font1 = pygame.font.Font(P_UI.path, 25)
        font0.set_underline(1)

        text_hold = font0.render("HOLD", 1, P_UI.black)
        text_level = font1.render("LEVEL", 1, P_UI.black)
        text_goal = font1.render("GOAL", 1, P_UI.black)
        text_next = font0.render("NEXT", 1, P_UI.black)
        text_score = font1.render("SCORE", 1, P_UI.black)
        num_level = pygame.font.Font(P_UI.path, 40).render(str(self.level), 1, P_UI.black)
        num_goal = pygame.font.Font(P_UI.path, 30).render(str(self.goal), 1, P_UI.black)
        num_score = pygame.font.Font(P_UI.path, 35).render(str(int(self.score)), 1, P_UI.black)

        self.screen.blit(text_hold, (39, 34))
        self.screen.blit(text_level, (40, 235))
        self.screen.blit(text_goal, (39, 360))
        self.screen.blit(text_next, (400, 30))
        self.screen.blit(text_score, (392, 300))
        self.screen.blit(num_level, (55, 280))
        self.screen.blit(num_goal, (50, 415))
        self.screen.blit(num_score, (410, 345))
        self.draw_static_block(self.next_1, 390, 85, self.block_size+2)
        self.draw_static_block(self.next_2, 400, 170, self.block_size-3)
        self.draw_static_block(self.next_3, 400, 220, self.block_size-3)
        if self.holding_block != None:
            self.draw_static_block(self.holding_block.piece_name, 30, 100, self.block_size+2)

    def draw(self):
        self.draw_board()
        self.draw_blocks(self.piece, dx=self.piece_x, dy=self.piece_y)
        self.draw_blocks(self.board, board=1)

class Tetris:
    DROP_EVENT = USEREVENT + 1

    def __init__(self):
        self.screen = pygame.display.set_mode((P_UI.WIDTH, P_UI.HEIGHT))
        self.clock = pygame.time.Clock()
        self.board = Board(self.screen)
        pygame.init()
        pygame.display.set_caption('Tetris_by_Lim')
        pygame.time.set_timer(Tetris.DROP_EVENT, 300)
        self.main_sound('back.wav')
        self.start()       

    def main_sound (self, file):
        pygame.mixer.music.load("./materials/sound/" + file)
        pygame.mixer.music.play(loops=-1 , start=0.0)

    def start(self):

        self.screen.fill(P_UI.backcolor)
        hei, size = 240, 20
        self.board.draw_static_block(2, 60, hei, size)
        self.board.draw_static_block(5, 160, hei, size)
        self.board.draw_static_block(7, 250, hei, size)
        self.board.draw_static_block(3, 350, hei, size)
        self.board.draw_static_block(4, 80, hei+80, size)
        self.board.draw_static_block(1, 200, hei+80, size)
        self.board.draw_static_block(6, 330, hei+80, size)
        image = pygame.image.load('./materials/image/logo.jpg')
        self.screen.blit(image, (80, 50))
        image2 = pygame.image.load('./materials/image/start.jpg')
        self.screen.blit(image2, (140, 380))
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.run()

            pygame.display.update()

    def handle_key(self, event_key):
        if event_key == K_DOWN:
            self.board.drop_piece()
        elif event_key == K_LEFT:
            self.board.move_piece(dx=-1, dy=0)
        elif event_key == K_RIGHT:
            self.board.move_piece(dx=1, dy=0)
        elif event_key == K_UP:
            self.board.rotate_piece()
        elif event_key == K_SPACE:
            self.board.full_drop_piece()
        elif event_key == K_ESCAPE:
            self.pause()
            # self.pause_sound.play()
        elif event_key == K_LSHIFT  :
            self.board.hold_block()
            # self.hold_sound.play()
        # elif event_key == K_q
            # self.board.rotate_piece(False)
        else : pass

    def push_key(self):
        press = pygame.key.get_pressed()
        if press[pygame.K_DOWN] : 
            self.board.set_timer(80)
        else :
            self.board.set_timer(P_UI.SPEED)


    def pause(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False

    def run(self):
        self.main_sound("main.mp3")

        pygame.time.set_timer(Tetris.DROP_EVENT, P_UI.SPEED)
        while True:
            if self.board.game_over():
                pygame.mixer.Sound(P_UI.game_over_path).play()
                over = pygame.font.Font(P_UI.path, 60).render(("Good Game !"), 1, P_UI.grey_2)
                self.screen.blit(over, (70, 230))
                pygame.display.update()
                pygame.time.delay(2000)
                pygame.quit()
                sys.exit()
            else:
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        self.handle_key(event.key)
                    elif event.type == Tetris.DROP_EVENT:
                        self.board.drop_piece()
                    self.push_key()

                self.board.draw()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Tetris()