import os
import pygame as p
import random as r

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GREY = (128,128,128)

# Constants and other parts of your code (as shown in your original code)...

class Projectile:
    def __init__(self, posx, posy, angle, speed, screen, radius):
        self.posx = posx
        self.posy = posy
        self.angle = angle
        self.speed = speed
        self.screen = screen
        self.radius = radius
        self.projectile_img = p.draw.circle(screen, RED, (self.posx, self.posy), self.radius)

    def display(self):
        p.draw.circle(self.screen, WHITE, (int(self.posx), int(self.posy)), 5)

    def update(self):
        self.posx += self.speed * p.math.cos(self.angle)
        self.posy += self.speed * p.math.sin(self.angle)