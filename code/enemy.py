from code.entity import ASSET_PATH#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pygame
from code.entity import ASSET_PATH

class AnimatedSprite:
    def __init__(self, frame_paths, fps=6):
        self.frames = [pygame.image.load(p).convert_alpha() for p in sorted(frame_paths)]
        self.fps = fps
        self.current = 0
        self.timer = 0.0

    def update(self, dt):
        self.timer += dt
        frame_time = 1000 / self.fps
        if self.timer >= frame_time:
            self.timer -= frame_time
            self.current = (self.current + 1) % len(self.frames)

    def frame(self):
        return self.frames[self.current]


class Enemy:
    def __init__(self, folder_name: str):
        # monta o caminho completo: Game/asset/<folder_name>
        spr_dir = os.path.join(ASSET_PATH, folder_name)
        if not os.path.isdir(spr_dir):
            raise ValueError(f"No animation folders found in {folder_name}")

        # carrega animações das subpastas Idle_body, Walk_body, etc.
        self.anim = {}
        for sub in os.listdir(spr_dir):
            path = os.path.join(spr_dir, sub)
            if os.path.isdir(path):
                key = sub.lower()
                pngs = [os.path.join(path, f)
                        for f in sorted(os.listdir(path))
                        if f.lower().endswith('.png')]
                if pngs:
                    self.anim[key] = AnimatedSprite(pngs)

        # estado inicial
        self.state = 'idle_body' if 'idle_body' in self.anim else next(iter(self.anim))
        self.image = self.anim[self.state].frame()
        self.rect = self.image.get_rect(topleft=(400, 300))  # ajuste conforme desejar

        # sinalizador de vida
        self.alive = True

        # velocidade ou lógica de patrulha
        self.speed = 2

    def update(self, dt):
        # ─── Se estiver em death_body, só anima e marca como morto ───────────
        if self.state == 'death_body':
            self.anim[self.state].update(dt)
            # ao chegar no último frame, marca para remoção
            if self.anim[self.state].current == len(self.anim[self.state].frames) - 1:
                self.alive = False
            # não faz mais nada além de animar morte
            return
        # ─────────────────────────────────────────────────────────────────────

        # Lógica normal de inimigo (ex: patrulha simples)
        # Exemplo: anda para a direita e volta ao chegar na borda
        self.rect.x += self.speed
        if self.rect.left < 0 or self.rect.right > 576:
            self.speed *= -1

        # atualiza animação de acordo com direção
        key = 'walk_body' if 'walk_body' in self.anim else self.state
        self.anim[key].update(dt)
        self.image = self.anim[key].frame()

    def draw(self, surface):
        surface.blit(self.image, self.rect)
