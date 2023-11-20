# -*- coding: utf-8 -*-
"""
Created on Thu Jul 27 18:17:34 2023

@author: patrick

Just found out I am teaching game class, so I need to practice.

"""

import pygame as p
import pandas as pd
from IPython.display import display
import random

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

moveInc = 5
moveIncforGhost = 3
df = pd.read_csv('PacMan/Map.csv').to_numpy()
intersectDf = pd.read_csv('PacMan/GhostMap.csv').to_numpy()
# display(df)
# display(intersectDf)
# print(intersectDf.shape)
# print(df.shape)
columns = df.shape[1]
rows = df.shape[0]
sprite_width = 50
sprite_height = 50

class tile():
    west = False
    east = False
    south = False
    north = False
    snack = False
    def setwall(self,type):
        if type == 1:
            self.north = True
            self.south = True

        if type == 2:
            self.west = True
            self.east = True

        if type == 3:
            self.north = True
            self.west = True
            self.snack = True

        if type == 4:
            self.north = True
            self.east = True
            self.snack = True

        if type == 5:
            self.east = True
            self.south = True
            self.snack = True

        if type == 6:
            self.west = True
            self.south = True
            self.snack = True

        if type == 7:
            self.north = True
            self.snack = True

        if type == 8:
            self.east = True
            self.snack = True

        if type == 9:
            self.south = True
            self.snack = True

        if type == 10:
            self.west = True
            self.snack = True
            
        if type == 11:
            self.east = True
            self.north = True
            self.south = True
        
        if type == 12:
            self.west = True
            self.north = True
            self.south = True

        if type == 13:
            self.north = True
            self.west = True

        if type == 14:
            self.north = True
            self.east = True

        if type == 15:
            self.east = True
            self.south = True

        if type == 16:
            self.west = True
            self.south = True
        
        if type == 17:
            self.north = True
        
        if type == 18:
            self.east = True
        
        if type == 19:
            self.south = True
        
        if type == 20:
            self.west = True
        
        if type > 20:
            self.snack = True
    
    def __init__(self,x,y,width,height,color,type,intersection):
        self.Rect = p.Rect(x,y,width,height)
        self.color = color

        self.westwall = p.Rect(self.Rect.topleft[0],self.Rect.topleft[1],width/10,height)
        self.eastwall = p.Rect(self.Rect.topright[0]-width/10,self.Rect.topright[1],width/10,height)
        self.northwall = p.Rect(self.Rect.topleft[0],self.Rect.topleft[1],width,height/10)
        self.southwall = p.Rect(self.Rect.bottomleft[0],self.Rect.bottomleft[1]-height/10,width,height/10)
        self.type = type
        self.setwall(type)
        if intersection == 1:
            self.intersection = True
        else:
            self.intersection = False

    def drawMe(self,screen,p):
        if self.west:
            p.draw.rect(screen,CYAN,self.westwall)
        if self.east:
            p.draw.rect(screen,CYAN,self.eastwall)
        if self.north:
            p.draw.rect(screen,CYAN,self.northwall)
        if self.south:
            p.draw.rect(screen,CYAN,self.southwall)

class map():
    grid = []
    openSpot = []
    point = 0

    def __init__(self,screenWidth,screenHeight,columns,rows,df):
        self.titleWidth = screenWidth/columns
        self.titleHeight = screenHeight/rows
        self.makeMap(columns,rows,df)
        
    def makeMap(self,columns,rows,df):
        for x in range(0,columns):
            row = []
            for y in range(0,rows):
                placeholderTitle = tile(50+self.titleWidth*x,50+self.titleHeight*y,self.titleWidth,self.titleHeight,WHITE,df[y][x],intersectDf[y][x])
                if placeholderTitle.snack:
                    self.openSpot.append([[x,y]])
                row.append(placeholderTitle)
                if (df[y][x] >2 and df[y][x] < 11) or df[y][x] > 20:
                    self.point +=1
            self.grid.append(row)
        #print(self.openSpot)

class Player(p.sprite.Sprite):
    canGoNorth = True
    canGoSouth = True
    canGoWest = True
    canGoEast = True

    dio = False
    dioDuration = 200
    dioTimer = 0

    dumbylist = []

    bullets = []

    health_points = 3
    health_spirtes = []
    dying = False
    playerMove = False

    useItem = True
    useItemCooldown = 10
    useItemCooldowntimer = 0

    invicible = False
    invicibleDuration = 150
    invicibletimer = 0

    killing = False
    killingDuration = 150
    killingtimer = 0



    def __init__(self, filename_base, pos_x, pos_y, nSprites, sprite_width, sprite_height):
        super().__init__()
        # Turn animate off.
        self.xtitle = int((pos_x - 50)/50)
        self.ytitle = int((pos_y - 50)/50)
        self.is_animating = False
        
        # Load sprites groups.
        # Right sprites.
        fileR = filename_base + "R.png"
        rightSprites = self.loadExtraSprites(fileR, nSprites, sprite_width, sprite_height)
        self.rightSprites = rightSprites
        self.sprites = rightSprites
        
        # Left Sprites.
        fileL = filename_base + "L.png"
        leftSprites = self.loadExtraSprites(fileL, nSprites, sprite_width, sprite_height)
        self.leftSprites = leftSprites
    
        # Up Sprites.
        fileU = filename_base + "U.png"
        upSprites = self.loadExtraSprites(fileU, nSprites, sprite_width, sprite_height)
        self.upSprites = upSprites
        
        # Down Sprites.
        fileU = filename_base + "D.png"
        downSprites = self.loadExtraSprites(fileU, nSprites, sprite_width, sprite_height)
        self.downSprites = downSprites

        fileDying = filename_base + "Dying.png"
        dyingSprites = self.loadExtraSprites(fileDying, 12, sprite_width, sprite_height)
        self.dyingSprites = dyingSprites

            
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.topleft = [pos_x, pos_y]
        for healthpointindex in range(self.health_points,0,-1):
            #fprint(healthpointindex)
            print(14-healthpointindex)
            self.health_spirtes.append(Health(sprite_width,sprite_width,sprite_height,[14-healthpointindex,11]))

        self.mode = 'r'
        
    def update(self, speed,map,inventory):
        if (self.is_animating == True):
            if self.mode != "dying":
                self.current_sprite += speed
                if (self.current_sprite >= len(self.sprites)):
                    self.current_sprite = 0
                #print(int(self.current_sprite))
                self.image = self.sprites[int(self.current_sprite)]
            else:
                if self.current_sprite < len(self.sprites)-1:
                    self.current_sprite += speed
                else:
                    print("the world")
                    self.mode = "r"
                    self.sprites = self.rightSprites
                    self.set_position(7 * sprite_width + 50 , 5 * sprite_height + 50)
                    self.dying = False
                    self.playerMove = False
                    self.current_sprite = 0
                self.image = self.sprites[int(self.current_sprite)]

        if(self.useItemCooldowntimer >= self.useItemCooldown and len(inventory) > 0):
            self.useItem = True
        else:
            self.useItem = False
            self.useItemCooldowntimer += speed
        
        if self.invicible:
            if self.invicibletimer < self.invicibleDuration:
                self.invicibletimer += 1
            else:
                self.invicibletimer = 0 
                self.invicible = False
        
        if self.killing:
            if self.killingtimer < self.killingDuration:
                self.killingtimer += 1
            else:
                self.killingtimer = 0 
                self.killing = False

        x = self.x -45
        y = self.y -45 
        self.xtitle = int(x/50)
        self.ytitle = int(y/50) 

        if self.xtitle > 14:
            self.xtitle = 0
            self.x = -5
        elif self.xtitle < 0:
            self.xtitle = 14
            self.x = 15*50 -5

        self.canGoWest = True
        self.canGoEast = True
        self.canGoNorth = True
        self.canGoSouth = True
        #print(self.xtitle,self.ytitle)
        if map.grid[self.xtitle][self.ytitle].west:
            self.canGoWest = False
        elif self.xtitle > 0:
            if map.grid[self.xtitle - 1][self.ytitle].east:
                self.canGoWest = False

        if map.grid[self.xtitle][self.ytitle].east:
            self.canGoEast = False
        elif self.xtitle < columns-1:
           # print(self.xtitle,columns-1)        
            if map.grid[self.xtitle + 1][self.ytitle].west:
                self.canGoEast = False

        if map.grid[self.xtitle][self.ytitle].north:
            self.canGoNorth = False
        elif self.ytitle > 0:
            if map.grid[self.xtitle][self.ytitle-1].south:
                self.canGoNorth = False

        if map.grid[self.xtitle][self.ytitle].south:
            self.canGoSouth = False
        elif self.xtitle <= columns-1:
            if map.grid[self.xtitle][self.ytitle+1].north:
                self.canGoSouth = False
        
        if p.Rect.collidepoint(self.rect,map.grid[self.xtitle][self.ytitle].Rect.center):
            if map.grid[self.xtitle][self.ytitle].snack:
                map.grid[self.xtitle][self.ytitle].snack = False
                map.point -= 1

    def canIGoThisWay(self,direction):
        if direction == "up":
            return self.canGoNorth
        if direction == "down":
            return self.canGoSouth
        if direction == "left":
            return self.canGoWest
        if direction == "right":
            return self.canGoEast
        
    def animate_me(self):
        self.is_animating = not(self.is_animating)
        
    def set_position(self, x0, y0):
        self.x = x0
        self.y = y0
        self.rect.topleft = [x0, y0]
        return
    
    def move_right(self):
        if (self.mode != 'r'):
            self.mode = 'r'
            self.sprites = self.rightSprites
        self.x = self.x + moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_left(self):
        if (self.mode != 'l'):
            self.mode = 'l'
            self.sprites = self.leftSprites
        self.x = self.x - moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_up(self):
        if (self.mode != 'u'):
            self.mode = 'u'
            self.sprites = self.upSprites
        
        self.y = self.y - moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_down(self):
        if (self.mode != 'd'):
            self.mode = 'd'
            self.sprites = self.downSprites
        self.y = self.y + moveInc
        self.rect.topleft = [self.x, self.y]
        return

    def move_dying(self):
        if (self.mode != "dying"):
            self.mode = "dying"
            self.sprites = self.dyingSprites
        return
    
    def get_sprite(self, sprite_index):
        return self.sprites[sprite_index]
    
    def add_sprite(self, mySprite):
        self.sprites.append(mySprite)
        return
    
    def loadExtraSprites(self, filename, nSprites, sprite_width, sprite_height):
        # Get the image from the file.
        spriteSheet = p.image.load(filename)
        
        # Load the sprites
        extra_sprites = []
        y = 0
        x = 0
        for j in range(nSprites):
            pixels = get_pixels_at(x, y, sprite_width, sprite_height, spriteSheet)
            extra_sprites.append(pixels)
            x = x + sprite_width
            
        return extra_sprites
    
    
    def getSprites(self, filename, nSprites, sprite_width, sprite_height):
        # Get the image from the file.
        spriteSheet = p.image.load(filename)
        
        # Load the sprites
        self.sprites = []
        y = 0
        x = 0
        for j in range(nSprites):
            pixels = get_pixels_at(x, y, sprite_width, sprite_height, spriteSheet)
            self.sprites.append(pixels)
            x = x + sprite_width
            
        return
    
    def saveSprites(self, fileName, spriteWidth, spriteHeight):
        # Make a surface to hold the game layer image.
        spriteSufaceWidth = spriteWidth * len(self.sprites)
        spriteSurfaceHeight = spriteHeight
        mySpriteSurface = p.Surface((spriteSufaceWidth, spriteSurfaceHeight))
        
        # Blit the sprites to the surface.
        x = 0
        y = 0
        for sprite in self.sprites:
            mySprite = p.transform.scale(sprite, [spriteWidth, spriteHeight])
            mySpriteSurface.blit(mySprite, [x, y])
            x = x + spriteWidth
            
        # Save the surface as .png
        p.image.save(mySpriteSurface, fileName)
        return
    
    def collideWithGhost(self,ghost):
        if(p.Rect.colliderect(self.rect,ghost.rect) and self.mode != "dying" and self.invicible is False):
            if len(self.health_spirtes)>1:
                print("dying")
                self.health_spirtes.pop()
                self.move_dying()
                self.mode = "dying"
                self.dying = True
                return False
            else:
                print("game over")
                return True
    
    def killingTime(self,ghost):
        if(p.Rect.colliderect(self.rect,ghost.rect) and self.killing):
            return True
            
    def specialMove(self,name,Spots,ghosts):

        if name == "apple":
            self.dio = True
            
        if name == "cherry":
            if len(self.health_spirtes) < 4:
                self.health_spirtes.append(Health(sprite_width,sprite_width,sprite_height,[11+len(self.health_spirtes),11]))

        if name == "key":
            self.invicible = True

        if name == "greenFruit":

            spot = random.choice(Spots)
            self.mode = "r"
            self.sprites = self.rightSprites
            print(spot)
            self.set_position(spot[0][0] * sprite_width + 50 , spot[0][1] * sprite_height +50 )
            self.dying = False
            self.playerMove = False
            self.current_sprite = 0

        if name == "orange":
            self.dumbylist.append(Health(sprite_width,sprite_width,sprite_height,[self.xtitle,self.ytitle]))
        
        if name == "ship":
            self.fire()
        
        if name == "strawberry":
            self.killing = True
        
        if name == "yellowstuff":
            for ghost in ghosts:
                ghost.setscared(True)

    def fire(self):
        print(self.rect.centerx,self.rect.centery)
        self.bullets.append(bullet(self.rect.centerx,self.rect.centery,10,10,WHITE,10,self.mode))
    
class bullet():
    IsExisting = True
  
    def __init__(self,x,y,width,height,color,speed,direction):

        self.hitbox = p.Rect(x,y,width,height)
        self.color = color
        self.baseSpeed = speed
        self.IsExisting = True
        self.direction = direction
    
    def collide(self,ghost):
        print(1)
        if p.Rect.collidepoint(ghost.rect,self.hitbox.center):
            ghost.stun = True
            return True 
        if self.hitbox.centerx > 15*50:
            return True
        if self.hitbox.centerx < 0:
            return True
        if self.hitbox.centery > 12*50:
            return True
        if self.hitbox.centery < 0:
            return True
        
    def move(self):
        if self.direction == "r":
            self.hitbox.centerx += self.baseSpeed

        if self.direction == "l":
            self.hitbox.centerx -= self.baseSpeed

        if self.direction == "u":
            self.hitbox.centery -= self.baseSpeed

        if self.direction == "d":
            self.hitbox.centery += self.baseSpeed


def get_pixels_at(x, y, width, height, image0):
    rect = p.Rect(x, y, width, height)
    pixels = p.Surface((width, height))
    pixels.blit(image0, (0, 0), rect)
    pixels.set_colorkey(BLACK)

    return pixels.convert_alpha()

class Enemy(p.sprite.Sprite):
    canGoNorth = False
    canGoSouth = False
    canGoWest = False
    canGoEast = False
    directionsChoice = ["up","down","left","right"]
    stun = False
    scared = False

    stunduration = 150
    stuntimer = 0

    scaredduration = 150 
    scaredtimer = 0

    def __init__(self, filename_base, pos_x, pos_y, nSprites, sprite_width, sprite_height,map):
        super().__init__()
        # Turn animate off.
        self.xtitle = int((pos_x - 50)/50)
        self.ytitle = int((pos_y - 50)/50)
        self.is_animating = False
        self.changing = False

        self.name = filename_base
        
        # Load sprites groups.
        # Right sprites.
        fileR = filename_base + "R.png"
        rightSprites = self.loadExtraSprites(fileR, nSprites, sprite_width, sprite_height)
        self.rightSprites = rightSprites
        self.sprites = rightSprites
        
        # Left Sprites.
        fileL = filename_base + "L.png"
        leftSprites = self.loadExtraSprites(fileL, nSprites, sprite_width, sprite_height)
        self.leftSprites = leftSprites
    
        # Up Sprites.
        fileU = filename_base + "U.png"
        upSprites = self.loadExtraSprites(fileU, nSprites, sprite_width, sprite_height)
        self.upSprites = upSprites
        
        # Down Sprites.
        fileU = filename_base + "D.png"
        downSprites = self.loadExtraSprites(fileU, nSprites, sprite_width, sprite_height)
        self.downSprites = downSprites
        
        fileScary = filename_base + "Scared.png"
        scarySprites = self.loadExtraSprites(fileScary, 2, sprite_width, sprite_height)
        self.scarySprites = scarySprites
            
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.topleft = [pos_x, pos_y]
        
        self.mode = 'r'
        self.direction = random.choice(self.myOption(map))
        
    def update(self, speed,map):
        self.whereCanIGo(map)
        if (self.is_animating == True):
            if self.scared:
                self.sprites = self.scarySprites
            self.current_sprite += speed
            if (self.current_sprite >= len(self.sprites)):
                self.current_sprite = 0
            self.image = self.sprites[int(self.current_sprite)]
        
        if self.stun:
            if self.stuntimer < self.stunduration:
                self.stuntimer += 1
            else:
                self.stuntimer = 0 
                self.stun = False
        
        if self.scared:
            if self.scaredtimer < self.scaredduration:
                self.scaredtimer += 1
            else:
                print(self.scared)
                self.scaredtimer = 0 
                self.scared = False
        

        #print(self.canGoWest,self.canGoNorth,self.canGoEast,self.canGoSouth)

    def whereCanIGo(self,map):
        x = self.x -45
        y = self.y -45 
        self.xtitle = int(x/50)
        self.ytitle = int(y/50) 

        if self.xtitle > 14:
            self.xtitle = 0
            self.x = -5
        elif self.xtitle < 0:
            self.xtitle = 14
            self.x = 15*50 -5

        self.canGoWest = True
        self.canGoEast = True
        self.canGoNorth = True
        self.canGoSouth = True

        if map.grid[self.xtitle][self.ytitle].west:
            self.canGoWest = False
        elif self.xtitle > 0:
            if map.grid[self.xtitle - 1][self.ytitle].east:
                self.canGoWest = False

        if map.grid[self.xtitle][self.ytitle].east:
            self.canGoEast = False
        elif self.xtitle < columns-1:
           # print(self.xtitle,columns-1)        
            if map.grid[self.xtitle + 1][self.ytitle].west:
                self.canGoEast = False

        if map.grid[self.xtitle][self.ytitle].north:
            self.canGoNorth = False
        elif self.ytitle > 0:
            if map.grid[self.xtitle][self.ytitle-1].south:
                self.canGoNorth = False

        if map.grid[self.xtitle][self.ytitle].south:
            self.canGoSouth = False
        elif self.xtitle <= columns-1:
            if map.grid[self.xtitle][self.ytitle+1].north:
                self.canGoSouth = False

    def canIGoThisWay(self,direction,map):
        if direction == "up":
            return self.canGoNorth
        if direction == "down":
            return self.canGoSouth
        if direction == "left":
            return self.canGoWest
        if direction == "right":
            return self.canGoEast
        
    def myOption(self,map):
        self.whereCanIGo(map)
        options = []
        
        if self.canGoNorth:
            options.append("up")
        if self.canGoEast:
            options.append("right")
        if self.canGoSouth:
            options.append("down")
        if self.canGoWest:
            options.append("left")
        
        return options

    def myOptionScared(self,map,pacMan):
        self.whereCanIGo(map)
        options = []
        above = False
        below = False
        left = False
        right = False
        if pacMan.rect.centerx - self.rect.centerx > 0:
            right = True
        else:
            left = True
        
        if pacMan.rect.centery - self.rect.centery > 0:
            below = True
        else:
            above = True
        
        if self.canGoNorth:
            if above is False:
                options.append("up")
        if self.canGoEast:
            if right is False:
                options.append("right")
        if self.canGoSouth:
            if below is False:
                options.append("down")
        if self.canGoWest:
            if left is False:
                options.append("left")
        
        return options

    def animate_me(self):
        self.is_animating = not(self.is_animating)
        
    def set_position(self, x0, y0):
        self.x = x0
        self.y = y0
        self.rect.topleft = [x0, y0]
        return
    
    def move_right(self):
        if (self.mode != 'r'):
            self.mode = 'r'
            self.sprites = self.rightSprites
    
        self.x = self.x + moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_left(self):
        if (self.mode != 'l'):
            self.mode = 'l'
            self.sprites = self.leftSprites
        
        self.x = self.x - moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_up(self):
        if (self.mode != 'u'):
            self.mode = 'u'
            self.sprites = self.upSprites
       
        self.y = self.y - moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_down(self):
        if (self.mode != 'd'):
            self.mode = 'd'
            self.sprites = self.downSprites
        
        self.y = self.y + moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_rights(self):
        if (self.mode != 'r'):
            self.mode = 'r'
        self.sprites = self.scarySprites
        print(len(self.scarySprites))
        self.x = self.x + moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_lefts(self):
        if (self.mode != 'l'):
            self.mode = 'l'
        print(len(self.scarySprites))
        self.sprites = self.scarySprites
        self.x = self.x - moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_ups(self):
        if (self.mode != 'u'):
            self.mode = 'u'
        print(len(self.scarySprites))
        self.sprites = self.scarySprites
        self.y = self.y - moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def move_downs(self):
        if (self.mode != 'd'):
            self.mode = 'd'
        print(len(self.scarySprites))
        self.sprites = self.scarySprites
        self.y = self.y + moveInc
        self.rect.topleft = [self.x, self.y]
        return
    
    def get_sprite(self, sprite_index):
        return self.sprites[sprite_index]
    
    def add_sprite(self, mySprite):
        self.sprites.append(mySprite)
        return
    
    def loadExtraSprites(self, filename, nSprites, sprite_width, sprite_height):
        # Get the image from the file.
        spriteSheet = p.image.load(filename)
        
        # Load the sprites
        extra_sprites = []
        y = 0
        x = 0
        for j in range(nSprites):
            pixels = get_pixels_at(x, y, sprite_width, sprite_height, spriteSheet)
            extra_sprites.append(pixels)
            x = x + sprite_width
            
        return extra_sprites
    
    def setscared(self,sacry):
        self.scared = sacry

class Item(p.sprite.Sprite):
    
    itemchoices = ["apple","cherry","key","greenFruit","orange","ship","strawberry","yellowstuff"]
    #itemchoices = ["yellowstuff"]

    def __init__(self, title_width, nSprites, sprite_width, sprite_height,spots):
        super().__init__()
        spot = random.choice(spots)
        pos_x = spot[0][0] * title_width + 50 
        pos_y = spot[0][1] * title_width + 50
        # Turn animate off.
        self.xtitle = int((pos_x - 50)/50)
        self.ytitle = int((pos_y - 50)/50)
        self.is_animating = False
        self.changing = False
        
        # Load sprites groups.
        # Right sprites.
        self.name = random.choice(self.itemchoices)
        file = "PacMan/" + self.name + ".png"
        fruitSprites = self.loadExtraSprites(file, nSprites, sprite_width, sprite_height)
        self.sprites = fruitSprites
            
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.topleft = [pos_x, pos_y]
        
        self.appear = True

    def update(self, speed,map):
        if (self.is_animating == True):
            self.current_sprite += speed
            if (self.current_sprite >= len(self.sprites)):
                self.current_sprite = 0
                self.appear = False
            else:
                self.appear = True
                
            self.image = self.sprites[int(self.current_sprite)]

    def checkCollidingly(self,otherRect):
        if p.Rect.colliderect(self.rect,otherRect):
            return True
        
    def inventoryLocation(self,index):
        self.rect.topleft = [(index+1)*50,12*50]

    def loadExtraSprites(self, filename, nSprites, sprite_width, sprite_height):
        # Get the image from the file.
        spriteSheet = p.image.load(filename)
        
        # Load the sprites
        extra_sprites = []
        y = 0
        x = 0
        for j in range(nSprites):
            pixels = get_pixels_at(x, y, sprite_width, sprite_height, spriteSheet)
            extra_sprites.append(pixels)
            x = x + sprite_width
            
        return extra_sprites
    
class Health(p.sprite.Sprite):

    def __init__(self, title_width,sprite_width, sprite_height,spots):
        super().__init__()
        pos_x = spots[0] * title_width + 50 
        pos_y = spots[1] * title_width + 50
        # Turn animate off.
        self.xtitle = int((pos_x - 50)/50)
        self.ytitle = int((pos_y - 50)/50)
        self.is_animating = False
        #print(spots)
        # Load sprites groups.
        # Right sprites.
        filehealthModels = "PacMan/healthPoints.png"
        healthSprites = self.loadExtraSprites(filehealthModels, 1, sprite_width, sprite_height)
        self.healthSprites = healthSprites
        self.sprites = self.healthSprites
            
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.x = pos_x
        self.y = pos_y
        self.rect.topleft = [pos_x, pos_y]
        
        self.appear = True

    def disappear(self):
        self.appear = False

    def loadExtraSprites(self, filename, nSprites, sprite_width, sprite_height):
        # Get the image from the file.
        spriteSheet = p.image.load(filename)
        
        # Load the sprites
        extra_sprites = []
        y = 0
        x = 0
        for j in range(nSprites):
            pixels = get_pixels_at(x, y, sprite_width, sprite_height, spriteSheet)
            extra_sprites.append(pixels)
            x = x + sprite_width
            
        return extra_sprites
    
    def collideGhost(self,ghost):
        if(p.Rect.colliderect(self.rect,ghost.rect)):
            print(1)
            ghost.stun = True 
            return True
    
def pyGameTemplate():
    
    p.init()
    
    dim = p.display.get_desktop_sizes()
    screenWidth = 750
    screenHeight = 550

    GAME_FONT = p.font.SysFont('Comic Sans MS', 40)
    size = (screenWidth+100, screenHeight+100)
    screen = p.display.set_mode(size)
    
    testMap = map(screenWidth,screenHeight,columns,rows,df)

    pacMan = Player("PacMan/pacMan", 7 * sprite_width + 50 , 5 * sprite_height + 50 , 3, sprite_width, sprite_height)
    cyanGhost = Enemy("PacMan/cyanGhost", 0 * sprite_width + 50 , 0 * sprite_height + 50 , 2, sprite_width,sprite_height,testMap)
    orangeGhost = Enemy("PacMan/orangeGhost", 14 * sprite_width + 50 , 0 * sprite_height + 50 , 2, sprite_width,sprite_height,testMap)
    redGhost = Enemy("PacMan/redGhost", 0 * sprite_width + 50 , 10 * sprite_height + 50 , 2, sprite_width,sprite_height,testMap)
    pinkGhost = Enemy("PacMan/pinkGhost", 14 * sprite_width + 50 , 10 * sprite_height + 50 , 2, sprite_width,sprite_height,testMap)
    #ghosts = [cyanGhost,orangeGhost,redGhost,pinkGhost]
    ghosts = [cyanGhost,orangeGhost,redGhost]


    Spawnrate = 300
    Spawnratetimer = 0
    SpawnrateIncreaser = 1

    item1 = Item(sprite_width, 1, sprite_width,sprite_height,testMap.openSpot) 
    items = [item1]


    inventory = []

    #ghosts = [cyanGhost]
    cyanGhost.animate_me()
    pacMan.animate_me()
    # Set the width and height of the screen [width, height]
     
    p.display.set_caption("basic Python graphics window()")
     
    # Loop until the user clicks the close button.
    running = True 
    direction = None 
    count = 0
    changing = True
    # Used to manage how fast the screen updates
    clock = p.time.Clock()
     
    # -------- Main Program Loop -----------
    while running:
        # --- Main event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        previousDirection = direction
        """ Check for keyboard presses. """
        key = p.key.get_pressed()
        if (key[p.K_ESCAPE] == True): 
            running = False
        if ((count % 50) == 0) and pacMan.dying is False:
            if (key[p.K_UP] == True): 
                direction = "up"
                pacMan.playerMove = True
            if (key[p.K_DOWN] == True): 
                direction = "down"
                pacMan.playerMove = True
            if (key[p.K_LEFT] == True):
                direction = "left"
                pacMan.playerMove = True
            if (key[p.K_RIGHT] == True):
                direction = "right"
                pacMan.playerMove = True
        
        if (key[p.K_SPACE] == True):
            if pacMan.useItem:
                itemName = inventory.pop().name 
                print(itemName)
                pacMan.specialMove(itemName,testMap.openSpot,ghosts)
                pacMan.useItem = False
                pacMan.useItemCooldowntimer = 0
        
        if ((count % 50) == 0):
            if pacMan.dying:
                pacMan.dying = True
            else:
                changing = pacMan.canIGoThisWay(direction)
        
        if changing and pacMan.dying is False and pacMan.playerMove:
            if (direction == "up"):
                pacMan.move_up()
            elif (direction == "down"):
                pacMan.move_down()
            elif (direction == "right"):
                pacMan.move_right()
            elif (direction == "left"):
                pacMan.move_left()
        else:
            direction = previousDirection
            
        # --- Game logic should go here
        if ((count % 50) == 0):
            for index,ghost in enumerate(ghosts):
                if pacMan.killing:
                    if(pacMan.killingTime(ghost)):
                        ghosts.pop(index)

            if(pacMan.dio is False):
                pausing = True
            else:
                pausing = False

            for ghost in ghosts:
                dead = pacMan.collideWithGhost(ghost)

                for index,dumby in enumerate(pacMan.dumbylist):
                    if dumby.collideGhost(ghost):
                        pacMan.dumbylist.pop(index)

                for index,bullet in enumerate(pacMan.bullets):
                    if bullet.collide(ghost):
                        pacMan.bullets.pop(index)
                
                if dead:
                    running = False
                
                if testMap.grid[ghost.xtitle][ghost.ytitle].intersection:
                    if ghost.scared is False:
                        possibleChoice = random.choice(ghost.myOption(testMap))
                    else:
                        choices = ghost.myOptionScared(testMap,pacMan)
                        if len(choices) > 0:
                            possibleChoice = random.choice(choices)
                        else:
                            ghost.direction = None
                    if ghost.canIGoThisWay(possibleChoice,testMap):
                        ghost.direction = possibleChoice
        
        

        if(pausing):
            for ghost in ghosts:
                    if ghost.stun is False:
                        if ghost.scared is False:
                            if (ghost.direction == "up"):
                                ghost.move_up()
                            elif (ghost.direction == "down"):
                                ghost.move_down()
                            elif (ghost.direction == "right"):
                                ghost.move_right()
                            elif (ghost.direction == "left"):
                                ghost.move_left()
                        else:
                            if (ghost.direction == "up"):
                                ghost.move_ups()
                            elif (ghost.direction == "down"):
                                ghost.move_downs()
                            elif (ghost.direction == "right"):
                                ghost.move_rights()
                            elif (ghost.direction == "left"):
                                ghost.move_lefts()  

        if pacMan.dio:
            if pacMan.dioTimer < pacMan.dioDuration:
                pacMan.dioTimer += 1
            else:
                pacMan.dio = False
        
        
        for item in items:
            if item.checkCollidingly(pacMan.rect):
                inventory.append(items.pop())
                for index,item in enumerate(inventory):
                    item.inventoryLocation(index)
        
        for bullet in pacMan.bullets:
            bullet.move()
        
        if len(items) == 0 and len(inventory) <= 5:
            if Spawnratetimer > Spawnrate:
                items.append(Item(sprite_width, 1, sprite_width,sprite_height,testMap.openSpot))
                Spawnratetimer = 0
            else:
                Spawnratetimer += SpawnrateIncreaser


        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
     
        # --- Drawing code should go here
        #p.draw.circle(screen, ORANGE, [350, 250], 50, 10)
        for x in range(0,columns):
            for y in range(0,rows):
                #p.draw.rect(screen,testMap.grid[x][y].color,testMap.grid[x][y].Rect)
                testMap.grid[x][y].drawMe(screen,p)
                if testMap.grid[x][y].snack:
                    p.draw.circle(screen, WHITE, testMap.grid[x][y].Rect.center, 5, 5)
        
        screen.blit(pacMan.image,pacMan.rect)

        for ghost in ghosts:
            screen.blit(ghost.image,ghost.rect)

        for item in items:
            screen.blit(item.image,item.rect)

        for powerup in inventory:
            screen.blit(powerup.image,powerup.rect)
        
        for healthsprite in pacMan.health_spirtes:
            screen.blit(healthsprite.image,healthsprite.rect)

        for dumby in pacMan.dumbylist:
            screen.blit(dumby.image,dumby.rect)

        for bullet in pacMan.bullets:
            p.draw.circle(screen,bullet.color,[bullet.hitbox.centerx,bullet.hitbox.centery],bullet.hitbox.width)

        pacMan.update(.10,testMap,inventory)

        for ghost in ghosts:
            ghost.update(.05,testMap)

        if testMap.point == 0:
            running = False
        
        Power_text = f"Item UP:{pacMan.useItem}"
        Power_surface = GAME_FONT.render(Power_text,False,RED)
        screen.blit(Power_surface, (50, 0))

        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)

        count = count + moveInc
     
    # Close the window and quit.
    p.quit()
    
    return

pyGameTemplate()