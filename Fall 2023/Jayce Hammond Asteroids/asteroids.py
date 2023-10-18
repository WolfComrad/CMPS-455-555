import pygame as p
from pygame import mixer
import math
import numpy
import random as r
from PlayerScripts.ship import Ship
from AsteroidScripts.rock import Rock
from PlayerScripts.healthbar import HealthBar
from PlayerScripts.bullet import Bullet
from MenuScripts.button import Button
from powerup import Powerup
import os

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
GREY = (128,128,128)

#DISPLAY CONSTS

screenWidth, screenHeight = 700, 700
size = (screenWidth, screenHeight)

#PATHS
    #SPRITES
playerSprite = "Assets\SpaceshipAssets\spaceship.png"
#imgPaths = os.listdir("Assets\ParallaxAssets")
bg_imgs = []
for i in range(1, 5):
    bg_img = p.image.load(f"Assets/ParallaxAssets/plx-{i}.png")
    bg_imgs.append(bg_img)
bg_width = bg_imgs[0].get_width()
bg_height = bg_imgs[0].get_width()

#UI CONSTS
title = "Asteroid Souls"

#GAME CONSTS
clock = p.time.Clock()
objArray = []
asteroidArray = []
global scrollY
global scrollX
scrollY = 0
scrollX = 0


#GAME VARS
global bulletSize
global playerSpeed
playerSpeed = 10
bulletSize = 5
powerUpArr = ["heal", "bullet_size", "player_speed", "player_stamina"]

#INITIALIZE SOUND
p.mixer.init()
bg_music = p.mixer.Sound("Assets\SFX\StigmaDreamscapeTheme _eScape.wav")
shootSound = p.mixer.Sound("Assets\SFX\Laser.mp3")
bulletGrowSound = p.mixer.Sound("Assets\SFX\MushroomSoundEffect.mp3")
gunUpgradeSound = p.mixer.Sound("Assets\SFX\shotgun-reload.mp3")
speedUpSound = p.mixer.Sound("Assets\SFX\LimitBreakSoundEffect.mp3")

#INITIALIZE GAME
def gameInit():
    #GLOBAL VARS
    global screen
    global surface
    global player
    global healthBar
    p.init()
    bg_music.play(1)
    if state == "GAME":
        p.mouse.set_visible(False)
    else:
        p.mouse.set_visible(True)
    screen = p.display.set_mode(size, p.RESIZABLE) 
    p.display.set_caption(title)
    surface = p.Surface(size)
    #objArray.append(rock)
    player = Ship(screenWidth / 2, screenHeight / 2, playerSpeed, playerSprite, 10, 20, 0, 0, 100, size)
    healthBar = HealthBar(0, 675, player.health)

def displayTitle(screenWidth, screenHeight):
        font = p.font.Font("Assets\Evil Empire.otf", 100)
        text = font.render("Asteroid", True, ORANGE, BLACK)
        text2 = font.render("Souls", True, ORANGE, BLACK)
        textRect = text.get_rect()
        text2Rect = text.get_rect()
        textRect.center = (screenWidth / 2 ,150)
        text2Rect.center = (textRect.center[0]+ 80, 250)
        screen.blit(text, textRect)
        screen.blit(text2, text2Rect)


#DISPLAY GAME
def gameDisplay():
    screenWidth, screenHeight = p.display.get_surface().get_size()
    size = screenWidth, screenHeight
    if state == "GAME":
        #screen.fill(BLACK)
        draw_bg()
        drawMouse()
        player.display(screen, mousePos)
        healthBar.displayHealth(screen)
        healthBar.displayStaminaBars(screen, 3)
        buff = r.randint(0, len(powerUpArr))
        Powerup(screen, buff, r.randint(0, 700), r.randint(0, 700)).draw()
        displayObjArray()
        displayKills(killCount, 600, 675)
        for rock in asteroidArray:
            rock.display(screen)
        p.display.update()
        clock.tick(60)

    if state == "START":
        screen.fill(BLACK)
        global startButton
        startButton = Button("Start", screenWidth / 2, screenHeight / 2.15)
        optionsButton = Button("Options", screenWidth / 2, screenHeight / 1.95)
        quitButton = Button("Quit", screenWidth / 2, screenHeight / 1.75)
        displayTitle(screenWidth, screenHeight)
        startButton.display(screen)
        optionsButton.display(screen)
        quitButton.display(screen)
        p.display.update()
        clock.tick(60)
        return startButton
    
def draw_bg():
    global scrollX
    scrollX -= 10
    min = 0
    max = 5
    for x in range(min, max):
        speed = 1
        count = 0
        for img in bg_imgs:
            count += 1
            screen.blit(img, ((x * bg_width) + scrollX * speed, 0))
            if count > 1:
                speed += 0.8

        
        
    if abs(scrollX) > bg_width:
        scrollX += bg_width
    

def randomizeRockSpawn():
    rockSpawnX = 0
    rockSpawnY = r.randint(0,700)
    if rockSpawnY < 100: 
        rockSpawnX = r.randint(0,700)
    elif rockSpawnY > 600:
        rockSpawnX = r.randint(0,700)
    else:
        rockSpawnX = r.randint(0, 100) or r.randint(600, 700)

    rockSpawnZone = rockSpawnX, rockSpawnY
    return rockSpawnZone

def drawMouse():
    crosshair = p.image.load("Assets\crosshair.png")
    crosshairRect = crosshair.get_rect()
    crosshairRect.center = (mousePos)
    screen.blit(crosshair, crosshairRect)

def displayKills(count, x , y):
    font = p.font.Font("Assets\Evil Empire.otf", 40)
    text = font.render("Kills: " + str(count), True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)

def displayObjArray():
    if objArray:
        for bullet in objArray:
            bullet.display(screen)
            bullet.update()

def spawnRock(spawnNum):
    i = 0
    while i < spawnNum:
        rock = Rock(randomizeRockSpawn()[0], randomizeRockSpawn()[1], screen, size)
        asteroidArray.append(rock)
        i += 1

def resetGame():
    # Reset all game-related variables
    global killCount, mobCount, player, healthBar, objArray, asteroidArray, playerSpeed, bulletSize
    killCount = 0
    mobCount = 0
    playerSpeed = 10
    bulletSize = 5
    healthBar = HealthBar(0, 675, player.health)
    player.reset()
    objArray = []
    asteroidArray = []


def main():
    global killCount
    global state
    global mobCount
    xDir, yDir = 0, 0
    running = True
    killCount = 0
    mobCount = 0
    projectilesArr = []
    #STATE
    state = "START"
    spawnable = True
    gameInit()
    spawnRock(mobCount)
    bulletBuff = False
    speedBuff = False
    healBuff = False
    staminaBuff = False
    gunBuff = False
    while running:
        global mousePos
        global bulletSize
        global playerSpeed
        if mobCount > 15:
            mobCount = 0
        else:
            mobCount += 5
        mousePos = p.mouse.get_pos()
        if state == "START":
            for event in p.event.get():
                if event.type == p.QUIT:
                    return
                if event.type == p.MOUSEBUTTONDOWN:
                    if(mousePos[0] >= startButton.x - 45 and mousePos[0] <= 400):
                        state = "GAME"
            gameDisplay()
            
        if killCount >= 20 and bulletBuff == False:
            bulletSize += 15
            bulletGrowSound.play(0)
            bulletBuff = True
        if killCount >= 30 and speedBuff == False:
            speedUpSound.play(0)
            playerSpeed += 5
            speedBuff = True
        if killCount >= 50 and gunBuff == False:
            gunUpgradeSound.play(0)
            player.weapon = "SHOTGUN"
            gunBuff = True

        if state == "GAME":
            angle = player.getAngle(mousePos)
            if len(asteroidArray) == 0:
                spawnRock(mobCount)
            for event in p.event.get():
                p.event.set_grab(False)
                if event.type == p.QUIT:
                    return
                if event.type == p.KEYDOWN:
                    if event.key == p.K_ESCAPE:
                        return
                    if event.key == p.K_SPACE:
                       if player.dash_invulnerable(3, 0.75) == "heal":
                           healthBar.health += 20
                        
                    #CONTROLS
                    if event.key == p.K_w:
                        yDir = -1
                    if event.key == p.K_s:
                        yDir = 1
                    if event.key == p.K_d:
                        xDir = 1
                    if event.key == p.K_a:
                        xDir = -1
                    if event.key == p.K_q:
                        player.dash(3, 20)
                if event.type == p.KEYUP:
                    if event.key == p.K_w or event.key == p.K_s:
                        yDir = 0
                    if event.key == p.K_d or event.key == p.K_a:
                        xDir = 0
                if event.type == p.MOUSEBUTTONDOWN and p.mouse.get_pressed()[0] == True:
                    if player.weapon == "BASE":
                        shootSound.play(0)
                        shot = Bullet(player.posx, player.posy, RED, bulletSize, 20, angle)
                        objArray.append(shot)
                    if player.weapon == "SHOTGUN":
                        shootSound.play(0)
                        for i in range(0, 3):
                            if i == 0:
                                spreadShot = Bullet(player.posx, player.posy, GREEN, bulletSize, 20, angle - 45)
                            if i == 1:
                                spreadShot = Bullet(player.posx, player.posy, GREEN, bulletSize, 20,  angle)
                            if i == 2:
                                spreadShot = Bullet(player.posx, player.posy, GREEN, bulletSize, 20,  angle + 45)
                            objArray.append(spreadShot)


                            
                for bullet in objArray:
                    for rock in asteroidArray:
                        if bullet.check_collision(rock):
                            killCount += 1
                            rock.exploded = True
                            rock.explode(projectilesArr)
                            asteroidArray.remove(rock)
                            if bullet in objArray:
                                objArray.remove(bullet)
                for projectile in projectilesArr:
                    projectile.display()

            

    #UPDATE
            player.update(xDir, yDir)
            for rock in asteroidArray:
                rock.update()
            if healthBar.updateHealth(player.col.checkCollision(asteroidArray, xDir, player)):
                resetGame()
                state = "START"
    #DISPLAY
            gameDisplay()
            p.event.pump()


main()