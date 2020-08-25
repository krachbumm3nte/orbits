import pygame
import numpy as np

import utils
from gameutils import GameObject


class Wall(GameObject):

    def __init__(self, collision_vector, color=(255, 255, 255)):
        self.coll_v = np.array(collision_vector)
        self.coll_norm = utils.perp(utils.unit_vector(self.coll_v[1] - self.coll_v[0]))
        print(self.coll_v, self.coll_norm)
        self.color = color

    def collides(self, point):
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
        Wall.__init__(self, points[:2])
        self.points = points

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, self.points)

    def collides(self, point):
        return


