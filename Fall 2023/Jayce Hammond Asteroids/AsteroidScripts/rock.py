import os
import pygame as p
from pygame import mixer
import math
import numpy
import random as r
from pathlib import Path
from AsteroidScripts.rockProjectiles import Projectile

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)

file_paths = os.listdir("Assets\AsteroidAssets")

asteroidImgs = []
colorArr = [WHITE, GREEN, RED, ORANGE, YELLOW, CYAN]

class Rock:
    def __init__(self, posx, posy, screen, screenSize):
        self.name = "Rock"
        self.width = 100
        self.height = 100
        self.posx = posx
        self.posy = posy
        self.screen = screen
        self.screenSize = screenSize
        self.exploded = False
        self.projectiles = []
        self.xdir = r.randint(-1, 1)
        if self.xdir == 0:
            self.xdir = 1
        self.xspeed = 8

        # Load all asteroid images into a list
        self.rock_images = [p.image.load(os.path.join("Assets/AsteroidAssets", path)) for path in file_paths]

        # Initialize the current frame index
        self.current_frame = 0

    def display(self, screen):
        if not self.exploded:
            screen.blit(self.rock_images[self.current_frame], (self.posx - 15, self.posy - 15))
        else:
            for projectile in self.projectiles:
                projectile.display()
            print("I DISPLAY")

    def update(self):
        self.posy += 5
        self.posx += self.xspeed * self.xdir
        # Rotate the image by updating the current frame
        self.current_frame = (self.current_frame + 1) % len(self.rock_images)
        if self.posy > self.screenSize[1]:
            self.posy = 0
        if self.posx > self.screenSize[0]:
            self.posx = 0
        if self.posx < 0:
            self.posx = self.screenSize[0]

    def explode(self, projectiles):
        num_projectiles = r.randint(3, 6)  # Adjust as needed
        for _ in range(num_projectiles):
            angle = r.uniform(0, 2 * numpy.pi)
            speed = r.uniform(1, 5)  # Adjust as needed
            projectiles.append(Projectile(self.posx, self.posy, angle, speed, self.screen, 50))
