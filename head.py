import random
import tracer
from orb import Orb
import numpy as np
import utils


def integ(x):
    return x ** 2 / 2.0 - x ** 3 / 3.0


class Head(Orb):
    interval = 0.05
    constant = 800
    dashing_f = [(integ(i + interval) - integ(i)) * constant for i in np.arange(0.0, 1.0, interval)]
    print(dashing_f)
    defaultspeed = 3

    def __init__(self, master, pos, dir=(0, 1)):
        Orb.__init__(self, master, pos, dir, [random.randrange(100, 255) for i in range(3)])
        self.speed = self.defaultspeed
        self.orbit_centre = None
        self.clockwise = False
        self.tracer = tracer.Tracer(self.pos, self.dir, self)
        self.angle = 0
        self.traversed_angle = 0
        self.rot_matrix = np.zeros((2, 2), dtype=float)
        self.dashing = False
        self.dashcounter = 0

    def update_direction(self, direction):
        self.tracer.deflection(self.pos, direction)

        self.dir = direction

    def check_wall_collisions(self):
        pos_new = self.predict_position()
        for w in self.master.walls:
            if utils.distance_p_l(pos_new, w.coll_v[0], w.coll_v[1]) <= self.radius:

                # intersect = utils.seg_intersect(self.pos, np.array([self. pos[i] + 50* self.direction[i] for i in range(2)]), w.coll_v[0], w.coll_v[1])
                intersect = utils.line_intersection(
                    (self.pos, self.pos + self.speed * self.dir),
                    (w.coll_v[0], w.coll_v[1]))

                if intersect and self.is_intersection_ahead(intersect):
                    dot = np.dot(self.dir, w.coll_norm)
                    out = self.dir - 2 * dot * w.coll_norm
                    self.update_direction(np.array(out))

                    if np.isnan(sum(self.dir)):
                        print('sheet')

    def move(self):
        if self.orbit_centre:
            v0 = self.pos - self.orbit_centre
            v1 = np.matmul(self.rot_matrix, v0)
            p1 = self.orbit_centre + v1
            self.traversed_angle += self.angle
            self.dir = utils.unit_vector(p1 - self.pos)
            self.pos = p1
        else:
            if self.dashing:
                if self.dashcounter >= len(self.dashing_f):
                    self.dashcounter = 0
                    self.dashing = False
                    self.speed = self.defaultspeed
                else:
                    self.speed = self.dashing_f[self.dashcounter]
                    self.dashcounter += 1
            self.pos = self.predict_position()

    def act(self):
        if self.dashing:
            return

        if self.orbit_centre:
            self.tracer.update(self.traversed_angle)
            self.tracer.deflection(self.pos, self.dir)
            self.traversed_angle = 0.0
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
        self.dashing = True

    def is_intersection_ahead(self, intersect):
        """

        angle_intersect = np.array([intersect[i] - self.pos[i] for i in range(2)])
        dot = np.dot(utils.unit_vector(angle_intersect), utils.unit_vector(self.direction))
        if dot > 1:
            print("fucked dot: " + str(dot))
            dot = 1
        if dot < -1:
            print("fucked dot: " + str(dot))
            dot = -1

        cos_a = math.degrees(math.acos(dot))

        if cos_a >= 0:
            print('ahead')
        """

        for i in range(2):
            if self.dir[i] == 0:
                continue
            if ((intersect[i] - self.pos[i]) / self.dir[i]) < 0:
                return False
        return True


# class PState:
