import pygame as p
import random
import math
from timer import Timer
from util import deg2Rad, getDist, rotatePoint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

colorPalette = [WHITE, GREEN, RED, YELLOW, CYAN, MAGENTA]
nColors = len(colorPalette)

# Space rock variables.
maxRockVelocity = 2
maxRockScaleFactor = 40

# bounds outside the camera
bound = 512

rock0 = [[[1, 1], [2, 0], [1, -1], [-1, -1], [-2, 0], [-1, 1], [1, 1]]]
rock1 = [[[1, 2], [3, 1], [3, -1], [1, -2], [-1, -2], [-3, -1], [-1, 2], [1, 2]]]
rock2 = [[[1, 1], [1, -1], [-0.5, -0.5], [-2, 0], [-1, 1], [1, 1]]]

spaceRocks = rock0 + rock1 + rock2
nRockTypes = len(spaceRocks)


class spaceRock():
  def __init__(self, gameWidth, gameHeight, minScaleX=5, minScaleY=5):
    self.x = random.randint(0 - bound, gameWidth + bound - 1)
    self.y = random.randint(0 - bound, gameHeight + bound - 1)
    self.heading = random.randint(0, 359)
    self.xVel = random.randint(-maxRockVelocity, maxRockVelocity)
    self.yVel = random.randint(-maxRockVelocity, maxRockVelocity)
    self.scaleFactorX = random.randint(minScaleX, maxRockScaleFactor) # default scale is 10, args passed for when two rocks merge 
    self.scaleFactorY = random.randint(minScaleY, maxRockScaleFactor)
    index = random.randint(0, nRockTypes - 1)
    self.myPoints = spaceRocks[index]
    self.didBounce = False

    # This is passed from main
    self.screenWidth = gameWidth
    self.screenHeight = gameHeight

    # Find center of rotation.
    xSum = ySum = 0
    for myPoint in self.myPoints:
      xSum = xSum + myPoint[0]
      ySum = ySum + myPoint[1]

    self.xc = xSum / len(self.myPoints)
    self.yc = ySum / len(self.myPoints)

    # Find a bounding box for this asteroid.
    xs = []
    ys = []
    for myPoint in self.myPoints:
      x = myPoint[0]
      y = myPoint[1]

      # Rotate and scale these points.
      xr, yr = rotatePoint(self.xc, self.yc, x, y, self.heading)
      xScale = xr * self.scaleFactorX
      yScale = yr * self.scaleFactorY
      xs.append(xScale)
      ys.append(yScale)

    self.minX = min(xs)
    self.maxX = max(xs) / 1.2 # make collision more generous?
    self.minY = min(ys)
    self.maxY = max(ys) / 1.2

    index = random.randint(0, nColors - 1)
    self.color = colorPalette[index]

    self.rect = p.Rect(self.x - self.maxX, self.y - self.maxY, 2 * self.maxX, 2 * self.maxY)

    self.isActive = True
  

  def moveMe(self):

    # limit speed
    limit = 3

    if self.xVel > limit:
      self.xVel = limit
    if self.xVel < -limit:
      self.xVel = -limit

    if self.yVel > limit:
      self.yVel = limit
    if self.yVel < -limit:
      self.yVel = -limit

    # Calculate new positon of space rock based on it's velocity.
    self.x = self.x + self.xVel
    self.y = self.y + self.yVel

    # If rock is outside of screen space wrap it to other side.
    if (self.x < 0 - bound):
      self.x = self.screenWidth + bound - 1
    elif (self.x > self.screenWidth + bound):
      self.x = 0 - bound

    if (self.y < 0 - bound):
      self.y = self.screenHeight + bound - 1
    elif (self.y > self.screenHeight + bound):
      self.y = 0 - bound
    
    # update rect for collision
    self.rect.x = self.x - self.maxX
    self.rect.y = self.y - self.maxY

    return


# :O

#if key input == m active turret
# if key input == s active shield
#
#  ship.shieldactive = true
# if ship.shield == true:
#  ship.shieldCharge = ship.ShieldCharge - 1
#  savespeed=  ship.speed  -- Make it so that any speed increases apply to this
#  ship.speed = ship.speed/2
#  if ship.shieldCharge<= 0:
#     ship.shield = false
#     ship.speed = savespeed
# PS, I don't know how to do any of this in python
# lol ok, this is a good outline tho!

  def drawMe(self, screen):
    
    points = []
    for myPoint in self.myPoints:
      # Get coords of point.
      x0 = float(myPoint[0])
      y0 = float(myPoint[1])

      # Rotate the point.
      myRadius = getDist(self.xc, self.yc, x0, y0)
      theta = math.atan2(y0 - self.yc, x0 - self.xc)
      radAng = deg2Rad(self.heading)
      xr = self.xc + myRadius * math.cos(radAng + theta)
      yr = self.yc + myRadius * math.sin(radAng + theta)

      # Scale.
      xs = xr * self.scaleFactorX
      ys = yr * self.scaleFactorY

      # Translate.
      xt = xs + self.x
      yt = ys + self.y

      # Put point into polygon point list.
      points.append([xt, yt])

    p.draw.polygon(screen, self.color, points, width=2)

    # debug check collision shape
    #p.draw.rect(screen, GREEN, self.rect, width=3)
    #screen.blit(self.mask_image, (self.rect.x, self.rect.y))

    return


  # for asteroids
  def checkCollisionAst(self, asteroid):
    color = asteroid.color

    smack = False
    sameCol = False

    # use pygame's collision check method for masks
    #rect_check = self.rect.colliderect(asteroid.rect)
    coll_check = self.rect.colliderect(asteroid.rect)

    if coll_check and (not self.didBounce):
      smack = True
      self.didBounce = True
      
      if self.color == color:
        sameCol = True
    
    elif (not coll_check) and (self.didBounce):
      self.didBounce = False

    return smack, sameCol


  # for bullets
  def checkCollision(self, x, y):
    smack = False

    point_check = self.rect.collidepoint(x, y)

    if point_check:
      smack = True

    return smack
  
  
  def reverseDir(self, asteroid):
    ang = math.atan2(asteroid.y - self.y, asteroid.x - self.x)
    newXVel = math.cos(ang)
    newYVel = math.sin(ang)

    speed = math.sqrt((self.xVel ** 2) + (self.yVel ** 2))

    self.xVel = -newXVel * speed
    self.yVel = -newYVel * speed


  def gravPull(self, ship):
    ang = math.atan2(ship.y - self.y, ship.x - self.x)

    # integers make it go WHACK, need to use small force
    force = 0.001

    xVelInc = math.cos(ang) * force
    yVelInc = math.sin(ang) * force

    self.xVel += xVelInc
    self.yVel += yVelInc


  def tick(self):
    for t in self.timers:
      t.tick()