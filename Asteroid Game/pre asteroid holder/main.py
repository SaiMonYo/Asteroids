''' main - handles user input '''
import pygame
from pygame import gfxdraw
import math
import random
import time

# importing the engines
import AsteroidEngine
import ShipEngine

# screen pixel dimensions
WIDTH = 600
HEIGHT = 600

pygame.init()
# FPS used to make things move at same speed no matter FPS
FPS = 60
win = pygame.display.set_mode((WIDTH, HEIGHT))
# used to implement FPS and to time things and wait
clock = pygame.time.Clock()

# creating the ship that the user will pilot
ship = ShipEngine.spaceship(win)
# list for the asteroids
asteroids = []


# making starting asteroids
for i in range(10):
    asteroid = AsteroidEngine.asteroid(win, 12, random.randint(1,3), (random.uniform(0, WIDTH), random.uniform(0, HEIGHT)), math.pi * 2 * random.random())
    asteroids.append(asteroid)


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
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        ship.rotate_left()
    # right arrow or 'd' key
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        ship.rotate_right()

    # w key or up arrow starts the thrusters, any key not forward will stop thrusters
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        ship.thrusting = True
    else:
        ship.thrusting = False

    # spawn a bullet on space button click
    # only when theres less that 5 bullets on screen
    if keys[pygame.K_SPACE] and len(ship.bullets) < 5:
        ship.spawn_bullet()


    # update bullets
    ship.update_bullets()
    ship.show_bullets()
    ship.delete_bullets()

    # ship movement
    ship.move(delta)
    ship.show()
    
    # showing asteroids
    for asteroid in asteroids:
        asteroid.update(delta)
        asteroid.show()

    # deleting hit asteroids
    for asteroid in asteroids:
        if ship.check_bullet_hits(asteroid):
            asteroids += asteroid.birth()
            asteroids.remove(asteroid)
        if ship.blow_up(asteroid):
            running = False

        
    # updating screen
    pygame.display.update()
    
