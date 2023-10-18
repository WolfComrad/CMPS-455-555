import pygame as p
import math
from util import deg2Rad, getDist, rotatePoint

maxExplodeCount = 30


class bullet:

  def __init__(self, x0, y0, heading, radius, velocity, screenWidth, screenHeight):
    self.x = x0
    self.y = y0
    self.heading = heading
    self.radius = radius
    self.velocity = velocity
    self.isActive = True
    self.exploding = False
    self.explodeCount = 20

    # This is passed from main
    self.screenWidth = screenWidth
    self.screenHeight = screenHeight

  def drawMe(self, surface, color):

    # Draw active bullets.
    if (self.isActive == True):
      x0 = self.x
      y0 = self.y
      center = [x0, y0]

      if (self.exploding):
        p.draw.circle(surface, color, center, self.explodeCount)
        self.explodeCount = self.explodeCount + 1
        if (self.explodeCount == maxExplodeCount):
          self.isActive = False
      else:
        p.draw.circle(surface, color, center, self.radius, width=1)

  def moveMe(self):
    if ((self.isActive) and (self.exploding == False)):

      # Calculate new positon of bullet based on it's velocity.
      radAng = deg2Rad(self.heading)
      self.x = self.x + self.velocity * math.cos(radAng)
      self.y = self.y + self.velocity * math.sin(radAng)

      # If bullet is outside of game space set it to inactive.
      x_check = ((self.x < 0) or (self.x > self.screenWidth))
      y_check = ((self.y < 0) or (self.y > self.screenHeight))

      if x_check or y_check:
        self.isActive = False

    return

  def setExplosion(self):
    self.exploding = True