import pygame as p
import math as m
from PIL import Image, ImageSequence

class Rocket():
    def __init__(self, turret, scr):
        self.scr = scr
        self.flying = False
        # from where it was fired
        self.height = 12*2
        self.width = 18*2
        self.explosion_width = 256
        self.explosion_height = 256
        self.x = turret.x + turret.width / 2 - self.width / 2
        self.y = turret.y + turret.height / 2 - self.height / 2
        self.vel = 1.5
        self.angle = turret.angle
        # graphics
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
        self.base_rocket = p.image.load("graphics/rocket.png")
        self.base_rocket = p.transform.scale(self.base_rocket, (self.width, self.height))
        self.rocket_rect = self.base_rocket.get_rect(topleft=(self.x, self.y))
        self.rocket = self.base_rocket
        
        self.explosion_frames = ["graphics/explosion/ex0.png", "graphics/explosion/ex1.png", "graphics/explosion/ex2.png",
                                 "graphics/explosion/ex3.png", "graphics/explosion/ex4.png"]
        self.explosion_playing = False
        self.frame_index = 0
        self.frame_time = 0
        
        # sounds
        self.rocket_flying_sound = p.mixer.Sound('sounds/rocket.wav')
        self.rocket_hit_sound = p.mixer.Sound('sounds/rockethit.wav')
        self.rocket_hit_bass = p.mixer.Sound('sounds/rockethit2.wav')
    
    def followTurret(self, turret):
        self.x = turret.x + turret.width / 2 - self.width / 2
        self.y = turret.y + turret.height / 2 - self.height / 2
        self.angle = turret.angle
        
    def drawRocket(self, turret):
        self.angle = turret.angle
        self.x += self.vel * m.cos(m.radians(self.angle)) 
        self.y -= self.vel * m.sin(m.radians(self.angle))
        
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
    
        self.rocket = p.transform.rotate(self.base_rocket, self.angle)
        self.rocket_rect = self.rocket.get_rect(center=(self.xCenter, self.yCenter))
        
        self.scr.screen.blit(self.rocket, self.rocket_rect)
        
        if (self.x + self.width < 0):
            self.x = self.scr.screenWidth
        elif (self.x > self.scr.screenWidth):
            self.x = 0 - self.width

        if (self.y + self.height < 0):
            self.y = self.scr.screenHeight
        elif (self.y > self.scr.screenHeight):
            self.y = 0 - self.height
        
    def drawExplosion(self):
        if self.explosion_playing == True and self.frame_index < 5:
            self.base_explosion = p.image.load(self.explosion_frames[self.frame_index])
            self.base_explosion = p.transform.scale(self.base_explosion, (self.explosion_width, self.explosion_height))
            self.explosion_rect = self.base_explosion.get_rect(topleft=(self.x, self.y))
            self.explosion = self.base_explosion
               
            self.xCenter = self.x + self.width/2
            self.yCenter = self.y + self.height/2
        
            self.explosion = p.transform.rotate(self.base_explosion, self.angle)
            self.explosion_rect = self.explosion.get_rect(center=(self.xCenter, self.yCenter))
            
            self.scr.screen.blit(self.explosion, self.explosion_rect)
            current_time = p.time.get_ticks()
            if current_time - self.frame_time >= 50:
                self.frame_time = p.time.get_ticks()
                self.frame_index += 1
        else:
            self.explosion_playing = False
                
    def reset(self, turret):
        self.flying = False
        # from where it was fired
        self.x = turret.x + turret.width / 2 - self.width / 2
        self.y = turret.y + turret.height / 2 - self.height / 2
        self.angle = turret.angle
        # graphics
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
        self.base_rocket = p.image.load("graphics/rocket.png")
        self.base_rocket = p.transform.scale(self.base_rocket, (self.width, self.height))
        self.rocket_rect = self.base_rocket.get_rect(topleft=(self.x, self.y))
        self.rocket = self.base_rocket
        
        self.explosion_frames = ["graphics/explosion/ex0.png", "graphics/explosion/ex1.png", "graphics/explosion/ex2.png",
                                 "graphics/explosion/ex3.png", "graphics/explosion/ex4.png"]
        self.explosion_playing = False
        self.frame_index = 0
        self.frame_time = 0