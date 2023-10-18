import os
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
MAGENTA = (255, 0, 255)

class Powerup:
    def __init__(self, screen, power_type, posx, posy):
        self.screen = screen
        self.power_type = power_type
        self.posx = posx
        self.posy = posy
        self.width  = 20
        self.height = 20
        self.rect = p.Rect(posx, posy, self.width, self.height)  # Rectangle for the power-up
        self.rect.center = (r.randint(50, 750), r.randint(50, 550))  # Random spawn location
        self.col = Collider(self)
        self.name = "POWERUP"

    def apply(self, player):
        if self.power_type == "heal":
            player.heal(50)  # Implement a heal method for the player
        elif self.power_type == "bullet_size":
            player.increase_bullet_size(1.25)  # Implement a method to increase bullet size
        elif self.power_type == "player_speed":
            player.increase_speed(1.5)  # Implement a method to increase player speed
        elif self.power_type == "player_stamina":
            player.increase_stamina()  # Implement a method to increase player stamina

    def draw(self):
        # Draw a colored rectangle based on the power-up type
        if self.power_type == "heal":
            p.draw.rect(self.screen, GREEN, self.rect)  # Green for healing
        elif self.power_type == "bullet_size":
            p.draw.rect(self.screen, RED, self.rect)  # Red for bullet size
        elif self.power_type == "player_speed":
            p.draw.rect(self.screen, CYAN, self.rect)  # Blue for player speed
        elif self.power_type == "player_stamina":
            p.draw.rect(self.screen, ORANGE, self.rect)  # Orange for player stamina