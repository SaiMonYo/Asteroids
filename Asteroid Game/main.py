''' main - handles user input '''
import pygame
from pygame import gfxdraw
import math
import random
import time
import os
import neat
import pickle

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

def main(genomes, config,):
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    
    nets = []
    ge = []
    ships = []
    # list for the asteroids
    asteroidsHolder = []

    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        ship = ShipEngine.spaceship(win)
        asteroids = AsteroidEngine.asteroid_holder(win, 10, ship, 200, 12)
        ship.cast_rays(asteroids.asteroids)
        asteroidsHolder.append(asteroids)
        ships.append(ship)
        g.fitness = 0
        ge.append(g)
        
    
    # used to implement FPS and to time things and wait
    clock = pygame.time.Clock()


    ## CREATING THE SHIP AND ASTEROID HOLDERS ##
    # creating the ship that the user will pilot
    #ship = ShipEngine.spaceship(win)

    asteroid_spawn_delay = 5
    asteroid_last_spawn  = 0


    #thruster = ParticlesEngine.thruster_particles(win, ship)

    # looping variable
    running = True
    while running:
        if len(ships) == 0:
            running = False
        i = 0
        delete = []
        for ship, asteroids in zip(ships, asteroidsHolder):
            if not i:
                win.fill((0,0,0))
            delta = clock.tick(FPS) / 1000
            for event in pygame.event.get():
                # user clicks the x
                if event.type == pygame.QUIT:
                    pygame.quit()

            output = nets[i].activate([ship.rayLengths[i] for i in range(ship.inputN)])
            
            # left arrow or 'a' key
            if output[0] > 0.5:
                ship.rotate_left()
            # right arrow or 'd' key
            if output[1] > 0.5:
                ship.rotate_right()

            # w key or up arrow starts the thrusters, any key not forward will stop thrusters
            if output[2] > 0.5:
                ship.thrusting = True
                #if show:
                    #thruster.update_particles(delta)
                    #thruster.show_particles()
            else:
                ship.thrusting = False
                #thruster.stop()

            # spawn a bullet on space button click
            # only when theres less that 5 bullets on screen
            if output[3] > 0.5:
                ship.spawn_bullet()




            # update bullets
            ship.update_bullets()
            if not i:
                ship.show_bullets()
            ship.delete_bullets()

            # ship movement
            ship.move(delta)
            if not i:
                ship.show()
            ship.cast_rays(asteroids.asteroids)
            #print(ship.rayLengths)
            
            # update asteroids
            asteroids.update_asteroids(delta)

            # show asteroids
            if not i:
                asteroids.show_asteroids()

            now = time.time()
            if now - asteroid_last_spawn > asteroid_spawn_delay:
                asteroids.spawn()
                asteroid_last_spawn = now
            
            # updating screen
            if not i:
                pygame.display.update()


            ge[i].fitness += 0.5
            result, points = asteroids.check_collisions()
            ge[i].fitness += points
            if not result:
                ships.pop(i)
                asteroidsHolder.pop(i)
                nets.pop(i)
                ge.pop(i)
            else:
                i += 1


'''
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
'''           

def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_path)
    
    pop = neat.Population(config)
    # Add a stdout reporter to show progress in the terminal.
    pop.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    pop.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    winner = pop.run(main, 50)
               
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)

