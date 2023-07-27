import pygame
import os
from game import Game
import json
import sys
from dragger import Dragger
import threading

class Main:
    def __init__(self):
        pygame.init()
        f=open('settings.json')
        self.settings=json.load(f)
        del f

        # initial pygame setup
        self.display_surface=pygame.display.set_mode((self.settings['window_width'],self.settings['window_height']))
        pygame.display.set_caption('Chess')
        self.clock=pygame.time.Clock()

        # essential main objects
        self.game=Game()
        self.dragger=Dragger()

    def run(self):
        while True:
            self.clock.tick(30)/1000

            # draw sprites
            self.game.render_background(self.display_surface)
            self.game.chess_board(self.display_surface)
            self.game.board.show_last_move(self.display_surface)
            self.game.get_hover(*pygame.mouse.get_pos(),self.display_surface)
            if self.dragger.dragging:
                self.game.board.show_moves(self.dragger.piece,self.dragger.initial_row,self.dragger.initial_col,self.display_surface)
            self.game.render_labels(self.display_surface)
            self.game.render_pieces(self.display_surface,self.dragger.piece)
            