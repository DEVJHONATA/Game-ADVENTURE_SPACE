#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
import pygame
from pygame.constants import K_RETURN, K_BACKSPACE

from code.const         import WIN_WIDTH, WIN_HEIGHT, FPS, SCORE_FILE, C_WHITE, C_YELLOW
from code.entity        import ASSET_PATH
from code.entityFactory import EntityFactory
from code.player        import Player
from code.enemy         import Enemy

class Level:
    def __init__(self, window, level_num, mode, controls_idx):
        self.window    = window
        self.level     = level_num
        self.mode      = mode
        self.controls  = controls_idx

        self.clock      = pygame.time.Clock()
        self.start_time = pygame.time.get_ticks()

        self.load()

        # ─── INSTANCIAÇÃO DE INIMIGOS ─────────────────────────────────────────
        self.villains = [
            # Enemy('slime1'),  # primeiro inimigo
            # Enemy('slime2'),
            Enemy('gorgon_1'),  # novos inimigos
            Enemy('gorgon_2'),
            Enemy('gorgon_3'),
        ]
        # ────────────────────────────────────────────────────────────────────────

    def load(self):
        # — Carrega música do nível —───────────────────────────────────────────
        for ext in ('wav', 'mp3'):
            path = os.path.join(ASSET_PATH, f'Level{self.level}.{ext}')
            if os.path.isfile(path):
                pygame.mixer.music.load(path)
                pygame.mixer.music.play(-1)
                break

        # — Carrega camadas de fundo via EntityFactory —────────────────────────
        self.bgs = EntityFactory.get_entity(f'Level{self.level}Bg')

        # — Instancia os jogadores (só nome da pasta em asset/) —───────────────
        self.players = [
            Player('hero1', controls_idx=0),
        ]
        if self.mode >= 1:
            self.players.append(
                Player('hero2', controls_idx=1)
            )

    def run(self):
        while True:
            # controla o frame rate
            dt = self.clock.tick(FPS)

            # 1) captura todos os eventos
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()

                # 2) propaga cada evento para o handle_event de cada player
                for p in self.players:
                    p.handle_event(e)

            # 3) input contínuo de teclas (movimento e pulo)
            keys = pygame.key.get_pressed()

            # determina direção do scroll baseado no player 1
            direction = None
            if keys[self.players[0].controls['left']]:
                direction = 'right'
            elif keys[self.players[0].controls['right']]:
                direction = 'left'

            # move as camadas de fundo
            for bg in self.bgs:
                bg.move(direction)

            # atualiza cada jogador (movimento/gravity/animação)
            for p in self.players:
                p.handle_input(keys)
                p.update(dt)

            # atualiza cada inimigo
            for v in self.villains:
                v.update(dt)

            # checa colisão e game over
            for p in self.players:
                for v in list(self.villains):
                    if p.rect.colliderect(v.rect):
                        if p.state in ('attack1', 'attack2'):
                            # jogador está atacando: acerta o inimigo em vez de morrer
                            v.state = 'death_body'
                            # opcional: marque v para remoção ao final da animação
                        else:
                            # jogador não está atacando: morre
                            return self.handle_death(p)
            # desenha tudo
            self.draw()

    def draw(self):
        self.window.fill((0, 0, 0))

        if self.mode < 2:
            # Single ou Coop: desenha tudo na mesma tela
            for bg in self.bgs:
                self.window.blit(bg.surf, bg.rect)
            for v in self.villains:
                v.draw(self.window)
            for p in self.players:
                p.draw(self.window)
        else:
            # Competitivo: split-screen horizontal
            half = WIN_HEIGHT // 2
            top = pygame.Surface((WIN_WIDTH, half))
            bot = pygame.Surface((WIN_WIDTH, half))
            top.fill((0, 0, 0))
            bot.fill((0, 0, 0))

            # Fundo para a parte superior
            for bg in self.bgs:
                r = bg.rect.copy()
                r.y -= half
                top.blit(bg.surf, r)

            # Desenha inimigos em ambas as metades
            for v in self.villains:
                v.draw(top)
                bot.blit(v.image, v.rect)

            # Desenha cada jogador na sua metade
            self.players[0].draw(top)
            self.players[1].draw(bot)

            self.window.blit(top, (0, 0))
            self.window.blit(bot, (0, half))

        pygame.display.flip()

    def handle_death(self, player):
        survived = (pygame.time.get_ticks() - self.start_time) // 1000
        name = ''
        font = pygame.font.SysFont(None, 32)
        entering = True

        while entering:
            self.window.fill((0, 0, 0))
            over = font.render(f'Game Over! Score {survived}', True, C_WHITE)
            prompt = font.render('Nome (10 letras): ' + name, True, C_YELLOW)
            self.window.blit(over, (100, 100))
            self.window.blit(prompt, (100, 140))
            pygame.display.flip()

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if e.type == pygame.KEYDOWN:
                    if e.key == K_BACKSPACE:
                        name = name[:-1]
                    elif e.key == K_RETURN and name:
                        entering = False
                    elif len(name) < 5 and e.unicode.isalnum():
                        name += e.unicode

        with open(SCORE_FILE, 'a') as f:
            f.write(f"{name} {survived}\n")

        return None