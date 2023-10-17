import pygame as p
import random
import math as m

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 200, 0)
CYAN = (0, 200, 250)
MAGENTA = (255, 0, 255)
PINK = (245, 160, 220)

screenWidth = 800
screenHeight = 500
# Set the width and height of the screen [width, height]
size = (screenWidth, screenHeight)
screen = p.display.set_mode(size)

def orientXY(x0, y0):
    x = x0
    y = screenHeight - y0
    return x, y

def makePongTable(screen, width, height, xul, yul):
    x, y = orientXY(xul, yul)
    myRect = p.Rect(xul, yul, width, height)
    p.draw.rect(screen, GREEN, myRect, width= 2)
    return


class paddle:
    def __init__(self, x0, y0, width, height, gunLen, gunAng):
        self.x = x0
        self.y = y0
        self.width = width
        self.height = height
        self.halfW = int(width/2)
        self.halfH = int(height/2)
        self.gunLen = gunLen
        self.gunTipX = 0
        self.gunTipY = 0
        self.gunAng = gunAng
        self.shootType = 0  # making use of powerups. 0 is none
        self.shrinkLvl = 0
        self.bullets = []   # each paddle will have its own array of bullets for determining when it can/can't fire
        self.shootTimer = 0 # timer for preventing a bajillion bullets on screen
        self.slowTimer = 0  # timer for temporarily slowing paddle upon being shot
        self.powerUpTimer = 0 # timer will let a power up end
        return
        

    def drawPaddle(self, screen):

        height = self.height * (1 - (0.1 * self.shrinkLvl))

        if (self.shrinkLvl == 0) and (self.shootType == 0):
            pColor = YELLOW
        elif (self.shootType == 1):
            pColor = CYAN
        elif (self.shootType == 2):
            pColor = RED
        elif (self.shrinkLvl > 0):
            pColor = PINK
        else:
            pColor = WHITE

        xul = self.x - self.halfW
        yul = self.y + (height / 2)
        x, y = orientXY(xul, yul)
        myRect = p.Rect(x, y, self.width, height)
        p.draw.rect(screen, pColor, myRect, width = 2)

        # draw gun
        angRad = (self.gunAng/180) * m.pi

        # draw gun on correct side determined by which
        # side the paddle is on
        if (self.x < screenWidth/2):
          padAdjX = self.width
        else:
          padAdjX = 0

        padAdjY = height / 2
          
        self.gunTipX = (x + padAdjX) + self.gunLen*m.cos(angRad)
        self.gunTipY = (y + padAdjY) + self.gunLen*m.sin(angRad)
      
        p.draw.line(screen, WHITE, [x + padAdjX, y + padAdjY], [self.gunTipX, self.gunTipY], 2)
        
        # draw power up time amount in the form of a bar at the bottom of paddle
        if (self.shootType > 0):
          cX, cY = self.x, (screenHeight - 25)
          
          xSide = (self.x - (screenWidth / 2)) / abs(self.x - (screenWidth / 2))
          lX, lY = self.x - (xSide * 30), (screenHeight - 25)
          timerlen = (self.powerUpTimer * xSide) / 4
          
          p.draw.line(screen, WHITE, (lX, lY), ((lX - timerlen, lY)), 8)
          
          if (self.shootType == 1):
            p.draw.circle(screen, CYAN, (cX, cY), 20, 20)
            p.draw.circle(screen, BLACK, (cX - 7, cY + 5), 5, 5)
            p.draw.circle(screen, BLACK, (cX + 7, cY + 5), 5, 5)
            p.draw.circle(screen, BLACK, (cX, cY - 5), 5, 5)
                    
          elif (self.shootType == 2):
            p.draw.circle(screen, YELLOW, (cX, cY), 20, 20)
            p.draw.polygon(screen, BLACK, [(cX - 10, cY - 10), (cX - 10, cY + 10), (cX + 2, cY)], 3)
            p.draw.polygon(screen, BLACK, [(cX, cY - 10), (cX, cY + 10), (cX + 12, cY)], 3)
        
        return
    
    def moveMe(self, yInc, botY, topY):
      
        if self.slowTimer > 0:
          yInc = yInc / 8
          
        height = self.height * (1 - (0.1 * self.shrinkLvl))
        
        self.x = self.x 
        self.y = self.y + yInc
        
        pTop = self.y + (height / 2)
        pBot = self.y - (height / 2)
        
        if (pTop > topY):
            self.y = self.y - (pTop - topY)
            
        if (pBot < botY):
            self.y = self.y + (botY - pBot)
        
        return
    
    def autoTrack(self, bX, bY, inc, botY, topY):
        if (bY > self.y):
            self.moveMe(inc, botY, topY)
        elif (bY < self.y):
            self.moveMe((-1 * inc), botY, topY)
        return
    
    def getPaddleXY(self):
        return self.x, self.y

    def getGunTip(self):
      return self.gunTipX, self.gunTipY

    def getGunAngle(self):
      return self.gunAng
    
    def didBallHit(self, bX, bY, bRad, side, ball):
        
        height = self.height * (1 - (0.1 * self.shrinkLvl))

        hit = False
        if (side == 'l'):
            if ((bX - bRad) < (self.x + self.halfW)):
                if ( (bY >= (self.y - (height / 2))) and (bY <= (self.y + (height / 2))) ):
                    hit = True

        
        elif (side == 'r'):
            if ((bX + bRad) > (self.x - self.halfW)):
                if ( (bY >= (self.y - (height / 2))) and (bY <= (self.y + (height / 2))) ):
                    hit = True
        
        # check collision in center of ball? possibly preventing double scoring when the ball gets behind the paddle
        elif (bX > (self.x)):
            if ( (bY >= (self.y - (height / 2))) and (bY <= (self.y + (height / 2))) ):
                hit = True
         
        return hit
    
    def didBullHit(self, bullArr):
        
        height = self.height * (1 - (0.1 * self.shrinkLvl))
        
        xul = self.x - self.halfW
        yul = self.y + (height / 2)
        x, y = orientXY(xul, yul)
        
        for b in bullArr:
            if (((b.x - b.radius) <= (x + self.halfW)) and ((b.x - b.radius) >= (x - self.halfW))):
                if ((b.y >= (y)) and (b.y <= (y + height))):
                    b.explodeMe(screen)
                    self.slowTimer = 60
                    if (self.shrinkLvl < 7.5):
                        self.shrinkLvl += 1
      
        return
    
    def collideBullets(self, bulletArr):
        
        for b1 in self.bullets:
            for b2 in bulletArr:
                if (((b1.x - b1.radius) <= (b2.x + b2.radius)) and ((b1.x - b1.radius) >= (b2.x - b2.radius))):
                    if ((b1.y >= (b2.y - b2.radius)) and (b1.y <= (b2.y + b2.radius))):
                        b1.explodeMe(screen)
                        b2.explodeMe(screen)

    def rotateMe(self, inc):
      self.gunAng = self.gunAng + inc
      if (self.gunAng > 410):
        self.gunAng = 410
      elif (self.gunAng < 310):
        self.gunAng = 310
      return
    
    def moveBullets(self, gWidth, gHeight):
      for b in self.bullets:
            b.moveMe(gWidth, gHeight)
            if (b.doIExist() == False):
                self.bullets.remove(b)
      return
    
    def drawBullets(self, screen):
      for j in range(0, len(self.bullets)):
          self.bullets[j].drawMe(screen)
    
    # limit how many shots are made based on timer
    def shoot(self):
        if self.shootTimer == 0:
            gx, gy = self.getGunTip()
            ang = self.getGunAngle()
            
            # shoot mode 1 affects timers
            if (self.shootType == 2):
                self.shootTimer = 10
            else:
                self.shootTimer = 45
        
            # shoot mode 2 is multibullet
            if self.shootType == 1:
                self.bullets.append(bullet(gx, gy, ang))
                self.bullets.append(bullet(gx, gy, ang + 5))
                self.bullets.append(bullet(gx, gy, ang + 10))
                self.bullets.append(bullet(gx, gy, ang - 5))
                self.bullets.append(bullet(gx, gy, ang - 10))
            
            else:
                self.bullets.append(bullet(gx, gy, ang))
      
        return

    def grow(self):
        if (self.shrinkLvl > 0):
            self.shrinkLvl -= 1
    
    # set powerup
    def powerUp(self, type):
        self.shootType = type
        self.powerUpTimer = 600
    
    # decrement timer(s) of paddle. # note to self: make timers objects to have an array of them in the paddle object?
    def tick(self):
      if self.shootTimer > 0:
        self.shootTimer -= 1
      if self.slowTimer > 0:
        self.slowTimer -= 1
      if self.powerUpTimer > 0:
        self.powerUpTimer -= 1
      elif (self.powerUpTimer <= 0):
        self.shootType = 0
      
      return
    

class ball:
    def __init__(self, x0, y0, radius, xVel0, yVel0):
        self.x = x0
        self.y = y0
        self.radius = radius
        self.xVel = xVel0
        self.yVel = yVel0
        self.bounceTimer = 0    # prevent ball from bouncing multiple times inside paddle and getting stuck
        return
    
    def drawMe(self, screen, color, font):
        x, y = orientXY(self.x, self.y)
        p.draw.circle(screen, color, [x, y], self.radius, 2)
        return
    
    def moveMe(self, xLeft, xRight, yLow, yHi):
        if (self.xVel > 15):
            self.xVel = 15
        elif (self.xVel < -15):
            self.xVel = -15
        if (self.yVel > 10):
            self.yVel = 10
        elif (self.yVel < -10):
            self.yVel = -10

        self.x = self.x + self.xVel
        self.y = self.y + self.yVel
        
        if ((self.x - self.radius) < xLeft):
            self.x = xLeft + self.radius
            self.xBounce()
            
        if ((self.x + self.radius) > xRight):
            self.x = xRight - self.radius
            self.xBounce()
            
        if ((self.y - self.radius) < yLow):
            self.y = yLow + self.radius
            self.yVel = -1 * self.yVel 
            
        if ((self.y + self.radius) > yHi):
            self.y = yHi - self.radius
            self.yVel = -1 * self.yVel 
            
        return

    # let bullets accelerate/decelerate ball
    def bullHit(self, bulletArr):

        x, y = orientXY(self.x, self.y) 

        for b in bulletArr:
            # collide
            # give some leeway, letting the ball get away from the goal before letting a bullet hit
            if ( self.bounceTimer <= 0 ):
              
              if ( ((b.x - b.radius) <= (x + self.radius)) and ((b.x - b.radius) >= (x - self.radius)) ):
                  if ( (b.y <= (y + self.radius)) and (b.y >= (y - self.radius)) ):
                      b.explodeMe(screen)
  
                      # force applied to ball
                      headingDeg = (b.heading / 180) * m.pi
                      self.xVel += (7 * m.cos(headingDeg))
                      self.yVel += (-1) * (5 * m.sin(headingDeg))

    
    def getXYRad(self):
        return self.x, self.y, self.radius
    
    def xBounce(self):
        if (self.bounceTimer <= 0):
            self.xVel = self.xVel * -1
            self.bounceTimer = 20
        return

    def tick(self):
        if (self.bounceTimer > 0):
            self.bounceTimer -= 1
            
        # let the ball decelerate
        decrement = .05
        if (self.xVel > 4):
            self.xVel -= decrement
        elif (self.xVel < -4):
            self.xVel += decrement
        
        if (self.yVel > 3):
            self.yVel -= decrement * 2
        elif (self.yVel < -3):
            self.yVel += decrement * 2


class bullet:
    def __init__(self, x0, y0, heading0, radius=7):
        self.x = x0
        self.y = y0
        self.radius = radius
        self.heading = heading0
        self.velocity = 20
        self.exists = True
        self.hit = False
        return
    
    def drawMe(self, s):
        if (self.hit == False):
            p.draw.circle(s, GREEN, [int(self.x), int(self.y)], self.radius, 1)
        else:
            self.explodeMe(s)
            
        return
    
    def moveMe(self, gameWidth, gameHeight):
        angRad = (self.heading / 180) * m.pi
        bX = self.x + self.velocity*m.cos(angRad)
        bY = self.y + self.velocity*m.sin(angRad)
        if ((bX > 50) and (bX < gameWidth))and((bY > 50) and (bY < gameHeight)):
            self.x = bX
            self.y = bY
        else:
            self.exists = False              
        return
    
    def doIExist(self):
        return self.exists
    
    def explodeMe(self, s):
        p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius-4, 1)
        p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius, 1)
        p.draw.circle(s, RED, [int(self.x), int(self.y)], self.radius+4, 1)
        p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+6, 1)
        p.draw.circle(s, ORANGE, [int(self.x), int(self.y)], self.radius+9, 1)
        p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+11, 1)
        p.draw.circle(s, YELLOW, [int(self.x), int(self.y)], self.radius+13, 1)
        
        self.hit = False
        self.exists = False
        return


# counts the score
class goal:
    
    def __init__(self, topX, topY, width, gameHeight):
        self.score = 0
        self.topX = topX
        self.topY = topY
        self.width = width
        self.height = gameHeight
        self.ballIn = False
    
    
    def didBallHit(self, ball):
        
        x, y = orientXY(ball.x, ball.y)
        hit = False

        # check goal-ball collision on both sides of ball
        if (((x - ball.radius) > self.topX) and ((x - ball.radius) <= (self.topX + self.width))) or (((x + ball.radius) > self.topX) and ((x + ball.radius) <= (self.topX + self.width))):
            if ( (y >= self.topY) and (y <= (self.topY + self.height)) ):
                    hit = True
         
        return hit
        
    # make sure a bajillion scores aren't made across frames
    def otherPaddleCanScore(self, ball):
        hit = self.didBallHit(ball)

        otherPaddleCanScore = False

        if (hit == True):
            if (self.ballIn == False):
                self.ballIn = True
                otherPaddleCanScore = True
        else:
            if (self.ballIn == True):
                self.ballIn = False

        return otherPaddleCanScore
                
        
    
    def drawMe(self, font, midX):
        
        # drawing goal area just for checking collision visually
        ##goalRect = p.Rect(self.topX, self.topY, self.width, self.height)
        ##p.draw.rect(screen, WHITE, goalRect, 1)
        
        scoretxtrender = font.render(str(self.score), True, (230, 230, 230))

        # display score in bottom middle-ish of screen.
        # Offset positive or negative depending on goal side
        xOffset = 50 * ( (self.topX - midX) / abs(self.topX - midX) )
        
        screen.blit(scoretxtrender, (midX + xOffset, (self.height + 60)))


# affects paddle's shoot modes - fast, shotgun
class pickUp():
  
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # type should correspond to existing paddle shoot types
        self.radius = 20  # for drawing and collision checking
      
    def drawMe(self):
      
        if (self.type == 1):
          
            p.draw.circle(screen, CYAN, (self.x, self.y), self.radius, self.radius)
            p.draw.circle(screen, BLACK, (self.x - 7, self.y + 5), 5, 5)
            p.draw.circle(screen, BLACK, (self.x + 7, self.y + 5), 5, 5)
            p.draw.circle(screen, BLACK, (self.x, self.y - 5), 5, 5)
            
        elif (self.type == 2):
            
            p.draw.circle(screen, YELLOW, (self.x, self.y), self.radius, self.radius)
            p.draw.polygon(screen, BLACK, [(self.x - 10, self.y - 10), (self.x - 10, self.y + 10), (self.x + 2, self.y)], 3)
            p.draw.polygon(screen, BLACK, [(self.x, self.y - 10), (self.x, self.y + 10), (self.x + 12, self.y)], 3)
          
    
    def didBullHit(self, b):
    
        hit = False
    
        if (((b.x - b.radius) <= (self.x + self.radius)) and ((b.x - b.radius) >= (self.x - self.radius))):
                if ((b.y >= (self.y - self.radius)) and (b.y <= (self.y + self.radius))):
                    b.explodeMe(screen)
                    hit = True
        
        return hit, self.type

    

def pongMe():
    
    p.init()
     
    p.display.set_caption("pongMe()")
    font = p.font.Font("freesansbold.ttf", 32)
    
    # Set up random number generator.
    random.seed()
     
    # Loop until the user clicks the close button.
    running = True 
     
    # Used to manage how fast the screen updates
    clock = p.time.Clock()
    
    # Set up some game objects.
    border = 50
    xMargin = 20
    gameHeight = screenHeight - 100
    gameWidth = screenWidth - 100
    
    leftX = border
    rightX = leftX + gameWidth
    yLow = border
    yHi = yLow + gameHeight
    
    midBoardX = border + int(gameWidth/2)
    midBoardY = border + int(gameHeight/2)
    
    leftPx = border + xMargin
    rightPx = border + gameWidth - xMargin
    paddleWidth = 20
    paddleHeight = 100
    paddleYinc = 3
    leftPaddle = paddle(leftPx, midBoardY, paddleWidth, paddleHeight, 30, 360)
    rightPaddle = paddle(rightPx, midBoardY, paddleWidth, paddleHeight, 30, 180)
    
    ballRad = 20
    xVel = random.randint(0, 2) + 2
    yVel = random.randint(0, 2) + 1
    duhBall = ball(midBoardX, midBoardY, ballRad, xVel, yVel)
    
    # like paddle bullets, pickups are in an array
    pickups = []
    
    leftGoal = goal((border - 5), (border), 15, gameHeight)
    rightGoal = goal((border + gameWidth - 10), (border), 15, gameHeight)

    # Possibly spawn a pick up every x seconds, eventid = 1
    p.time.set_timer(1, 5000)

    # Timer that lets paddles grow back, eventid = 2
    p.time.set_timer(2, 4000)
    
    # -------- Main Program Loop -----------
    while running:
        # --- Main event loop
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == 1:
              
                # spawning pickup is a coin toss, it won't always happen
                c = random.randint(0, 1)
                
                # pos and type will be random, within middle area of game board
                puX, puY = random.randint(midBoardX - int(gameWidth / 5), midBoardX + int(gameWidth / 5)), random.randint(midBoardY - int(gameHeight / 2.5), midBoardY + int(gameHeight / 2.5))
                puT = random.randint(1, 2)
                
                if (c > 0) and ( len(pickups) < 3 ):
                  pickups.append( pickUp(puX, puY, puT) )
                  
            if event.type == 2:
                leftPaddle.grow()
                rightPaddle.grow()
        
        """ Check for keyboard presses. """
        key = p.key.get_pressed()
        
        # Handle keypresses.
        if (key[p.K_ESCAPE] == True): 
            running = False
        if (key[p.K_w] == True): 
            leftPaddle.moveMe(paddleYinc, yLow, yHi)
        if (key[p.K_s] == True): 
            leftPaddle.moveMe(-paddleYinc, yLow, yHi)
        if (key[p.K_a] == True) or (key[p.K_UP] == True):
            leftPaddle.rotateMe(-3)
        if (key[p.K_d] == True) or (key[p.K_DOWN] == True):
            leftPaddle.rotateMe(3)
        if (key[p.K_SPACE] == True):
            leftPaddle.shoot()
        
        rightPaddle.shoot()
            
        # --- Game logic should go here
        
        # Move the ball
        duhBall.moveMe(leftX, rightX, yLow, yHi)
        
        # Get Ball position.
        bX, bY, bRad = duhBall.getXYRad()
        
        # Move right paddle.
        rightPaddle.autoTrack(bX, bY, paddleYinc, yLow, yHi)
        
        # Check for a hit on the left paddle.
        hit = leftPaddle.didBallHit(bX, bY, bRad, 'l', duhBall)
        # If there was a hit, do a bounce.
        if (hit == True):
            duhBall.xBounce()
        else:
            # Check for a hit on the right paddle.
            hit = rightPaddle.didBallHit(bX, bY, bRad, 'r', duhBall)
            if (hit == True):
                duhBall.xBounce()
        
        # check if valid score was made
        if (leftGoal.otherPaddleCanScore(duhBall)):
            rightGoal.score += 1
        elif (rightGoal.otherPaddleCanScore(duhBall)):
            leftGoal.score += 1

        
        # tick down paddle timers
        leftPaddle.tick()
        rightPaddle.tick()

        duhBall.tick()

        # --- Move bullets 
        leftPaddle.moveBullets(gameWidth + 50, gameHeight + 50)
        rightPaddle.moveBullets(gameWidth + 50, gameHeight + 50)

            
        # --- Screen-clearing code goes here
     
        # Here, we clear the screen to black. Don't put other drawing commands
        # above this, or they will be erased with this command.
     
        # If you want a background image, replace this clear with blit'ing the
        # background image.
        screen.fill(BLACK)
        
        # Check for bullets hitting objects
        # checks here because it draws the explosion
        leftPaddle.didBullHit(rightPaddle.bullets)
        rightPaddle.didBullHit(leftPaddle.bullets)

        duhBall.bullHit(leftPaddle.bullets)
        duhBall.bullHit(rightPaddle.bullets)
        
        # one paddle will take care of other paddle's bullets colliding
        leftPaddle.collideBullets(rightPaddle.bullets)
        
        # get a pickup to power up the paddle
        for b in leftPaddle.bullets:
            for pU in pickups:
                hit, type = pU.didBullHit(b)
            
                if hit:
                  leftPaddle.powerUp(type)
                  pickups.remove(pU)
        
        for b in rightPaddle.bullets:
            for pU in pickups:
                hit, type = pU.didBullHit(b)
            
                if hit:
                  rightPaddle.powerUp(type)
                  pickups.remove(pU)
    
    
        # --- Drawing code should go here
        makePongTable(screen, gameWidth, gameHeight, 50, 50)
        leftPaddle.drawPaddle(screen)
        rightPaddle.drawPaddle(screen)
        duhBall.drawMe(screen, ORANGE, font)

        leftPaddle.drawBullets(screen)
        rightPaddle.drawBullets(screen)
        
        leftGoal.drawMe(font, midBoardX)
        rightGoal.drawMe(font, midBoardX)
        
        for pu in pickups:
            pu.drawMe()
        
              
        # --- Go ahead and update the screen with what we've drawn.
        p.display.flip()
     
        # --- Limit to 60 frames per second
        clock.tick(60)
     
    # Close the window and quit.
    p.quit()
    
    return

pongMe()