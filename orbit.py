import pygame


class Orbit:
    def __init__(self, pos, radius, color):
        self.color = color
        self.pos = pos
        self.radius = radius

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.radius)