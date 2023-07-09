import pygame,json,os,copy
from square import Square
from piece import *
from move import Move
from tkinter import *

# global textures
textures={}

def create_surfaces():
    for color in ['white','black']:
        textures[color]={}
        for image in ['rook','bishop','queen','king','knight','pawn']:
            path=os.path.join('pieces',color,f'{image}.png')
            surface=pygame.image.load(path).convert_alpha()
            textures[color][image]=surface

class Board:
    def __init__(self,theme,down):
        f=open('settings.json')
        self.settings=json.load(f)
        del f
        create_surfaces()
        
    def _create(self):
        for row in range(self.settings['ROWS']):
            for col in range(self.settings['COLS']):
                self.squares[row][col]=Square(row, col)

    def _add_pieces(self,color):
        if self.down=='white':
            (pawn_piece,other_piece)=(6,7) if color=='white' else (1,0)
        else:
            (pawn_piece,other_piece)=(1,0) if color=='white' else (6,7)

        # pawns
        for col in range(self.settings['COLS']):
            self.squares[pawn_piece][col]=Square(pawn_piece,col,Pawn(color,textures[color]['pawn'].get_rect(),self.down))

        # knights
        self.squares[other_piece][1]=Square(other_piece, 1,Knight(color,textures[color]['knight'].get_rect()))
        self.squares[other_piece][6]=Square(other_piece,6,Knight(color,textures[color]['knight'].get_rect()))

        # Bishops
        self.squares[other_piece][2]=Square(other_piece, 2,Bishop(color,textures[color]['bishop'].get_rect()))
        self.squares[other_piece][5]=Square(other_piece, 5,Bishop(color,textures[color]['bishop'].get_rect()))

        # Rooks
        self.squares[other_piece][0]=Square(other_piece, 0,Rook(color,textures[color]['rook'].get_rect()))
        self.squares[other_piece][7]=Square(other_piece, 7,Rook(color,textures[color]['rook'].get_rect()))

        # Queen
        col=3 if self.down=='white' else 4
        self.squares[other_piece][col]=Square(other_piece, col,Queen(color,textures[color]['queen'].get_rect()))

        # King
        col=4 if self.down=='white' else 3
        self.squares[other_piece][col]=Square(other_piece, col,King(color,textures[color]['king'].get_rect()))
    