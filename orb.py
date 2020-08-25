import numpy as np
import utils
import pygame
from gameutils import GameObject


def integ(x):
    return x ** 2 / 2.0 - x ** 3 / 3.0


class Orb(GameObject):
    speed_decay = 0.1
    defaultspeed = 3
    dash_speed = 5
    constant = 1800
    interval = 0.02
    dashing_f = [(integ(i + interval) - integ(i)) * constant + defaultspeed for i in np.arange(0.0, 1.0, interval)]
    max_dash_length = len(dashing_f)

    def __init__(self, master, pos, direction, color=None):
        self.pos = np.array(pos)
        if color is None:
            color = [255 for i in range(3)]
        self.color = color
        self.master = master
        self.radius = 10
        self.dir = utils.unit_vector(direction)
        self.speed = 0

    def move(self):
        self.pos = self.predict_position()

    def move_to(self, pos_new):
        self.pos = pos_new

    def predict_position(self):
        return self.pos + self.dir * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, [int(val) for val in self.pos], self.radius)

    def fire(self):
        self.speed = self.dash_speed


