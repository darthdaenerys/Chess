import pygame

class Square:
    def __init__(self,row,col,piece=None):
        self.row=row
        self.col=col
        self.piece=piece
        self.rect=pygame.rect.Rect(61+self.col*80,40+self.row*80,80,80)