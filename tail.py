from orb import Orb


class Tail(Orb):

    def __init__(self, master, pos, direction):
        Orb.__init__(self, master, pos, direction)
        self.color
