# particle.py

import pygame
import random
from constants import TRANSPARENCY_DEC, AGE_INC

class Particle:
    def __init__(self, x, y, size, lifespan, transparency, color, mode):
        self.x = x
        self.y = y
        self.size = size
        self.lifespan = lifespan
        self.transparency = transparency
        self.color = color
        self.mode = mode

    def update(self):
        self.lifespan -= AGE_INC
        self.transparency -= TRANSPARENCY_DEC
        if self.transparency < 0:
            self.transparency = 0

    def is_dead(self):
        return self.lifespan <= 0 or self.transparency <= 0

    def draw(self, surface):
        if self.transparency > 0:
            alpha_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
            color = (*self.color, self.transparency)
            if self.mode == 2:  # Complex mode
                # Draw multiple circles to simulate a cloud or fire
                for _ in range(3):
                    offset_x = random.randint(-self.size // 4, self.size // 4)
                    offset_y = random.randint(-self.size // 4, self.size // 4)
                    radius = random.randint(self.size // 4, self.size // 2)
                    pygame.draw.circle(
                        alpha_surface,
                        color,
                        (self.size // 2 + offset_x, self.size // 2 + offset_y),
                        radius,
                    )
            else:
                pygame.draw.circle(
                    alpha_surface,
                    color,
                    (self.size // 2, self.size // 2),
                    self.size // 2,
                )
            surface.blit(
                alpha_surface, (self.x - self.size // 2, self.y - self.size // 2)
            )