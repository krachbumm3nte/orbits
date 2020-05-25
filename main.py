#! /usr/bin/env python

import os
import math
import random
from itertools import combinations

import pygame
import head
import orbit
from wall import PolyWall, RectWall
import utils


def distance(self, point):
    x, y = self.vector
    return abs(x * point[0] + y * point[1]) / math.sqrt(x ** 2 + y ** 2)


class Game:

    def __init__(self):

        # Initialise pygame
        os.environ["SDL_VIDEO_CENTERED"] = "1"
        pygame.init()

        s_width = 1600
        s_height = 800
        # Set up the display
        self.screen = pygame.display.set_mode((s_width, s_height))

        self.clock = pygame.time.Clock()

        # define cornerpoints
        wall_thickness = 20.0
        c_depth = 250.0
        p0 = (wall_thickness, wall_thickness)
        p1 = (s_width - wall_thickness, wall_thickness)
        p2 = (s_width - wall_thickness, s_height - wall_thickness)
        p3 = (wall_thickness, s_height - wall_thickness)
        self.walls = [
            RectWall((p0, p1), (0.0, 0.0), (wall_thickness, s_height)),
            RectWall((p1, p2), (s_width - wall_thickness, 0.0), (wall_thickness, s_height)),
            RectWall((p2, p3), (0.0, s_height - wall_thickness), (s_width, wall_thickness)),
            RectWall((p3, p0), (0.0, 0.0), (s_width, wall_thickness)),

            PolyWall(((0, c_depth), (c_depth, 0.0), (0.0, 0.0))),
            PolyWall(((s_width - c_depth, 0.0), (s_width, c_depth), (s_width, 0.0))),
            PolyWall(((s_width, s_height - c_depth), (s_width - c_depth, s_height), (s_width, s_height))),
            PolyWall(((0, s_height - c_depth), (c_depth, s_height), (0.0, s_height)))
        ]

        self.orbits = [orbit.Orbit((500, 600), 100, [40 for i in range(3)]),
                       orbit.Orbit((900, 500), 100, [40 for i in range(3)]),
                       orbit.Orbit((200, 400), 100, [40 for i in range(3)])]

        self.players = [head.Head(self, (200.0, 200.0), utils.unit_vector((-1, 0)))]
        # self.players = [head.Head(self, (random.randrange(200.0, 1400.0), random.randrange(200.0, 600.0)), utils.unit_vector((random.random()*2 - 1, random.random() * 2 - 1))) for i in range(10)]
        # self.players = [orb.Orb(self, (701.0, 200.0), utils.unit_vector((-1, 0))), orb.Orb(self, (100.0, 259.0), utils.unit_vector((1, 0)))]

        self.tail = False

    def compute(self):

        running = True
        paused = False
        while running:



            self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    running = False
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        running = False
                    elif e.key == pygame.K_SPACE:
                        self.players[0].act()
                    elif e.key == pygame.K_LEFT:
                        paused = not paused


            if paused:
                continue

            # Move the player if an arrow key is pressed
            key = pygame.key.get_pressed()



            # Draw the scene
            self.screen.fill((0, 0, 0))
            color = (255, 200, 0)

            for wall in self.walls:
                wall.draw(self.screen)

            for o in self.orbits:
                o.draw(self.screen)

            for player in self.players:
                player.move()
                pygame.draw.circle(self.screen, player.color, [int(val) for val in player.pos], player.radius)
                trace = player.tracer.retrace(player.pos, player.dir, player.traversed_angle if player.orbit_centre else None)
                for pos in trace:
                    pygame.draw.circle(self.screen, player.color, [int(val) for val in pos], 10)

                player.check_wall_collisions()

            pairs = combinations(range(len(self.players)), 2)
            for i, j in pairs:
                if utils.overlaps(self.players[i], self.players[j]):
                    utils.change_velocities(self.players[i], self.players[j])

            pygame.display.flip()




Game().compute()
