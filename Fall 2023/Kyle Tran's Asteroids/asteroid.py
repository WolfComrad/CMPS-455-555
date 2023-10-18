import pygame as p
import math 
import random
import copy

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
colorPalette = [WHITE, GREEN, RED, ORANGE, YELLOW, CYAN, MAGENTA]
asteroidImageChoice = ["asteroid/Asteroids_02/Asteroids_64x64_001.png","asteroid/Asteroids_02/Asteroids_64x64_002.png","asteroid/Asteroids_02/Asteroids_64x64_003.png","asteroid/Asteroids_02/Asteroids_64x64_004.png",
                       "asteroid/Asteroids_02/Asteroids_64x64_005.png","asteroid/Asteroids_02/Asteroids_64x64_006.png","asteroid/Asteroids_02/Asteroids_64x64_007.png","asteroid/Asteroids_02/Asteroids_64x64_008.png",]

screenWidth = 2200
screenHeight = 1200
maxRockScaleFactor = 40

#Utility functions



def deg2Rad(degrees):

    rad = (math.pi/180.0) * degrees
    return rad

def rad2Deg(radian):

    deg = (180/math.pi) * radian
    return deg

class projectitle:

    IsExisting = True
  
    def __init__(self,x,y,width,height,color,angle,speed):

        self.hitbox = p.Rect(x,y,width,height)
        self.color = color
        self.baseSpeed = speed
        self.speedX = self.baseSpeed * math.cos(deg2Rad(angle +90 ))
        self.speedY = self.baseSpeed * -1 * math.sin(deg2Rad(angle+ 90))
        self.IsExisting = True
    
    def collide(self,object):

            if self.IsExisting is True :
                if object.rect.centerx < self.hitbox.x and object.rect.centerx + object.rect.centerwidth > self.hitbox.x:
                    if object.rect.centery < self.hitbox.y and object.rect.centery + object.rect.centerheight >self.hitbox.y:
                        self.IsExisting = False
                        return True
                    
    def moveP(self,size):

        if self.hitbox.centerx > size[0] + 50 or self.hitbox.centerx < -50 or self.hitbox.centery > size[1] + 50 or self.hitbox.centery < -50:
            self.IsExisting = False
        self.hitbox.centerx = self.hitbox.centerx + self.speedX
        self.hitbox.centery = self.hitbox.centery + self.speedY
    
    def collisionWithRock(self,asteriods,ship):

        for asteriod in asteriods:
            if self.hitbox.centerx >= asteriod.rect.left - self.hitbox.width and self.hitbox.centerx <= asteriod.rect.right + self.hitbox.width:
                if self.hitbox.centery <= asteriod.rect.bottom and self.hitbox.centery >= asteriod.rect.top:
                    asteriod.IsExisting = False
                    self.IsExisting = False
                    wackeffect(asteriod.type,ship)
                    return True              

def wackeffect(asteriodId,ship):
    print(asteriodId)
    if asteriodId == 0:
        ship.score +=2
    if asteriodId == 1:
        ship.lives += 1
    if asteriodId == 2:
        if(ship.ammo < ship.ammo_size):
            ship.ammo += 1
    if asteriodId == 3:
        ship.gold += 1
    if asteriodId == 4:
        if(ship.ammo < ship.ammo_size):
            ship.ammo += 1
    if asteriodId == 5:
        ship.shield_duration += 30
    if asteriodId == 6:
        if(ship.ammo < ship.ammo_size):
            ship.ammo += 1
    if asteriodId == 7:
        ship.score -= 2

    

class spaceShip(p.sprite.Sprite):

    speed = 15
    angle = 0
    bullets = []
    fireRate = 0
    blinkdistance = 175
    blinkduration = 0
    startblinking = False
    blinking = False
    blinkcooldown = 10
    lives = 3
    shield_duration = 100
    shield_turn = False
    score = 0
    winningScore = 30
    gold = 0
    ammo = 20
    ammo_size = 20

    def __init__(self,x,y):

        super().__init__()
        self.image = p.image.load("asteroid/spaceship_small_red.png")
        self.grayimage = p.image.load("asteroid/graySpaceShip.png")
        self.size = self.image.get_size()
        self.graysize = self.grayimage.get_size()
        # create a 2x bigger image than self.image
        self.image = p.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        self.grayimage = p.transform.scale(self.grayimage, (int(self.size[0]*2), int(self.size[1]*2)))
        self.rotatedImage = p.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = [x,y]
        self.rotatedRect = self.rotatedImage.get_rect()
        self.rotatedRect.center = self.rect.center
        self.head = [self.rect.centerx + self.rect.width/2 * math.cos(deg2Rad(self.angle +90 )) ,self.rect.centery + self.rect.height/2 * -1 * math.sin(deg2Rad(self.angle+ 90)) ]
        self.shieldImage = p.image.load("asteroid\shield.png")
        self.shieldSize= self.shieldImage.get_size()
        self.shieldImage = p.transform.scale(self.shieldImage, (int(self.shieldSize[0]/2), int(self.shieldSize[1]/2)))
        self.shieldRect = self.shieldImage.get_rect()
        self.shieldRect.center = [x,y]
    
    def move(self):

        self.rect.centerx = self.rect.centerx + self.speed * math.cos(deg2Rad(self.angle +90 ))
        self.rect.centery = self.rect.centery + self.speed * -1 * math.sin(deg2Rad(self.angle+ 90))
        self.rotatedRect.centerx = self.rect.centerx 
        self.rotatedRect.centery = self.rect.centery 
        self.shieldRect.centerx = self.rect.centerx
        self.shieldRect.centery = self.rect.centery
        if self.blinking and self.startblinking:
            self.rect.centerx = self.rect.centerx + self.blinkdistance * math.cos(deg2Rad(self.angle +90 ))
            self.rect.centery = self.rect.centery + self.blinkdistance * -1 * math.sin(deg2Rad(self.angle+ 90))
            self.rotatedRect.centerx = self.rect.centerx 
            self.rotatedRect.centery = self.rect.centery 
            self.startblinking = False

    
    def rotate(self,rotation):

        self.angle = self.angle + rotation * 5
        self.rotatedImage = p.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedImage.get_rect()
        self.rotatedRect.center = self.rect.center
        self.head = [self.rect.centerx + self.rect.width/2 * math.cos(deg2Rad(self.angle +90 )) ,self.rect.centery + self.rect.height/2 * -1 * math.sin(deg2Rad(self.angle+ 90)) ]
        #self.rect.center = center
    
    def fire(self):
        self.ammo -= 1

        bullet = projectitle(self.head[0],self.head[1],10,10,WHITE,self.angle,20)
        self.bullets.append(bullet)
        self.fireRate = 5

    def blink(self):

        self.blinkduration = 50
        self.startblinking = True
        self.rotatedGrayImage = p.transform.rotate(self.grayimage, self.angle)
        self.grayRotatedRect = self.rotatedGrayImage.get_rect()
        self.grayRotatedRect.center = self.rect.center
        self.blinklocation = copy.deepcopy(self.rect)
        self.blinklocation.width = self.blinklocation.width/2
        self.blinklocation.height = self.blinklocation.height/2
        self.blinkcooldown = 10

    def blocking(self,EnemyShips):
        if self.shield_duration > 0 and self.shield_turn:
            for EnemyShip in EnemyShips:
                for bullet in EnemyShip.bullets:
                    if bullet.hitbox.centerx > self.shieldRect.left - self.shieldRect.width/4 and bullet.hitbox.centerx < self.shieldRect.right + self.shieldRect.width/4 and bullet.hitbox.centery > self.shieldRect.top - self.shieldRect.height/4 and bullet.hitbox.centery < self.shieldRect.bottom + self.shieldRect.height/4:
                        bullet.IsExisting = False

    def gethit(self,enemyShips,asteriods):
        for enemyShip in enemyShips:
            for bullet in enemyShip.bullets:
                if bullet.hitbox.centerx > self.rect.left and bullet.hitbox.centerx < self.rect.right and bullet.hitbox.centery > self.rect.top and bullet.hitbox.centery < self.rect.bottom:
                    bullet.IsExisting = False
                    self.lives -= 1
        for asteroid in asteriods:
            if asteroid.rect.centerx > self.rect.left and asteroid.rect.centerx < self.rect.right and asteroid.rect.centery > self.rect.top and asteroid.rect.centery < self.rect.bottom:  
                asteroid.IsExisting = False
                self.lives -= 1
            
def spawnPoint(size):

    spawnChoice = random.randint(1,4)
    if spawnChoice == 1:
        return [0,random.randint(50,size[1]-50)]
    if spawnChoice == 2:
        return [size[0],random.randint(50,size[1]-50)]
    if spawnChoice == 3:
        return [random.randint(50,size[0]-50),0]
    if spawnChoice == 4:
        return [random.randint(50,size[0]-50),size[1]]

def spawnAngle(spawnPoint,size):

    if spawnPoint[0] >= 0 and spawnPoint[0] <= size[0]/2 and spawnPoint[1] >= 0 and spawnPoint[1] <= size[1]/2:
        return random.randint(290,340)
    if spawnPoint[0] >= size[0]/2 and spawnPoint[0] <= size[0] and spawnPoint[1] >= 0 and spawnPoint[1] <= size[1]/2:
        return random.randint(200,250)
    if spawnPoint[0] >= 0 and spawnPoint[0] <= size[0]/2 and spawnPoint[1] >= size[1]/2 and spawnPoint[1] <= size[1]:
        return random.randint(20,70)
    if spawnPoint[0] >= size[0]/2 and spawnPoint[0] <= size[0] and spawnPoint[1] >= size[1]/2 and spawnPoint[1] <= size[1]:
        return random.randint(110,160)

class asteroid(p.sprite.Sprite):

    speed = 10
    orientation = random.randint(1,4)

    def __init__(self,size):

        super().__init__()
        self.IsExisting = True
        self.type = random.randint(0,len(asteroidImageChoice)-1)
        self.image = p.image.load(asteroidImageChoice[self.type])
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.image = p.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1])*2))
        self.rect = self.image.get_rect()
        self.rect.center = spawnPoint(size)
        self.angle = spawnAngle(self.rect.center,size)
        self.speedX = self.speed * math.cos(math.radians(self.angle))
        self.speedY = self.speed * -1 * math.sin(math.radians(self.angle))
    
    def move(self,size):

        self.rect.centerx = self.rect.centerx + self.speedX
        self.rect.centery = self.rect.centery + self.speedY
        if self.rect.centerx > size[0] + self.size[0]  or self.rect.centerx < 0 - size[0]:
            self.IsExisting = False
        if self.rect.centery > size[1] + self.size[1] or self.rect.centery < 0 - size[1]:
            self.IsExisting = False


choicesX = [1,2,3,4,6,7,8,9]
choicesY = [1,2,3,4,6,7,8,9]
def spawnPointBlackHole(size):

    randomX = random.choice(choicesX)
    randomY = random.choice(choicesY)

    if random.randint(0,1) == 1:
        choicesX.remove(randomX)
    else:
        choicesY.remove(randomY) 

    return [size[0]/10 * randomX,size[1]/10 * randomY]

class blackHole(p.sprite.Sprite):

    gravity = 10
    lengthOfDeath = 20
    def __init__(self,size):

        super().__init__()
        self.IsExisting = True
        self.image = p.image.load("asteroid/blackhole.png")
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.image = p.transform.scale(self.image, (int(self.size[0]/5), int(self.size[1]/5)))
        self.rect = self.image.get_rect()
        self.rect.center = spawnPointBlackHole(size)
    
    def pullingIn(self,listofAsteriods):

        for asteriod in listofAsteriods:
            if asteriod.rect.centery > self.rect.top and asteriod.rect.centery < self.rect.bottom and asteriod.rect.centerx > self.rect.left and asteriod.rect.centerx < self.rect.right:
                if self.rect.centerx - asteriod.rect.centerx > 0:
                    asteriod.rect.centerx += self.gravity
                else: 
                    asteriod.rect.centerx -= self.gravity
                
                if self.rect.centery - asteriod.rect.centery > 0:
                    asteriod.rect.centery += self.gravity
                else: 
                    asteriod.rect.centery -= self.gravity

    def crushing(self,listofAsteriods):

        for asteriod in listofAsteriods:
            if asteriod.rect.centery > self.rect.centery - self.lengthOfDeath and asteriod.rect.centery < self.rect.centery + self.lengthOfDeath and asteriod.rect.centerx > self.rect.centerx - self.lengthOfDeath and asteriod.rect.centerx < self.rect.centerx + self.lengthOfDeath:
                asteriod.IsExisting= False

class enemyShip(p.sprite.Sprite):

    speed = 10
    angle = 90
    bullets = []
    fireRate = 0

    def __init__(self,size):

        super().__init__()
        self.IsExisting = True
        self.image = p.image.load("asteroid\spaceship_small_blue.png")
        self.size = self.image.get_size()
        # create a 2x bigger image than self.image
        self.image = p.transform.scale(self.image, (int(self.size[0]*2), int(self.size[1]*2)))
        self.rect = self.image.get_rect()
        self.rect.center = spawnPointEnemyShip(size)
        self.angle = spawnAngleEnemyShip(self.rect.center,size)
        self.image = p.transform.rotate(self.image, self.angle - 90)
        self.speedX = self.speed * math.cos(math.radians(self.angle))
        self.speedY = self.speed * -1 * math.sin(math.radians(self.angle))

    
    def move(self,size):

        self.rect.centerx = self.rect.centerx + self.speedX
        self.rect.centery = self.rect.centery + self.speedY
        if self.rect.centerx > size[0]  or self.rect.centerx < 0:
            self.IsExisting = False
        if self.rect.centery > size[1]  or self.rect.centery < 0:
            self.IsExisting = False

    def fire(self,userShip):

        if self.fireRate == 0:
            firingAngle = rad2Deg(math.atan((self.rect.centerx-userShip.rect.centerx)/(self.rect.centery-userShip.rect.centery)))
            if self.rect.centery-userShip.rect.centery < 0:
                firingAngle = 180 + firingAngle
            bullet = projectitle(self.rect.centerx,self.rect.centery,10,10,RED,firingAngle,10)
            self.bullets.append(bullet)
            self.fireRate = 30


def spawnPointEnemyShip(size):

    spawnChoice = random.randint(1,4)
    if spawnChoice == 1:
        return [0,random.randint(0,size[1])]
    if spawnChoice == 2:
        return [size[0],random.randint(0,size[1])]
    if spawnChoice == 3:
        return [random.randint(0,size[0]),0]
    if spawnChoice == 4:
        return [random.randint(0,size[0]),size[1]]
    
def spawnAngleEnemyShip(spawnPoint,size):

    if spawnPoint[0] == 0 and spawnPoint[1] >= 0 and spawnPoint[1] <= size[1]:
        return 0
    if spawnPoint[0] == size[0] and spawnPoint[1] >= 0 and spawnPoint[1] <= size[1]:
        return 180
    if spawnPoint[0] >= 0 and spawnPoint[0] <= size[0] and spawnPoint[1] == 0:
        return 270
    if spawnPoint[0] >= size[0]/2 and spawnPoint[0] <= size[0] and spawnPoint[1] >= size[1]:
        return 90
    
    return 0


def pyGameTemplate():
    
    p.init()
    GAME_FONT = p.font.SysFont('Comic Sans MS', 60)
    bg = p.image.load("asteroid/spacefield.png")
    dim = p.display.get_desktop_sizes()
    mainscreen = 0
    screenWidth = dim[mainscreen][0]
    screenHeight = dim[mainscreen][1]
    image = p.transform.scale(bg, (screenWidth, screenHeight))
    image_rect = image.get_rect()

    pausing = False
    pausingdelay = 5
    
    # Set the width and height of the screen [width, height]
    size = (screenWidth, screenHeight)
    screen = p.display.set_mode(size)
     
    p.display.set_caption("basic Python graphics window()")
     
    # Loop until the user clicks the close button.
    running = True 
     
    # Used to manage how fast the screen updates
    clock = p.time.Clock()

    ship = spaceShip(screenWidth/2,screenHeight/2)

    ship_group = p.sprite.Group()
    ship_group.add(ship)
    
    listAsteriods = []
    listBlackHole = []
    listEnemyShip = []


    # -------- Main Program Loop -----------
    while running:
        # --- Main event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
        
        """ Check for keyboard presses. """
        key = p.key.get_pressed()
        
        if (key[p.K_ESCAPE] == True): 
            running = False
        if (key[p.K_w] == True):
            ship.move()

        if (key[p.K_s] == True):
            pass

        if (key[p.K_a] == True):
            ship.rotate(2)

        if (key[p.K_d] == True):
            ship.rotate(-2)

        if (key[p.K_q] == True):
            if ship.blinkcooldown == 0:
                ship.blink()

        if (key[p.K_SPACE] == True):
            if(ship.fireRate == 0 and ship.ammo > 0):
                ship.fire()
            pass

        if (key[p.K_e] == True):
            if ship.shield_turn == False:
                ship.shield_turn = True
            else:
                ship.shield_turn = False

        if (key[p.K_p] == True):
            if pausingdelay == 0:
                if pausing is False:
                    pausing = True
                    pausingdelay = 5
                else:
                    pausing = False
                    pausingdelay = 5
            
        # --- Game logic should go here
        if pausing is False:

            if ship:
                ship.blocking(listEnemyShip)
                ship.gethit(listEnemyShip,listAsteriods)

            if ship.bullets:
                for bullet in ship.bullets:
                    bullet.moveP(size)
                    if(bullet.collisionWithRock(listAsteriods,ship)):
                        ship.score +=1

            if listAsteriods:
                for object in listAsteriods:
                    object.move(size)

            if len(listAsteriods) < 4:
                listAsteriods.append(asteroid(size))

            if listBlackHole:
                for object in listBlackHole:
                    object.pullingIn(listAsteriods)
                    object.crushing(listAsteriods)
            
            if len(listBlackHole) < 4:
                listBlackHole.append(blackHole(size))

            if listEnemyShip:
                for object in listEnemyShip:
                    object.move(size)
                    if object.fireRate > 0:
                        object.fireRate -= 1
                    object.fire(ship)
                    for bullet in object.bullets:
                        bullet.moveP(size)
            
            if len(listEnemyShip) < 1:
                listEnemyShip.append(enemyShip(size))

        if ship.score == ship.winningScore:
            running = False
                
        # Garbage Collection
        removeBullets = []
        if ship.bullets:
            for index1,bullet in enumerate(ship.bullets):
                if bullet.IsExisting is False:
                    removeBullets.append(index1)
            removeBullets.sort(reverse=True)
            for index1 in removeBullets:
                ship.bullets.pop(index1)
        
        removeAsteriods = []
        if listAsteriods:
            for index2,asteroidobj in enumerate(listAsteriods):
                if asteroidobj.IsExisting is False:
                    removeAsteriods.append(index2)
            removeAsteriods.sort(reverse=True)
            for index2 in removeAsteriods:
                listAsteriods.pop(index2)
        
        removeEnemyShip = []
        if listEnemyShip:
            for EnemyShip in listEnemyShip:
                removeEnemyBullets = []
                if EnemyShip.bullets:
                    for index4,bullet in enumerate(EnemyShip.bullets):
                        if bullet.IsExisting is False :
                            removeEnemyBullets.append(index4)
                    removeEnemyBullets.sort(reverse=True)
                    for index4 in removeEnemyBullets:
                        EnemyShip.bullets.pop(index4)

            for index3,EnemyShipobj in enumerate(listEnemyShip):
                if EnemyShipobj.IsExisting is False:
                    removeEnemyShip.append(index3)
            removeEnemyShip.sort(reverse=True)
            for index3 in removeEnemyShip:
                listEnemyShip.pop(index3)

        if ship.fireRate > 0:
            ship.fireRate -= 1
        
        if ship.shield_duration > 0 and ship.shield_turn:
            ship.shield_duration -= 1

        if pausingdelay > 0:
            pausingdelay -= 1
        
        if ship.blinkcooldown > 0:
            ship.blinkcooldown -= 1
        
        if ship.blinkduration > 0:
            ship.blinkduration -= 1
        else:
            ship.blinking = True

        if ship.lives <= 0:
            running = False
            
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.blit(image, image_rect)

        for blackhole in listBlackHole:
            screen.blit(blackhole.image,blackhole.rect)

        if ship.startblinking is False:
            screen.blit(ship.rotatedImage,ship.rotatedRect)
        else:
            screen.blit(ship.rotatedGrayImage,ship.grayRotatedRect)

        for asteriodsobj in listAsteriods:
            screen.blit(asteriodsobj.image,asteriodsobj.rect)

        for EnemyShip in listEnemyShip:
            screen.blit(EnemyShip.image,EnemyShip.rect)
            #p.draw.rect(screen, GREEN,asteroidobj.rect)
        # --- Drawing code should go here
        # p.draw.line(screen, GREEN, [screenWidth/2, 0], [screenWidth/2, screenHeight], 2)
        # p.draw.line(screen, YELLOW, [0, screenHeight/2], [screenWidth, screenHeight/2], 2)
        if ship.shield_duration > 0 and ship.shield_turn:
            screen.blit(ship.shieldImage,ship.shieldRect)

        for bullet in ship.bullets:
            if bullet.IsExisting:
                p.draw.circle(screen,bullet.color,[bullet.hitbox.centerx,bullet.hitbox.centery],bullet.hitbox.width)
        
        for EnemyShip in listEnemyShip:
            for bullet in EnemyShip.bullets:
                if bullet.IsExisting:
                    p.draw.circle(screen,bullet.color,[bullet.hitbox.centerx,bullet.hitbox.centery],bullet.hitbox.width)


        #display ish
        shield_text = f"Shield duration:{ship.shield_duration}"
        shield_surface = GAME_FONT.render(shield_text,False,GREEN)
        screen.blit(shield_surface, (50, 150))

        gold_text = f"Gold:{ship.gold}"
        gold_surface = GAME_FONT.render(gold_text,False,GREEN)
        screen.blit(gold_surface, (screenWidth -220, 150))

        life_text = f"Lives:{ship.lives}"
        life_surface = GAME_FONT.render(life_text,False,GREEN)
        screen.blit(life_surface, (screenWidth -220, 50))

        ammo_text = f"Ammo:{ship.ammo}/{ship.ammo_size}"
        ammo_surface = GAME_FONT.render(ammo_text,False,GREEN)
        screen.blit(ammo_surface, (screenWidth -370, 250))

        if ship.score < ship.winningScore :
            human_text = f"Score:{ship.score}"
            human_surface = GAME_FONT.render(human_text,False,GREEN)
            screen.blit(human_surface, (50, 50))
        else:
            level_text = f"Level Completed"
            text_surface = GAME_FONT.render(level_text,False,GREEN)
            screen.blit(text_surface, (screenWidth/2 - screenWidth/10, screenHeight/2 - screenHeight/10))
            p.display.flip()
            p.time.delay(1000)

        if ship.lives <= 0 and running == False:
            death_text = f"You dead"
            death_surface = GAME_FONT.render(death_text,False,GREEN)
            screen.blit(death_surface, (screenWidth/2 - screenWidth/9, screenHeight/2 - screenHeight/9))        
            p.display.flip()
            p.time.delay(1000)

                
        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(100)
     
    # Close the window and quit.
    p.quit()
    
    return

pyGameTemplate()