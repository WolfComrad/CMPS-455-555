import pygame as p
import math as m
import random as r
    
class Asteroid():
    def __init__(self, scr):
        self.scr = scr
        self.width = 40
        self.height = 35
        self.type = 0
        self.image = ""
        self.health = 0
        self.x = 0
        self.y = 0
        self.velX = r.uniform(0.5, 1)
        self.velY = r.uniform(0.5, 1)
        self.bounceX = 1
        self.bounceY = 1
        self.angle = r.randint(0, 360)
        self.special = False
        self.bounce = False
        #sounds
        self.special_sound = p.mixer.Sound('sounds/special.wav')
        
    def makeGraphics(self):
        self.base_asteroid = p.image.load(self.image)
        self.base_asteroid = p.transform.scale(self.base_asteroid, (self.width, self.height))
        self.asteroid_rect = self.base_asteroid.get_rect(topleft=(self.x, self.y))
        self.asteroid = self.base_asteroid
    
    def drawAsteroid(self):
        self.x += self.velX * self.bounceX * m.cos(m.radians(self.angle)) 
        self.y -= self.velY * self.bounceY * m.sin(m.radians(self.angle))
        
        self.xCenter = self.x + self.width/2
        self.yCenter = self.y + self.height/2
    
        self.asteroid = p.transform.rotate(self.base_asteroid, self.angle)
        self.asteroid_rect = self.asteroid.get_rect(center=(self.xCenter, self.yCenter))
        
        self.scr.screen.blit(self.asteroid, self.asteroid_rect)
        # wrapping around the screen
        if self.x + self.width < 0:
            self.x = self.scr.screenWidth
            self.y = r.randint(0, self.scr.screenHeight)
            self.angle = r.randint(0, 360)
        elif self.x > self.scr.screenWidth:
            self.x = 0 - self.width
            self.y = r.randint(0, self.scr.screenHeight)
            self.angle = r.randint(0, 360)

        if self.y + self.height < 0:
            self.y = self.scr.screenHeight
            self.x = r.randint(0, self.scr.screenWidth)
            self.angle = r.randint(0, 360)
        elif self.y > self.scr.screenHeight:
            self.y = 0 - self.height
            self.x = r.randint(0, self.scr.screenWidth)
            self.angle = r.randint(0, 360)

    def makeAsteroid(self):
        self.generateSize()
        self.generatePostion()
        self.generateType()
        self.makeGraphics()
    
    def generateSize(self):
        # tuple of height and width
        case0 = (self.width / 2, self.height / 2, 0)
        case1 = (self.width, self.height, 1)
        case2 = (self.width * 2, self.height * 2, 2)
        case3 = (self.width * 5, self.height * 5, 3)
        
        choices = [case0, case1, case2, case3]
        cases = [0, 1, 2, 3]
        weights = [0.2, 0.4, 0.3, 0.1]
        
        self.width, self.height, self.type = self.generate(choices, cases, weights)
        
    def generateType(self):
        case0 = ("graphics/asteroid/asteroid0.png", 5, False)
        case1 = ("graphics/asteroid/asteroid1.png", 3, False)
        case2 = ("graphics/asteroid/asteroid2.png", 1, False)
        case3 = ("graphics/asteroid/specialasteroid.png", 8, True)
        
        choices = [case0, case1, case2, case3]
        cases = [0, 1, 2, 3]
        weights = [0.5, 0.3, 0.2, 0.1]
        
        self.image, self.health, self.special = self.generate(choices, cases, weights)
        
    def generatePostion(self):
        # tuple of 4 which represent x range and y range
        case0 = (0, self.scr.screenWidth, 0, 100)
        case1 = (0, self.scr.screenWidth, self.scr.screenHeight - 100, self.scr.screenHeight) 
        case2 = (0, 100, 0, self.scr.screenHeight)
        case3 = (self.scr.screenWidth - 100, self.scr.screenWidth, 0, self.scr.screenHeight)
        
        choices = [case0, case1, case2, case3]
        cases = [0, 1, 2, 3]
        weights = [0.25, 0.25, 0.25, 0.25]
        
        case = self.generate(choices, cases, weights)
        
        self.x = r.randint(case[0], case[1])
        self.y = r.randint(case[2], case[3])
        
    def makePiece(self, a):
        self.width = self.width / 2
        self.height = self.height / 2
        self.type = 0
        self.image = "graphics/asteroid/asteroid2.png"
        self.special = False
        self.health = 1
        self.x = a.x
        self.y = a.y
        self.makeGraphics()   
        
    def generate(self, choices, cases, weights):
        choice = r.choices(cases, weights=weights, k=1)[0]
        
        for i in range(len(choices)):
            if choice == i:
                return choices[i]
            
    def bounceIt(self):
        self.checkBounce()
        if self.bounce == False:
            self.bounce = True
            self.bounce_time = p.time.get_ticks()
            self.bounceX = -1
            self.bounceY = -1
    
    def checkBounce(self):
        if self.bounce == True:
            current_time = p.time.get_ticks()
            if current_time - self.bounce_time >= 200:
                self.bounce = False  
            
class Asteroids():
    def __init__(self, scr):
        self.scr = scr
        self.asteroids = []
        self.makeAsteroids()
        self.bullethit_sound = p.mixer.Sound('sounds/bullethit.wav')
        
    def makeAsteroids(self):
        for i in range(0, 10):
            asteroid = Asteroid(self.scr)
            asteroid.makeAsteroid()
            self.asteroids.append(asteroid)
            
    def drawAsteroids(self):
        for asteroid in self.asteroids:
            asteroid.drawAsteroid()
          
    def didAsteroidsCollide(self):
        for a in self.asteroids:
            a_left_X = a.x
            a_right_X = a.x + a.width
            a_bot_Y = a.y
            a_top_Y = a.y + a.height
            for b in self.asteroids:
                b_left_X = b.x - a.width
                b_right_X = b.x + b.width + a.width
                b_bot_Y = b.y - a.height
                b_top_Y = b.y + b.height + a.height
                if a != b:
                    if ((a_left_X <= b_right_X <= a_right_X and a_bot_Y <= b_top_Y <= a_top_Y) or
                        #top left
                        (a_left_X <= b_left_X <= a_right_X and a_bot_Y <= b_top_Y <= a_top_Y) or
                        #top right
                        (a_left_X <= b_right_X <= a_right_X and a_bot_Y <= b_bot_Y <= a_top_Y) or 
                        #bot left
                        (a_left_X <= b_left_X <= a_right_X and a_bot_Y <= b_bot_Y <= a_top_Y) or
                        #bot right
                        ((b_left_X <= a_left_X and b_right_X >= a_right_X) and a_bot_Y <= b_top_Y <= a_top_Y) or
                        #whole top
                        ((b_left_X <= a_left_X and b_right_X >= a_right_X) and a_bot_Y <= b_bot_Y <= a_top_Y) or 
                        #whole bot
                        (a_left_X <= b_right_X <= a_right_X and (b_bot_Y <= a_bot_Y and b_top_Y >= a_top_Y)) or
                        #whole left
                        (a_left_X <= b_left_X <= a_right_X and (b_bot_Y <= a_bot_Y and b_top_Y >= a_top_Y)) or
                        #whole right
                        ((b_left_X >= a_left_X and b_right_X <= a_right_X) and a_bot_Y <= b_top_Y <= a_top_Y) or
                        #between top
                        ((b_left_X >= a_left_X and b_right_X <= a_right_X) and a_bot_Y <= b_bot_Y <= a_top_Y) or
                        #between bot
                        (a_left_X <= b_right_X <= a_right_X and (b_bot_Y >= a_bot_Y and b_top_Y <= a_top_Y)) or
                        #between left
                        (a_left_X <= b_left_X <= a_right_X and (b_bot_Y >= a_bot_Y and b_top_Y <= a_top_Y))
                        #between right
                        ):
                        if a.type > b.type:
                            b.bounceIt()
                        elif a.type < b.type:
                            a.bounceIt()
                        else:
                            a.bounceIt()
                            b.bounceIt()
                            
    def isDestroyed(self, a, ship, rocket):
        if a.health == 0 and a.type == 2:
            for i in range(0, 3):
                asteroid = Asteroid(self.scr)
                asteroid.makePiece(a)
                self.asteroids.append(asteroid)
            self.asteroids.remove(a)
            if a.special == True:
                ship.score += 10
                a.special_sound.play()
                ship.power_up = True
            else:
                ship.score += 2
        elif a.health == 0 and a.type == 3:
            for i in range(0, 5):
                asteroid = Asteroid(self.scr)
                asteroid.makePiece(a)
                self.asteroids.append(asteroid)
            self.asteroids.remove(a)
            if a.special == True:
                ship.score += 10
                a.special_sound.play()
                ship.power_up = True
            else:
                ship.score += 3
        elif a.health == 0:
            self.asteroids.remove(a)
            if a.special == True:
                ship.score += 10
                a.special_sound.play()
                ship.power_up = True
            else:
                ship.score += 1
            
        self.didWin(ship)
        
    def didWin(self, ship):
        if not self.asteroids:
            ship.win = True
            
    def didBulletHit(self, bullets, ship, rocket):
        for a in self.asteroids:
            for b in bullets:
                if ((a.x < b.x and a.x+a.width > b.x and a.y < b.y and a.y+a.height > b.y) or 
                    (a.x < b.x+b.width and a.x > b.x and a.y < b.y and a.y+a.height > b.y) or
                    (a.x < b.x+b.width and a.x > b.x and a.y < b.y+b.height and a.y > b.y) or
                    (a.x < b.x and a.x+a.width > b.x and a.y < b.y+b.height and a.y > b.y)):
                    bullets.remove(b)
                    a.health -= 1
                    self.isDestroyed(a, ship, rocket)
                    self.bullethit_sound.play()
                    
    def didRocketHit(self, rocket, ship):
        rocket.rocket_hit_bass.play()
        rocket.rocket_hit_sound.play()
        
        for a in self.asteroids:
            if ((a.x < rocket.x and a.x+a.width > rocket.x and a.y < rocket.y and a.y+a.height > rocket.y) or 
                (a.x < rocket.x+rocket.explosion_width and a.x > rocket.x and a.y < rocket.y and a.y+a.height > rocket.y) or
                (a.x < rocket.x+rocket.explosion_width and a.x > rocket.x and a.y < rocket.y+rocket.explosion_height and a.y > rocket.y) or
                (a.x < rocket.x and a.x+a.width > rocket.x and a.y < rocket.y+rocket.explosion_height and a.y > rocket.y)):
                a.health = 0
                self.isDestroyed(a, ship, rocket)
                if ship.power_up == True:
                    rocket.frame_index = 0
                    rocket.frame_time = 0
                
    def reset(self):
        self.asteroids.clear()