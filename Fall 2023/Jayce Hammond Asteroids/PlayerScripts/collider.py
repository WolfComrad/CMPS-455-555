import pygame as p
from pygame import mixer
import math
import numpy
import random as r

p.mixer.init()
dmgSound = p.mixer.Sound("Assets\SFX\dmgSFX.mp3")

class Collider:
    def __init__(self, parent):
        self.posx = parent.posx
        self.posy = parent.posy
        self.width = parent.width
        self.height = parent.height
        self.center = (self.posx, self.posy)
    
    def checkCollision(self, objArray, xDir, parent):
        #Calculate the distance between the collider and the center of the obj
        collided = False
        for obj in objArray:
            distance = math.sqrt((parent.posx - obj.posx) ** 2 + (parent.posy - obj.posy) ** 2)

            #Check if a collision has occurred
            if distance < (self.width / 2) + (obj.width / 2):
                dmgSound.play(0)
                collided = True
                return collided