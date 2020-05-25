import pygame
import numpy as np

import utils


class Wall:

    def __init__(self, collision_vector, color=(255, 255, 255)):
        self.coll_v = np.array(collision_vector)
        self.coll_norm = self.collision_normal(collision_vector)
        self.color = color

    def collision_normal(self, points):
        a, b = points
        vector = (a[0] - b[0], a[1] - b[1])
        normal = -vector[1], vector[0]
        return utils.unit_vector(normal)

    def collides(self, point):
        pass

    def draw(self, screen):
        pass


class RectWall(Wall):
    def __init__(self, collision_vector, pos, shape):
        Wall.__init__(self, collision_vector)
        self.pos = pos
        self.rect = pygame.rect.Rect(self.pos, shape)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

    def collides(self, point):
        return self.rect.collidepoint(point[0], point[1])


class PolyWall(Wall):
    def __init__(self, points):
        Wall.__init__(self, points[0:2])
        self.points = points

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)

    def collides(self, point):
        return


