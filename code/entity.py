#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
from abc import ABC, abstractmethod

import pygame
from code.const import WIN_WIDTH, WIN_HEIGHT

# class Entity(ABC):
#
#     def __init__(self,name:str, position:tuple):
#         self.name = name
#         self.surf = pygame.image.load('./asset/'+name+'.png')
#         self.rect = self.surf.get_rect(left=position[0], top=position[1])
#         self.speed = 0
#
#
#
#     @abstractmethod
#     def move(self, ):
#         pass

BASE_PATH  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSET_PATH = os.path.join(BASE_PATH, 'asset')

class Entity:
    def __init__(self, name: str, position: tuple):
        path = os.path.join(ASSET_PATH, f'{name}.png')
        self.surf = pygame.image.load(path).convert_alpha()
        self.rect = self.surf.get_rect(topleft=position)

    def move(self, direction=None):
        raise NotImplementedError
