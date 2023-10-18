import math
import helperFunctions as hF
import pygame as p
import constants as c

basicShip = [[3, 0], [0, 4], [5, 4], [14, 0], [5, -4], [0, -4], [3, 0]]

screenWidth = 1920
screenHeight = 1080

flashLightPoints = [[-c.screenHeight, c.screenWidth], [-c.screenHeight, -c.screenWidth], [c.screenHeight, -c.screenWidth], [c.screenHeight, c.screenWidth]]

class spaceShip:
    
    def __init__(self, x0, y0, heading0, scaleFactor0, points):
        self.x = x0
        self.y = y0
        self.heading = heading0
        self.scaleFactor = scaleFactor0
        self.speedx = 0
        self.speedy = 0
        self.thrust = 0
        self.health = 10
        self.gas = 100

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

        self.myDrawThrust = False
        self.lens = (self.x, self.y)
        self.lensSize = 5
        
        self.flashLightOn = False
        self.flashLightLeft = []
        self.flashLightRight = []
        self.battery = 360

        return

    def setGunSpot(self, gunSpot):
        self.gunSpot = gunSpot
        return

    def getGunSpot(self):
        return self.gunX, self.gunY
    
    def updateLens(self):
        self.lens = (self.x, self.y)
        return
    
    def getLens(self):
        return self.x, self.y
    
    def drawLens(self, screen):
        p.draw.circle(screen, c.WHITE, self.getLens(), 100, 1)
        p.draw.circle(screen, c.GREY1, self.getLens(), 110, 1)
        p.draw.circle(screen, c.GREY2, self.getLens(), 120, 1)
        return
    
    def moveMe(self, bulletTime):
        # Move ship along current course.
        if not bulletTime:
            self.x = self.x + self.speedx 
            self.y = self.y + self.speedy
        else: 
            self.x = self.x + self.speedx * c.bulletTimeSlowFactor
            self.y = self.y + self.speedy * c.bulletTimeSlowFactor
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
    
    def thrustUp(self, inc, maxSpeed, bulletTime):
        self.thrust = 0.5*(inc**2)
        radAng = hF.deg2Rad(self.heading)
        if not bulletTime:
            self.speedx = self.speedx + self.thrust * math.cos(radAng)
        else: 
            self.speedx = self.speedx + self.thrust * math.cos(radAng) * c.bulletTimeSlowFactor
        if (self.speedx >= maxSpeed):
            self.speedx = maxSpeed
        elif (self.speedx <= -1*maxSpeed):
            self.speedx = -1*maxSpeed

        if not bulletTime:
            self.speedy = self.speedy + self.thrust * math.sin(radAng)
        else:
            self.speedy = self.speedy + self.thrust * math.sin(radAng) * c.bulletTimeSlowFactor
        if (self.speedy >= maxSpeed):
            self.speedy = maxSpeed
        elif (self.speedy <= -1*maxSpeed):
            self.speedy = -1*maxSpeed

        return
    
    def thrustDown(self):
        self.thrust = self.thrust * 0.9

        return
    
    def gasUp(self, bulletTime):
        if not bulletTime:
            self.gas += 1
        else:
            self.gas += c.bulletTimeSlowFactor
        return
    
    def gasDown(self, bulletTime):
        if not bulletTime:
            self.gas -= 3
        else:
            self.gas -= 3 * c.bulletTimeSlowFactor    
        return 
    
    def turn(self, inc):
        self.heading = self.heading + inc

        if (self.heading > 359):
            self.heading = 0
        elif (self.heading < 0):
            self.heading = 359

        return
    
    def drawMe(self, screen, color, myShip):
        points = []
        isTheGunSpot = False
        for myPoint in myShip:
            if (myPoint == self.gunSpot):
                isTheGunSpot = True
                
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

            x, y = (xt, yt)

            # Put point into polygon point list.
            points.append([x, y])

        p.draw.polygon(screen, color, points, width=2)
        return
    
    def drawFlashlight(self, screen):
        x0, y0 = [14,0]    
        # Rotate the point.
        myRadius = hF.getDist(self.xc, self.yc, x0, y0)
        theta = math.atan2(y0 - self.yc, x0 - self.xc)
        radAng = hF.deg2Rad(self.heading)
        xStartr = self.xc + myRadius*math.cos(radAng + theta)
        yStartr = self.yc + myRadius*math.sin(radAng + theta)

        # Scale.
        xStarts = xStartr * self.scaleFactor
        yStarts = yStartr * self.scaleFactor

        # Translate.
        xStart = xStarts + self.x
        yStart = yStarts + self.y

        x1 ,y1 = [screenWidth, -300]
        myRadius = hF.getDist(self.xc, self.yc, x1, y1)
        theta = math.atan2(y1 - self.yc, x1 - self.xc)
        radAng = hF.deg2Rad(self.heading)
        xLeftEndr = self.xc + myRadius*math.cos(radAng + theta)
        yLeftEndr = self.yc + myRadius*math.sin(radAng + theta)

        # Scale.
        xLeftEnds = xLeftEndr * self.scaleFactor
        yLeftEnds = yLeftEndr * self.scaleFactor

        # Translate.
        xLeftEnd = xLeftEnds + self.x
        yLeftEnd = yLeftEnds + self.y

        x2 ,y2 = [screenWidth, 300]
        myRadius = hF.getDist(self.xc, self.yc, x2, y2)
        theta = math.atan2(y2 - self.yc, x2 - self.xc)
        radAng = hF.deg2Rad(self.heading)
        xRightEndr = self.xc + myRadius*math.cos(radAng + theta)
        yRightEndr = self.yc + myRadius*math.sin(radAng + theta)

        # Scale.
        xRightEnds = xRightEndr * self.scaleFactor
        yRightEnds = yRightEndr * self.scaleFactor

        # Translate.
        xRightEnd = xRightEnds + self.x
        yRightEnd = yRightEnds + self.y

        self.flashLightLeft = [xLeftEnd, yLeftEnd]
        self.flashLightRight = [xRightEnd, yRightEnd]

        points = [[xStart, yStart], [xLeftEnd, yLeftEnd]]
        # Get coords of point.
        for point in flashLightPoints:
            x0 = float(point[0])
            y0 = float(point[1])
            # Rotate the point.
            myRadius = hF.getDist(self.xc, self.yc, x0, y0)
            theta = math.atan2(y0 - self.yc, x0 - self.xc)
            radAng = hF.deg2Rad(self.heading)
            xr = self.xc + myRadius*math.cos(radAng + theta)
            yr = self.yc + myRadius*math.sin(radAng + theta)

            # Scale.
            xs = xr * self.scaleFactor
            ys = yr * self.scaleFactor

            # Translate.
            xt = xs + self.x
            yt = ys + self.y

            x, y = (xt, yt)

            # Put point into polygon point list.
            points.append([x, y])
            p.draw.line(screen, c.GREEN, [xStart, yStart], [x,y])

        points.append([xRightEnd, yRightEnd])
        points.append([xStart, yStart])

        p.draw.polygon(screen, c.BLACK, points)
        p.draw.line(screen, c.WHITE, [xStart, yStart], [xLeftEnd, yLeftEnd])
        p.draw.line(screen, c.WHITE, [xStart, yStart], [xRightEnd, yRightEnd])
        return

    def drawThrust(self, screen, color):
        x0, y0 = [0,0]    
        # Rotate the point.
        myRadius = hF.getDist(self.xc, self.yc, x0, y0)
        theta = math.atan2(y0 - self.yc, x0 - self.xc)
        radAng = hF.deg2Rad(self.heading)
        xStartr = self.xc + myRadius*math.cos(radAng + theta)
        yStartr = self.yc + myRadius*math.sin(radAng + theta)

        # Scale.
        xStarts = xStartr * self.scaleFactor
        yStarts = yStartr * self.scaleFactor

        # Translate.
        xStart = xStarts + self.x
        yStart = yStarts + self.y

        x1 ,y1 = [-5, 0]
        myRadius = hF.getDist(self.xc, self.yc, x1, y1)
        theta = math.atan2(y1 - self.yc, x1 - self.xc)
        radAng = hF.deg2Rad(self.heading)
        xEndr = self.xc + myRadius*math.cos(radAng + theta)
        yEndr = self.yc + myRadius*math.sin(radAng + theta)

        # Scale.
        xEnds = xEndr * self.scaleFactor
        yEnds = yEndr * self.scaleFactor

        # Translate.
        xEnd = xEnds + self.x
        yEnd = yEnds + self.y
        
        p.draw.line(screen, color, [xStart, yStart], [xEnd, yEnd], 2)

        return
