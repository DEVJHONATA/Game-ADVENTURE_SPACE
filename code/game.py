#!/usr/bin/python
# -*- coding: utf-8 -*-
import pygame, os
from code.const import FPS, MENU_OPTION, SCORE_FILE, C_WHITE, C_YELLOW, WIN_WIDTH, WIN_HEIGHT
from code.menu import Menu
from code.level import Level

class Game:
    def __init__(self): pygame.init(); pygame.mixer.init(); self.win=pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT)); self.clock=pygame.time.Clock()
    def show_scores(self):
        font=pygame.font.SysFont(None,28)
        lines=[]
        if os.path.isfile(SCORE_FILE):
            with open(SCORE_FILE) as f: lines=f.readlines()
        display=True
        while display:
            self.win.fill((0,0,0))
            y=100
            for ln in lines:
                text=font.render(ln.strip(),True,C_WHITE); self.win.blit(text,(100,y)); y+=30
            info=font.render('Press Enter to return',True,C_YELLOW); self.win.blit(info,(100,y+20))
            pygame.display.flip()
            for e in pygame.event.get():
                if e.type==pygame.QUIT: pygame.quit(); quit()
                if e.type==pygame.KEYDOWN and e.key==pygame.K_RETURN: display=False
    def run(self):
        menu=Menu(self.win)
        while True:
            choice=menu.run()
            if choice=='EXIT': break
            if choice=='SCORE': self.show_scores(); continue
            mode=MENU_OPTION.index(choice)
            lvl=Level(self.win,1,mode,list(range(mode+1)))
            lvl.run()
        pygame.quit()
