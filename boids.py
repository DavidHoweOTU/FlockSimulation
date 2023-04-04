"""
=== Pygame Flock Simulation ===
authors: David Howe, Gerhard Yu
last-edited: 2023/03/30 - 5:14pm
"""

import math
import random
import numpy as np
import pygame
import sys

# set up the colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BACKGROUND = BLACK


# GLOBAL CONSTANTS
######################
MIN_DISTANCE = 10

COHERENCE = 100
SEPARATION = 20
ALIGNMENT = 5

SYS_HEIGHT  = 480
SYS_WIDTH   = 640

OBJECTS = np.matrix([[50, 50]]) #object/obstacle can add more if needed
SPEED_LIMIT = 0.1 #3/60 for m/s
######################

#unsure about this change if needed
class Obstacles(pygame.sprite.Sprite):
    def __init__(self, objects):
        self.image = pygame.Surface(objects)
        self.image.fill(BACKGROUND)
        pygame.draw.line(self.image, BLUE, objects, objects)



class Boid(pygame.sprite.Sprite):
    def __init__(self, r):
        # random position
        self.x = random.uniform(-100, 100)
        self.y = random.uniform(-100, 100)
        # random speed
        self.speed_x = 0
        self.speed_y = 0
        
        # pygame
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([2*r,2*r])
        self.image.fill(BACKGROUND)
        pygame.draw.circle(self.image, RED, (r,r), r, r)
        self.rect = self.image.get_rect()
        self.r = r

    # RULE 1
    def coherence(self, boids):
        # Find average position of nearby boids
        nearby_boid_count = 0
        overall_x = 0
        overall_y = 0
        
        for boid in boids:
            if self != boid:
                if self.is_close_to(boid):
                    overall_x += boid.x
                    overall_y += boid.y
                    nearby_boid_count += 1
                    
        # Avoid divide by zero
        if (nearby_boid_count == 0): 
            nearby_boid_count = 1
        
        c_x = overall_x / nearby_boid_count
        c_y = overall_y / nearby_boid_count
        
        # Move towards center
        self.speed_x += (c_x - self.x) / COHERENCE
        self.speed_y += (c_y - self.y) / COHERENCE
        
    # RULE 2
    def separation(self, boids):
        # Move away from nearby boids
        for boid in boids:
            if self != boid:
                if self.is_close_to(boid):
                    self.speed_x += (self.x - boid.x) / SEPARATION
                    self.speed_y += (self.y - boid.y) / SEPARATION
        
    # RULE 3
    def alignment(self, boids):
        # Find average velocity of nearby boids
        nearby_boid_count = 0
        velocity_x = 0
        velocity_y = 0
        
        for boid in boids:
            if self != boid:
                if self.is_close_to(boid):
                    velocity_x += boid.speed_x
                    velocity_y += boid.speed_y
                    nearby_boid_count += 1

        # Avoid divide by zero
        if (nearby_boid_count == 0): 
            nearby_boid_count = 1            
        
        c_x = velocity_x / nearby_boid_count
        c_y = velocity_y / nearby_boid_count
        
        # Align with group
        boid.speed_x += (c_x - boid.speed_x) / ALIGNMENT
        boid.speed_y += (c_y - boid.speed_y) / ALIGNMENT
        
    # RULE 4
    def boundaries(self):
        # TODO - AVOID SCREEN BORDER
        # You can use SYS_HEIGHT & SYS_WIDTH to do this
        if abs(self.x - SYS_WIDTH) < MIN_DISTANCE:
            self.speed_x = 0 - self.speed_x
        if abs(self.y - SYS_HEIGHT) < MIN_DISTANCE:
            self.speed_y = 0 - self.speed_y
        #pass
        
    # RULE 5
    def speedlimit(self):
        # TODO - CAP BOID SPEEDS AT A GIVEN LIMIT
        # You can make a new global constant called SPEED_LIMIT to do this
        if self.speed_x > SPEED_LIMIT:
            self.speed_x = self.speed_x * SPEED_LIMIT
        if self.speed_y > SPEED_LIMIT:
            self.speed_y = self.speed_y * SPEED_LIMIT
        #still unsure about this one
        #pass

    def avoidObject(self):
        size = np.shape(OBJECTS)
        for columns in range(size[0]):
            #checks if x is too close to the objects x value and if it is reverse its direction
            if abs(self.x - OBJECTS[columns][0]) < MIN_DISTANCE:
                self.speed_x = 0 - self.speed_x
            #checks if y is too close to the objects y value and if it is reverse its direction
            if abs(self.y - OBJECTS[columns][1]) < MIN_DISTANCE:
                self.speed_y = 0 - self.speed_y



        
    def update_boid(self, boids):
        # Apply rules
        self.coherence(boids)
        self.separation(boids)
        self.alignment(boids)
        self.boundaries()
        self.avoidObject()
        self.speedlimit()
        
        # Move boid
        self.x += self.speed_x
        self.y += self.speed_y

    def is_close_to(self, other):
        return abs((self.x - other.x)) < MIN_DISTANCE and abs((self.y - other.y)) < MIN_DISTANCE
    


class System:
    def __init__(self, h, w):
        self.h = h
        self.w = w
        self.boids = []
        self.objects = pygame.sprite.Group()
        self.dt = 1.0
        
    def add_boid(self, r):
        new_boid = Boid(r)
        self.boids.append(new_boid)
        self.objects.add(new_boid)

    #remove if needed
    def add_obstacle(self, object):
        obstacle = Obstacles(object)
        
    def update_sys(self):
        for boid in self.boids:
            # Update boids
            boid.update_boid(self.boids)
            sx, sy = self.fit_to_screen(boid.x, boid.y)
            
            # Update sprite coordinates
            boid.rect.x, boid.rect.y = sx-boid.r, sy-boid.r
            
            # Uncomment to print info
            # print(f'BOID:X{boid.x},Y{boid.y},SX{sx},SY{sy},VX{boid.speed_x},VY{boid.speed_y}')
        
        self.dt += 1
        self.objects.update()
            
    def fit_to_screen(self, x, y):
        # !!! This function could also be used 
        # !!! to scale if needed
        
        # Moves 0,0 to centre of screen
        sx = int(x + self.w/2)
        sy = int(y + self.h/2)
        return sx, sy
    
    def draw(self, screen):
        self.objects.draw(screen)

        
        

def main():
    # LOCAL CONSTANTS
    ########################
    NUM_BOIDS   = 20
    BOID_RADIUS = 10
    ########################
    
    # Initializing pygame
    print ('Flock Simulation')
    print ('==========================')
    print ('Press r to resume')
    print ('Press p to pause')
    print ('Press q to quit')
    print ('==========================')
    
    clock = pygame.time.Clock()
    
    pygame.init()
    screen = pygame.display.set_mode((SYS_WIDTH, SYS_HEIGHT))
    pygame.display.set_caption('Flock Simulation')
    
    # Create system
    system = System(SYS_HEIGHT, SYS_WIDTH)
    
    # Generate boids
    for i in range(NUM_BOIDS):
        system.add_boid(BOID_RADIUS)

    # Generate obstacles, remove if needed
    size = np.shape(OBJECTS)
    for x in range(size[0]):
        system.add_obstacle(OBJECTS[x])
    
    # Run simulation
    total_frames = 1000000
    frame = 0
    paused = False
    
    while frame < total_frames:
        clock.tick(15) # run at 30fps

        event = pygame.event.poll()
        
        # Keyboard inputs
        if event.type == pygame.KEYDOWN and event.key == pygame.K_p:
            paused = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            paused = False
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            pygame.quit()
            sys.exit(0)
        else:
            pass

        if not paused:
            system.update_sys()
        
            screen.fill(BACKGROUND) # clear the background
            system.draw(screen)
            pygame.display.flip()
            frame += 1

    pygame.quit()
    
    

if __name__ == '__main__':
    main()