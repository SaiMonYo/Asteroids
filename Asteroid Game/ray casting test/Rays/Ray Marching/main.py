''' main - handles user input '''
import pygame
from pygame import gfxdraw
import math
import random
import time

WHITE = (255,255,255)
BLACK = (  0,  0,  0)


vector2D = pygame.math.Vector2

class circle():
    def __init__(self, win, pos, r):
        self.win = win
        self.pos = vector2D(pos)
        self.r = r

    def show(self):
        gfxdraw.aacircle(self.win, int(self.pos.x), int(self.pos.y), self.r, WHITE)


class caster():
    def __init__(self, win, pos, angle):
        self.win = win
        self.pos = vector2D(pos)
        self.point = self.pos
        self.angle = angle
        #self.angles = [0, math.pi * 0.25, math.pi * 0.5, math.pi * 0.75, math.pi, math.pi * 1.25, math.pi * 1.5, math.pi * 1.75]
        n = 180
        self.angles = [math.pi * i * 2 / n for i in range(1,n + 1)]
        self.castcircle = 10

    def cast_ray(self, circles):
        '''
        self.castcircle = 10
        self.point = self.pos
        while self.castcircle > 1 and self.castcircle < 500:
            minDist = math.inf
            for circ in circles:
                dist = (circ.pos - self.point).length() - circ.r
                minDist = min(minDist, dist)
            self.castcircle = minDist
            x,y = math.cos(self.angle) * self.castcircle + self.point.x, math.sin(self.angle) * self.castcircle + self.point.y
            gfxdraw.aacircle(self.win, int(self.point.x), int(self.point.y), int(self.castcircle), WHITE)
            pygame.draw.aaline(self.win, WHITE, self.point, (x, y), 10)
            self.point = vector2D(x, y)
            pygame.display.update()
            #time.sleep(0.1)
        '''
        for angle in self.angles:
            self.castcircle = 10
            self.point = self.pos
            while self.castcircle > 1 and self.castcircle < 500:
                minDist = math.inf
                for circ in circles:
                    dist = (circ.pos - self.point).length() - circ.r
                    minDist = min(minDist, dist)
                self.castcircle = minDist
                x,y = math.cos(angle) * self.castcircle + self.point.x, math.sin(angle) * self.castcircle + self.point.y
                #gfxdraw.aacircle(self.win, int(self.point.x), int(self.point.y), int(self.castcircle), WHITE)
                pygame.draw.line(self.win, WHITE, self.point, (x, y), 1)
                self.point = vector2D(x, y)
                #pygame.display.update()
                #time.sleep(0.01)
            



# screen pixel dimensions
WIDTH = 1000
HEIGHT = 1000

pygame.init()
# FPS used to make things move at same speed no matter FPS
FPS = 60
win = pygame.display.set_mode((WIDTH, HEIGHT))
# used to implement FPS and to time things and wait
clock = pygame.time.Clock()


circles = [circle(win, (random.randint(0,1000),random.randint(0,1000)), 40) for x in range(10)]
castuhs = [caster(win, (random.randint(0,1000), random.randint(0,1000)), random.random()* math.pi * 2)]
castuh = caster(win, (500, 500), 0)

# looping variable
running = True
while running:
    win.fill((0,0,0))
    delta = clock.tick(FPS) / 1000
    for event in pygame.event.get():
        
        # user clicks the x
        if event.type == pygame.QUIT:
            running = False

    # keyboard input
    keys = pygame.key.get_pressed()
    # left arrow or 'a' key
    if keys[pygame.K_a]:
        castuh.pos += vector2D(-5, 0)
    # right arrow or 'd' key
    if keys[pygame.K_d]:
        castuh.pos += vector2D(5, 0)

    if keys[pygame.K_s]:
        castuh.pos += vector2D(0, 5)

    if keys[pygame.K_w]:
        castuh.pos += vector2D(0, -5)

    if keys[pygame.K_LEFT]:
        castuh.angle -= 0.01
    # right arrow or 'd' key
    if keys[pygame.K_RIGHT]:
        castuh.angle += 0.01
    
    for circ in circles:
        circ.show()

    castuh.cast_ray(circles)
    #castuh.angle += 0.01
    

    pygame.display.update()
