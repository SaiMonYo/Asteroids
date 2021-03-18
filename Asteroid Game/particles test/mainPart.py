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
        self.acc = -G * vector2D(0, -0.07)
        self.vel += self.acc
        self.pos += self.vel
        self.alpha -= self.tick * delta
        if self.alpha <= 0:
            self.dead = True
        
    def show(self):
        if self.dead:
            return
        colour = (self.colour[0], self.colour[1], self.colour[2], self.alpha)
        pygame.gfxdraw.filled_circle(self.win, int(self.pos.x), int(self.pos.y), self.radius, self.colour)

# screen pixel dimensions
WIDTH = 600
HEIGHT = 600

pygame.init()
# FPS used to make things move at same speed no matter FPS
FPS = 60
win = pygame.display.set_mode((WIDTH, HEIGHT))
# used to implement FPS and to time things and wait
clock = pygame.time.Clock()

#part = particle(win, math.pi, 5000, 100, (300, 300))

particles = []


running = True
start = time.time()
while running:
    for event in pygame.event.get():
        # user clicks the x
        if event.type == pygame.QUIT:
            running = False
        mousePos = pygame.mouse.get_pos()
    for x in range(100):
        colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        part = particle(win, math.pi * 2 * random.random(), 1 * random.uniform(0.8, 1.2), random.uniform(1.6, 2.4), mousePos, 1, colour)
        particles.append(part)
    delta = clock.tick(FPS) / 1000
    print(delta)
    #print(part.alpha)
    win.fill((0,0,0))
    for p in particles:
        if p.dead:
            particles.remove(p)
        p.update(delta)
    for p in particles:
        p.show()

    pygame.display.update()
        
    
