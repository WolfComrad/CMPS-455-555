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
maxRockVelocity = 3
maxRockScaleFactor = 40
maxRockTypes = 3

rock0 = [[[1,1], [1,-1], [-1,-1], [-1,1], [1,1]]]
rock1 = [[[1,2], [3,1], [3,-1], [1,-2], [-1,-2], 
         [-3,-1], [-3,1], [-1,2], [1,2]]]
rock2 = [[[1,1], [1,0], [1,-1], [-2,-1], [-2,1], [1,1]]]

spaceRocks = rock0 + rock1 + rock2
nRockTypes = len(spaceRocks)
nAsteroids = 20

maxExplodeCount = 30
maxShootingDelay = 30


basicShip = [[3,0], [0,3], [6,0], [0,-3], [3,0]]

# Utility functions.

def orientXY(x0, y0):
    x = x0
    y = screenHeight - y0
    return x, y

def deg2Rad(degrees):
    rad = (math.pi/180.0) * degrees
    return rad

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

class sword:
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
    def __init__(self, shipX, shipY):
        self.x = random.randint(0, screenWidth - 1)
        self.y = random.randint(0, screenHeight - 1)
        self.heading = random.randint(0, 359)
        self.xVel = random.randint(1, maxRockVelocity)
        self.yVel = random.randint(1, maxRockVelocity)
        self.type = "normal"
        self.timeOfBorn = 0
        if(random.randint(0, 1) == 1):
            self.xVel = -self.xVel
        if(random.randint(0,1) == 1):
            self.yVel = -self.yVel
        
        self.scaleFactorX = random.randint(10, maxRockScaleFactor)
        self.scaleFactorY = random.randint(10, maxRockScaleFactor)
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
        xrand = random.randint(0,1)
        yrand = random.randint(0,1)
        if(xrand == 1 or math.floor(shipX) + 20 >= screenWidth -1):
            self.x = random.randint(0, math.floor(shipX) - 20)
        elif(xrand == 0 or math.floor(shipX) - 20 <= 0):
            self.x = random.randint(math.floor(shipX) + 20, screenWidth - 1)
        if(yrand == 1 or math.floor(shipY) + 20 >= screenHeight - 1):
            self.y = random.randint(0, math.floor(shipY) - 20)
        elif(yrand == 0 or math.floor(shipY) - 20 <= 0):
            self.y = random.randint(math.floor(shipY) + 20, screenHeight - 1)
                      
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
            if(self.type == "normal"):
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
                    xt = xs  + self.x
                    yt = ys  + self.y
                    
                    # Orient to 0,0 being upper left.
                    x, y = orientXY(xt, yt)
                    
                    # Put point into polygon point list.
                    points.append([x, y])
                
                p.draw.polygon(screen, self.color, points, width = 2)
            else:
                if(self.type == "sword"):
                    self.color = WHITE
                if(self.type == "trigun"):
                    self.color = RED
                if(self.type == "missle"):
                    self.color = GREEN
                p.draw.circle(screen, self.color, orientXY(self.x, self.y), 20)
        
        return
    
    def checkCollision(self, x, y):
        smack = False
        if(self.type == "normal"):
            if ((x >= self.minX+self.x) and (x <= self.maxX+self.x)):
                if ((y >= self.minY+self.y) and (y <= self.maxY+self.y)):
                    smack = True
        else:
            if(getDist(self.x, self.y, x, y) < 30):
                smack = True
        return smack

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
                p.draw.circle(surface, color, center, self.radius, width = 1)           
        
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
        self.exploding = False
        self.explodeCount = 20
        self.fieldForce = False
        self.state = "normal"
        
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
        
        self.gunSpot2 = []
        self.gunX2 = 0
        self.gunY2 = 0
        
        self.gunSpot3 = []
        self.gunX3 = 0
        self.gunY3 = 0
        
        self.shieldSpot = []
        self.shieldX = 0
        self.shieldY = 0
        
        self.swordSpot = []
        self.tX = 0
        self.tY = 0
        self.mySword = sword(self.x, self.y, 30)
        
        return
    
    
    def setGunSpot(self, gunSpot):
        self.gunSpot = gunSpot
        return
    
    def setGunSpot2(self, gunSpot):
        self.gunSpot2 = gunSpot
        return
    
    def setGunSpot3(self, gunSpot):
        self.gunSpot3 = gunSpot
        return
    
    def setShieldSpot(self, shieldSpot):
        self.shieldSpot = shieldSpot
        return
    
    def getGunSpot(self):
        return self.gunX, self.gunY
    
    def getGunSpot2(self):
        return self.gunX2, self.gunY2
    
    def getGunSpot3(self):
        return self.gunX3, self.gunY3
    
    def getShieldSpot(self):
        return self.shieldX, self.shieldY
    
    def setSwordSpot(self, tSpot):
        self.swordSpot = tSpot
        return

    def getSwordSpot(self):
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
        isTheGunSpot2 = False
        isTheGunSpot3 = False
        isTheShieldSpot = False
        isTheSwordSpot = False
        for myPoint in myShip:
            if (myPoint == self.gunSpot):
                isTheGunSpot = True
                
            if (myPoint == self.gunSpot2):
                isTheGunSpot2 = True
                
            if (myPoint == self.gunSpot3):
                isTheGunSpot3 = True
                
            if (myPoint == self.shieldSpot):
                isTheShieldSpot = True
                
            if (myPoint == self.swordSpot):
                isTheSwordSpot = True
                
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
            xt = xs  + self.x
            yt = ys  + self.y
            
            # Save gun position.
            if (isTheGunSpot == True):
                self.gunX = xt
                self.gunY = yt
                isTheGunSpot = False
            
            if (isTheGunSpot2 == True):
                self.gunX2 = xt
                self.gunY2 = yt
                isTheGunSpot2 = False
                
            if (isTheGunSpot3 == True):
                self.gunX3 = xt
                self.gunY3 = yt
                isTheGunSpot3 = False
                
            if (isTheSwordSpot == True):
                self.tX = xt
                self.tY = yt
                self.mySword.setXY(self.tX, self.tY)
                isTheSwordSpot = False
                
            if (isTheShieldSpot == True):
                self.shieldX,self.shieldY = orientXY(xt, yt)
                isTheShieldSpot = False
            
            # Orient to 0,0 being upper left.
            x, y = orientXY(xt, yt)
            
            # Put point into polygon point list.
            points.append([x, y])
        if (self.exploding):
                p.draw.circle(screen, color, [self.shieldX, self.shieldY], self.explodeCount)
                self.explodeCount = self.explodeCount + 1
                if (self.explodeCount == maxExplodeCount):
                    p.time.delay(700)
                    p.quit() 
        if(self.fieldForce):
            p.draw.circle(screen, GREEN, [self.shieldX, self.shieldY], 40, 1)
            p.draw.polygon(screen, color, points, width = 2)
        if(self.state == "sword"):
            p.draw.polygon(screen, color, points, width = 2)
            self.mySword.drawMe(screen)
        else:
            p.draw.polygon(screen, color, points, width = 2)
        return
    
    def turn(self, inc):
        self.heading = self.heading + inc
        
        if (self.heading > 359):
            self.heading = 0
        elif (self.heading < 0):
            self.heading = 359
        
            
        return
    def setExplosion(self):
        self.exploding = True
    
    def forceField(self, setting):
        if(setting):
            self.fieldForce = True
        else:
            self.fieldForce = False
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
    ship = spaceShip(gameMidX, gameMidY, initialHeading, scaleFactor, basicShip)
    shipSpeed = 3
    ship.setGunSpot([6,0])
    ship.setGunSpot2([0,3])
    ship.setGunSpot3([0, -3])
    ship.setShieldSpot([3,0])
    ship.setSwordSpot([6, 0])
    shieldEnergy = 3
    timer = 0
    timerSnap = 0
    timerHit = 0
    timerState = 0
    timerPow = 0
    timerDash = 0
    color = ORANGE
    swing = False
    swingInc = -2
    swingCount = 26
    ship.mySword.setGunAngle(ship.heading + 46)
    
    # Bullet stuff
    bullets = []
    bulletSize = int(0.5 * scaleFactor)
    bulletSpeed = 3 * shipSpeed
    shotCount = 0
    
    # Make some asteroids - that is space rocks.
    myAsteroids = []
    for j in range(nAsteroids):
        myAsteroids.append(spaceRock(gameMidX, gameMidY))
    
    # Clock/game frame things.
    tickTock = 0
    myPowerups = []
    
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
        if (key[p.K_w] == True): 
            ship.moveMe(shipSpeed)
        if (key[p.K_s] == True): 
            ship.moveMe(-1 * shipSpeed)
        if (key[p.K_a] == True):
            ship.turn(2)
        if (key[p.K_d] == True):
            ship.turn(-2)
        if (key[p.K_LSHIFT]):
            if(timer - timerDash >= 180):
                ship.moveMe(100)
                timerDash = timer
        if (key[p.K_j] == True):
            if (shotCount == 0 and ship.state != "sword"):
                gunX, gunY = ship.getGunSpot()
                gunX2, gunY2 = ship.getGunSpot2()
                gunX3, gunY3 = ship.getGunSpot3()
                myBullet = bullet(gunX, gunY, ship.heading, bulletSize, bulletSpeed)
                bullets.append(myBullet)
                if(ship.state == "trigun"):
                    myBullet = bullet(gunX2, gunY2, ship.heading, bulletSize, bulletSpeed)
                    bullets.append(myBullet)
                    myBullet = bullet(gunX3, gunY3, ship.heading, bulletSize, bulletSpeed)
                    bullets.append(myBullet)
                shotCount = maxShootingDelay
            if (ship.state == "sword"):
                swing = True
        if (key[p.K_k] == True):
            if(ship.fieldForce == False):
                ship.forceField(True)
                timerSnap = timer
            elif(ship.fieldForce == True and timer - timerSnap >= 120):
                ship.forceField(False)
            
        # --- Game logic should go here
        # Move bullets and asteroids.
        for b in bullets:
            b.moveMe()
            
        for a in myAsteroids:
            a.moveMe()
            
        # Check to see if a bullet hit an asteroid.
        count = 0
        for a in myAsteroids:
            countB = 0
            for b in bullets:
                if (a.isActive and b.isActive):
                    smacked = a.checkCollision(b.x, b.y)
                    if (smacked == True):
                        randChan = random.randint(0, 100)
                        if(randChan >= 50):
                            b.setExplosion()
                            a.isActive = False
                        elif(randChan <= 49 and timer - timerPow > 300):
                            a.timeOfBorn = timer
                            timerPow = timer
                            randAbil = random.randint(0, 4)
                            if(randAbil == 0 or randAbil == 1):
                                a.type = "trigun"
                            else:
                                a.type = "sword"
                            myPowerups.append(a)
                        myAsteroids.pop(count)
                        bullets.pop(countB)
                        if(shieldEnergy != 3):
                            shieldEnergy = shieldEnergy + 1
                countB = countB + 1
            if (a.isActive):
                smacked = a.checkCollision(ship.x, ship.y)    
                if (smacked == True and timer >= 180):
                    if(ship.fieldForce == True and timer - timerHit > 120):
                        a.xVel = -a.xVel
                        a.yVel = -a.yVel
                        shieldEnergy = shieldEnergy - 1 
                    if(ship.state == "sword"):
                        a.xVel = -a.xVel
                        a.yVel = -a.yVel
                    else:
                        ship.setExplosion()
            if (a.isActive and swing):
                gx, gy = ship.mySword.getGunTip()
                smacked = a.checkCollision(gx, gy)
                smacked2 = a.checkCollision(ship.mySword.x, ship.mySword.y)
                if(smacked == True or smacked2 == True):
                    a.isActive = False
                    myAsteroids.pop(count)
            count= count + 1
        countpow = 0   
        for pow in myPowerups:
            if (pow.isActive):
                smacked = pow.checkCollision(ship.x, ship.y)    
                if (smacked == True):
                    ship.state = pow.type
                    pow.isActive = False
                    myPowerups.pop(countpow)
                    timerState = timer
            countpow = countpow + 1
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
     
        # --- Drawing code should go here
        # Spaceship
        if(shieldEnergy == 0):
            ship.fieldForce = False
        if(ship.state == "normal"):
            color = ORANGE
        if(ship.state == "missle"):
            color = GREEN
        if(ship.state == "trigun"):
            color = RED
        if(ship.state == "sword"):
            color = WHITE
        ship.drawMe(screen, color, basicShip)
        
        # Bullets
        for b in bullets:
            b.drawMe(screen, RED)
            
        # Asteroids
        for a in myAsteroids:
            a.drawMe(screen)
        
        count = 0
        for pow in myPowerups:
            if(timer - pow.timeOfBorn >= 300):
                pow.isActive = False
                myPowerups.pop(count)
            pow.drawMe(screen)
            count = count + 1
            
        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
        
        # Update frame count.
        tickTock = tickTock + 1
        
        # Implement shooting delay to keep bullet count lower.
        if (shotCount > 0):
            shotCount = shotCount - 1
        # Do some book keeping on arrays.
        # Remove inactive elements of bullets array.
        # Remove inactive elements of asteroids array.
        if (swingCount == -46):
            swingInc = 2
        if (swingCount == 46):
            swingInc = -2
        if (swing == True):
            swingCount = swingCount + swingInc
            ship.mySword.setGunAngle(ship.heading + swingCount) 
        if (myAsteroids == []):
            for j in range(nAsteroids):
                myAsteroids.append(spaceRock(ship.x, ship.y))
        if(timer - timerSnap >= 180):
            ship.forceField(False)
        if(timer - timerState >= 300):
            ship.state = "normal"
            swing = False
        timer = timer + 1
     
    # Close the window and quit.
    p.quit()
    
    return


asteroidMe()
