#!/usr/bin/python
# -*- coding: utf-8 -*-

from code.entity import Entity
from code.const import WIN_WIDTH

class Background(Entity):
    def __init__(self, name: str, position: tuple,layer: int = 0):
        super().__init__(name, position)
        self.layer = layer  # camada: 0 = fundo distante, 1 = médio, 2 = frente

    def move(self,direction: str = None ):
        # speed_map = {0: 0.3, 1: 0.6, 2: 1.0}  # velocidades por camada
        # if direction == "left":
        #     self.rect.x += speed_map[self.layer]
        # elif direction == "right":
        #     self.rect.x -= speed_map[self.layer]
        #
        # # Loop para paralaxe infinita
        # if self.rect.right < 0:
        #     self.rect.left = 576
        # elif self.rect.left > 576:
        #     self.rect.right = 0
        speed_map = {0: 0.2, 1: 0.4, 2: 0.6, 3: 0.8, 4: 1.0}
        speed = speed_map.get(self.layer, 1.0)

        if direction == "left":
            self.rect.x += speed
        elif direction == "right":
            self.rect.x -= speed

            # Reposiciona quando sai da tela (loop)
            if self.rect.right < 0:
                self.rect.left = WIN_WIDTH
            elif self.rect.left > WIN_WIDTH:
                self.rect.right = 0