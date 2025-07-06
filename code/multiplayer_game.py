import pygame, os

class AnimatedSprite:
    def __init__(self, folder, loop=True, frame_time=100):
        self.frames = []
        for fn in sorted(os.listdir(folder)):
            if fn.lower().endswith('.png'):
                img = pygame.image.load(os.path.join(folder, fn)).convert_alpha()
                self.frames.append(img)
        self.loop = loop
        self.frame_time = frame_time
        self.index = 0
        self.timer = 0
    def update(self, dt):
        if not self.frames: return
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0 if self.loop else len(self.frames)-1
    def frame(self):
        return self.frames[self.index] if self.frames else None


def PLAYER_CONTROLS():
    return None