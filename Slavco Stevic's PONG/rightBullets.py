import pygame as p
class rightBullets():
    def __init__(self):
        self.bullets = []
        
    def fireBullet(self, bullet, scr):
        self.bullets.append(bullet)
        bullet.drawing = True
        bullet.drawMe(scr)
    
    def drawBullets(self, scr):
        for bullet in self.bullets:
            bullet.drawMe(scr)
            
    def didBulletHit(self, scr, leftP):
        for bullet in self.bullets:
            if (bullet.x <= leftP.x and (bullet.y >= leftP.paddleTop and bullet.y <= leftP.paddleBot)):
                bullet.explode(scr)
                leftP.bulletHit()
                self.bullets.remove(bullet)
            elif bullet.x + 16 <= scr.leftX:
                bullet.explode(scr)
                self.bullets.remove(bullet)
    
    def reset(self):
        self.bullets.clear()
    
class rightBullet():
    def __init__(self, rightP):
        self.x = rightP.x - 32
        self.height = 32
        self.y = rightP.y + rightP.halfH - self.height/2
        self.width = 64
        
        self.speedX = 10
        
        self.bullet = p.image.load("Fireball\\fireball.gif")
        self.bullet_rect = self.bullet.get_rect()
        
        self.drawing = False
        
    def drawMe(self, scr):
        if self.drawing == True:
            self.bullet_rect.center = (self.x, self.y)
            myRect = p.Rect(self.x, self.y, self.width, self.height)
            self.bullet = p.transform.scale(self.bullet, (myRect.width, myRect.height))
            self.bullet_rect.topleft = myRect.topleft
            #p.draw.rect(scr.screen, (0,0,0), myRect, width = 0)
            scr.screen.blit(self.bullet, self.bullet_rect)
            self.x = self.x - self.speedX
        
    def explode(self, scr):
        self.explosion = p.image.load("Explosion\\explosion.gif")
        self.explosion_rect = self.explosion.get_rect()
        self.explosion_rect.center = (self.x, self.y)
        myRect = p.Rect(self.x, self.y, self.width, self.height)
        self.explosion = p.transform.scale(self.explosion, (myRect.width, myRect.height))
        self.explosion_rect.topleft = myRect.topleft
        #p.draw.rect(scr.screen, (0,0,0), myRect, width = 0)
        scr.screen.blit(self.explosion, self.explosion_rect)