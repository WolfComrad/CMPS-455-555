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

file_paths = os.listdir("Assets\SpaceshipAssets")
shipImgs = []

class Ship:
    def __init__(self, posx, posy, speed, img, width, height, xDir, yDir, health, screenSize):
        #Player position and direction values
        self.posx = posx
        self.posy = posy
        self.xDir = xDir
        self.yDir = yDir
        #Image loading
        self.img = img
        #Sizing of ship
        self.width = width
        self.height = height
        self.screenSize = screenSize
        #Player Vars
        self.speed = speed
        self.health = health
        self.name = "Player"
        self.ship = p.image.load(self.img)
        self.col = Collider(self)
        #Firing values
        self.weapon = "BASE"
        self.stam = 3

        # Load all asteroid images into a list
        self.ship_images = [p.image.load(os.path.join("Assets\SpaceshipAssets", path)) for path in file_paths]

        # Initialize the current frame index
        self.current_frame = 0


    def display(self, screen, mousePos):
        self.ship = p.image.load(self.img)
        self.ship = p.transform.rotate(self.ship, -math.degrees(self.getAngle(mousePos)))
        screen.blit(self.ship, (self.posx - 25, self.posy - 25))

    def dash(self, stam, dist):
        self.current_frame = (self.current_frame + 1) % len(self.ship_images)
        if self.stam > 0:
            self.posx += dist * self.xDir
            self.posy += dist * self.yDir

    def dash_invulnerable(self, stam, dist):
        if stam > 0:
            original_x = self.posx
            original_y = self.posy
            self.posx += original_x + dist * self.xDir
            if self.health < 100:
                 return "heal"


    def update(self, xDir, yDir):
            self.posx = self.posx + self.speed * xDir
            self.posy = self.posy + self.speed * yDir
            if self.posy > self.screenSize[1]:
                self.posy = 0
            if self.posx > self.screenSize[0]:
                self.posx = 0
            if self.posx < 0:
                self.posx = self.screenSize[0]

            #self.col.checkCollision(obj, self.xDir, self)


    def getAngle(self, mousePos):
            # Lock the x-coordinate of the mouse at x = 325
            mouse_x = mousePos[0] # Get the x-coordinate of the mouse
            mouse_y = mousePos[1]  # Get the y-coordinate of the mouse

            # Calculate the angle in radians
            angle = math.atan2(mouse_y - self.posy, mouse_x - self.posx)

            # Convert the angle to degrees and ensure it's within -90 to 90 degrees
            angle_degrees = math.degrees(angle)
            adjusted_angle_degrees = angle_degrees if -90 <= angle_degrees <= 90 else (angle_degrees + 180) % 360 - 180

            # Convert the angle back to radians
            adjusted_angle = math.radians(adjusted_angle_degrees)

            return adjusted_angle
    


    def reset(self):
        self.posx = self.screenSize[0] // 2  # Reset player's X position to the center of the screen
        self.posy = self.screenSize[1] // 2  # Reset player's Y position to the center of the screen
        self.xDir = 0  # Reset X direction
        self.yDir = 0  # Reset Y direction
        self.health = 100  # Reset player's health
        self.weapon = "BASE"
    

    