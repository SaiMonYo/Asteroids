''' engine - handles physics and drawing functions '''
import pygame
from pygame import gfxdraw
import math
import random
import time
import copy

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
        
        
        self.angle = math.pi

        self.thrusting = False
        self.acc = vector2D(0, 0)
        self.vel = vector2D(0, 0)
        self.maxSpeed = 5

        self.bulletCooldown = 0.3
        self.lastShot = 0

        self.bullets = []


        self.update_points()

# ---------------------------------------------------------------------------------------------------------------#
    def rotate_right(self):
        self.angle += 0.1

    def rotate_left(self):
        self.angle -= 0.1


# ---------------------------------------------------------------------------------------------------------------#
    def update_points(self):
        x1 = (self.vHeight / 2) * math.cos(self.angle) + self.pos.x
        y1 = (self.vHeight / 2) * math.sin(self.angle) + self.pos.y


        x2 = 2 * self.pos.x - x1
        y2 = 2 * self.pos.y - y1

        if x2 - x1 != 0:
            gradient = (y2 - y1) / (x2 - x1)
        else:
            gradient = 9999999999999999999999999999999999999999999999999999999999999


        dy = math.sqrt((self.base/2)**2/(gradient**2 + 1))
        dx = -gradient * dy

        x3 = x2 + dx
        y3 = y2 + dy

        x4 = x2 - dx
        y4 = y2 - dy

        self.points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
    
    def move(self, delta):
        if self.thrusting:
            self.thrust()
        else:
            self.thrust_off()
            
        self.vel += self.acc
        self.pos += self.vel * delta * 3
        self.vel *= 0.97

        self.update_points()
        self.wrap_around()

    def thrust(self):
        direction = vector2D(0, 0)
        direction.x = math.cos(self.angle)
        direction.y = math.sin(self.angle)

        if direction.length() > 0:
            direction = direction.normalize()

        self.acc = direction * self.maxSpeed

    def thrust_off(self):
        self.acc = vector2D(0, 0)

    def wrap_around(self):
        if self.pos.x > self.width:
            self.pos.x = 0
        elif self.pos.x < 0:
            self.pos.x = self.width
        
        if self.pos.y > self.height:
            self.pos.y = 0
        elif self.pos.y < 0:
            self.pos.y = self.height
        return

# ---------------------------------------------------------------------------------------------------------------#
    def blow_up(self, asteroid):
        for point in self.points:
            if (point - asteroid.pos).length() < asteroid.length:
                return True
        return False

# ---------------------------------------------------------------------------------------------------------------#
    def spawn_bullet(self):
        now = time.time()
        if not now - self.lastShot > self.bulletCooldown:
            return
        bull = bullet(self.win, self.angle, self.pos)
        self.bullets.append(bull)
        self.lastShot = now

    def update_bullets(self):
        for bull in self.bullets:
            bull.move()

    def show_bullets(self):
        for bull in self.bullets:
            bull.show()

    def bullet_delete_filter(self, bull):
        if bull.pos.x > self.width:
            return False
        elif bull.pos.x < 0:
            return False
        
        if bull.pos.y > self.height:
            return False
        elif bull.pos.y < 0:
            return False

        if bull.touched:
            return False
        return True
        
    def delete_bullets(self):
        self.bullets = list(filter(self.bullet_delete_filter, self.bullets))

    def check_bullet_hits(self, asteroid):
        for bullet in self.bullets:
            if bullet.hit(asteroid):
                return True
        return False
                    


    # ---------------------------------------------------------------------------------------------------------------#
    def show(self):   

        pygame.draw.aaline(self.win, WHITE, self.points[0], self.points[3], 100)

        pygame.draw.aaline(self.win, WHITE, self.points[2], self.points[0], 100)
        pygame.draw.aaline(self.win, WHITE, self.points[3], self.points[0], 100)
        pygame.draw.aaline(self.win, WHITE, self.points[2], self.points[3], 100)

        gfxdraw.aacircle(self.win, int(self.points[0][0]), int(self.points[0][1]), 2, WHITE)





# ---------------------------------------------------------------------------------------------------------------#
class bullet():
    def __init__(self, win, angle, pos):
        self.win = win
        
        self.angle = angle
        self.pos = vector2D(copy.deepcopy(pos))

        self.direction = vector2D(0, 0)
        self.direction.x = math.cos(self.angle)
        self.direction.y = math.sin(self.angle)

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        self.maxBulletSpeed = 10
        self.vel = self.direction * 6
        self.endPos = vector2D(self.pos + self.direction * 10)

        self.touched = False

# ---------------------------------------------------------------------------------------------------------------#
    def hit(self, asteroid):
        if (self.endPos - asteroid.pos).length() < asteroid.length:
            self.touched = True
            return True
        return False
        
# ---------------------------------------------------------------------------------------------------------------#
    def move(self):
        self.pos += self.vel
        self.endPos += self.vel
        
# ---------------------------------------------------------------------------------------------------------------#
    def show(self):
        pygame.draw.aaline(self.win, WHITE, (self.pos), (self.endPos), 10)
        


        

        
        
