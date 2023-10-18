import pygame as p
import math
from timer import Timer
from util import deg2Rad, getDist, rotatePoint

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)


class spaceShip:

    def __init__(self, x0, y0, heading0, scaleFactor0, points, screenWidth, screenHeight):
      self.x = x0
      self.y = y0
      self.screenX = x0
      self.screenY = y0
      self.heading = heading0
      self.scaleFactor = scaleFactor0
      self.isActive = True
      self.hitTimer = Timer()

      self.shieldCharge = 100
      self.shieldActive = False

      self.ammo = 4   # patties are ammo, ammo is patties
      self.lives = 5  # start with a few
    
      # This is passed from main
      self.screenWidth = screenWidth
      self.screenHeight = screenHeight

      # Collision circle, for interacting with game objects like asteroids
      self.collRect = p.rect.Rect(self.x - 4, self.y - 16, 36, 36)

      # Field for gravity
      self.gravRect = p.rect.Rect(self.x - 240, self.y - 240, 512, 512)
    
      # Find center of rotation.
      xSum = ySum = 0
      for myPoint in points:
        xSum = xSum + myPoint[0]
        ySum = ySum + myPoint[1]
    
      self.xc = xSum / len(points)
      self.yc = ySum / len(points)
    
      self.gunSpot = []
      self.gunX = 0
      self.gunY = 0
    
      return


    def setGunSpot(self, gunSpot):
      self.gunSpot = gunSpot
      return
    

    def getGunSpot(self):
      return self.gunX, self.gunY
    

    def moveMe(self, inc):
      # Move ship along current course.
      radAng = deg2Rad(self.heading)
      self.x = self.x + inc * math.cos(radAng)
      self.y = self.y + inc * math.sin(radAng)
      # If ship goes out of screen, wrap it other side.
      if (self.x < 0):
        self.x = self.screenWidth - 1
      elif (self.x > self.screenWidth):
        self.x = 0
    
      if (self.y < 0):
        self.y = self.screenHeight - 1
      elif (self.y > self.screenHeight):
        self.y = 0
    
      return
    

    def drawMe(self, screen, color, myShip):
      points = []
      isTheGunSpot = False

      if self.isActive:
        
        if self.hitTimer.get() >= 0:

          for i in range(2, 4):
            if self.hitTimer.get() % i == 0:
              color = BLACK


        for myPoint in myShip:
          if (myPoint == self.gunSpot):
            isTheGunSpot = True
      
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
          xs = xr * self.scaleFactor
          ys = yr * self.scaleFactor
      
          # Translate.
          xt = xs + self.x
          yt = ys + self.y
      
          # Save gun position.
          if (isTheGunSpot is True):
            self.gunX = xt
            self.gunY = yt
            isTheGunSpot = False
      
          # Put point into polygon point list.
          points.append([xt, yt])
      
        p.draw.polygon(screen, color, points, width=2)

        # for debug
        #p.draw.rect(screen, GREEN, self.collRect, 2)
        #p.draw.rect(screen, GREEN, self.gravRect, 2)
      
      return
    

    def checkCollision(self, object):

      collide = self.coll_mask.overlap(object.coll_mask, (self.x - object.x, self.y - object.y))

      return collide
    

    def turn(self, inc):
      self.heading = self.heading + inc
    

    def face(self, inc):
      self.heading = inc

      if (self.heading > 359):
        self.heading -= 360
      elif (self.heading < 0):
        self.heading += 360
      
      return

    def getangletomouse(self):
      mouse_pos = p.mouse.get_pos()
      ship_pos = (self.x, self.y)

      dx = ship_pos[0] - mouse_pos[0]
      dy = ship_pos[1] - mouse_pos[1]

      radians = math.atan2(dy, dx)
      radians %= 2 * math.pi

      angle = math.degrees(radians) + 180

      return angle

    def addAmmo(self):
      self.ammo += 1


    # return boolean, used for if statement in main
    # only allow a shot if you have ammo left
    def shoot(self):
      ammoLeft = (self.ammo > 0)

      if ammoLeft:
        self.ammo -= 1

      return ammoLeft
    

    def hit(self):
      if self.hitTimer.get() < 0:
        self.hitTimer.set(270)

        if self.lives > 0:
          self.lives -= 1

          if self.lives == 0:
            self.isActive = False


    def tick(self):
      self.hitTimer.tick()