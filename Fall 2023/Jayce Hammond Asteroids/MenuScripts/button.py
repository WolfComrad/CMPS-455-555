import pygame as p
from pygame import mixer
import math
import numpy
import random as r
from PlayerScripts.ship import Ship
from AsteroidScripts.rock import Rock
from PlayerScripts.healthbar import HealthBar
from PlayerScripts.bullet import Bullet


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


class Button():
    def __init__(self, text, x, y):
        self.x = x
        self.y = y
        font = p.font.Font("Assets\Evil Empire.otf", 40)
        self.text = font.render(str(text), True, WHITE, GREY)
        self.textRect = self.text.get_rect()
        self.textRect.center = (x, y)


    def display(self, screen):
        screen.blit(self.text, self.textRect)