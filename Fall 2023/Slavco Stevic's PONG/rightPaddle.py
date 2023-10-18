import pygame as p

class rightPaddle:
    def __init__(self, x, y, width, height): 
        # Paddle
        self.halfW = int(width/2)
        self.halfH = int(height/2)
        self.x = x
        self.y = y - self.halfH #adjusting left corner
        self.width = width
        self.height = height
        self.speedY = 5
        
        self.paddleTop = self.y
        self.paddleBot = self.y + 2*self.halfH
        
        self.hit = False
        self.hit_time = 0
        
        self.paddle2 = p.image.load("Paddles\\paddle-2.png")
        self.paddle2_rect = self.paddle2.get_rect()
        
        self.life = 5
        self.over = False

    def drawPaddle(self, scr):
        self.paddle2_rect.center = (self.x, self.y)
        myRect = p.Rect(self.x, self.y, self.width, self.height)
        self.paddle2 = p.transform.scale(self.paddle2, (myRect.width, myRect.height))
        self.paddle2_rect.topleft = myRect.topleft
        #p.draw.rect(scr.screen, (0,0,0), myRect, width = 0)
        scr.screen.blit(self.paddle2, self.paddle2_rect)
        
    def drawScore(self, scr):
        for i in range(0, self.life):
            myRect = p.Rect(scr.screenWidth - i*35 - 50, 0, 30, 10)
            p.draw.rect(scr.screen, (0, 255, 0), myRect, width = 0)
        if self.life != 5:
            for i in range(self.life, 5):
                myRect = p.Rect(scr.screenWidth - i*35 - 50, 0, 30, 10)
                p.draw.rect(scr.screen, (255, 0, 0), myRect, width = 0)
        
    
    def moveMe(self, dir, scr):
        self.checkSpeedTime()
        
        self.x = self.x 
        if dir == -1:
            self.y = self.y - self.speedY
        elif dir == 1:
            self.y = self.y + self.speedY
        
        self.paddleTop = self.y
        self.paddleBot = self.y + 2*self.halfH
        
        if (self.paddleTop < scr.topY):
            self.y = self.y + (scr.topY - self.paddleTop)
            
        if (self.paddleBot > scr.botY):
            self.y = self.y - (self.paddleBot - scr.botY)
    
    def autoTrack(self, bX, bY, scr):
        self.x = self.x 
        self.y = bY - self.halfH
        
        self.paddleTop = self.y
        self.paddleBot = self.y + 2*self.halfH
        
        if (self.paddleTop < scr.topY):
            self.y = self.y + (scr.topY - self.paddleTop)
            
        if (self.paddleBot > scr.botY):
            self.y = self.y - (self.paddleBot - scr.botY)
    
    def didBallHit(self, bX, bY):
        hit = False
        
        if (bX > (self.x - self.halfW)):
            if ( (bY >= self.paddleTop) and 
                (bY <= self.paddleBot) ):
                hit = True
                
        return hit
    
    def bulletHit(self):
        if self.hit == False:
            self.hit = True
            self.hit_time = p.time.get_ticks()
            self.speedY = self.speedY - 3
        self.life = self.life - 1
        
        if self.life == 0:
            self.over = True
                       
    def checkSpeedTime(self):
        if self.hit == True:
            current_time = p.time.get_ticks()
            if current_time - self.hit_time >= 5000:
                self.speedY = self.speedY + 3
                self.hit = False
                
    def reset(self, scr):
        self.life = 5
        self.over = False
        self.x = scr.rightX
        self.y = scr.midY - self.halfH #adjusting left corner