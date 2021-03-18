''' engine - handles physics and drawing functions of the ship'''
import pygame
from pygame import gfxdraw
import math
import random
import time
import copy

import ParticlesEngine

WHITE = (255, 255, 255)

vector2D = pygame.math.Vector2

class spaceship():
    def __init__(self, win):
        # vertical height
        self.vHeight = 20
        # base width
        self.base    = 16
        
        self.win = win
        self.width, self.height = self.win.get_size()

        # getting pos of the ship - centroid of the triangle
        self.pos = vector2D(self.width / 2, self.height / 2)
        
        # getting the angle the ship is pointing in
        self.angle = math.pi

        ## MOVEMENT
        self.thrusting = False
        self.acc = vector2D(0, 0)
        self.vel = vector2D(0, 0)
        self.maxSpeed = 5

        ## BULLETS ##
        self.bulletCooldown = 0.3
        self.lastShot = 0
        self.bullets = []

        ## 3 outside points of the ship
        self.update_points()

        ## RAY MARCHING ##
        self.inputN = 16
        self.rayAngles = [math.pi * i * 2 / self.inputN for i in range(1, self.inputN + 1)]
        self.rayLengths = []

# ---------------------------------------------------------------------------------------------------------------#
    def rotate_right(self):
        # incrementing angle
        self.angle += 0.1

    def rotate_left(self):
        # decreasing angle
        self.angle -= 0.1


# ---------------------------------------------------------------------------------------------------------------#
    def update_points(self):
        # getting head of the ship
        x1 = (self.vHeight / 2) * math.cos(self.angle) + self.pos.x
        y1 = (self.vHeight / 2) * math.sin(self.angle) + self.pos.y

        # getting pos oppsosite x1, and y1
        x2 = 2 * self.pos.x - x1
        y2 = 2 * self.pos.y - y1

        # logic for gradient handling
        # Div 0 Error
        if x2 - x1 != 0:
            gradient = (y2 - y1) / (x2 - x1)
        else:
            # big number
            gradient = 9999999999999999999999999999999999999999999999999999999999999

        # differnce of x and y
        dy = math.sqrt((self.base/2)**2/(gradient**2 + 1))
        dx = -gradient * dy

        # getting two base points
        x3 = x2 + dx
        y3 = y2 + dy

        x4 = x2 - dx
        y4 = y2 - dy

        # creating list
        # for ease of use in other function
        self.points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    
    def move(self, delta):
        if self.thrusting:
            self.thrust()
        else:
            self.thrust_off()

        # updating velocity based on acceleration
        # and pos based on velocity
        self.vel += self.acc
        self.pos += self.vel * delta * 3
        # dampening
        self.vel *= 0.97

        # getting vertex points
        self.update_points()
        # wraps around screen
        self.wrap_around()

    def thrust(self):
        # creating new vector in direction of the angle of the ship
        direction = vector2D(0, 0)
        # polar coordinates to cartesian
        direction.x = math.cos(self.angle)
        direction.y = math.sin(self.angle)

        # normalise the direction vector
        if direction.length() > 0:
            direction = direction.normalize()

        # multiplying by the max speed
        self.acc = direction * self.maxSpeed

    def thrust_off(self):
        # set acceleration to 0 as it isnt accelerating
        self.acc = vector2D(0, 0)

    def wrap_around(self):
        # logic to make the ship wrap around the screen
        # go off right side come back left side
        if self.pos.x > self.width:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = self.width
        
        if self.pos.y > self.height:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = self.height

# ---------------------------------------------------------------------------------------------------------------#
    def blow_up(self, asteroid):
        # looping through the vertices of the ship
        for point in self.points:
            # checking if the point is within the radius of asteroid
            if (point - asteroid.pos).length() < asteroid.length:
                return True
        return False

# ---------------------------------------------------------------------------------------------------------------#
    def spawn_bullet(self):
        # only spawns a bullet after a delay
        now = time.time()
        if not now - self.lastShot > self.bulletCooldown:
            return
        bull = bullet(self.win, self.angle, self.pos)
        self.bullets.append(bull)
        self.lastShot = now

    def update_bullets(self):
        # moving bullets
        for bull in self.bullets:
            bull.move()

    def show_bullets(self):
        # showing all the bullets
        for bull in self.bullets:
            bull.show()

    def bullet_delete_filter(self, bull):
        # filter to delete bullets once they are off screen
        if bull.pos.x > self.width:
            return False
        elif bull.pos.x < 0:
            return False
        if bull.pos.y > self.height:
            return False
        elif bull.pos.y < 0:
            return False

        # or if it has hit an asteroid
        if bull.touched:
            return False
        return True
        
    def delete_bullets(self):
        # filtering using above function
        # converting back to list object
        self.bullets = list(filter(self.bullet_delete_filter, self.bullets))

    def check_bullet_hits(self, asteroid):
        # checking if any of the bullets have hit an asteroid
        for bullet in self.bullets:
            if bullet.hit(asteroid):
                return True
        return False

    
    # ---------------------------------------------------------------------------------------------------------------#
    def cast_rays(self, asteroids):
        # function to get distances in the 8 directions
        self.rayLengths = []
        for angle in self.rayAngles:
            castRadius = 10
            point = self.pos
            while castRadius > 1 and castRadius < 500:
                minDist = math.inf
                for asteroid in asteroids:
                    dist = (asteroid.pos - point).length() - asteroid.length
                    minDist = min(dist, minDist)
                castRadius = minDist
                x, y = math.cos(angle) * castRadius + point.x, math.sin(angle) * castRadius + point.y
                point = vector2D(x, y)
            self.rayLengths.append((self.pos - point).length())
            #pygame.draw.aaline(self.win, WHITE, point, self.pos, 1)
                    
    


    # ---------------------------------------------------------------------------------------------------------------#
    def show(self):
        # drawing lines from head of ship to bases
        pygame.draw.aaline(self.win, WHITE, self.points[2], self.points[0], 100)
        pygame.draw.aaline(self.win, WHITE, self.points[3], self.points[0], 100)
        # drawing line across the bases
        pygame.draw.aaline(self.win, WHITE, self.points[2], self.points[3], 100)

        # drawing an anti aliased circle at the head of ship
        gfxdraw.aacircle(self.win, int(self.points[0][0]), int(self.points[0][1]), 2, WHITE)





# ---------------------------------------------------------------------------------------------------------------#
class bullet():
    def __init__(self, win, angle, pos):
        # window to draw to
        self.win = win

        # angle the bullet is heading
        self.angle = angle
        # copy.deepcopy of pure vector2D doesnt work on school computers
        # copying each element and floating them works though
        self.pos = vector2D(float(copy.deepcopy(pos.x)), float(copy.deepcopy(pos.y)))

        # getting directionf
        # polar to cartesian
        self.direction = vector2D(0, 0)
        self.direction.x = math.cos(self.angle)
        self.direction.y = math.sin(self.angle)


        # normalising
        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        # max speed 
        self.maxBulletSpeed = 10
        # velocity of the bullet
        self.vel = self.direction * 6
        # end position
        self.endPos = vector2D(self.pos + self.direction * 10)

        # touched an asteroid
        self.touched = False

# ---------------------------------------------------------------------------------------------------------------#
    def hit(self, asteroid):
        # checking if bullet is in the asteroids radius
        if (self.endPos - asteroid.pos).length() < asteroid.length:
            self.touched = True
            return True
        return False
        
# ---------------------------------------------------------------------------------------------------------------#
    def move(self):
        # moving
        self.pos += self.vel
        self.endPos += self.vel
        
# ---------------------------------------------------------------------------------------------------------------#
    def show(self):
        # draw an anti aliased line from start to end positions
        pygame.draw.aaline(self.win, WHITE, (self.pos), (self.endPos), 10)
