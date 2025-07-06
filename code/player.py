#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, pygame
from code.entity import ASSET_PATH

CLICK_MAX_INTERVAL = 300  # ms máximos entre cliques para considerar "duplo"

class AnimatedSprite:
    def __init__(self, frame_paths, fps=10):
        self.frames = [pygame.image.load(p).convert_alpha() for p in sorted(frame_paths)]
        self.fps = fps; self.current = 0; self.timer = 0.0

    def update(self, dt):
        self.timer += dt
        frame_time = 1000/self.fps
        if self.timer >= frame_time:
            self.timer -= frame_time
            self.current = (self.current+1) % len(self.frames)

    def frame(self):
        return self.frames[self.current]

class Player:
    def __init__(self, folder_name: str, controls_idx: int):
        spr_dir = os.path.join(ASSET_PATH, folder_name)
        if not os.path.isdir(spr_dir):
            raise FileNotFoundError(f"Sprite folder não encontrado: {spr_dir}")

        # carrega animações
        self.anim = {}
        for sub in os.listdir(spr_dir):
            path = os.path.join(spr_dir, sub)
            if os.path.isdir(path):
                key = sub.lower()
                pngs = [os.path.join(path,f)
                        for f in sorted(os.listdir(path))
                        if f.lower().endswith('.png')]
                if pngs:
                    self.anim[key] = AnimatedSprite(pngs)

        # estado inicial
        self.state = 'idle' if 'idle' in self.anim else next(iter(self.anim))
        self.image = self.anim[self.state].frame()
        self.rect = self.image.get_rect(topleft=(100,300))

        # física
        self.vel = pygame.math.Vector2(0,0)
        self.on_ground = True

        # contador de cliques de ataque
        self._last_attack_time = 0

        # controles (0 = hero1 setas+SPACE, 1 = hero2 WASD+RCTRL)
        controls_map = [
            {'left':pygame.K_LEFT,'right':pygame.K_RIGHT,'jump':pygame.K_UP,'attack':pygame.K_SPACE},
            {'left':pygame.K_a,'right':pygame.K_d,'jump':pygame.K_w,'attack':pygame.K_RCTRL}
        ]
        self.controls = controls_map[controls_idx]

    def handle_input(self, keys):
        # movimento horizontal / idle
        # Se já estamos em attack1 ou attack2, não sobrescrever
        if self.state in ('attack1', 'attack2'):
            return
        self.vel.x = 0
        if keys[self.controls['left']]:
            self.vel.x = -5
            if 'walk' in self.anim: self.state = 'walk'
        elif keys[self.controls['right']]:
            self.vel.x = 5
            if 'walk' in self.anim: self.state = 'walk'
        else:
            if self.on_ground and 'idle' in self.anim:
                self.state = 'idle'

        # pulo
        if keys[self.controls['jump']] and self.on_ground:
            self.vel.y = -12
            self.on_ground = False
            if 'jump' in self.anim: self.state = 'jump'

    def handle_event(self, event):
        # deve ser chamado em Level.run para cada pygame.event
        if event.type == pygame.KEYDOWN and event.key == self.controls['attack']:
            now = pygame.time.get_ticks()
            if now - self._last_attack_time <= CLICK_MAX_INTERVAL:
                # duplo clique
                if 'attack2' in self.anim:
                    self.state = 'attack2'
                else:
                    self.state = 'attack1'
            else:
                # clique simples
                if 'attack1' in self.anim:
                    self.state = 'attack1'
                elif 'attack' in self.anim:
                    self.state = 'attack'
            self._last_attack_time = now

    def update(self, dt):
        # gravidade
        self.vel.y += 0.5
        self.rect.x += int(self.vel.x)
        self.rect.y += int(self.vel.y)
        # chão em y=300
        if self.rect.bottom >= 300:
            self.rect.bottom = 300
            self.vel.y = 0
            self.on_ground = True

        # animação
        anim = self.anim.get(self.state, self.anim[next(iter(self.anim))])
        anim.update(dt)
        self.image = anim.frame()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    #         {'left': pygame.K_a,    'right': pygame.K_d,    'jump': pygame.K_w,    'attack': pygame.K_SPACE},
    #         {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT,'jump': pygame.K_UP,   'attack': pygame.K_RCTRL}
    #     ]
    #     self.controls = controls_map[controls_idx]
    #
    # def handle_input(self, keys):
    #     self.vel.x = 0
    #     if keys[self.controls['left']]:
    #         self.vel.x = -5
    #         if 'walk' in self.anim: self.state = 'walk'
    #     elif keys[self.controls['right']]:
    #         self.vel.x = 5
    #         if 'walk' in self.anim: self.state = 'walk'
    #     else:
    #         if self.on_ground and 'idle' in self.anim:
    #             self.state = 'idle'
    #
    #     if keys[self.controls['jump']] and self.on_ground:
    #         self.vel.y = -12
    #         self.on_ground = False
    #         if 'jump' in self.anim: self.state = 'jump'
    #
    #     if keys[self.controls['attack']]:
    #         if 'attack' in self.anim: self.state = 'attack'
    #
    # def update(self, dt):
    #     self.vel.y += 0.5
    #     self.rect.x += int(self.vel.x)
    #     self.rect.y += int(self.vel.y)
    #
    #     # chão em y=300
    #     if self.rect.bottom >= 300:
    #         self.rect.bottom = 300
    #         self.vel.y = 0
    #         self.on_ground = True
    #
    #     anim = self.anim.get(self.state, self.anim[next(iter(self.anim))])
    #     anim.update(dt)
    #     self.image = anim.frame()
    #
    # def draw(self, surface):
    #     surface.blit(self.image, self.rect)
             # Hero1
