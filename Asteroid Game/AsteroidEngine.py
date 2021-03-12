import pygame
from pygame import gfxdraw
import math
import random
import time
import copy

WHITE = (255, 255, 255)

vector2D = pygame.math.Vector2

class asteroid():
    def __init__(self, win, n, size, pos):
        self.win = win
        self.width, self.height = self.win.get_size()
        
        self.n = n
        self.size = size
        
        self.xoff, self.yoff = pos
        self.pos = vector2D(pos)

        self.points = []
        self.lengths= []
        
        self.angleChange = math.pi * 2 / self.n
        self.startAngle = math.pi * 2 * random.random()

        self.direction = math.pi * 2 * random.random()
        self.vel = vector2D(math.cos(self.direction), math.sin(self.direction))

        if size == 3:
            self.length = 50
            self.vel *= 10

        elif size == 2:
            self.length = 30
            self.vel *= 17

        else:
            self.length = 10
            self.vel *= 25
        
        for i in range(self.n):
            l = self.length * random.uniform(0.5, 1)
            self.lengths.append(l)
            x = math.cos(self.startAngle + self.angleChange * i) * l + self.xoff
            y = math.sin(self.startAngle + self.angleChange * i) * l + self.yoff

            self.points.append(vector2D(x, y))

    def wrap_around(self):
        wrapped = False
        if self.pos.x > self.width + self.length:
            wrapped = True
            self.pos.x = 0 - self.length
            
        elif self.pos.x < 0 - self.length:
            wrapped = True
            self.pos.x = self.width + self.length
        
        if self.pos.y > self.height + self.length:
            wrapped = True
            self.pos.y = 0 - self.length
        elif self.pos.y < 0 - self.length:
            wrapped = True
            self.pos.y = self.height + self.length
        return wrapped

    def update(self, delta):
        for p in self.points:
            p += self.vel * delta
        self.pos += self.vel * delta
        result = self.wrap_around()
        if result:
            self.xoff, self.yoff = self.pos
            for i in range(len(self.points)):
                x = math.cos(self.startAngle + self.angleChange * i) * self.lengths[i] + self.xoff
                y = math.sin(self.startAngle + self.angleChange * i) * self.lengths[i] + self.yoff
                self.points[i] = vector2D(x, y)

    def birth(self):
        self.size -= 1 
        if self.size == 0:
            return []

        baby1 = asteroid(self.win, 12, self.size, self.pos + vector2D(random.randint(-10, 10), random.randint(-10, 10)))
        baby2 = asteroid(self.win, 12, self.size, self.pos + vector2D(random.randint(-10, 10), random.randint(-10, 10)))

        self.size -= 10

        return [baby1, baby2]


    def show(self):
        #print(self.points)
        pygame.draw.lines(self.win, WHITE, True, self.points)



