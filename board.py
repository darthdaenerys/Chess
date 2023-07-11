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
        self.down=down
        self.squares=[[0,0,0,0,0,0,0,0] for _ in range(self.settings['ROWS'])]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')
        self.last_move=None
        self.theme=theme
    
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
    
    def calc_moves(self,piece,row,col,check=True):
        '''
            Calculates all the valid moves of a piece for a specific position
        '''
        def linear_moves():
            for (j,k) in [(1,0),(-1,0),(0,1),(0,-1)]:
                for i in range(1,8):
                    newrow=row+i*j
                    newcol=col+i*k
                    if Square.inrange(newrow,newcol):
                        if self.squares[newrow][newcol].isempty_or_rival(piece.color):
                            final_piece=self.squares[newrow][newcol].piece
                            move=Move(Square(row,col),Square(newrow,newcol,final_piece))
                            if check:
                                if not self.incheck(piece,move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            if self.squares[newrow][newcol].has_rival_piece(piece.color):
                                break
                        else: break
                    else: break
        
    def show_last_move(self,display_surface):
        if self.last_move:
            for square in [self.last_move.initial,self.last_move.final]:
                color=self.theme.trace_color.light if (square.row+square.col)%2==0 else self.theme.trace_color.dark
                rect=pygame.rect.Rect(61+square.col*80,40+square.row*80,80,80)
                pygame.draw.rect(display_surface,color,rect)
