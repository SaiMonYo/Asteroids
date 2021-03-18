import pygame
from pygame import gfxdraw
import math
import random
import time
import copy

import ParticlesEngine

WHITE = (255, 255, 255)

vector2D = pygame.math.Vector2

class asteroid():
    def __init__(self, win, n, size, pos, direction):
        # win to draw to
        self.win = win
        self.width, self.height = self.win.get_size()

        # polygon edges
        self.n = n

        # size number 3-1
        self.size = size

        # x offset, y offset
        # used for polar coordinates
        self.xoff, self.yoff = pos
        self.pos = vector2D(pos)

        # points of the polygon
        self.points = []
        # lengths away from centre of polygon for the points
        self.lengths= []

        # angle it changes each iteration to draw an n sided shape
        self.angleChange = math.pi * 2 / self.n
        # random rotation
        self.startAngle = math.pi * 2 * random.random()

        # direction its heading in
        self.direction = direction
        # veloctiy going in the direction
        self.vel = vector2D(math.cos(self.direction), math.sin(self.direction))

        # biggest, slowest
        if size == 3:
            self.length = 50
            self.vel *= 10

        # middle
        elif size == 2:
            self.length = 30
            self.vel *= 17

        # smallest, fastest
        else:
            self.length = 10
            self.vel *= 25
        
        for i in range(self.n):
            # from 0.5 of the length
            # cant get bigger than the length
            # easier to use this way
            l = self.length * random.uniform(0.5, 1)
            # storing lengths
            self.lengths.append(l)
            # polar conversion
            x = math.cos(self.startAngle + self.angleChange * i) * l + self.xoff
            y = math.sin(self.startAngle + self.angleChange * i) * l + self.yoff

            # appending the vector
            self.points.append(vector2D(x, y))

    def wrap_around(self):
        # using this so we can refind the points
        # after going out the screen on the other side
        wrapped = False
        # adding or subtracting lenghts
        # this is to prevent the asteroids to just jump from side to the other
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

        # returning whether we wrapped
        return wrapped

    def update(self, delta):
        # updating each of the points by velocity
        for p in self.points:
            p += self.vel * delta
        # moving centre
        self.pos += self.vel * delta
        # wrap around and see if we did wrap around
        result = self.wrap_around()
        if result:
            # gets the new x and y offsets
            self.xoff, self.yoff = self.pos
            for i in range(len(self.points)):
                # new x and y values
                x = math.cos(self.startAngle + self.angleChange * i) * self.lengths[i] + self.xoff
                y = math.sin(self.startAngle + self.angleChange * i) * self.lengths[i] + self.yoff
                # replacing the old point with new point
                self.points[i] = vector2D(x, y)

    def birth(self):
        # minus 1 from size
        self.size -= 1
        # if it was smallest size
        # this will be True
        # we dont want to spawn
        if self.size == 0:
            return []

        # creates a new asteroid with similar position and direction to parent asteroid
        child1 = asteroid(self.win, 12, self.size, self.pos + vector2D(random.randint(-10, 10), random.randint(-10, 10)), self.direction * random.uniform(0.6, 1.4))
        child2 = asteroid(self.win, 12, self.size, self.pos + vector2D(random.randint(-10, 10), random.randint(-10, 10)), self.direction * random.uniform(0.6, 1.4))

        # sets size to be less than 0 so it will be deleted
        self.size = -1

        # return the list of the child asteroids
        return [child1, child2]


    def show(self):
        #print(self.points)

        # draw lines from each of the points with first and last points joined
        pygame.draw.lines(self.win, WHITE, True, self.points)



class asteroid_holder():
    def __init__(self, win, startingSize, ship, spawnRadius, n):
        self.win = win
        self.width, self.height = self.win.get_size()
        
        self.startingSize = startingSize
        self.ship = ship
        self.spawnRadius = spawnRadius

        self.asteroidScores = {
            3: 20,
            2: 50,
            1: 100}
        
        self.n = n
        self.asteroids = []
        self.explosions = []
        for x in range(startingSize):
            self.spawn(True)
        

    def spawn(self, start = False):
        if start:

            x = self.ship.pos.x
            y = self.ship.pos.y
            while math.hypot(x - self.ship.pos.x, y - self.ship.pos.y) < self.spawnRadius:
                x = random.uniform(0, self.width)
                y = random.uniform(0, self.width)

            size = random.choice([1] + [2] * 2 + [3] * 3)

            direction = math.pi * 2 * random.random()
            
            newAsteroid = asteroid(self.win, self.n, size, (x, y), direction)
            self.asteroids.append(newAsteroid)
            return

        quad = random.randint(1,8)
        
        # x coordinates
        if quad in [1, 4, 6]:
            x = random.uniform(0, -self.width)
        elif quad in [3, 5, 8]:
            x = random.uniform(self.width, 2 * self.width)
        else:
            x = random.uniform(0, self.width)


        if quad in [1, 2, 3]:
            y = random.uniform(0, -self.height)
        elif quad in [6, 7, 8]:
            y = random.uniform(self.height, 2 * self.height)
        else:
            y = random.uniform(0, self.height)
        

        size = random.choice([1] + [2] * 2 + [3] * 3)

        direction = math.pi * 2 * random.random()
        
        newAsteroid = asteroid(self.win, self.n, size, (x, y), direction)
        self.asteroids.append(newAsteroid)


        
    def update_asteroids(self, delta):
        for asteroid in self.asteroids:
            asteroid.update(delta)

        for explosion in self.explosions:
            explosion.update_particles(delta)

        for i in range(len(self.explosions)-1, -1, -1):
            dead = explosion.update_particles(delta)
            if dead:
                self.explosions.pop(i)
        

    def show_asteroids(self):
        for asteroid in self.asteroids:
            asteroid.show()
        for explosion in self.explosions:
            explosion.show_particles()

    def check_collisions(self):
        score = 0
        for asteroid in self.asteroids:
            if self.ship.check_bullet_hits(asteroid):
                score += self.asteroidScores[asteroid.size]
                explosion = ParticlesEngine.explosion(self.win, asteroid.pos)
                explosion.make_explosion()
                self.explosions.append(explosion)
                self.asteroids += asteroid.birth()
                self.asteroids.remove(asteroid)
            if self.ship.blow_up(asteroid):
                return False, score
        return True, score



