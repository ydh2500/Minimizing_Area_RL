import numpy as np
import random as rd

class gener_Piece:
    
    def __init__(self, x, y):
        self.generate(x, y)
        
    def generate(self,x ,y):
        shape = np.ones([x,y]).tolist()
        self.shape = shape
        
    def get(self):
        return self.shape
    

Test = [gener_Piece(3,4).get(),
        gener_Piece(7,3).get(),
        gener_Piece(3,3).get(),
        gener_Piece(4,5).get(),
        ]        


PIECES = {1: Test}
TETRIMINO_SIZE = 3
