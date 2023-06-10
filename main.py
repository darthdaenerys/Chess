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
            if self.dragger.dragging:
                self.dragger.drag_piece(self.display_surface)

            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_t:
                        self.game.change_theme()
                    elif event.key==pygame.K_r:
                        self.game.reset()
                    elif event.key==pygame.K_s:
                        self.game.reset(swap=True)
                    elif event.key==pygame.K_b:
                        self.game.change_background()

                if pygame.mouse.get_pressed()[0]:
                    x,y=pygame.mouse.get_pos()
                    col,row=(x-61)//80,(y-40)//80
                    if self.dragger.dragging:
                        self.dragger.update()
                        self.game.chess_board(self.display_surface)
                        self.game.board.show_last_move(self.display_surface)
                        self.game.board.show_moves(self.dragger.piece,self.dragger.initial_row,self.dragger.initial_col,self.display_surface)
                        self.game.render_labels(self.display_surface)
                        self.game.render_pieces(self.display_surface,self.dragger.piece)
                        self.dragger.drag_piece(self.display_surface)
                    elif col<8 and col>=0 and row>=0 and row<8:
                        if self.game.board.squares[row][col].has_piece() and self.game.board.squares[row][col].piece.color==self.game.next_player:
                            self.dragger.save_initials(x-30,y-20,row,col,self.game.board.squares[row][col].piece)
                            self.dragger.dragging=True

                elif event.type==pygame.MOUSEBUTTONUP:
                    if self.dragger.dragging:
                        move=self.game.get_move(self.dragger)
                        valid,capture,castle,check=self.game.board.validate_move(self.dragger.piece,move)
                        if valid:
                            self.game.board.move_piece(self.dragger.piece,move)
                            self.game.board.set_en_passant(self.dragger.piece)
                            self.game.alternate_turn()
                            self.game.render_pieces(self.display_surface,self.dragger.piece)
                            self.game.clear_all_moves()
                            if self.game.board.king_incheck(self.dragger.piece,move.final.row,move.final.col):
                                check=True
                                capture=False
                                self.dragger.piece.clear_moves()
                            self.game.sound(capture=capture,castle=castle,check=check)
                            self.game.calculate_all_moves(self.game.next_player)
                            if self.game.over():
                                self.game.sound(True,True,True,True)
                    self.dragger.undrag()

            # update surface
            pygame.display.update()

if __name__=="__main__":
    game=Main()
    game.run()