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