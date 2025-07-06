#!/usr/bin/python
# -*- coding: utf-8 -*-
from code.background import Background
from code.const import WIN_WIDTH


class EntityFactory:


    @staticmethod
    def get_entity(entity_name: str, position=(0, 0)):
        layers = []
                # list_bg=[]
                # for i in range(4):
                #     list_bg.append(Background(f'Level1Bg{i}', (i * 576, 0), layer=i % 3))
                # return list_bg
        if entity_name == 'Level1Bg':
            images = ['Level1Bg0', 'Level1Bg1', 'Level1Bg2', 'Level1Bg3']
        elif entity_name == 'Level2Bg':
            images = ['1', '2', '3', '4']  # Summer7 layers
        elif entity_name == 'Level3Bg':
            images = ['1', '2', '3', '4']  # Summer8 layers
        else:
            return []
        for i, img in enumerate(images):
            layers.append(Background(img, (i * WIN_WIDTH, 0), layer=i))
        return layers

