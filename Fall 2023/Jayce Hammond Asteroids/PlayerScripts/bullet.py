import pygame as p
from pygame import mixer
import math
import numpy
import random as r
from PlayerScripts.collider import Collider

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)


class Bullet:
    def __init__(self, posx, posy, color, radius, speed, angle):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.radius = radius
        self.speed = speed
        self.angle = angle

        bLength = 20
        self.posx, self.posy = self.calculateInitialPosition(posx, posy, angle, bLength)

        #self.bullet = p.draw.circle(screen, RED, (self.posx, self.posy), self.radius)
        #self.rect = p.Rect(self.posx - self.radius, self.posy - self.radius, 2 * self.radius, 2 * self.radius)

    def display(self, screen):
        self.bullet = p.draw.circle(screen, RED, (self.posx, self.posy), self.radius)

    def getRect(self):
        return self.rect

    def update(self):
        self.posx += self.speed * math.cos(self.angle)
        self.posy += self.speed * math.sin(self.angle)

    def calculateInitialPosition(self, posx, posy, angle, distance):
        new_x = posx + distance * math.cos(angle)
        new_y = posy + distance * math.sin(angle)

        return new_x, new_y
    
    def check_collision(self, rock):
        # Calculate the distance between the bullet and the center of the rock
        distance = math.sqrt((self.posx - rock.posx) ** 2 + (self.posy - rock.posy) ** 2)

        # Check if a collision has occurred (assuming the bullet radius is small)
        if distance < self.radius + (rock.width / 2):
            return True