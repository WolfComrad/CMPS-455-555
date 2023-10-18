# -*- coding: utf-8 -*-
"""
Created on Tue Oct  3 13:00:54 2023

base asteroid code by Dr. Patrick McDowell
modified by Brady, Robert, and Cam
"""

import pygame as p
import random
import math
import os
from util import deg2Rad, getDist, rotatePoint

# import game objects
from bullet import bullet
from spaceRock import spaceRock
from spaceShip import spaceShip
from grill import grill
from animatedSprite import animatedSprite
from customer import customer

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
nColors = len(colorPalette)

# screen dimensions, for camera
screenWidth = 1480
screenHeight = 920

# game dimensions, for game world
gameWidth = 2000
gameHeight = 2000

gameMidX = screenWidth / 2
gameMidY = screenHeight / 2

# General constants and variables defined.
# Keep asteroid count low, they won't exist too far outside the camera
nAsteroids = 40
maxShootingDelay = 30

basicShip = [[3, 0], [0, 3], [6, 0], [0, -3], [3, 0]]

# append game objects to this list whenever they're instantiated, used for camera offset function to have the camera work
entities = []


class camera:
    
  def __init__(self, x, y, width, height):
    self.topLeftX = x
    self.topLeftY = y
    self.width = width
    self.height = height
    self.halfW = width / 2
    self.halfH = height / 2

  def moveCamSide(self, speed, heading):
    heading = heading + 90
    radAng = deg2Rad(heading)
    # x*pi/180

    incX = (speed * math.cos(radAng))
    incY = (speed * math.sin(radAng))
    self.topLeftX += incX
    self.topLeftY += incY

    # If center of camera goes out of screen, wrap it other side.
    if (self.topLeftX + (self.width / 2) < 0):
      self.topLeftX = gameWidth - (self.width / 2) - 1
    elif (self.topLeftX + (self.width / 2) > gameWidth):
      self.topLeftX = 0 - (self.width / 2)

    if (self.topLeftY + (self.height / 2) < 0):
      self.topLeftY = gameHeight - (self.height / 2) - 1
    elif (self.topLeftY + (self.height / 2) > gameHeight):
      self.topLeftY = 0 - (self.height / 2)

    return incX, incY
  

  def moveCam(self, speed, heading):
    radAng = deg2Rad(heading)

    incX = (speed * math.cos(radAng))
    incY = (speed * math.sin(radAng))
    self.topLeftX += incX
    self.topLeftY += incY

    # If center of camera goes out of screen, wrap it other side.
    if (self.topLeftX + (self.width / 2) < 0):
      self.topLeftX = gameWidth - (self.width / 2) - 1
    elif (self.topLeftX + (self.width / 2) > gameWidth):
      self.topLeftX = 0 - (self.width / 2)

    if (self.topLeftY + (self.height / 2) < 0):
      self.topLeftY = gameHeight - (self.height / 2) - 1
    elif (self.topLeftY + (self.height / 2) > gameHeight):
      self.topLeftY = 0 - (self.height / 2)
  
    return incX, incY

  # offset object positions. One method for single objects, one method for a list of them
  # called by moveCam
  def offsetObjects(self, obj, incX, incY):

    if type(obj) == list:
      for o in obj:
        o.x -= incX
        o.y -= incY
    
    else:
      obj.x -= incX
      obj.y -= incY



def asteroidMe():
  # Initialize pygame.
  p.init()

  p.mixer.music.load("./funnyspacegame.ogg")
  p.mixer.music.play(-1)
  p.mixer.music.set_volume(0.1)
  font = p.font.SysFont("bebasregular", 48, True)
  beegfont = p.font.SysFont("Agency FB", 64, True)

  # Set the width and height of the screen [width, height]
  size = (screenWidth, screenHeight)
  screen = p.display.set_mode(size)

  p.display.set_caption("Asteroid Frycook")

  # Set up random number generator.
  random.seed()

  # Loop until the user clicks the close button.
  running = True

  # Used to manage how fast the screen updates
  clock = p.time.Clock()
  
  # camera object
  c = camera(0, 0, screenWidth, screenHeight)

  # the grill
  theGrill = grill(460, 240, screenWidth, screenHeight)

  # Set up some game objects.
  # Space ship stuff.
  initialHeading = 90
  scaleFactor = 6
  ship = spaceShip(gameMidX, gameMidY, initialHeading, scaleFactor, basicShip, gameWidth, gameHeight)
  shipSpeed = 5
  ship.setGunSpot([6, 0])

  # animation(s)
  explosionImg = []
  for filename in os.listdir("./sprites/explosion"):
    filename = "./sprites/explosion/" + filename
    explosionImg.append(p.image.load(filename))

  explosionAnim = animatedSprite(ship.x - 16, ship.y - 32, explosionImg, 2)
  explosionAnim.set_speed(0.1)

  # Bullet stuff
  bullets = []
  bulletSize = int(0.5 * scaleFactor)
  bulletSpeed = 3 * shipSpeed
  shotCount = 0
  act_count = 0

  # Make some asteroids - that is space rocks.
  myAsteroids = []

  # Used for randomly deciding where to spawn asteroids
  left, top = False, False
  bound = 512
  
  if random.randint(0, 2) == 1:
    left = True

  if random.randint(0, 2) == 1:
    top = True


  # return x, y coords out of camera view
  def getOutofView():

    x, y = 0, 0

    # spawn asteroids out of view, so they don't just pop in and the player sees it
    if left:
      x = random.randint(0 - bound + 1, 0)
    else:
      x = random.randint(screenWidth, screenWidth + bound - 1)
    
    if top:
      y = random.randint(0 - bound + 1, 0)
    else:
      y = random.randint(screenHeight, screenHeight + bound - 1)

    return x, y

  # quick roid spawn function
  def spawnAsteroid():
    ast = spaceRock(gameWidth, gameHeight)

    # spawn asteroids out of view, so they don't just pop in and the player sees it
    x, y = getOutofView()

    ast.x = x
    ast.y = y

    myAsteroids.append(ast)


  for j in range(nAsteroids):
    spawnAsteroid()

  # Clock/game frame things.
  tickTock = 0
  p.time.set_timer(1, 2000) # spawn rocks every x seconds, don't go over len nAsteroids
  p.time.set_timer(2, 1000) # spawn new customer if one doesn't exist

  score = 0

  aliem = customer(random.randint(0, gameWidth), random.randint(0, gameHeight), gameWidth, gameHeight)


  # -------- Main Program Loop -----------
  while running:

    # --- Main event loop
    for event in p.event.get():
      if event.type == p.QUIT:
        running = False

      # spawn asteroids
      if (event.type == 1):
        if len(myAsteroids) < nAsteroids:
          spawnAsteroid()
      
      # spawn customers
      if (event.type == 2):
        if aliem.satiated and ((aliem.x < (0 - aliem.rect.width) or aliem.x > screenWidth + aliem.rect.width) or (aliem.y < 0 - aliem.rect.height or aliem.y > screenHeight + aliem.rect.height)):
          aliem = customer(random.randint(0, gameWidth), random.randint(0, gameHeight))
        print(aliem.x, aliem.y)
      
      # click patty
      if (event.type == p.MOUSEBUTTONUP):

        # make them watch their patties burn after they lose
        if ship.isActive:
          for pat in theGrill.patties:
            x, y = p.mouse.get_pos()
            cookedPatty = pat.checkClick(x, y)

            if cookedPatty:
              ship.addAmmo()
          

    """ Check for keyboard presses. """
    key = p.key.get_pressed()

    # Handle keypresses.
    if (key[p.K_ESCAPE] == True):
      running = False

    # don't allow camera to move when dead
    if ship.isActive:

      if (key[p.K_w] == True):
        incX, incY = c.moveCam(shipSpeed, 270)

        for e in entities:
          c.offsetObjects(e, incX, incY)

      if (key[p.K_s] == True):
        incX, incY = c.moveCam(shipSpeed, 90)
        
        for e in entities:
          c.offsetObjects(e, incX, incY)

      if (key[p.K_a] == True):
        incX, incY = c.moveCam(shipSpeed, 180)

        for e in entities:
          c.offsetObjects(e, incX, incY)


      if (key[p.K_d] == True):
        # ship.moveMe(-1 * shipSpeed)
        incX, incY = c.moveCam(shipSpeed, 0)

        for e in entities:
          c.offsetObjects(e, incX, incY)


      if (key[p.K_q] == True):
        ship.turn(-3)


      if (key[p.K_e] == True):
        ship.turn(3)


      if (key[p.K_LSHIFT] == True):

        if ship.shieldActive == False and act_count>9:
          ship.shieldActive = True
          act_count = 0
          print("Shield is Active(WIP)")
        if ship.shieldActive == True and act_count>9:
          ship.shieldActive = False
          act_count = 0
          print("Shield is No Longer Active")


      if (key[p.K_SPACE] == True):
        if (shotCount == 0) and (ship.shoot()):
          gunX, gunY = ship.getGunSpot()
          myBullet = bullet(gunX, gunY, ship.heading, bulletSize, bulletSpeed, gameWidth, gameHeight)
          bullets.append(myBullet)
          shotCount = maxShootingDelay


    # stop music when dead
    if not ship.isActive and p.mixer.music.get_busy():
      p.mixer.music.stop()
        

        
    # --- Game logic should go here
    
    # camera function
    
    # Move bullets and asteroids.
    for b in bullets:
      b.moveMe()


    # move asteroids only when ship is alive. Game is "paused" after death
    if ship.isActive:

      ship.face(ship.getangletomouse())

      # make a gianter asteroid
      merge = False
      newAst = None

      # prevent "can't find x in list.remove(x)" error
      toRemove0, toRemove1 = False, False

      for a in myAsteroids:

        a.moveMe()

        # collisions
        for aa in myAsteroids:
          if (a != aa):

            smack, sameCol = a.checkCollisionAst(aa)
            if ship.collRect.colliderect(a.rect):
              ship.hit()

            if ship.gravRect.colliderect(a.rect):
              a.gravPull(ship)

            # only "merge" rocks if their scales are smallish. Make a bigger rock when they merge
            if sameCol and (a.scaleFactorX < 25 or a.scaleFactorY < 25) and (aa.scaleFactorX < 25 or aa.scaleFactorY < 25):
              newAst = spaceRock(gameWidth, gameHeight, 35, 35)
              merge = True
              newAst.x = a.x
              newAst.y = a.y
              newAst.color = a.color

              toRemove0 = a
              toRemove1 = aa

            elif smack:
              a.reverseDir(aa)
              #aa.reverseDir()
      
      if merge:
        myAsteroids.remove(toRemove0)
        myAsteroids.remove(toRemove1)

        myAsteroids.append(newAst)
      

      # customer collision 
      if aliem != None:
        serve = aliem.checkCollision(ship)

        if serve and aliem.satiated:
          score += 100



    # Check to see if a bullet hit an asteroid.
    for a in myAsteroids:
      for b in bullets:

        if (a.isActive and b.isActive):
          smacked = a.checkCollision(b.x, b.y)

          if (smacked == True):
            b.setExplosion()
            a.isActive = False
            if not b.isActive: bullets.remove(b)
            myAsteroids.remove(a)
            score += 5

    # --- Screen-clearing code goes here

    # Here, we clear the screen to black. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)

    # --- Drawing code should go here

    # Bullets
    for b in bullets:
      b.drawMe(screen, RED)

    # Asteroids
    for a in myAsteroids:
      a.drawMe(screen)

    # Spaceship
    ship.drawMe(screen, ORANGE, basicShip)
      # game over
    if not ship.isActive:
      explosionAnim.play(screen)
      screen.blit(beegfont.render("Game Over", True, (255,255,255)), ((screenWidth / 2) - 116, (screenHeight / 2) - 128))

    if aliem != None:
      aliem.drawMe(screen)

    # remove later
    #p.draw.rect(screen, GREEN, p.Rect(0 - c.topLeftX, 0 - c.topLeftY, gameWidth, gameHeight), width = 2)

    # UI text
    txt = "Patties: " + str(ship.ammo)
    ammotxt = font.render(txt, True, (255,255,255))
    txt = "Hits: " + str(ship.lives)
    livestxt = font.render(txt, True, (255,255,255))
    txt = "Score: " + str(score)
    scoretxt = font.render(txt, True, (255,255,255))

    screen.blit(ammotxt, (20, screenHeight - 60))
    screen.blit(livestxt, (20, screenHeight - 110))
    screen.blit(scoretxt, (20, screenHeight - 160))


    # it's a sort of mini-display for the corner, so it should be drawn last on top of everything
    theGrill.drawMe(screen)
      
    # --- Go ahead and update the screen with what we've drawn.
    p.display.flip()

    # --- Limit to 60 frames per second. Tick game object timers here
    clock.tick(60)
    theGrill.tick()
    ship.tick()

    # Update frame count.
    tickTock = tickTock + 1

    # Implement shooting delay to keep bullet count lower.
    if (shotCount > 0):
      shotCount = shotCount - 1
    # Do some book keeping on arrays.
    # Remove inactive elements of bullets array.
    # Remove inactive elements of asteroids array.

    # replace objects in entities list
    entities.clear()
    # we don't want the ship in the list, else it will not stay centered
    # entities.append(ship)
    entities.append(myAsteroids)
    entities.append(bullets)
    if aliem != None: entities.append(aliem)

  # Close the window and quit.
  p.quit()

  return


asteroidMe()