import tracer
from orb import Orb
import utils
import numpy as np


class State:

    def compute(self, pos, dir):
        pass

    def next(self, action):
        pass


class Dash_state(State):

    def __init__(self, **kwargs):
        self.counter = 0
        self.head = kwargs['head']
        self.head.tracer.add_trace(tracer.Dash(self.head.pos, self.head.dir))
        self.head.fire()


    def compute(self, pos, dir):
        self.head.speed = Orb.dashing_f[self.counter]
        self.counter += 1
        return self.head.predict_position(), dir

    def next(self, action):
        if self.counter >= Orb.max_dash_length:
            self.head.speed = self.head.defaultspeed
            return 'Flight_state', {}


class Flight_state(State):
    def __init__(self, **kwargs):
        self.head = kwargs['head']
        self.head.tracer.add_trace(tracer.Flight(self.head.pos, self.head.dir))

    def compute(self, pos, dir):
        return self.head.predict_position(), dir

    def next(self, action):
        if action:
            orbit_centre = self.head.check_orbit_collisions()
            if orbit_centre:
                return 'Orbit_state', {'orbit_centre': orbit_centre}
            return 'Dash_state', {}


class Orbit_state(State):

    def __init__(self, **kwargs):
        self.head = kwargs['head']
        self.orbit_centre = kwargs['orbit_centre']
        v_centre = self.orbit_centre - self.head.pos
        self.clockwise = np.cross(self.head.dir, v_centre) < 0
        self.angle = self.head.speed / utils.distance_p_p(self.head.pos, self.orbit_centre)
        self.rot_matrix = utils.rotation_matrix(self.angle, self.clockwise)
        self.head.tracer.add_trace(tracer.Orbit(self.head.pos, self.orbit_centre, self.clockwise, self.angle))

    def compute(self, pos, dir):
        v0 = pos - self.orbit_centre
        v1 = np.matmul(self.rot_matrix, v0)
        p1 = self.orbit_centre + v1
        return p1, utils.unit_vector(p1 - pos)

    def next(self, action):
        if action:
            return 'Flight_state', {}
