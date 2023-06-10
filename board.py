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
        
        def diagonal_moves():
            for x,y in [(1,1),(1,-1),(-1,-1),(-1,1)]:
                for i,j in [(1,1),(2,2),(3,3),(4,4),(5,5),(6,6),(7,7)]:
                    newrow=row+i*x
                    newcol=col+j*y
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

        def castle_possible(rook_col,king_col) -> bool:
            if rook_col<king_col:
                for j in range(rook_col+1,king_col):
                    if not self.squares[row][j].isempty():
                        return False
            else:
                for j in range(king_col+1,rook_col):
                    if not self.squares[row][j].isempty():
                        return False
            return True

        def en_passant_possible(final_col,r):
            if Square.inrange(final_col) and row==r:
                if self.squares[row][final_col].has_rival_piece(piece.color):
                    if isinstance(self.squares[row][final_col].piece,Pawn):
                        if self.squares[row][final_col].piece.en_passant:
                            return True
            return False

        if isinstance(piece, Pawn):
            # vertical moves
            for i in range(2-piece.moved):
                newrow=row+(i+1)*piece.direction
                newcol=col
                if Square.inrange(newrow,newcol):
                    if self.squares[newrow][newcol].isempty():
                        final_piece=self.squares[newrow][newcol].piece
                        move=Move(Square(row,col),Square(newrow,newcol,final_piece))
                        if check:
                            if not self.incheck(piece,move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else: break
                else: break
            
            # diagonal captures
            for i in [1,-1]:
                newrow=row+piece.direction
                newcol=col+i
                if Square.inrange(newrow,newcol):
                    if self.squares[newrow][newcol].has_rival_piece(piece.color):
                        final_piece=self.squares[newrow][newcol].piece
                        move=Move(Square(row,col),Square(newrow,newcol,final_piece))
                        if check:
                            if not self.incheck(piece,move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
            
            # en-passant moves
            if self.down=='white':
                r=3 if piece.color=='white' else 4
                newrow=2 if piece.color=='white' else 5
            else:
                r=3 if piece.color=='black' else 4
                newrow=2 if piece.color=='black' else 5

            # left en passant
            if en_passant_possible(col-1,r):
                final_piece=self.squares[row][col-1].piece
                move=Move(Square(row,col),Square(newrow,col-1,final_piece))
                if check:
                    if not self.incheck(piece,move):
                        piece.add_move(move)
                else:
                    piece.add_move(move)

            # right en passant
            if en_passant_possible(col+1,r):
                final_piece=self.squares[row][col+1].piece
                move=Move(Square(row,col),Square(newrow,col+1,final_piece))
                if check:
                    if not self.incheck(piece,move):
                        piece.add_move(move)
                else:
                    piece.add_move(move)

        if isinstance(piece, Rook):
            linear_moves()

        if isinstance(piece, Bishop):
            diagonal_moves()

        if isinstance(piece, Knight):
            moves=[(-2,1),(-1,2),(1,2),(2,1),(2,-1),(1,-2),(-1,-2),(-2,-1)]
            for move in moves:
                newrow=row+move[0]
                newcol=col+move[1]
                if Square.inrange(newrow,newcol):
                    if self.squares[newrow][newcol].isempty_or_rival(piece.color):
                        final_piece=self.squares[newrow][newcol].piece
                        move=Move(Square(row,col),Square(newrow,newcol,final_piece))
                        if check:
                            if not self.incheck(piece,move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

        if isinstance(piece, Queen):
            linear_moves()
            diagonal_moves()

        if isinstance(piece, King):
            for i,j in [(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1),(-1,-1)]:
                newrow=row+i
                newcol=col+j
                if Square.inrange(newrow,newcol):
                    if self.squares[newrow][newcol].isempty_or_rival(piece.color):
                        final_piece=self.squares[newrow][newcol].piece
                        move=Move(Square(row,col),Square(newrow,newcol,final_piece))
                        if check:
                            if not self.incheck(piece,move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
            
            if not piece.moved:

                # king side castling
                num=0 if self.down=='black' else 7
                king_rook=self.squares[row][num].piece
                if isinstance(king_rook,Rook) and not king_rook.moved and castle_possible(num,col):
                    piece.king_rook=king_rook
                    if self.down=='white':
                        move1=Move(Square(row,col),Square(row,col,piece))
                        move2=Move(Square(row,col),Square(row,col+1,piece))
                        move3=Move(Square(row,col),Square(row,col+2,piece))
                    else:
                        move1=Move(Square(row,col),Square(row,col,piece))
                        move2=Move(Square(row,col),Square(row,col-1,piece))
                        move3=Move(Square(row,col),Square(row,col-2,piece))
                    if check:
                        if not self.incheck(piece,move1) and not self.incheck(piece,move2) and not self.incheck(piece,move3):
                            piece.add_move(move3)
                            king_rook.add_move(Move(Square(row,7),Square(row,5))) if self.down=='white' else king_rook.add_move(Move(Square(row,0),Square(row,2)))

                # queen side castling
                num=0 if self.down=='white' else 7
                queen_rook=self.squares[row][num].piece
                if isinstance(queen_rook,Rook) and not queen_rook.moved and castle_possible(num,col):
                    piece.queen_rook=queen_rook
                    if self.down=='white':
                        move1=Move(Square(row,col),Square(row,col,piece))
                        move2=Move(Square(row,col),Square(row,col-1,piece))
                        move3=Move(Square(row,col),Square(row,col-2,piece))
                    else:
                        move1=Move(Square(row,col),Square(row,col,piece))
                        move2=Move(Square(row,col),Square(row,col+1,piece))
                        move3=Move(Square(row,col),Square(row,col+2,piece))
                    if check:
                        if not self.incheck(piece,move1) and not self.incheck(piece,move2) and not self.incheck(piece,move3):
                            piece.add_move(move3)
                            queen_rook.add_move(Move(Square(row,0),Square(row,3))) if self.down=='white' else queen_rook.add_move(Move(Square(row,7),Square(row,4)))
    
    def move_piece(self,piece,move,castle=False,check=False):
        initial_square=move.initial
        final_square=move.final

        # remove opponent's pawn after en passant
        if isinstance(piece,Pawn):
            diff=final_square.col-initial_square.col
            if diff!=0 and self.squares[final_square.row][final_square.col].isempty():
                self.squares[initial_square.row][initial_square.col+diff].piece=None

        self.squares[initial_square.row][initial_square.col].piece=None
        self.squares[final_square.row][final_square.col].piece=piece
        piece.moved=True
        
        if not castle:
            self.last_move=move
            if isinstance(piece,King) and self.castling(initial_square,final_square):
                diff=final_square.col-initial_square.col
                if self.down=='white':
                    rook=piece.queen_rook if diff<0 else piece.king_rook
                else:
                    rook=piece.queen_rook if diff>0 else piece.king_rook
                self.move_piece(rook,rook.moves[-1],castle=True)

        if isinstance(piece,Pawn) and not check:
            self.check_promotion(piece,final_square,check)
    
    def check_promotion(self,piece,final,check=False):
        if check:
            return final.row==0 or final.row==7
        elif final.row==0 or final.row==7:
            window=Tk()
            def buttonclicked(message):
                if message=='queen':
                    self.squares[final.row][final.col].piece=Queen(piece.color,textures[piece.color]['queen'].get_rect())
                elif message=='rook':
                    self.squares[final.row][final.col].piece=Rook(piece.color,textures[piece.color]['rook'].get_rect())
                elif message=='knight':
                    self.squares[final.row][final.col].piece=Knight(piece.color,textures[piece.color]['knight'].get_rect())
                else:
                    self.squares[final.row][final.col].piece=Bishop(piece.color,textures[piece.color]['bishop'].get_rect())
                window.destroy()
            bishop=Button(window,text='Bishop',command=lambda m='bishop':buttonclicked(m))
            bishop.place(x=30,y=50)
            knight=Button(window,text='Knight',command=lambda m='knight':buttonclicked(m))
            knight.place(x=120,y=50)
            queen=Button(window,text='Queen',command=lambda m='queen':buttonclicked(m))
            queen.place(x=30,y=120)
            rook=Button(window,text='Rook',command=lambda m='rook':buttonclicked(m))
            rook.place(x=120,y=120)

            window.title('Pawn Promotion')
            window.geometry("200x200+10+10")
            window.mainloop()

    def incheck(self,piece,move) -> bool:
        temp_piece=copy.deepcopy(piece)
        temp_board=copy.deepcopy(self)

        temp_board.move_piece(temp_piece,move,castle=True,check=True)
        for row in range(self.settings['ROWS']):
            for col in range(self.settings['COLS']):
                if temp_board.squares[row][col].has_rival_piece(piece.color):
                    temp_board.calc_moves(temp_board.squares[row][col].piece,row,col,False)
                    for m in temp_board.squares[row][col].piece.moves:
                        if isinstance(m.final.piece,King):
                            return True
        return False

    def castling(self,initial,final) -> bool:
        return abs(initial.col-final.col)==2
    
    def set_en_passant(self,piece):
        if isinstance(piece,Pawn):
            for row in range(self.settings['ROWS']):
                for col in range(self.settings['COLS']):
                    if isinstance(self.squares[row][col].piece,Pawn):
                        self.squares[row][col].piece.en_passant=False
            piece.en_passant=True

    def king_incheck(self,rival_piece,row,col):
        self.calc_moves(rival_piece,row,col,False)
        for move in rival_piece.moves:
            if isinstance(move.final.piece,King):
                return True
        return False
    
    def validate_move(self,piece,move) -> tuple:
        for possible_move in piece.moves:
            capture=False
            castle=False
            if Square.inrange(move.final.row,move.final.col):
                if self.squares[move.final.row][move.final.col].has_rival_piece(piece.color):
                    capture=True
                if isinstance(piece,Pawn):
                    diff=move.final.col-move.initial.col
                    if diff!=0 and self.squares[move.final.row][move.final.col].isempty():
                        capture=True
                if isinstance(piece,King) and abs(move.final.col-move.initial.col)==2:
                    castle=True
            if possible_move.final.row==move.final.row and possible_move.final.col==move.final.col:
                return True,capture,castle,False
        return False,False,False,False

    def show_moves(self,piece,row,col,surface):
        if self.settings['helper']:
            for move in piece.moves:
                color=self.theme.moves_color.light if (row+col)%2==0 else self.theme.moves_color.dark
                rect=pygame.rect.Rect(61+move.final.col*80,40+move.final.row*80,80,80).inflate(-4,-4)
                pygame.draw.rect(surface, color, rect)
    
    def show_last_move(self,display_surface):
        if self.last_move:
            for square in [self.last_move.initial,self.last_move.final]:
                color=self.theme.trace_color.light if (square.row+square.col)%2==0 else self.theme.trace_color.dark
                rect=pygame.rect.Rect(61+square.col*80,40+square.row*80,80,80)
                pygame.draw.rect(display_surface,color,rect)
