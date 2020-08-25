import random
import tracer
from orb import Orb
import numpy as np
import utils
import pygame
from state import State


class Head(Orb):




    def __init__(self, master, pos, dir=(0, 1), starting_orbs=15):
        Orb.__init__(self, master, pos, dir, [random.randrange(100, 255) for i in range(3)])
        self.speed = self.defaultspeed
        self.orbit_centre = None
        self.clockwise = False
        self.tracer = tracer.Tracer(self.pos, self.dir, self.dashing_f)
        self.angle = 0 # TODO: still required?
        self.rot_matrix = np.zeros((2, 2), dtype=float)
        self.dashing = False
        self.radius = 15
        self.children = [Orb(self, self.pos, self.dir, self.color) for i in range(starting_orbs)]
        self.dashcounter = 0

    def reflect(self, direction):
        print('reflect')
        self.tracer.deflection(self.pos, direction)
        self.dir = direction

    def get_color(self):
        if self.dashing:
            return 255, 255, 255
        else:
            return self.color

    def check_wall_collisions(self):
        pos_new = self.predict_position() + self.dir * self.radius
        for w in self.master.walls:

            intersect = utils.seg_intersect((self.pos, pos_new), w.coll_v)
            # TODO: fix this shite
            if intersect:
                dot = np.dot(self.dir, w.coll_norm)
                out = self.dir - 2 * dot * w.coll_norm
                self.reflect(np.array(-out))

                if np.isnan(sum(self.dir)):
                    print('sheet')
                return
            #print(intersect, self.pos, self.dir, self.speed, pos_new, w.coll_v)

    def update(self):
        self.tracer.update()

        if self.dashing:
            if self.dashcounter >= self.max_dash_length:
                self.dashing = False
                self.speed = self.defaultspeed
                self.dashcounter = 0
                self.tracer.add_trace(tracer.Flight(self.pos, self.dir))
            else:
                self.speed = self.dashing_f[self.dashcounter]
                self.dashcounter += 1

    def move(self):

        if self.orbit_centre:
            v0 = self.pos - self.orbit_centre
            v1 = np.matmul(self.rot_matrix, v0)
            p1 = self.orbit_centre + v1
            self.dir = utils.unit_vector(p1 - self.pos)
            self.pos = p1
        else:
            self.pos = self.predict_position()

        # update positions of tail orbs
        tail_positions = self.tracer.retrace(len(self.children), 0)

        for i in range(len(tail_positions)):
            self.children[i].move_to(tail_positions[i])

    def act(self):
        if self.dashing:
            return

        if self.orbit_centre:
            self.tracer.deflection(self.pos, self.dir)
            self.orbit_centre = None
            return

        for orbit in self.master.orbits:
            if utils.distance_p_p(self.pos, orbit.pos) < orbit.radius:
                self.orbit_centre = orbit.pos
                v_centre = self.orbit_centre - self.pos
                self.clockwise = np.cross(self.dir, v_centre) < 0
                self.angle = self.speed / utils.distance_p_p(self.pos, self.orbit_centre)
                self.rot_matrix = utils.rotation_matrix(self.angle, self.clockwise)
                self.tracer.add_trace(tracer.Orbit(self.pos, self.orbit_centre, self.clockwise, self.angle))

                return
        print('pew')
        self.fire()
        self.dashing = True
        self.tracer.add_trace(tracer.Dash(self.pos, self.dir))


    def fire(self):
        bullet = self.children.pop()
        bullet.fire()

    def draw(self, screen):
        pygame.draw.circle(screen, self.get_color(), [int(val) for val in self.pos], self.radius)
        for child in self.children:
            child.draw(screen)

    class dashState(State):


    class OrbitState(State):
        def on_enter(self, head):

            pass





