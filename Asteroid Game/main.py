''' main - handles user input '''
import pygame
from pygame import gfxdraw
import math
import random
import time

import AsteroidEngine
import ShipEngine


def filter_asteroids(asteroid):
    if asteroid.size <= 0:
        return False
    return True


WIDTH = 600
HEIGHT = 600

pygame.init()

FPS = 60
win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

ship = ShipEngine.spaceship(win)
asteroids = []

for i in range(10):
    asteroid = AsteroidEngine.asteroid(win, 12, random.randint(1,3), (random.uniform(0, WIDTH), random.uniform(0, HEIGHT)))
    asteroids.append(asteroid)

running = True

while running:
    win.fill((0,0,0))
    delta = clock.tick(FPS) / 1000
    for event in pygame.event.get():
            # user clicks the x
            if event.type == pygame.QUIT:
                running = False
            
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ship.rotate_left()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ship.rotate_right()
    
    if keys[pygame.K_w]:
        ship.thrusting = True
    else:
        ship.thrusting = False

    if keys[pygame.K_SPACE] and len(ship.bullets) < 5:
        ship.spawn_bullet()

    ship.update_bullets()
    ship.show_bullets()
    ship.delete_bullets()
    
    ship.move(delta)
    ship.show()

    for asteroid in asteroids:
        asteroid.update(delta)
        asteroid.show()

    newAsteroids = []
    for asteroid in asteroids:
        if ship.check_bullet_hits(asteroid):
            newAsteroids.append(asteroid.birth())
        if ship.blow_up(asteroid):
            running = False
            
    for s in newAsteroids:
        asteroids += s

    

    asteroids = list(filter(filter_asteroids, asteroids))
        
            
    
    
    pygame.display.update()
    
