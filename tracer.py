import time

import head
import utils

speed = 3
delay = 18


class Tracer:

    def __init__(self, pos, dir, dt):
        self.dash_table = dt
        self.steps = [Init_position(pos), Flight(pos, dir)]
        self.start_time = time.time()

    def add_trace(self, trace):
        trace.timestamp = time.time() - self.start_time
        self.steps.append(trace)

    def retrace(self, tail_length, offset):
        temp_steps = list(self.steps)  # TODO: iterator
        current = temp_steps.pop()

        return current.retrace_path(temp_steps, delay + offset, tail_length)

    def deflection(self, pos, direction):
        top = self.steps[-1]
        if isinstance(top, Orbit):
            self.add_trace(Flight(pos, direction))
        else:
            top.add_reflection(pos, direction)

    def update(self):
        self.steps[-1].update()


class Step(object):

    def __init__(self, pos):
        self.timestamp = time.time()
        self.pos = pos

    def update(self):
        pass

    def retrace_path(self, remaining_steps, offset, remaining_orbs):
        pass


class Flight(Step):

    def __init__(self, pos, direction):
        super(Flight, self).__init__(pos)
        self.p_list = [[pos, direction, 0]]

    def update(self):
        self.p_list[-1][2] += 1

    def add_reflection(self, pos, direction):
        self.p_list.append([pos, direction, 0])

    def retrace_path(self, remaining_steps, offset, remaining_orbs):
        previous_step = remaining_steps.pop()
        result = []
        for pos, dir, frame_counter in reversed(self.p_list):
            frame_counter -= offset

            while frame_counter >= 0:
                if len(result) >= remaining_orbs:
                    return result
                result.append(pos + dir * frame_counter * speed)
                frame_counter -= delay
            offset = -frame_counter
        return result + previous_step.retrace_path(remaining_steps, offset, remaining_orbs - len(result))


class Orbit(Step):

    def __init__(self, pos, orbit_centre, clockwise, angle):
        super(Orbit, self).__init__(pos)
        self.angle = angle
        self.orbit_centre = orbit_centre
        self.clockwise = clockwise
        self.frame_counter = 0
        self.radius = utils.distance_p_p(self.pos, self.orbit_centre)

    def update(self):
        self.frame_counter += 1

    def retrace_path(self, remaining_steps, offset, remaining_orbs):
        retraced_frames = offset
        out = []

        rot_matrix = utils.rotation_matrix(self.angle * delay, not self.clockwise)
        i = 0
        while True:
            if i >= remaining_orbs:
                return out

            if retraced_frames >= self.frame_counter:
                previous_step = remaining_steps.pop()
                return out + previous_step.retrace_path(remaining_steps,
                                                        retraced_frames - self.frame_counter,
                                                        remaining_orbs - i)

            if i == 0:
                p2 = utils.rotate_p_around_p(self.pos, self.orbit_centre,
                                             utils.rotation_matrix((self.frame_counter - offset) * self.angle,
                                                                   self.clockwise))
            else:
                p2 = utils.rotate_p_around_p(out[i - 1], self.orbit_centre, rot_matrix)
            retraced_frames += delay
            out.append(p2)
            i += 1


class Dash(Step):

    def __init__(self, pos, direction):
        self.dashlist = head.Head.dashing_f
        super(Dash, self).__init__(pos)
        self.p_list = [[pos, direction, 0]]
        self.dashcounter = 0

    def update(self):
        self.p_list[-1][2] += 1

    def add_reflection(self, pos, direction):
        l1 = [pos, direction, self.p_list[-1][2]]
        self.p_list.append(l1)

    def retrace_path(self, remaining_steps, offset, remaining_orbs):
        previous_step = remaining_steps.pop()
        result = []
        dc = self.p_list[-1][2]
        if dc >= offset:
            dc -= offset
            for i in reversed(range(len(self.p_list))):
                pos, dir = self.p_list[i][0:2]
                dc_min = 0 if i == 0 else self.p_list[i - 1][2]

                while True:
                    if len(result) >= remaining_orbs:
                        return result

                    s = sum(self.dashlist[dc_min:dc])
                    if dc <= dc_min:
                        break
                    result.append(pos + dir * s)

                    if dc < delay:
                        return result + previous_step.retrace_path(remaining_steps, delay - dc,
                                                                   remaining_orbs - len(result))
                    dc -= delay

            offset = -dc
        else:
            offset -= dc

        return result + previous_step.retrace_path(remaining_steps, offset, remaining_orbs - len(result))


class Init_position(Step):

    def __init__(self, pos):
        super(Init_position, self).__init__(pos)
        self.timestamp = 0

    def __str__(self):
        return "started at point: {}".format(self.pos)

    def retrace_path(self, remaining_steps, offset, remaining_orbs):
        return []
