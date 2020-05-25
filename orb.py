from random import random

import numpy as np

import utils


class Orb:
    speed_decay = 0.1

    def __init__(self, master, pos, direction, color=None):
        if color is None:
            color = [255 for i in range(3)]
        self.color = color
        self.master = master
        self.radius = 30
        self.pos = np.array(pos)
        self.dir = utils.unit_vector(direction)
        self.speed = 0

    def move(self):
        self.pos = self.predict_position()


    def predict_position(self):
        return self.pos + self.dir * self.speed



