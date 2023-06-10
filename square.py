import pygame

class Square:
    def __init__(self,row,col,piece=None):
        self.row=row
        self.col=col
        self.piece=piece
        self.rect=pygame.rect.Rect(61+self.col*80,40+self.row*80,80,80)
    
    def has_piece(self) -> bool:
        return self.piece!=None
    
    @staticmethod
    def inrange(*args) -> bool:
        for arg in args:
            if arg<0 or arg>7:
                return False
        return True
    
    def isempty(self) -> bool:
        return self.piece==None
    
    def has_team_piece(self,color) -> bool:
        return self.piece!=None and self.piece.color==color
    
    def has_rival_piece(self,color) -> bool:
        return self.piece!=None and self.piece.color!=color
    
    def isempty_or_rival(self,color) -> bool:
        return self.has_rival_piece(color) or self.isempty()
    
    def has_rival_piece_or_team_piece(self,color) -> bool:
        return self.has_rival_piece(color) or self.has_team_piece(color)