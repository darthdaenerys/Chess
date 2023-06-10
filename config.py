import pygame
from sound import Sound
from theme import Theme
import os
import json

class Config:
    def __init__(self):
        f=open('settings.json')
        self.settings=json.load(f)
        del f
        self.themes=[]
        self.theme_idx=self.settings['theme_idx']
        self.background_idx=self.settings['background_idx']
        self._add_theme()
        self.theme_idx%=len(self.themes)
        self.background_idx%=len(os.listdir('backgrounds'))
        self.theme=self.themes[self.theme_idx]
        self.font=pygame.font.SysFont('monospace',18,bold=True)
        self.sound=Sound(os.path.join('sounds'))

    def change_theme(self):
        self.theme_idx+=1
        self.theme_idx%=len(self.themes)
        self.settings['theme_idx']=self.theme_idx
        obj=json.dumps(self.settings,indent=4)
        with open('settings.json','w') as f:
            f.write(obj)
            f.close()
        self.theme=self.themes[self.theme_idx]

    def change_background(self):
        self.background_idx+=1
        self.background_idx%=len(os.listdir('backgrounds'))
        self.settings['background_idx']=self.background_idx
        obj=json.dumps(self.settings,indent=4)
        with open('settings.json','w') as f:
            f.write(obj)
            f.close()

    def _add_theme(self):
        green=Theme((234,235,200),(119,154,80),(244,247,116),(172,195,51),'#C86464','#9b4e4e')
        brown=Theme((237,192,168),(101,67,33),(245,234,100),(209,185,59),'#C86464','#9b4e4e')
        blue=Theme((229,220,200),(60,95,135),(123,187,227),(43,119,192),'#C86464','#C84646')
        gray=Theme((140,139,138),(86,85,84),(99,126,143),(82,102,120),'#C86464','#C84646')
        cyberpunk=Theme((233,157,225),(15,65,97),(96,41,207),(51,23,107),'#1aa0ac','#1aa0ac')
        gogreen=Theme((153,230,162),(15,50,11),(186,173,65),(158,143,12),'#26a71f','#1b7416')
        summer=Theme((212,159,103),(19,45,74),(203,53,194),(120,32,115),'#5346a4','#403680')
        garnet=Theme((223,121,121),(108,17,17),(213,198,66),(134,123,27),'#76b252','#52b25d')
        self.themes=[green,brown,blue,gray,cyberpunk,gogreen,summer,garnet]