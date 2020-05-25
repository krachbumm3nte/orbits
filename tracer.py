import time
import utils

speed = 3
delay = 10
num_orbs = 20


class Tracer:

    def __init__(self, pos, dir, master):
        self.steps = [Init_position(pos), Flight(pos, dir)]
        self.start_time = time.time()
        self.master = master

    def add_trace(self, trace):
        trace.timestamp = time.time() - self.start_time
        self.steps.append(trace)

    def retrace(self, position, direction, in_orbit):
        temp_steps = list(self.steps) # TODO: iterator
        current = temp_steps.pop()

        if not in_orbit:
            current.update_distance_from_p(position)
            return current.retrace_path(temp_steps, delay, num_orbs)
        else:
            current.traversed_angle = in_orbit
            return current.retrace_path(temp_steps, delay, num_orbs)

    def deflection(self, pos, direction):
        top = self.steps[-1]
        if isinstance(top, Flight):
            top.add_reflection(pos, direction)

        else:
            self.add_trace(Flight(pos, direction))

    def update(self, value):
        self.steps[-1].update(value)


class Step(object):

    def __init__(self, pos):
        self.timestamp = time.time()
        self.pos = pos

    def update(self, distance):
        pass

    def retrace_path(self, remaining_steps, offset, remaining_orbs):
        pass


class Flight(Step):

    def __init__(self, pos, direction):
        super(Flight, self).__init__(pos)
        self.p_list = [[pos, direction, 0]]

    def update(self, distance):
        self.p_list[-1][2] = distance

    def update_distance_from_p(self, p):
        self.update(utils.distance_p_p(self.p_list[-1][0], p))

    def add_reflection(self, pos, direction):
        self.update_distance_from_p(pos)
        self.p_list.append([pos, direction, 0])

    def retrace_path(self, remaining_steps, offset, remaining_orbs):
        previous_step = remaining_steps.pop()
        result = []
        for i in reversed(range(len(self.p_list))):
            pos, dir, dist = self.p_list[i]
            print(dist, offset, i)
            dist -= offset

            while dist >= delay:
                if len(result) >= remaining_orbs:
                    print('res = ', result)
                    return result
                result.append(pos + dir * dist)
                dist -= delay * speed
            print('res = ', result)
            print(dist)
            if dist > 0:
                result.append(pos + dir * dist)
                dist -= delay * speed
            offset = -dist
        return result + previous_step.retrace_path(remaining_steps, offset, remaining_orbs - len(result))


class Orbit(Step):

    def __init__(self, pos, orbit_centre, clockwise, angle):
        super(Orbit, self).__init__(pos)
        self.angle = angle * delay
        self.orbit_centre = orbit_centre
        self.clockwise = clockwise
        self.traversed_angle = 0
        self.radius = utils.distance_p_p(self.pos, self.orbit_centre)

    def update(self, angle):
        self.traversed_angle = angle

    def retrace_path(self, remaining_steps, offset, remaining_orbs):
        if remaining_orbs == 0:
            return []
        retraced_angle = offset / self.radius
        out = [utils.rotate_p_around_p(self.pos, self.orbit_centre,
                                       utils.rotation_matrix(self.traversed_angle - retraced_angle,
                                                             self.clockwise))]

        rot_matrix = utils.rotation_matrix(self.angle, not self.clockwise)
        i = 1
        while i < remaining_orbs:
            p2 = utils.rotate_p_around_p(out[i - 1], self.orbit_centre, rot_matrix)
            retraced_angle += self.angle
            if retraced_angle > self.traversed_angle:
                previous_step = remaining_steps.pop()
                return out + previous_step.retrace_path(remaining_steps,
                                                        (retraced_angle - self.traversed_angle) * self.radius,
                                                        remaining_orbs - i)
            out.append(p2)
            i += 1

        return out


class Dash(Step):

    def __init__(self, pos, direction):
        super(Dash, self).__init__(pos)


class Init_position(Step):

    def __init__(self, pos):
        super(Init_position, self).__init__(pos)
        self.timestamp = 0

    def __str__(self):
        return "started at point: {}".format(self.pos)

    def retrace_path(self, remaining_steps, offset, remaining_orbs):
        return []
