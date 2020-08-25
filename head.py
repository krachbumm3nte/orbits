import random
import tracer
from orb import Orb
import numpy as np
import utils
import pygame
import state
from state import State


class Head(Orb):

    def __init__(self, master, pos, dir=(0, 1), starting_orbs=15):
        Orb.__init__(self, master, pos, dir, [random.randrange(100, 255) for i in range(3)])
        self.speed = self.defaultspeed
        self.tracer = tracer.Tracer(self.pos, self.dir, self.dashing_f)
        self.radius = 15
        self.children = [Orb(self, self.pos, self.dir, self.color) for i in range(starting_orbs)]
        self.state = state.Flight_state(**{"head": self})
        self.action = False

    def reflect(self, direction):
        print('reflect', self.dir, direction)
        self.tracer.deflection(self.pos, direction)
        self.dir = direction

    def get_color(self):
        if isinstance(self.state, state.Dash_state):
            return 255, 255, 255
        else:
            return self.color

    def check_wall_collisions(self):
        pos_new = self.pos + self.dir * (self.radius + self.speed)
        for w in self.master.walls:

            intersect = utils.seg_intersect((self.pos, pos_new), w.coll_v)
            # TODO: fix this shite
            if intersect:
                dot = np.dot(self.dir, w.coll_norm)
                print(w.coll_norm, dot, self.dir)
                out = self.dir - 2 * dot * w.coll_norm
                self.reflect(np.array(out))

                if np.isnan(sum(self.dir)):
                    print('sheet')
                return
            # print(intersect, self.pos, self.dir, self.speed, pos_new, w.coll_v)

    def update(self):
        self.tracer.update()

        new_state = self.state.next(self.action)
        self.action = False

        if new_state:
            args = new_state[1]
            args['head'] = self
            self.state = getattr(state, new_state[0])(**args)

    def move(self):

        self.pos, self.dir = self.state.compute(self.pos, self.dir)

        # update positions of tail orbs
        tail_positions = self.tracer.retrace(len(self.children), 0)

        for i in range(len(tail_positions)):
            self.children[i].move_to(tail_positions[i])

    def act(self):
        self.action = True

    def check_orbit_collisions(self):
        for orbit in self.master.orbits:
            if utils.distance_p_p(self.pos, orbit.pos) < orbit.radius:
                return orbit.pos

    def fire(self):
        print('pew')
        bullet = self.children.pop()
        bullet.fire()

    def draw(self, screen):
        pygame.draw.circle(screen, self.get_color(), [int(val) for val in self.pos], self.radius)
        for child in self.children:
            child.draw(screen)
