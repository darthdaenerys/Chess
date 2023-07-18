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