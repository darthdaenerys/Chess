import os

class Piece:
    def __init__(self,name,color,value,rect):
        self.name=name
        self.color=color
        self.value=value if self.color=='white' else -value
        self.root_path=os.path.join('pieces',self.color)
        self.moved=False
        self.moves=[]
        self.rect=rect
    
    def add_move(self,move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves=[]

class Pawn(Piece):
    def __init__(self,color,rect,down):
        super().__init__('pawn',color, 1.0,rect)
        self.down=down
        self.en_passant=False
        if self.down=='white':
            self.direction=-1 if color=='white' else 1
        else:
            self.direction=1 if color=='white' else -1

class Knight(Piece):
    def __init__(self,color,rect):
        super().__init__('knight', color,3.0,rect)

class Bishop(Piece):
    def __init__(self,color,rect):
        super().__init__('bishop', color, 3.0,rect)

class Rook(Piece):
    def __init__(self,color,rect):
        super().__init__('rook', color, 5.0,rect)

class Queen(Piece):
    def __init__(self,color,rect):
        super().__init__('queen',color,9.0,rect)

class King(Piece):
    def __init__(self,color,rect):
        super().__init__('king',color,100.0,rect)
        self.king_rook=None
        self.queen_rook=None
        self.castled=False