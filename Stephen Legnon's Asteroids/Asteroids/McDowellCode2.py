# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 17:29:28 2023

@author: patrick

Here we will make a basic shooting game.  Asteroids like.

"""

import pygame as p
import random
import math

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

colorPalette = [WHITE, GREEN, RED, ORANGE, YELLOW, CYAN, MAGENTA]
nColors = len(colorPalette)

screenWidth = 1600
screenHeight = 850

gameMidX = screenWidth/2
gameMidY = screenHeight/2

# General constants and variables defined.
# Space rock variables.
maxRockVelocity = 2
maxRockScaleFactor = 40
maxRockTypes = 3

# These rocks all have 0, 0 close to their center.
rock0 = [[[1, 1], [1, -1], [-1, -1], [-1, 1], [1, 1]]]
rock1 = [[[1, 2], [3, 1], [3, -1], [1, -2], [-1, -2],
         [-3, -1], [-3, 1], [-1, 2], [1, 2]]]
rock2 = [[[1, 1], [1, 0], [1, -1], [-2, -1], [-2, 1], [1, 1]]]

spaceRocks = rock0 + rock1 + rock2
nRockTypes = len(spaceRocks)
nAsteroids = 100

maxExplodeCount = 30
maxShootingDelay = 10


basicShip = [[3, 0], [0, 4], [5, 4], [14, 0], [5, -4], [0, -4], [3, 0]]

# Utility functions.


def orientXY(x0, y0):
    x = x0
    y = screenHeight - y0
    return x, y


def deg2Rad(degrees):
    rad = (math.pi/180.0) * degrees
    return rad

def rad2Deg(radians):
    deg = (radians/math.pi) * 180
    return deg


def getDist(x0, y0, x1, y1):
    dist = (x1 - x0)**2 + (y1 - y0)**2
    dist = math.sqrt(dist)
    return dist


def rotatePoint(xc, yc, x, y, deg):
    currentAng = math.atan2(y - yc, x - xc)
    angRad = deg2Rad(deg)
    totalAng = currentAng + angRad
    dist = getDist(xc, yc, x, y)
    xNew = xc + math.cos(totalAng)*dist
    yNew = yc + math.sin(totalAng)*dist

    return xNew, yNew

# Objects.

class turret:
    def  __init__(self, x0, y0, rad0):
        self.x = x0
        self.y = y0
        self.rad = rad0
        self.gunLen = rad0*2
        self.gunAngle = 90
        self.gunTipX = 0
        self.gunTipY = 0      
        return
    
    def drawMe(self, s):
       x, y = orientXY(self.x, self.y)
       p.draw.circle(s, WHITE, [x, y], self.rad, 1)
       angRad = deg2Rad(self.gunAngle)
       self.gunTipX = self.x + self.gunLen*math.cos(angRad)
       self.gunTipY = self.y + self.gunLen*math.sin(angRad)
       gx, gy = orientXY(self.gunTipX, self.gunTipY)
       p.draw.line(s, WHITE, [x, y], [gx, gy], 1)
       
    def rotateMe(self, inc):
       self.gunAngle = self.gunAngle + inc
       if (self.gunAngle >= 360):
           self.gunAngle = 0
       elif (self.gunAngle < 0):
           self.gunAngle = 359
       return
   
    def getGunTip(self):
       x = self.gunTipX
       y = self.gunTipY
       
       return x, y
   
    def getGunAngle(self):
       return self.gunAngle
   
    def setGunAngle(self, myAngle):
        self.gunAngle = myAngle
        return
   
    def getXY(self):
        return self.x, self.y
    
    def setXY(self, x0, y0):
        self.x = x0
        self.y = y0
        return
   



class spaceRock:
    def __init__(self):
        self.x = random.randint(0, screenWidth - 1)
        self.y = random.randint(0, screenHeight - 1)
        self.heading = random.randint(0, 359)
        self.xVel = random.randint(-maxRockVelocity, maxRockVelocity)
        self.yVel = random.randint(-maxRockVelocity, maxRockVelocity)
        self.scaleFactorX = random.randint(1, maxRockScaleFactor)
        self.scaleFactorY = random.randint(1, maxRockScaleFactor)
        index = random.randint(0, nRockTypes - 1)
        self.myPoints = spaceRocks[index]

        # Find center of rotation.
        xSum = ySum = 0
        for myPoint in self.myPoints:
            xSum = xSum + myPoint[0]
            ySum = ySum + myPoint[1]

        self.xc = xSum/len(self.myPoints)
        self.yc = ySum/len(self.myPoints)

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
        self.maxX = max(xs)
        self.minY = min(ys)
        self.maxY = max(ys)
        
        # Find average x and y of the points.
        xav = []
        for x in xs:
            xav.append(abs(x))
            
        yav = []
        for y in ys:
            yav.append(abs(y))
            
        xmean = sum(xav)/len(xav)
        ymean = sum(yav)/len(yav)
        
        
        # Find a radius for bounce detection.
        self.bounceRadius = math.sqrt(xmean * xmean + ymean * ymean)
        self.bouncing = False

        index = random.randint(0, nColors - 1)
        self.color = colorPalette[index]

        self.isActive = True

    def moveMe(self):
        # Calculate new positon of space rock based on it's velocity.
        self.x = self.x + self.xVel
        self.y = self.y + self.yVel

        # If rock is outside of game space wrap it to other side.
        if (self.x < 0):
            self.x = screenWidth - 1
        elif (self.x > screenWidth):
            self.x = 0

        if (self.y < 0):
            self.y = screenHeight - 1
        elif (self.y > screenHeight):
            self.y = 0

        return

    def drawMe(self, screen):
        if (self.isActive):
            points = []
            for myPoint in self.myPoints:
                # Get coords of point.
                x0 = float(myPoint[0])
                y0 = float(myPoint[1])

                # Rotate the point.
                myRadius = getDist(self.xc, self.yc, x0, y0)
                theta = math.atan2(y0 - self.yc, x0 - self.xc)
                radAng = deg2Rad(self.heading)
                xr = self.xc + myRadius*math.cos(radAng + theta)
                yr = self.yc + myRadius*math.sin(radAng + theta)

                # Scale.
                xs = xr * self.scaleFactorX
                ys = yr * self.scaleFactorY

                # Translate.
                xt = xs + self.x
                yt = ys + self.y

                # Orient to 0,0 being upper left.
                x, y = orientXY(xt, yt)

                # Put point into polygon point list.
                points.append([x, y])

            p.draw.polygon(screen, self.color, points, width=2)
        return

    def checkCollision(self, x, y, stayAlive):
        smack = False
        if ((x >= self.minX+self.x) and (x <= self.maxX+self.x)):

            if ((y >= self.minY+self.y) and (y <= self.maxY+self.y)):
                smack = True
                self.isActive = stayAlive
        return smack
    
    def didAstroidsCollide(self, x1, y1, br1):
        whack = False
        astroidDist = getDist(x1, y1, self.x, self.y)
        whackDist = self.bounceRadius + br1
        if (astroidDist < whackDist):
            whack = True
        
        return whack
    
    def bounce(self):
        xOrY = random.randint(0, 100)
        if (xOrY < 50):
            self.xVel = -1 * self.xVel
        else:
            self.yVel = -1 * self.yVel
        return


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

    def drawMe(self, surface, color):
        # Draw active bullets.
        if (self.isActive == True):
            x0 = self.x
            y0 = self.y
            x, y = orientXY(x0, y0)
            center = [x, y]

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
            self.x = self.x + self.velocity*math.cos(radAng)
            self.y = self.y + self.velocity*math.sin(radAng)
            # If bullet is outside of game space set it to inactive.
            if ((self.x < 0) or (self.x > screenWidth)):
                self.isActive = False
            elif ((self.y < 0) or (self.y > screenHeight)):
                self.isActive = False
        return

    def setExplosion(self):
        self.exploding = True


class spaceShip:
    def __init__(self, x0, y0, heading0, scaleFactor0, points):
        self.x = x0
        self.y = y0
        self.heading = heading0
        self.scaleFactor = scaleFactor0

        # Find center of rotation.
        xSum = ySum = 0
        for myPoint in points:
            xSum = xSum + myPoint[0]
            ySum = ySum + myPoint[1]

        self.xc = xSum/len(points)
        self.yc = ySum/len(points)

        self.gunSpot = []
        self.gunX = 0
        self.gunY = 0
        
        self.turretSpot = []
        self.tX = 0
        self.tY = 0
        self.myTurret = turret(self.x, self.y, 12)
        self.proximityOn = False

        return

    def setGunSpot(self, gunSpot):
        self.gunSpot = gunSpot
        return
    
    def activateProximity(self):
        self.proximityOn = True
        return
    
    def turnOffProximity(self):
        self.proximityOn = False
        return

    def getGunSpot(self):
        return self.gunX, self.gunY
    
    def setTurretSpot(self, tSpot):
        self.turretSpot = tSpot
        return

    def getTurretSpot(self):
        return self.tX, self.tY

    def moveMe(self, inc):
        # Move ship along current course.
        radAng = deg2Rad(self.heading)
        self.x = self.x + inc * math.cos(radAng)
        self.y = self.y + inc * math.sin(radAng)
        # If ship goes out of screen, wrap it other side.
        if (self.x < 0):
            self.x = screenWidth - 1
        elif (self.x > screenWidth):
            self.x = 0

        if (self.y < 0):
            self.y = screenHeight - 1
        elif (self.y > screenHeight):
            self.y = 0

        return

    def drawMe(self, screen, color, myShip):
        points = []
        isTheGunSpot = False
        isTurretSpot = False
        for myPoint in myShip:
            if (myPoint == self.gunSpot):
                isTheGunSpot = True
                
            if (myPoint == self.turretSpot):
                isTurretSpot = True

            # Get coords of point.
            x0 = float(myPoint[0])
            y0 = float(myPoint[1])

            # Rotate the point.
            myRadius = getDist(self.xc, self.yc, x0, y0)
            theta = math.atan2(y0 - self.yc, x0 - self.xc)
            radAng = deg2Rad(self.heading)
            xr = self.xc + myRadius*math.cos(radAng + theta)
            yr = self.yc + myRadius*math.sin(radAng + theta)

            # Scale.
            xs = xr * self.scaleFactor
            ys = yr * self.scaleFactor

            # Translate.
            xt = xs + self.x
            yt = ys + self.y

            # Save gun position.
            if (isTheGunSpot == True):
                self.gunX = xt
                self.gunY = yt
                isTheGunSpot = False
            # Save the turret position    
            if (isTurretSpot == True):
                self.tX = xt
                self.tY = yt
                isTurretSpot = False

            # Orient to 0,0 being upper left.
            x, y = orientXY(xt, yt)

            # Put point into polygon point list.
            points.append([x, y])

        p.draw.polygon(screen, color, points, width=2)
        self.myTurret.setXY(self.tX, self.tY)
        self.myTurret.drawMe(screen)
        return

    def turn(self, inc):
        self.heading = self.heading + inc

        if (self.heading > 359):
            self.heading = 0
        elif (self.heading < 0):
            self.heading = 359

        return


def asteroidMe():
    # Initialize pygame.
    p.init()

    # Set the width and height of the screen [width, height]
    size = (screenWidth, screenHeight)
    screen = p.display.set_mode(size)

    p.display.set_caption("asteroidMe()")

    # Set up random number generator.
    random.seed()

    # Loop until the user clicks the close button.
    running = True

    # Used to manage how fast the screen updates
    clock = p.time.Clock()

    # Set up some game objects.
    # Space ship stuff.
    initialHeading = 90
    scaleFactor = 6
    ship = spaceShip(gameMidX, gameMidY, initialHeading,
                     scaleFactor, basicShip)
    shipSpeed = 3
    ship.setGunSpot([14, 0])
    ship.setTurretSpot([3, 0])

    # Bullet stuff
    bullets = []
    bulletSize = int(0.5 * scaleFactor)
    bulletSpeed = 3 * shipSpeed
    shotCount = 0
    proximityCount = 0

    # Make some asteroids - that is space rocks.
    myAsteroids = []
    for j in range(nAsteroids):
        myAsteroids.append(spaceRock())

    # Clock/game frame things.
    tickTock = 0

    # -------- Main Program Loop -----------
    while running:
        # --- Main event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

        """ Check for keyboard presses. """
        key = p.key.get_pressed()

        # Handle keypresses.
        if (key[p.K_ESCAPE] == True):
            running = False
        if (key[p.K_UP] == True):
            ship.moveMe(shipSpeed)
        if (key[p.K_DOWN] == True):
            ship.moveMe(-1 * shipSpeed)
        if (key[p.K_LEFT] == True):
            ship.turn(1)
        if (key[p.K_RIGHT] == True):
            ship.turn(-1)
        if (key[p.K_o] == True):
            ship.turnOffProximity()
        if (key[p.K_p] == True):
            ship.activateProximity()
        if (key[p.K_SPACE] == True):
            if (shotCount == 0):
                gunX, gunY = ship.getGunSpot()
                myBullet = bullet(gunX, gunY, ship.heading,
                                  bulletSize, bulletSpeed)
                bullets.append(myBullet)
                shotCount = maxShootingDelay

        # --- Game logic should go here
        
        # Handle close proximity ship protection.
        if (ship.proximityOn == False):
            ship.myTurret.setGunAngle(ship.heading)
        else:
            if (len(myAsteroids) > 0):
                # Find closest asteroid and shoot it if it is in range.
                close = 10000
                j = 0
                myIndex = 0
                for a in myAsteroids:
                    dist = getDist(a.x, a.y, ship.x, ship.y)
                    if (dist < close):
                        close = dist
                        myIndex = j
                    j = j+1
                    
                closeAsteroid = myAsteroids[myIndex]
                tx, ty = ship.myTurret.getXY()
                
                asteroidAngRad = math.atan2(closeAsteroid.y - ty, closeAsteroid.x - tx)
                asteroidAng = rad2Deg(asteroidAngRad)
                ship.myTurret.setGunAngle(asteroidAng)
                
                if (close < 150):
                    if (proximityCount == 0):
                        gunX, gunY = ship.myTurret.getGunTip()
                        myBullet = bullet(gunX, gunY, ship.myTurret.gunAngle,
                                          bulletSize, bulletSpeed)
                        bullets.append(myBullet)
                        proximityCount = maxShootingDelay/2
                
        # Move bullets and asteroids.
        for b in bullets:
            b.moveMe()

        for a in myAsteroids:
            a.moveMe()
            a.bouncing = False

        # Check to see if a bullet hit an asteroid.
        for a in myAsteroids:
            for b in bullets:
                if (a.isActive and b.isActive):
                    smacked = a.checkCollision(b.x, b.y, False)
                    if (smacked == True):
                        b.setExplosion()

        # Check for astroid to astroid collisions.
        for a in myAsteroids:
            for A in myAsteroids:
                if (a != A):
                    if (a.isActive and A.isActive):
                        if (a.bouncing == False) and (A.bouncing == False):
                            smacked = a.checkCollision(A.x, A.y, True)
                            #whacked = a.didAstroidsCollide(A.x, A.y, A.bounceRadius)
                            if (smacked == True):
                                a.bounce()
                                A.bounce()
                                a.bouncing = True
                                A.bouncing = True

        # --- Screen-clearing code goes here

        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.

        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)

        # --- Drawing code should go here
        # Spaceship
        ship.drawMe(screen, ORANGE, basicShip)

        # Bullets
        for b in bullets:
            b.drawMe(screen, RED)

        # Asteroids
        for a in myAsteroids:
            a.drawMe(screen)

        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

        # Update frame count.
        tickTock = tickTock + 1

        # Implement shooting delay to keep bullet count lower.
        if (shotCount > 0):
            shotCount = shotCount - 1
            
        if (proximityCount > 0):
            proximityCount = proximityCount - 1

        # Do some book keeping on arrays.
        # Remove inactive elements of bullets array.
        for b in bullets:
            if (b.isActive == False):
                bullets.remove(b)
        # Remove inactive elements of asteroids array.
        for a in myAsteroids:
            if (a.isActive == False):
                myAsteroids.remove(a)

    # Close the window and quit.
    p.quit()

    return


asteroidMe()