import pygame
from pygame import gfxdraw
import math
import random
import time

vector2D = pygame.math.Vector2

G = 1

class particle():
    def __init__(self, win, direction, lifetime, vel, pos, radius, colour):
        self.win = win
        x = math.cos(direction)
        y = math.sin(direction)

        self.direction = direction
        self.lifetime = lifetime
        self.FPS = FPS
        self.tick = 255 / self.lifetime
        self.alpha = 255
        self.vel = vector2D(x, y)
        self.vel *= vel
        self.pos = vector2D(pos)

        self.radius = radius
        self.colour = colour

        self.dead = False

    def update(self, delta):
        self.acc = -G * vector2D(0, -0.12)
        self.vel += self.acc
        self.pos += self.vel
        self.alpha -= self.tick * delta
        if self.alpha <= 0:
            self.dead = True
        
    def show(self):
        if self.dead:
            return
        colour = (self.colour[0], self.colour[1], self.colour[2], self.alpha)
        pygame.gfxdraw.filled_circle(self.win, int(self.pos.x), int(self.pos.y), self.radius, colour)


class firework():
    def __init__(self, win, speed, x, colour, radius):
        self.win = win
        self.height, self.width = self.win.get_size()

        self.speed = speed

        self.vel = vector2D(0, -10) * self.speed
        self.acc = vector2D(0, 0)

        self.pos = vector2D(x, self.height)
        self.colour = colour

        self.radius = radius
        
        self.exploded = False
        self.particles = []

    def update(self, delta):
        if not self.exploded:
            self.acc = -G * vector2D(0, -0.07)
            self.vel += self.acc
            self.pos += self.vel

            if self.vel.y >= 0:
                self.exploded = True
                for x in range(1000):
                    part = particle(self.win, random.random() * math.pi * 2, random.uniform(0.9, 1.1), random.uniform(0.1 * self.radius, 2 * self.radius), self.pos, 1, self.colour)
                    self.particles.append(part)
            return

        for i in range(len(self.particles) - 1, -1, -1):
            self.particles[i].update(delta)
            if self.particles[i].dead:
                self.particles.pop(i)
        '''
        delete = []
        for p in self.particles:
            p.update(delta)
            if p.dead:
                delete.append(p)
        for i in delete:
            self.particles.remove(i)
        '''
        
                

    def show(self):
        if not self.exploded:
            pygame.gfxdraw.filled_circle(self.win, int(self.pos.x), int(self.pos.y), 5, self.colour)
            return
        for p in self.particles:
            p.show()


# screen pixel dimensions
WIDTH = 1000
HEIGHT = 1000

pygame.init()
# FPS used to make things move at same speed no matter FPS
FPS = 60
win = pygame.display.set_mode((WIDTH, HEIGHT))
# used to implement FPS and to time things and wait
clock = pygame.time.Clock()


fireworks = []
last_firework = 0
firework_cooldown = 0.1
#fire = firework(win, 0.8, random.uniform(0, WIDTH), (0, 255, 255))

running = True
while running:
    delta = clock.tick(FPS) / 1000
    win.fill((0, 0, 0))
    
    now = time.time()
    if now - last_firework >= firework_cooldown:
        colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        radius = random.uniform(0.5, 1.3)
        
        work = firework(win, random.uniform(0.5, 1.2), random.uniform(0, WIDTH), colour, radius)
        fireworks.append(work)
        last_firework = now
        
        
    for event in pygame.event.get():
        # user clicks the x
        if event.type == pygame.QUIT:
            running = False
    for fire in fireworks:
        fire.update(delta)
        fire.show()
    for fire in fireworks:
        if len(fire.particles) == 0 and fire.exploded:
            fireworks.remove(fire)

    pygame.display.update()

    
