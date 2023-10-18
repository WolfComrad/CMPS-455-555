import pygame as p
import math
import constants as c
import helperFunctions as hF

class bullet:
    def __init__(self, x0, y0, heading, radius, velocity):
        self.x = x0
        self.y = y0
        self.heading = heading
        self.radius = radius
        self.velocity = velocity
        self.isActive = True
        self.exploding = False
        self.explodeCount = 20
        self.isVisible = True

    def drawMe(self, surface, color):
        # Draw active bullets.
        if (self.isActive == True):
            x0 = self.x
            y0 = self.y
            x, y = (x0, y0)
            center = [x, y]

            if (self.exploding):
                p.draw.circle(surface, color, center, self.explodeCount)
                self.explodeCount = self.explodeCount + 1
                if (self.explodeCount == c.maxExplodeCount):
                    self.isActive = False
            else:
                p.draw.circle(surface, color, center, self.radius, width=1)

    def moveMe(self, bulletTime):
        if ((self.isActive) and (self.exploding == False)):
            # Calculate new positon of bullet based on it's velocity.
            radAng = hF.deg2Rad(self.heading)
            if not bulletTime:
                self.x = self.x + self.velocity*math.cos(radAng)
                self.y = self.y + self.velocity*math.sin(radAng)
            else:
                self.x = self.x + self.velocity*math.cos(radAng)*c.bulletTimeSlowFactor
                self.y = self.y + self.velocity*math.sin(radAng)*c.bulletTimeSlowFactor
            # If bullet is outside of game space set it to inactive.
            if ((self.x < 0) or (self.x > c.screenWidth)):
                self.isActive = False
            elif ((self.y < 0) or (self.y > c.screenHeight)):
                self.isActive = False
        return

    def setExplosion(self):
        self.exploding = True