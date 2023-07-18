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