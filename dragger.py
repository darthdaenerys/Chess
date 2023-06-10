import pygame
import os

# global textures
textures={}
drag_textures={}
def create_surfaces():
    for color in ['white','black']:
        textures[color]={}
        drag_textures[color]={}
        for image in ['rook','bishop','queen','king','knight','pawn']:
            path=os.path.join('pieces',color,f'{image}.png')
            surface=pygame.image.load(path).convert_alpha()
            textures[color][image]=surface
            path=path=os.path.join('pieces',color,f'{image}_100px.png')
            surface=pygame.image.load(path).convert_alpha()
            drag_textures[color][image]=surface

class Dragger:
    def __init__(self):
        self.position=(0,0)
        self.initial_pos=(0,0)
        self.row=0
        self.col=0
        self.initial_row=0
        self.initial_col=0
        self.dragging=False
        self.piece=None
        create_surfaces()
    
    def get_position(self) -> tuple:
        x,y=pygame.mouse.get_pos()
        x-=30
        y-=20
        return x,y
    
    def save_initials(self,x,y,row,col,piece):
        self.piece=piece
        self.initial_pos=(x,y)
        self.initial_row,self.initial_col=row,col
        self.piece.rect.center=self.initial_pos
    
    def drag_piece(self,display_surface):
        self.update()
        display_surface.blit(drag_textures[self.piece.color][self.piece.name],self.piece.rect.topleft)
    
    def undrag(self):
        if self.piece!=None:
            self.piece.texture_path=os.path.join(self.piece.root_path,f'{self.piece.name}.png')
            self.piece=None
            self.dragging=False
    
    def update(self):
        self.position=self.get_position()
        self.piece.rect.center=self.position