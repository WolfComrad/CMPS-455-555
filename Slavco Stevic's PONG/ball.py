import pygame as p
import random

class ball:
    def __init__(self, scr):
        self.radius = 40
        self.x = scr.midBoardX - self.radius/2
        self.y = scr.midBoardY - self.radius/2
        
        self.xVel = random.randint(0, 2) + 2
        self.yVel = random.randint(0, 2) + 1
        
        self.ball = p.image.load("Ball\\ballfinal.png")
        self.ball_rect = self.ball.get_rect()
        
        self.bounce = False
        self.bounce_time = 0

    
    def drawMe(self, scr):
        self.ball_rect.center = (self.x, self.y)
        myRect = p.Rect(self.x, self.y, self.radius, self.radius)
        self.ball = p.transform.scale(self.ball, (myRect.width, myRect.height))
        #p.draw.rect(scr.screen, (0,0,0), myRect, width = 0)
        self.ball_rect.topleft = myRect.topleft
        
        scr.screen.blit(self.ball, self.ball_rect)
    
    def moveMe(self, xLeft, xRight, yLow, yHi, leftP, rightP):
        self.x = self.x + self.xVel
        self.y = self.y + self.yVel
        self.checkBounce()
        if (self.x < xLeft):
            if self.bounce == False:
                self.bounce = True
                self.bounce_time = p.time.get_ticks()
                self.x = xLeft
                self.xVel = -1 * self.xVel
                leftP.life = leftP.life - 1
                
            if leftP.life == 0:
                leftP.over = True
            
        if ((self.x + self.radius) > xRight):
            if self.bounce == False:
                self.bounce = True
                self.bounce_time = p.time.get_ticks()
                self.x = xRight - self.radius
                self.xVel = -1 * self.xVel
                rightP.life = rightP.life - 1
                
            if rightP.life == 0:
                rightP.over = True
            
        if (self.y < yLow):
            self.y = yLow
            self.yVel = -1 * self.yVel 
            
        if ((self.y + self.radius) > yHi):
            self.y = yHi - self.radius
            self.yVel = -1 * self.yVel 
            
        return
    
    def getXYRad(self):
        return self.x + self.radius/2, self.y + self.radius/2, self.radius
    
    def xBounce(self):
        self.checkBounce()
        if self.bounce == False:
            self.bounce = True
            self.bounce_time = p.time.get_ticks()
            self.xVel = self.xVel * -1
        return
    
    def checkBounce(self):
        if self.bounce == True:
            current_time = p.time.get_ticks()
            if current_time - self.bounce_time >= 500:
                self.bounce = False
            
    def didBulletHit(self, rBullets, lBullets, scr):
        if self.xVel > 0:
            for bullet in rBullets.bullets:
                if ((bullet.x <= self.x + self.radius and bullet.x + bullet.width >= self.x) and 
                    (bullet.y <= self.y + self.radius and bullet.y + bullet.height >= self.y)):
                    self.xBounce()
                    bullet.explode(scr)
                    rBullets.bullets.remove(bullet)
        elif self.xVel < 0:
            for bullet in lBullets.bullets:
                if ((bullet.x + bullet.width >= self.x and bullet.x <= self.x + self.radius) and 
                    (bullet.y <= self.y + self.radius and bullet.y + bullet.height >= self.y)):
                    self.xBounce()
                    bullet.explode(scr)
                    lBullets.bullets.remove(bullet)