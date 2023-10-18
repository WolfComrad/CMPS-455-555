import pygame as p
import math 
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

screenWidth = 900
screenHeight = 600


class hitarea:
    destroy = False
    x = 0
    y = 0
    width = 0
    height = 0
    def __init__(self,x,y,width,height,color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color

class projectitle:
    baseSpeed = 7
    IsExisting = True
  
    def __init__(self,x,y,width,height,color,enemyX,enemyY):
        self.hitbox = hitarea(x,y,width,height,color)
        self.angle = math.atan((enemyY-y)/(enemyX-x))
        self.speedX = self.baseSpeed * math.cos(self.angle)
        self.speedY = self.baseSpeed * math.sin(self.angle)
        self.IsExisting = True
    
    def collide(self,player):
            if self.IsExisting is True :
                if player.hitarea.x < self.hitbox.x and player.hitarea.x + player.hitarea.width > self.hitbox.x:
                    if player.hitarea.y < self.hitbox.y and player.hitarea.y + player.hitarea.height >self.hitbox.y:
                        self.IsExisting = False
                        return True
                    
    def move(self):
        if self.hitbox.x > 900:
            self.IsExisting = False
        if self.hitbox.y > 600 or self.hitbox.x < 0:
            self.IsExisting = False
        self.hitbox.x = self.hitbox.x + self.speedX
        self.hitbox.y = self.hitbox.y + self.speedY

class enemy:
    exist = True
    hitbox = []
    projectable = []
    duration = 0
    hitable = True
    fireRate = 100
    cooldownfire = 100
    numberOfParts = 14
    
    head1 = hitarea(40,150,80,80,WHITE)
    head2 = hitarea(120,150,80,80,WHITE)
    head3 = hitarea(120,230,80,80,WHITE)
    head4 = hitarea(40,230,80,80,WHITE)
    leg1 = hitarea(45,310,10,50,WHITE)
    leg2 = hitarea(65,310,10,50,WHITE)
    leg3 = hitarea(85,310,10,50,WHITE)
    leg4 = hitarea(105,310,10,50,WHITE)
    leg5 = hitarea(125,310,10,50,WHITE)
    leg6 = hitarea(145,310,10,50,WHITE)
    leg7 = hitarea(165,310,10,50,WHITE)
    eyeball1 = hitarea(70,200,40,10,BLACK)
    eyeball2 = hitarea(140,200,40,10,BLACK)
    mouth = hitarea(110,240,40,40,BLACK)

    hitbox.append(head1)
    hitbox.append(head2)
    hitbox.append(head3)
    hitbox.append(head4)
    hitbox.append(eyeball1)
    hitbox.append(eyeball2)
    hitbox.append(mouth)
    hitbox.append(leg1)
    hitbox.append(leg2)
    hitbox.append(leg3)
    hitbox.append(leg4)
    hitbox.append(leg5)
    hitbox.append(leg6)
    hitbox.append(leg7)
    

    def collide(self,ball):
        count = 0
        for part in self.hitbox:
            if part.destroy:
                count += 1
            if count == self.numberOfParts:
                self.exist = False
            if part.destroy is False and self.hitable:
                if part.x < ball.intialBallx and part.x + part.width + ball.radius > ball.intialBallx:
                    if part.y < ball.intialBally and part.y + part.height + ball.radius > ball.intialBally:
                        part.destroy = True
                        return True
                  
    def makeunhitable(self):
        self.hitable = False
    
    def makehitable(self):
        self.hitable = True
    
    def fireball(self,playerX,playerY):
        fireball = projectitle(160,260,10,10,RED,playerX,playerY)
        self.projectable.append(fireball)

    def moveProjectable(self):
        for object in self.projectable:
            object.move()
    
    def collidefireball(self,player):
        hitting = False
        for object in self.projectable:
            one = object.collide(player)
            if one:
                hitting = one
        return hitting

class human:
    destroy = False
    life = 3

    def __init__(self,x,y,width,height,color):
        self.hitarea = hitarea(x,y,width,height,color)

    def die(self):
        self.destroy = True
        self.life = self.life -1
    
    def revive(self):
        self.destroy = False
            

class gameball:
    
    duration = 0
    intialBallx = 435
    intialBally = 290
    radius = 30
    ball = p.Rect(intialBallx,intialBally,radius,radius)

    multipler = 6
    ballspeedx = 5
    ballspeedy = 5

    def stop(self):
        self.ballspeedx = 0
        self.ballspeedy = 0
        self.intialBallx = 450
        self.intialBally = 300
    
    def reset(self):
        Xrand = random.choice([-1,1])
        Yrand = random.choice([-1,1])
        self.ballspeedx = 5 * Xrand
        self.ballspeedy = 5 * Yrand


def pyGamePong():
    
    p.init()
    p.font.init()
    GAME_FONT = p.font.SysFont('Comic Sans MS', 60)
    
    pause = False
    # Set the width and height of the screen [width, height]
    size = (screenWidth, screenHeight)
    bg = p.image.load("pong/nether.jpg")
    image = p.transform.scale(bg, (screenWidth, screenHeight))
    image_rect = image.get_rect()
    screen = p.display.set_mode(size)

    screen.blit(image, image_rect)
    intialHumanY= 250
    speed = 7

    theBall = gameball()    
    
    p.display.set_caption("basic Python graphics window()")
     
    # Loop until the user clicks the close button.
    running = True 
     
    # Used to manage how fast the screen updates
    clock = p.time.Clock()

    player2 = human(800,intialHumanY,40,100,CYAN)
    theEnemy = enemy()
  
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
        if (key[p.K_UP] == True):
            if(player2.hitarea.y > 0 and player2.destroy is False):
                player2.hitarea.y = player2.hitarea.y - speed
            pass
        if (key[p.K_DOWN] == True): 
            if(player2.hitarea.y < 450 and player2.destroy is False):
                player2.hitarea.y = player2.hitarea.y + speed
            pass
        if (key[p.K_LEFT] == True):
            pass
        if (key[p.K_RIGHT] == True):
            pass
        if (key[p.K_SPACE] == True):
            if pause:
                theBall.reset()
                player2.revive()
                pause = False
            pass
        if (key[p.K_p]== True):
            if player2.destroy :
                player2.revive()

        #check boundaries
        if theBall.intialBallx < 15:
            theBall.ballspeedx = theBall.ballspeedx * -1
        if theBall.intialBallx > 860:
            player2.die()
            theBall.stop()
            pause = True

        if theBall.intialBally < 15 or theBall.intialBally > 560:
            theBall.ballspeedy = theBall.ballspeedy * -1

        if player2.hitarea.x < theBall.intialBallx and player2.hitarea.x + player2.hitarea.width > theBall.intialBallx:
            if player2.hitarea.y < theBall.intialBally and player2.hitarea.y + player2.hitarea.height > theBall.intialBally:
                if player2.destroy is False:
                    if theBall.duration == 0:
                        theBall.ballspeedx = theBall.ballspeedx *-1
                        theBall.duration = 30
        
        if(theEnemy.collide(theBall)):
            theEnemy.makeunhitable()
            theEnemy.duration = 200
            theBall.ballspeedx = theBall.ballspeedx *-1
        
        if theEnemy:
            if theEnemy.exist is False:
                running = False
            theEnemy.moveProjectable()
            hitting = theEnemy.collidefireball(player2)
            if hitting:
                player2.die()
                theBall.stop()
                pause = True
            if player2.destroy is False:
                if theEnemy.cooldownfire == 0:
                    theEnemy.fireball(player2.hitarea.x,player2.hitarea.y)
                    theEnemy.cooldownfire = theEnemy.fireRate
                else:
                    theEnemy.cooldownfire = theEnemy.cooldownfire -1
            

        theBall.intialBallx = theBall.intialBallx + theBall.ballspeedx
        theBall.intialBally = theBall.intialBally + theBall.ballspeedy
       
        if player2.life == 0:
            running = False

        # --- Game logic should go here
        
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
        screen.blit(image, image_rect)
        
        # --- Drawing code should go here
        p.draw.circle(screen, ORANGE, [theBall.intialBallx,theBall.intialBally], theBall.radius)
        if player2.destroy is False:
            p.draw.rect(screen,player2.hitarea.color,p.Rect(player2.hitarea.x,player2.hitarea.y,player2.hitarea.width,player2.hitarea.height))
        else:
            if player2.life != 0:
                human_text = f"Life remaining: {player2.life}"
                text_surface = GAME_FONT.render(human_text,False,GREEN)
                screen.blit(text_surface, (380, 50))
            else:
                human_text = f"Game Over"
                text_surface = GAME_FONT.render(human_text,False,GREEN)
                screen.blit(text_surface, (380, 50))

        if theEnemy:
            for part in theEnemy.hitbox:
                if part.destroy is False:
                    if theEnemy.hitable:
                        p.draw.rect(screen,part.color,p.Rect(part.x,part.y,part.width,part.height))
                    else:
                        p.draw.rect(screen,RED,p.Rect(part.x,part.y,part.width,part.height))
            for object in theEnemy.projectable:
                if object.IsExisting:
                    p.draw.circle(screen,object.hitbox.color,[object.hitbox.x,object.hitbox.y],object.hitbox.width)
            
        if pause:
            if player2.life != 0:
                human_text = f"Life remaining: {player2.life}"
                text_surface = GAME_FONT.render(human_text,False,GREEN)
                screen.blit(text_surface, (380, 50))
            else:
                human_text = f"Game Over"
                text_surface = GAME_FONT.render(human_text,False,GREEN)
                screen.blit(text_surface, (380, 50))

        if theEnemy.duration > 0:
            theEnemy.duration = theEnemy.duration - 1
        else:
            theEnemy.makehitable()
        
        if theBall.duration > 0:
            theBall.duration = theBall.duration -1
                
        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
    # Close the window and quit.
    if running is False:
        if theEnemy.exist:
            human_text = f"Game Over"
            text_surface = GAME_FONT.render(human_text,False,GREEN)
            screen.blit(text_surface, (380, 50))
            p.display.flip()
        else:
            human_text = f"You Win"
            text_surface = GAME_FONT.render(human_text,False,GREEN)
            screen.blit(text_surface, (380, 50))
    p.time.delay(1000)
    p.display.flip()
    p.quit()
    
    return

pyGamePong()