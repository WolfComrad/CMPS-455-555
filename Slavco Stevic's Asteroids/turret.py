import pygame as p

class Turret:
    def  __init__(self, scr):
        self.scr = scr
        # position and initial angle
        self.width = 21
        self.height = 18
        self.x = scr.screenWidth / 2 - self.width / 2
        self.y = scr.screenHeight / 2 - self.height / 2
        self.angle = 0
        # center of rotation
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
        # turret graphics
        self.base_turret = p.image.load("graphics/turret.png")
        self.base_turret = p.transform.scale(self.base_turret, (self.width, self.height))
        self.turret_rect = self.base_turret.get_rect(topleft=(self.x, self.y))
        self.turret = self.base_turret
    
    def drawTurret(self):
        self.scr.screen.blit(self.turret, self.turret_rect)

    def rotateTurret(self, inc):
        if inc == 'L':
            self.angle = self.angle + 1
        elif inc == 'R':
            self.angle = self.angle - 1
            
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
        
        self.turret = p.transform.rotate(self.base_turret, self.angle)
        self.turret_rect = self.turret.get_rect(center=(self.xCenter, self.yCenter))
        self.drawTurret()

    def reset(self):
        # position and initial angle
        self.width = 21
        self.height = 18
        self.x = self.scr.screenWidth / 2 - self.width / 2
        self.y = self.scr.screenHeight / 2 - self.height / 2
        self.angle = 0
        # center of rotation
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
        # turret graphics
        self.base_turret = p.image.load("graphics/turret.png")
        self.base_turret = p.transform.scale(self.base_turret, (self.width, self.height))
        self.turret_rect = self.base_turret.get_rect(topleft=(self.x, self.y))
        self.turret = self.base_turret