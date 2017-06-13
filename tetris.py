import pygame
import sys
import random
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

    # PIECES = {1: O, 2: I, 3: L, 4: J, 4ㅣ5: Z, 6:S, 7:T}
    COLORS = { 1: yellow, 2: cyan, 3: orange, 4: blue, 5: red, 6: green, 7:pink}

    # width
    WIDTH = 500
    # height
    HEIGHT = 520


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
        for _ in range(self.t_height):
            self.board.append([0] * self.t_width)
        self.generate_piece()

    def generate_piece(self):
        mino = Mino()
        self.piece = mino
        self.color = mino.color
        self.piece_x, self.piece_y = 3, 2

    def pos_to_pixel(self, x, y):
        return self.block_size*(x+2), self.block_size*(y-2)

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

    def full_drop_piece(self):
        while self._can_drop_piece():
            self.drop_piece()
        self.drop_piece()

    def rotate_piece(self, clockwise=True):
        self._try_rotate_piece(clockwise)

    def _delete_line(self, y):
        for y in reversed(range(1, y+1)):
            self.board[y] = list(self.board[y-1])

    def delete_lines(self):
        remove = [y for y, row in enumerate(self.board) if all(row)]
        for y in remove:
            self._delete_line(y)

    def game_over(self):
        return sum(self.board[0]) > 0 or sum(self.board[1]) > 0

    def draw_blocks(self, array2d, dx=0, dy=0, board=0):
        for y, row in enumerate(array2d):
            y += dy
            if y >= 2 and y < self.t_height:
                for x, block in enumerate(row):
                    x += dx
                    x_pix, y_pix = self.pos_to_pixel(x, y)
                    if block:
                        # match block and color
                        color = P_UI.COLORS [block]
                        # draw block
                        pygame.draw.rect(self.screen, color,
                                         (  x_pix, y_pix,
                                            self.block_size,
                                            self.block_size))
                    if board:
                        pygame.draw.rect(self.screen, P_UI.grey,
                        (  x_pix, y_pix,
                            self.block_size,
                            self.block_size), 1)
                        
    def draw_board(self):
        x_pix, y_pix = self.pos_to_pixel(0, 1)
        self.screen.fill(P_UI.backcolor)

        # pygame.draw.rect(self.screen,
        #             P_UI.black,
        #             Rect(x_pix-20, y_pix-20, 
        #             self.t_width * self.block_size +40, (self.t_height-1) * self.block_size +40))
        # pygame.draw.rect(self.screen,
        #             P_UI.green,
        #             Rect(x_pix-20, y_pix-20, 
        #             self.t_width * self.block_size +40, (self.t_height-1) * self.block_size +40),3)        
        
        pygame.draw.rect(self.screen,
                    P_UI.grey_2,
                    Rect(x_pix, y_pix, 
                    self.t_width * self.block_size, (self.t_height-1) * self.block_size),13)        

        pygame.draw.rect(self.screen,
                    P_UI.t_background,
                    Rect(x_pix, y_pix, 
                    self.t_width * self.block_size, (self.t_height-1) * self.block_size))
   


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

    def pause(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    running = False

    def run(self):
        pygame.init()
        pygame.time.set_timer(Tetris.DROP_EVENT, 500)

        while True:
            if self.board.game_over():
                print ("Game over")
                pygame.quit()
                sys.exit()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    self.handle_key(event.key)
                elif event.type == Tetris.DROP_EVENT:
                    self.board.drop_piece()

            self.board.draw()
            pygame.display.update()
            self.clock.tick(60)


if __name__ == "__main__":
    Tetris().run()