import pygame
from pygame import gfxdraw
import math
import random
import time
import copy

WHITE = (255, 255, 255)

vector2D = pygame.math.Vector2

class particle():
    def __init__(self, win, direction, lifetime, vel, pos, radius, colour):
        self.win = win
        x = math.cos(direction)
        y = math.sin(direction)

        self.direction = direction
        self.lifetime = lifetime
        self.tick = 255 / self.lifetime
        self.alpha = 255
        self.vel = vector2D(x, y)
        self.vel *= vel
        self.pos = vector2D(pos)

        self.radius = radius
        self.colour = colour

        self.dead = False

    def update(self, delta):
        #self.acc = -G * vector2D(0, -0.12)
        #self.vel += self.acc
        self.pos += self.vel
        self.alpha -= self.tick * delta
        if self.alpha <= 0:
            self.dead = True
        
    def show(self):
        if self.dead:
            return
        colour = (self.colour[0], self.colour[1], self.colour[2], self.alpha)
        pygame.gfxdraw.filled_circle(self.win, int(self.pos.x), int(self.pos.y), self.radius, colour)


class thruster_particles():
    def __init__(self, win, ship):
        self.win = win
        self.ship = ship

        #self.angle = -self.ship.angle 

        self.particles = []

    def stop(self):
        self.particles = []

    def update_particles(self, delta):
        for x in range(5):
            colour = WHITE
            part = particle(self.win, random.uniform(self.ship.angle - math.pi, self.ship.angle) - math.pi /2, 0.3 * random.uniform(0.5, 1), random.uniform(1, 1.5), self.ship.points[1], 3, colour)
            self.particles.append(part)

        for p in self.particles:
            p.update(delta)

    def show_particles(self):
        for i in range(len(self.particles)-1, -1, -1):
            self.particles[i].show()
            if self.particles[i].dead:
                self.particles.pop(i)



class explosion():
    def __init__(self, win, pos):
        self.win = win
        self.pos = pos
        self.particles = []
        self.exploded = False

    def make_explosion(self):
        for x in range(100):
            part = particle(self.win, random.random() * 2 * math.pi, 0.2 * random.uniform(0.5, 1), random.uniform(2, 2.5), self.pos, 3, WHITE)
            self.particles.append(part)
        self.exploded = True

    def update_particles(self, delta):
        if len(self.particles) == 0 and self.exploded:
            return True
        for i in range(len(self.particles)-1, -1, -1):
            self.particles[i].update(delta)
            if self.particles[i].dead:
                self.particles.pop(i)
        return False
                
    def show_particles(self):
        for particle in self.particles:
            particle.show()


