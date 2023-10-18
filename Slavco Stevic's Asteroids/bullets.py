import pygame as p
import math as m

class Bullets():
    def __init__(self, scr):
        self.scr = scr
        self.bullets = []
        # sounds
        self.shoot_sound = p.mixer.Sound('sounds/shoot.wav')
        
    def fireBullet(self, bullet):
        self.bullets.append(bullet)
        bullet.drawBullet()
        self.shoot_sound.play()
    
    def drawBullets(self):
        for bullet in self.bullets:
            bullet.drawBullet()
            
    def bulletCollision(self):        
        for bullet in self.bullets:
            bullet_x_left = bullet.x
            bullet_x_right = bullet.x + bullet.width
            if bullet_x_left <= 0 or bullet_x_right >= self.scr.screenWidth:
                self.bullets.remove(bullet)
                    
    def reset(self):
        self.bullets.clear()
            
    
class Bullet():
    def __init__(self, turret, scr):
        self.scr = scr
        # from where it was fired
        self.height = 6
        self.width = 17
        self.x = turret.x + turret.width / 2 - self.width / 2
        self.y = turret.y + turret.height / 2 - self.height / 2
        self.vel = 2.0
        self.angle = turret.angle
        # graphics
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
        self.base_bullet = p.image.load("graphics/bullet.png")
        self.base_bullet = p.transform.scale(self.base_bullet, (self.width, self.height))
        self.bullet_rect = self.base_bullet.get_rect(topleft=(self.x, self.y))
        self.bullet = self.base_bullet
        
    def drawBullet(self):
        self.x += self.vel * m.cos(m.radians(self.angle)) 
        self.y -= self.vel * m.sin(m.radians(self.angle))
        
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
    
        self.bullet = p.transform.rotate(self.base_bullet, self.angle)
        self.bullet_rect = self.bullet.get_rect(center=(self.xCenter, self.yCenter))
        
        self.scr.screen.blit(self.bullet, self.bullet_rect)
    '''    
    def explode(self, scr):
        self.explosion = p.image.load("Explosion-2\\explosion-2.gif")
        self.explosion_rect = self.explosion.get_rect()
        self.explosion_rect.center = (self.x, self.y)
        myRect = p.Rect(self.x, self.y, self.width, self.height)
        self.explosion = p.transform.scale(self.explosion, (myRect.width, myRect.height))
        self.explosion_rect.topleft = myRect.topleft
        scr.screen.blit(self.explosion, self.explosion_rect)
    '''