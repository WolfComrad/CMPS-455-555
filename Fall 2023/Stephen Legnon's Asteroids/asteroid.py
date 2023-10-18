import math
import random
import pygame as p
import constants as c
import helperFunctions as hF

class spaceRock:
    def __init__(self):
        self.x = random.randint(0, c.screenWidth - 1)
        self.y = random.randint(0, c.screenHeight - 1)
        self.heading = random.randint(0, 359)
        self.xVel = random.randint(-c.maxRockVelocity, c.maxRockVelocity)
        self.yVel = random.randint(-c.maxRockVelocity, c.maxRockVelocity)
        self.scaleFactorX = random.randint(1, c.maxRockScaleFactor)
        self.scaleFactorY = random.randint(1, c.maxRockScaleFactor)
        index = random.randint(0, c.nRockTypes - 1)
        self.myPoints = c.spaceRocks[index]
        self.isVisible = False

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
            xr, yr = hF.rotatePoint(self.xc, self.yc, x, y, self.heading)
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

        index = random.randint(0, c.nColors - 1)
        self.color = c.WHITE

        self.isActive = True

    def moveMe(self, bulletTime):
        # Calculate new positon of space rock based on it's velocity.
        if not bulletTime:
            self.x = self.x + self.xVel
            self.y = self.y + self.yVel
        else: 
            self.x = self.x + self.xVel * c.bulletTimeSlowFactor
            self.y = self.y + self.yVel * c.bulletTimeSlowFactor
        # If rock is outside of game space wrap it to other side.
        if (self.x < 0):
            self.x = c.screenWidth - 1
        elif (self.x > c.screenWidth):
            self.x = 0

        if (self.y < 0):
            self.y = c.screenHeight - 1
        elif (self.y > c.screenHeight):
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
                myRadius = hF.getDist(self.xc, self.yc, x0, y0)
                theta = math.atan2(y0 - self.yc, x0 - self.xc)
                radAng = hF.deg2Rad(self.heading)
                xr = self.xc + myRadius*math.cos(radAng + theta)
                yr = self.yc + myRadius*math.sin(radAng + theta)

                # Scale.
                xs = xr * self.scaleFactorX
                ys = yr * self.scaleFactorY

                # Translate.
                xt = xs + self.x
                yt = ys + self.y
                x, y = xt, yt

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
        astroidDist = hF.getDist(x1, y1, self.x, self.y)
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