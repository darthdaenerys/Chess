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
