import pygame
import json
from board import Board
from move import Move
from config import Config
from square import Square
import random
import os

# global textures
textures={}
def _create_surfaces():
    for color in ['white','black']:
        textures[color]={}
        for image in ['rook','bishop','queen','king','knight','pawn']:
            path=os.path.join('pieces',color,f'{image}.png')
            surface=pygame.image.load(path).convert_alpha()
            textures[color][image]=surface

class Game:
    def __init__(self,swap=False):
        f=open('settings.json')
        self.settings=json.load(f)
        f.close()
        del f
        self.config=Config()
        _create_surfaces()
        if not swap:
            if self.settings['player']=='random':
                self.down=random.choice(['white','black'])
            elif self.settings['player']=='white':
                self.down='white'
            else:
                self.down='black'
        else:
            self.down='white' if self.down=='black' else 'black'
        self.board=Board(self.config.theme,self.down)
        self.opponent='black' if self.down=='white' else 'white'
        self.next_player='white'
        self.hovered_square=None
        image=os.listdir('backgrounds')[self.settings['background_idx']]
        self.background_surface=pygame.image.load(os.path.join('backgrounds',image)).convert()
        self.alphacol={0:'a',1:'b',2:'c',3:'d',4:'e',5:'f',6:'g',7:'h'}
        self.calculate_all_moves('white')
        self.sound(start=True)

    def render_background(self,display_surface):
        display_surface.blit(self.background_surface,(0,0))
    
    def chess_board(self,display_surface):
        theme=self.config.theme
        for row in range(self.settings["ROWS"]):
            for col in range(self.settings["COLS"]):
                color=theme.square_color.light if (row+col)%2==0 else theme.square_color.dark
                rect=pygame.rect.Rect(61+col*80,40+row*80,80,80)
                pygame.draw.rect(display_surface,color,rect)
    
    def render_pieces(self,display_surface,drag_piece):
        self.update_pieces(drag_piece)
        
        # blit piece surfaces on the chess board
        for row in range(self.settings["ROWS"]):
            for col in range(self.settings["COLS"]):
                if self.board.squares[row][col].has_piece() and self.board.squares[row][col].piece!=drag_piece:
                    piece=self.board.squares[row][col].piece
                    piece.rect=textures[piece.color][piece.name].get_rect(center=self.board.squares[row][col].rect.center)
                    display_surface.blit(textures[piece.color][piece.name],piece.rect.topleft)
    
    def render_labels(self,display_surface):
        theme=self.config.theme
        for row in range(self.settings['ROWS']):
            color=theme.square_color.dark if row%2==0 else theme.square_color.light
            num=self.settings['ROWS']-row if self.down=='white' else (9-self.settings['ROWS']+row)
            label=self.config.font.render(str(num),True,color)
            position=(61+5,40+5+row*80)
            display_surface.blit(label,position)
        for col in range(self.settings['COLS']):
            color=theme.square_color.dark if (col+7)%2==0 else theme.square_color.light
            num=col if self.down=='white' else 7-col
            label=self.config.font.render(self.alphacol[num],True,color)
            position=(61+col*80+65,40+7*80+60)
            display_surface.blit(label,position)

    def show_hover(self,display_surface):
        if self.hovered_square:
            color=(180,180,180)
            rect=pygame.rect.Rect(61+self.hovered_square.col*80,40+self.hovered_square.row*80,80,80)
            pygame.draw.rect(display_surface,color,rect,width=3)

    def get_hover(self,x,y,display_surface):
        x-=61
        y-=40
        col,row=x//80,y//80
        self.hovered_square=self.board.squares[row][col] if Square.inrange(row,col) else None
        self.show_hover(display_surface)

    def clear_all_moves(self):
        for row in range(self.settings['ROWS']):
            for col in range(self.settings['COLS']):
                if self.board.squares[row][col].has_piece():
                    self.board.squares[row][col].piece.clear_moves()

    # TODO: optimize the method -> increases CPU utililization
    def calculate_all_moves(self,color):
        for row in range(self.settings['ROWS']):
            for col in range(self.settings['COLS']):
                if self.board.squares[row][col].has_piece() and self.board.squares[row][col].piece.color==color:
                    self.board.calc_moves(self.board.squares[row][col].piece,row,col)
    
    def get_move(self,dragger):
        x,y=dragger.get_position()
        x-=61
        y-=40
        released_row,released_col=y//80,x//80
        initial_square=Square(dragger.initial_row,dragger.initial_col,dragger.piece)
        final_square=Square(released_row,released_col,dragger.piece)
        return Move(initial_square,final_square)

    def update_pieces(self,drag_piece):
        for row in range(self.settings['ROWS']):
            for col in range(self.settings['COLS']):
                if self.board.squares[row][col].has_piece() and self.board.squares[row][col].piece!=drag_piece:
                    self.board.squares[row][col].piece.rect.center=self.board.squares[row][col].rect.center

    def alternate_turn(self):
        self.next_player='black' if self.next_player=='white' else 'white'

    def change_theme(self):
        self.config.change_theme()
        self.board.theme=self.config.theme
    
    def sound(self,capture=False,start=False,castle=False,check=False):
        sound=self.config.sound
        if capture and start and castle and check:
            sound.end_sound.play()
            return
        if start:
            sound.start_sound.play()
            return
        if capture:
            sound.capture_sound.play()
            return
        if castle:
            sound.castle_sound.play()
            return
        if check:
            sound.check_sound.play()
            return
        sound.move_sound.play()
        
    def change_background(self):
        self.config.change_background()
        f=open('settings.json')
        self.settings=json.load(f)
        f.close()
        image=os.listdir('backgrounds')[self.settings['background_idx']]
        self.background_surface=pygame.image.load(os.path.join('backgrounds',image)).convert()

    def reset(self,swap=False):
        self.__init__(swap)
    
    def over(self):
        game_over=True
        for row in range(self.settings['ROWS']):
            for col in range(self.settings['COLS']):
                if self.board.squares[row][col].has_team_piece(self.next_player):
                    if len(self.board.squares[row][col].piece.moves)!=0:
                        game_over=False
                        break
            if not game_over:
                break
        return game_over