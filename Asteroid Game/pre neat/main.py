''' main - handles user input '''
import pygame
from pygame import gfxdraw
import math
import random
import time

# importing the engines
import AsteroidEngine
import ShipEngine
import ParticlesEngine

# screen pixel dimensions
WIDTH = 1000
HEIGHT = 1000

pygame.init()
# FPS used to make things move at same speed no matter FPS
FPS = 60
win = pygame.display.set_mode((WIDTH, HEIGHT))
# used to implement FPS and to time things and wait
clock = pygame.time.Clock()


## CREATING THE SHIP AND ASTEROID HOLDERS ##
# creating the ship that the user will pilot
ship = ShipEngine.spaceship(win)
# list for the asteroids
asteroids = AsteroidEngine.asteroid_holder(win, 10, ship, 200, 12)

asteroid_spawn_delay = 3
asteroid_last_spawn  = 0

score = 0

thruster = ParticlesEngine.thruster_particles(win, ship)

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
        thruster.update_particles(delta)
        thruster.show_particles()
    else:
        ship.thrusting = False
        thruster.stop()

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
    ship.cast_rays(asteroids.asteroids)
    #print(ship.rayLengths)
    
    # update asteroids
    asteroids.update_asteroids(delta)

    # show asteroids
    asteroids.show_asteroids()

    # check hits
    result, points = asteroids.check_collisions()
    score += points
    if not result:
        running = False

    now = time.time()
    if now - asteroid_last_spawn > asteroid_spawn_delay:
        asteroids.spawn()
        asteroid_last_spawn = now
    
    # updating screen
    pygame.display.update()



# ---------------------------------------------------------------------------------------------------------------#
                                        ## HANDLING AFTER GAME ENDS ##
def end_screen(ending):
    # everything explodes same time
    if ending == 0:
        explosions = []
        explosion = ParticlesEngine.explosion(win, ship.pos)
        explosions.append(explosion)
        for asteroid in asteroids.asteroids:
            explosion = ParticlesEngine.explosion(win, asteroid.pos)
            explosions.append(explosion)

        for boom in explosions:
            boom.make_explosion()

        for x in range(20):
            win.fill((0, 0, 0))
            delta = clock.tick(FPS) / 1000
            for boom in explosions:
                boom.update_particles(delta)
                boom.show_particles()
            pygame.display.update()

    # ship explodes and asteroids dissapear
    if ending == 1:
        explosion = ParticlesEngine.explosion(win, ship.pos)
        explosion.make_explosion()
        for x in range(20):
            win.fill((0, 0, 0))
            delta = clock.tick(FPS) / 1000
            explosion.update_particles(delta)
            explosion.show_particles()
            pygame.display.update()

    # ship explodes asteroids stay
    if ending == 2:
        explosion = ParticlesEngine.explosion(win, ship.pos)
        explosion.make_explosion()
        for x in range(20):
            win.fill((0, 0, 0))
            delta = clock.tick(FPS) / 1000
            # update asteroids
            asteroids.update_asteroids(delta)

            # show asteroids
            asteroids.show_asteroids()
            explosion.update_particles(delta)
            explosion.show_particles()
            pygame.display.update()

    # ship explodes and asteroids exploded one after each other
    if ending == 3:
        explosions = []
        explosion = ParticlesEngine.explosion(win, ship.pos)
        explosions.append(explosion)
        explosions[0].make_explosion()
        for asteroid in asteroids.asteroids:
            expl = ParticlesEngine.explosion(win, asteroid.pos)
            explosions.append(expl)

        while len(explosions) != 1:
            win.fill((0,0,0))
            delta = clock.tick(FPS) / 1000
            # show asteroids
            for i in range(len(explosions)-1, -1, -1):
                explosions[i].show_particles
                result = explosions[i].update_particles(delta)
                if result and len(asteroids.asteroids) != 0:
                    explosions.pop(i)
                    asteroids.asteroids.pop(i-1)
                    
            expl = random.choice(explosions) if len(explosions) != 0 else 0
            if not expl or not expl.exploded:
                expl.make_explosion()

            for boom in explosions:
                boom.show_particles()

            asteroids.show_asteroids()
            pygame.display.update()
        win.fill((0,0,0))
        pygame.display.update()
            
                    



end_screen(3)
print(f"YOU SCORED - {score} POINTS!!!")

