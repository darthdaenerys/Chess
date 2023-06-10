import pygame
import os

class Sound:
    def __init__(self,root_path) -> None:
        self.move_sound=pygame.mixer.Sound(os.path.join(root_path,'move.wav'))
        self.capture_sound=pygame.mixer.Sound(os.path.join(root_path,'capture.wav'))
        self.start_sound=pygame.mixer.Sound(os.path.join(root_path,'game_start.wav'))
        self.end_sound=pygame.mixer.Sound(os.path.join(root_path,'game_end.wav'))
        self.check_sound=pygame.mixer.Sound(os.path.join(root_path,'check.wav'))
        self.castle_sound=pygame.mixer.Sound(os.path.join(root_path,'castle_01.wav'))