import pygame as p
import math as m
from turret import Turret

class spaceShip:
    def __init__(self, scr):
        self.scr = scr
        self.playing = True
        self.win = False
        self.defeat = False
        # ship position = (x, y)
        self.width = 26 * 2
        self.height = 30 * 2
        self.x = self.scr.screenWidth / 2 - self.width / 2
        self.y = self.scr.screenHeight / 2 - self.height / 2
        self.angle = 0
        self.vel = 1.3
        # center of rotation
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
        # stats
        self.lives = 4
        self.hit = False
        self.hit_time = 0
        self.invincibility = False
        self.shield_time = 0
        self.shield = False
        self.shield_dimensions = 52 *2
        self.power_up = True
        self.score = 0
        self.updateShipGraphics()
        # sounds
        self.win_sound = p.mixer.Sound('sounds/win.wav')
        self.lose_sound = p.mixer.Sound('sounds/lose2.wav')
        self.invincibility_sound = p.mixer.Sound('sounds/invincibility.wav')
        self.ambience_sound = p.mixer.Sound('sounds/ambience.wav')
        self.shield_sound = p.mixer.Sound('sounds/shield.wav')
        self.start_sound = p.mixer.Sound('sounds/start.wav')
        # turret
        self.turret = Turret(scr)

    def updateShipGraphics(self):
        if self.lives == 4:
            self.image = "graphics/ship/ship4.png"
        elif self.lives == 3:
            self.image = "graphics/ship/ship3.png"
        elif self.lives == 2:
            self.image = "graphics/ship/ship2.png"
        elif self.lives == 1:
            self.image = "graphics/ship/ship1.png"
            
        self.base_ship = p.image.load(self.image)
        self.base_ship = p.transform.scale(self.base_ship, (self.width, self.height))
        self.ship_rect = self.base_ship.get_rect(topleft=(self.x, self.y))
        self.ship = self.base_ship
        
        self.base_ship_invincibility = p.image.load("graphics/invincibility.png")
        self.base_ship_invincibility = p.transform.scale(self.base_ship_invincibility, (self.width, self.height))
        self.ship_invincibility_rect = self.base_ship_invincibility.get_rect(topleft=(self.x, self.y), center=(self.xCenter, self.yCenter))
        self.ship_invincibility = self.base_ship_invincibility
        
        self.base_ship_shield = p.image.load("graphics/shield.png")
        self.base_ship_shield = p.transform.scale(self.base_ship_shield, (self.shield_dimensions, self.shield_dimensions))
        self.ship_shield_rect = self.base_ship_shield.get_rect(topleft=(self.x, self.y), center=(self.xCenter, self.yCenter))
        self.ship_shield = self.base_ship_shield
        
        self.transform()
        
    def drawShip(self):
        self.scr.screen.blit(self.ship, self.ship_rect)
        if self.invincibility == True:
            self.scr.screen.blit(self.ship_invincibility, self.ship_invincibility_rect)
            
        if self.shield == True:
            self.transform()
            self.scr.screen.blit(self.ship_shield, self.ship_shield_rect)
    
    def moveShip(self, inc):
        if inc == 'Up':
            x = self.vel * m.cos(m.radians(self.angle))
            y = self.vel * m.sin(m.radians(self.angle))
            
            if 0 <= (self.x + x) <= self.scr.screenWidth - self.width and 0 <= (self.y - y) <= self.scr.screenHeight - self.height:
                self.x += x
                self.y -= y
                self.turret.x += x
                self.turret.y -= y

        elif inc == 'L':
            self.angle = self.angle + 1
        elif inc == 'R':
            self.angle = self.angle - 1
        self.transform()
            
    def transform(self):    
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
        
        self.ship = p.transform.rotate(self.base_ship, self.angle)
        self.ship_rect = self.ship.get_rect(topleft=(self.x, self.y), center=(self.xCenter, self.yCenter))
        
        if self.invincibility == True:
            self.ship_invincibility = p.transform.rotate(self.base_ship_invincibility, self.angle)
            self.ship_invincibility_rect = self.ship_invincibility.get_rect(topleft=(self.x, self.y), center=(self.xCenter, self.yCenter))
            
        if self.shield == True:
            self.ship_shield = p.transform.rotate(self.base_ship_shield, self.angle)
            self.ship_shield_rect = self.ship_shield.get_rect(topleft=(self.x, self.y), center=(self.xCenter, self.yCenter))    
            
    def gotHit(self):
        if self.hit == True:
            current_time = p.time.get_ticks()
            if current_time - self.hit_time >= 3000:
                self.hit = False
                self.invincibility = False
    
    def didYouLose(self):
        if self.lives == 0:
            self.defeat = True
         
    def didAsteroidHit(self, asteroids, rocket):
        for a in asteroids.asteroids:
            a_left_X = a.x
            a_right_X = a.x + a.width
            a_bot_Y = a.y
            a_top_Y = a.y + a.height
            
            ship_left_X = self.x
            ship_right_X = self.x + self.width
            ship_bot_Y = self.y
            ship_top_Y = self.y + self.height
                    
            if ((ship_left_X <= a_right_X <= ship_right_X and ship_bot_Y <= a_top_Y <= ship_top_Y) or
                   #top left
                   (ship_left_X <= a_left_X <= ship_right_X and ship_bot_Y <= a_top_Y <= ship_top_Y) or
                   #top right
                   (ship_left_X <= a_right_X <= ship_right_X and ship_bot_Y <= a_bot_Y <= ship_top_Y) or 
                   #bot left
                   (ship_left_X <= a_left_X <= ship_right_X and ship_bot_Y <= a_bot_Y <= ship_top_Y) or
                   #bot right
                   ((a_left_X <= ship_left_X and a_right_X >= ship_right_X) and ship_bot_Y <= a_top_Y <= ship_top_Y) or
                   #whole top
                   ((a_left_X <= ship_left_X and a_right_X >= ship_right_X) and ship_bot_Y <= a_bot_Y <= ship_top_Y) or 
                   #whole bot
                   (ship_left_X <= a_right_X <= ship_right_X and (a_bot_Y <= ship_bot_Y and a_top_Y >= ship_top_Y)) or
                   #whole left
                   (ship_left_X <= a_left_X <= ship_right_X and (a_bot_Y <= ship_bot_Y and a_top_Y >= ship_top_Y)) or
                   #whole right
                   ((a_left_X >= ship_left_X and a_right_X <= ship_right_X) and ship_bot_Y <= a_top_Y <= ship_top_Y) or
                   #between top
                   ((a_left_X >= ship_left_X and a_right_X <= ship_right_X) and ship_bot_Y <= a_bot_Y <= ship_top_Y) or
                   #between bot
                   (ship_left_X <= a_right_X <= ship_right_X and (a_bot_Y >= ship_bot_Y and a_top_Y <= ship_top_Y)) or
                   #between left
                   (ship_left_X <= a_left_X <= ship_right_X and (a_bot_Y >= ship_bot_Y and a_top_Y <= ship_top_Y))
                   #between right
                   ):
                    if self.shield == True:
                        a.health = 0
                        asteroids.isDestroyed(a, self, rocket)
                    else:
                        a.bounceIt()
                        self.gotHit()  
                        if self.hit == False:
                            self.hit = True
                            self.hit_time = p.time.get_ticks()
                            self.lives -= 1
                            self.invincibility = True
                            self.invincibility_sound.play()
                            self.updateShipGraphics()
            
    def didShieldExpire(self):
        if self.shield == True:
            current_time = p.time.get_ticks()
            if current_time - self.shield_time >= 5000:
                self.power_up = False
                self.shield = False
                
    def didRocketHit(self, rocket):
        if ((self.x < rocket.x and self.x+self.width > rocket.x and self.y < rocket.y and self.y+self.height > rocket.y) or 
            (self.x < rocket.x+rocket.explosion_width and self.x > rocket.x and self.y < rocket.y and self.y+self.height > rocket.y) or
            (self.x < rocket.x+rocket.explosion_width and self.x > rocket.x and self.y < rocket.y+rocket.explosion_height and self.y > rocket.y) or
            (self.x < rocket.x and self.x+self.width > rocket.x and self.y < rocket.y+rocket.explosion_height and self.y > rocket.y)):
            self.gotHit()  
            if self.hit == False:
                self.hit = True
                self.hit_time = p.time.get_ticks()
                self.lives = 0
                self.invincibility = True
                self.invincibility_sound.play()
                self.updateShipGraphics()
                        
    def reset(self):
        self.playing = False
        # ship position = (x, y)
        self.width = 26 * 2
        self.height = 30 * 2
        self.x = self.scr.screenWidth / 2 - self.width / 2
        self.y = self.scr.screenHeight / 2 - self.height / 2
        self.angle = 0
        self.vel = 1
        # center of rotation
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
        # stats
        self.lives = 4
        self.hit = False
        self.hit_time = 0
        self.invincibility = False
        self.score = 0
        self.updateShipGraphics()
        # turret
        self.turret = Turret(self.scr)
                    