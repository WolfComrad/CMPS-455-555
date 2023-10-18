import pygame as p
from leftPaddle import leftPaddle
from rightPaddle import rightPaddle
from pongGraphics import makePongTable
from ball import ball
from leftBullets import leftBullets
from leftBullets import leftBullet
from rightBullets import rightBullets
from rightBullets import rightBullet
import sys

class Screen:
    def __init__(self, bg):
        self.screenWidth = 1280
        self.screenHeight = 720
        self.border = 20
        
        self.background = p.transform.scale(bg, (self.screenWidth, self.screenHeight))
        self.background_rect = self.background.get_rect()
        self.screen = p.display.set_mode((self.screenWidth, self.screenHeight))
        
        self.leftX = self.border
        self.rightX = self.screenWidth - 3*self.border
        self.ballRightX = self.screenWidth - self.border
        self.midY = int(self.screenHeight / 2)
        
        self.yLow = self.border
        self.yHi = self.screenHeight - self.border
        
        self.midBoardX = self.border + int(self.screenWidth/2)
        self.midBoardY = self.border + int(self.screenHeight/2)
        
        self.botY = self.screenHeight - self.border
        self.topY = self.border
    
    def apply_background(self):
        self.screen.blit(self.background, self.background_rect)
    
def graphics(scr):
    p.init()
    
    leftP = leftPaddle(scr.leftX, scr.midY, 40, 150)
    rightP = rightPaddle(scr.rightX, scr.midY, 40, 150)
    bball = ball(scr)
    
    lBullets = leftBullets()
    rBullets = rightBullets()
    
    llast_fire_time = 0
    rlast_fire_time = 0
    running = True
    game = True
    while running:
        scr.apply_background()
        
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            
            if event.type == p.KEYDOWN and event.key == p.K_SPACE:
                lcurr_fire_time = p.time.get_ticks()
                if lcurr_fire_time - llast_fire_time >= 500:
                    llast_fire_time = lcurr_fire_time
                    lBullet = leftBullet(leftP)
                    lBullets.fireBullet(lBullet, scr)
                    
            if event.type == p.KEYDOWN and event.key == p.K_a:
                rcurr_fire_time = p.time.get_ticks()
                if rcurr_fire_time - rlast_fire_time >= 500:
                    rlast_fire_time = rcurr_fire_time
                    rBullet = rightBullet(rightP)
                    rBullets.fireBullet(rBullet, scr) 

            if event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                game = True
                leftP.reset(scr)
                rightP.reset(scr)
                lBullets.reset()
                rBullets.reset()
                bball = ball(scr)
                
        # END GAME SCREEN
        text = "GAME OVER!"
        font = p.font.Font(None, 100)
        text_surface = font.render(text, True, (255, 0, 0))
        text_rect = text_surface.get_rect()
        text_rect.center = (scr.screenWidth // 2, scr.screenHeight // 2)
              
        """ Check for keyboard presses. """
        key = p.key.get_pressed()
        
        if game == False:
            scr.screen.blit(text_surface, text_rect)
            
        if game:
            # Movement
            bball.moveMe(scr.leftX, scr.ballRightX, scr.yLow, scr.yHi, leftP, rightP)
            bX, bY, bRad = bball.getXYRad()
            #rightP.autoTrack(bX, bY, scr)
            auto = False
            if auto:
                rcurr_fire_time = p.time.get_ticks()
                if rcurr_fire_time - rlast_fire_time >= 1000:
                    rlast_fire_time = rcurr_fire_time
                    rBullet = rightBullet(rightP)
                    rBullets.fireBullet(rBullet, scr) 
            
            if (key[p.K_ESCAPE] == True): 
                running = False
            if (key[p.K_UP] == True): 
                leftP.moveMe(-1, scr)
                pass
            if (key[p.K_DOWN] == True): 
                leftP.moveMe(1, scr)
                pass
            if (key[p.K_w] == True):
                rightP.moveMe(-1, scr)
                pass
            if (key[p.K_s] == True):
                rightP.moveMe(1, scr)
                pass

        
            # Collisions
            # Check for a bullet hit on left and right paddle.
            lBullets.didBulletHit(scr, rightP)
            rBullets.didBulletHit(scr, leftP)
            
            # Check for a left and right bullet hit on the ball
            bball.didBulletHit(rBullets, lBullets, scr)
            
            # Check for a ball hit on the left paddle.
            
            ballhit = leftP.didBallHit(bX, bY, bRad)
            # If there was a hit, do a bounce.
            if (ballhit == True):
                bball.xBounce()
            else:
                # Check for a ball hit on the right paddle.
                ballhit = rightP.didBallHit(bX, bY)
                if (ballhit == True):
                    bball.xBounce()
                    
            # Drawing            
            bball.drawMe(scr)
            lBullets.drawBullets(scr)
            rBullets.drawBullets(scr)
            
            if leftP.over == True:
                game = False
            elif rightP.over == True:
                game = False
                
        makePongTable(scr.screen, scr.screenWidth, scr.screenHeight, scr.border)
        leftP.drawPaddle(scr)
        leftP.drawScore(scr)
        rightP.drawPaddle(scr)
        rightP.drawScore(scr)
        
        p.display.flip()
    
    p.quit()
    
### MAIN ###
bg = p.image.load("background\\backgroundMain.png")
scr = Screen(bg)

graphics(scr)