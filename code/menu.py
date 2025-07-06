#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, pygame
from code.const import WIN_WIDTH, COLOR_ORANGE, MENU_OPTION, C_WHITE, C_YELLOW
from code.entity import ASSET_PATH

class Menu:
    def __init__(self, window):
        self.window = window
        # Menu background image
        self.bg = pygame.image.load(os.path.join(ASSET_PATH, 'Summer5.png')).convert()
        self.rect = self.bg.get_rect()

    def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
        font = pygame.font.SysFont('Lucida Sans Typewriter', text_size)
        surf = font.render(text, True, text_color).convert_alpha()
        rect = surf.get_rect(center=text_center_pos)
        self.window.blit(surf, rect)

    def run(self):
        option = 0
        # Load and play menu music
        music_file = os.path.join(ASSET_PATH, 'MENU.mp3')
        pygame.mixer.music.load(music_file)
        pygame.mixer.music.play(-1)

        while True:
            # Draw background
            self.window.blit(self.bg, self.rect)
            # Draw title
            self.menu_text(50, 'ADVENTURE', COLOR_ORANGE, (WIN_WIDTH/2, 50))
            self.menu_text(50, 'SPACE', COLOR_ORANGE, (WIN_WIDTH/2, 100))
            # Draw options
            for i, text in enumerate(MENU_OPTION):
                color = C_YELLOW if i == option else C_WHITE
                self.menu_text(20, text, color, (WIN_WIDTH/2, 170 + i*25))

            pygame.display.flip()

            # Handle input
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_DOWN:
                        option = (option + 1) % len(MENU_OPTION)
                    elif e.key == pygame.K_UP:
                        option = (option - 1) % len(MENU_OPTION)
                    elif e.key == pygame.K_RETURN:
                        return MENU_OPTION[option]











# import os
# from tkinter.font import Font
# from code.entity import ASSET_PATH
# import pygame
# from pygame.rect import Rect
# from pygame.surface import Surface
#
# from code.const import WIN_WIDTH, COLOR_ORANGE, MENU_OPTION, C_WHITE, C_YELLOW
#
#
# class Menu:
#     def __init__(self, window):
#         self.window = window
#         self.blackgroundMenu = pygame.image.load('./asset/Summer5.png')
#         self.rect = self.blackgroundMenu.get_rect(left=0,
#                                                   top=0)  # dizendo aqui que o RECT (retangulo ivizivel ) ressebe blackgroundmenu (imagem do menu )
#
#     def run(self, ):
#         menu_option = 0
#         #  MUSIC
#         # pygame.mixer_music.load('./asset/MENU.mp3')
#         pygame.mixer.music.load(os.path.join(ASSET_PATH, 'MENU.mp3'))
#         pygame.mixer_music.play(-1)
#         while True:
#             #DRAW IMAGES
#             self.window.blit(source=self.blackgroundMenu,
#                              dest=self.rect)  # dizemos que a imagem tem que aparecer no rect
#             self.menu_text(text_size=50, text="ADVENTURE", text_color=COLOR_ORANGE,
#                            text_center_pos=((WIN_WIDTH / 2), 50))
#             self.menu_text(text_size=50, text="SPACE", text_color=COLOR_ORANGE,
#                            text_center_pos=((WIN_WIDTH / 2), 100))
#
#             for i in range(len(MENU_OPTION)):
#                 if i == menu_option:
#                     self.menu_text(text_size=20, text=MENU_OPTION[i], text_color=C_YELLOW,
#                                text_center_pos=((WIN_WIDTH / 2), 170 + i * 25)
#                                )
#                 else:
#                     self.menu_text(text_size=20, text=MENU_OPTION[i], text_color= C_WHITE,
#                                    text_center_pos=((WIN_WIDTH / 2), 170 + i * 25)
#                                    )
#             pygame.display.flip()
#
#             # Check for all events
#             for e in pygame.event.get():
#                 if e.type == pygame.QUIT:
#                     pygame.quit();
#                     quit()
#                 elif e.type == pygame.KEYDOWN:
#                     if e.key == pygame.K_DOWN:
#                         option = (option + 1) % len(MENU_OPTION)
#                     elif e.key == pygame.K_UP:
#                         option = (option - 1) % len(MENU_OPTION)
#                     elif e.key == pygame.K_RETURN:
#                         return MENU_OPTION[option]

    # def menu_text(self, text_size: int, text: str, text_color: tuple, text_center_pos: tuple):
    #     text_font: Font = pygame.font.SysFont(name="Lucida Sans Typewriter", size=text_size)
    #     text_surf: Surface = text_font.render(text, True, text_color).convert_alpha()
    #     text_rect: Rect = text_surf.get_rect(center=text_center_pos)
    #     self.window.blit(source=text_surf, dest=text_rect)
