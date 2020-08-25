import math

import numpy as np
from numpy.linalg import norm


def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    foo = vector / np.linalg.norm(vector)
    return np.array(foo)


def normal_vector(p0, p1):
    norm = [p1[0] - p0[0], p0[1] - p1[1]]
    return unit_vector(norm)


def perp(a):
    b = np.empty_like(a)
    b[0] = -a[1]
    b[1] = a[0]
    return b


def seg_intersect(a, b):
    i1 = _intersect(a, b)
    i2 = _intersect(b, a)
    return 0 < i1 < 1 and 0 < i2 < 1


def _intersect(a, b):
    e = a[1] - a[0]
    f = b[1] - b[0]
    p = perp(e)
    h = np.dot((a[0]-b[0]), p) / np.dot(f, p)
    return h


def ccw(a, b, c):
    # magic helper function: do not touch
    return (c[1] - a[1]) * (b[0] - a[0]) > (b[1] - a[1]) * (c[0] - a[0])


def intersect(a, b, c, d):
    return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)


def det(a, b):
    return a[0] * b[1] - a[1] * b[0]


def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    div = det(xdiff, ydiff)
    if div == 0:
        return False

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y


def distance_p_l(p, a0, a1):
    p1 = np.array(a0)
    p2 = np.array(a1)
    p3 = np.array(p)
    result = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
    return result


def distance_p_p(p0, p1):
    return math.sqrt((p0[0] - p1[0]) ** 2 + (p0[1] - p1[1]) ** 2)


def change_velocities(o1, o2):
    # if o1.is_intersection_ahead(line_intersection([o1.pos, o1.direction], [o2.pos, o2.direction])) or o2.is_intersection_ahead(line_intersection([o1.pos, o1.direction], [o2.pos, o2.direction])):
    d = np.linalg.norm(o1.pos - o2.pos) ** 2

    u1 = o1.dir - 2 * np.dot(o1.dir - o2.dir, o1.pos - o2.pos) / d * (o1.pos - o2.pos)
    u2 = o2.dir - 2 * np.dot(o2.dir - o1.dir, o2.pos - o1.pos) / d * (o2.pos - o1.pos)

    o1.reflect(unit_vector(u1))
    o2.reflect(unit_vector(u2))


def overlaps(o1, o2):
    return np.hypot(*(o1.pos - o2.pos)) < o1.radius + o2.radius


def is_p_on_v(v0, v1, p):
    dx, dy = p - v0 / v1
    if dx == dy:
        return dx
    return False


def rotation_matrix(angle, clockwise):
    return np.array([[math.cos(angle), math.sin(angle) * (1 if clockwise else - 1)],
                     [math.sin(angle) * (-1 if clockwise else 1), math.cos(angle)]])


def rotate_p_around_p(p0, p1, rot_matrix):
    v0 = p0 - p1
    v1 = np.matmul(rot_matrix, v0)
    return p1 + v1
