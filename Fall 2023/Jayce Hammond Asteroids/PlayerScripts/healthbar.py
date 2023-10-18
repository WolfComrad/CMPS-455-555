import pygame as p
from pygame import mixer
import math
import numpy
import random as r
from PlayerScripts.ship import Ship
from AsteroidScripts.rock import Rock

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)


class HealthBar:
    def __init__(self, posx, posy, health):
        self.posx = posx
        self.posy = posy
        self.health = health
        self.staminaCharge = 3

    def displayHealth(self, screen):
        healthBar = p.draw.rect(screen, RED, p.Rect(self.posx, self.posy, 200, 10), 200)
        damageBar = p.draw.rect(screen, CYAN, p.Rect(self.posx, self.posy, self.health * 2, 10), 200)

    def displayStaminaBars(self, screen, maxCharge):
        barWidth = 0
        posx = 0
        staminaBarArr = []
        for i in range(0, maxCharge):
            bar = p.draw.rect(screen, ORANGE, p.Rect(posx + barWidth, self.posy + 20, 40, 20))
            staminaBarArr.append(bar)
            posx += barWidth
            barWidth = 40

    def updateHealth(self, colBool):
        if colBool == True:
            self.health -= 2
            print(self.health)
            if self.health  == 0:
                return True