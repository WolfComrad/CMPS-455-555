import pygame as p
import math
import numpy
import random as r
from pygame import mixer

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

#Resolution Vars
screenWidth = 700
screenHeight = 700
size = (screenWidth, screenHeight)

#Game Loop Init
p.init()
mixer.init()
screen = p.display.set_mode(size)
p.display.set_caption("Definitely Normal Pong")
clock = p.time.Clock()
surface = p.Surface(size)


#GAME CONSTS
ballSpeed = 4
playerSpeed = 7
objArray = []
gunPic = "download.png"
parry_sound = p.mixer.Sound("parry.wav")
bg_sound = p.mixer.Sound("The Twinning - Final Fantasy XIV (Piano Arrangement).wav")
point_sound = p.mixer.Sound("Roblox Death Sound (Oof) - Sound Effect (HD).wav")
state = "RUNNING"
scoreGoal = 1000

#Object Classes
class Gun:
    def __init__(self, posx, posy, img, angle):
        self.posx = posx
        self.posy = posy
        self.img = img
        self.gun = p.image.load(self.img)
        self.angle = angle
        self.firing = False  # Add a flag to track if the gun is firing
        self.fire_cooldown = 15  # Add a cooldown period (in frames) between shots
        self.cooldown_counter = 0  # Initialize the cooldown counter
        self.col = False


    def display(self, posx, posy, mousePos):
        self.gun = p.image.load(self.img)
        self.gun = p.transform.rotate(self.gun, -numpy.clip(math.degrees(self.getAngle(mousePos)), -90, 90))
        screen.blit(self.gun,(posx, posy))
        

    def update(self, posx, posy):
        self.posx = posx
        self.posy = posy

    def fire(self):
        if not self.firing and self.cooldown_counter <= 0:
            self.firing = True
            self.cooldown_counter = self.fire_cooldown
            return True
        return False

    def updateCooldown(self):
        if self.cooldown_counter > 0:
            self.cooldown_counter -= 1
            if self.cooldown_counter == 0:
                self.firing = False
    
    def getAngle(self, mouse_pos):
        # Lock the x-coordinate of the mouse at x = 325
        mouse_x_locked = 325
        mouse_y = mouse_pos[1]  # Get the y-coordinate of the mouse

        # Calculate the angle in radians
        angle = math.atan2(mouse_y - self.posy, mouse_x_locked - self.posx)

        # Convert the angle to degrees and ensure it's within -90 to 90 degrees
        angle_degrees = math.degrees(angle)
        adjusted_angle_degrees = angle_degrees if -90 <= angle_degrees <= 90 else (angle_degrees + 180) % 360 - 180

        # Convert the angle back to radians
        adjusted_angle = math.radians(adjusted_angle_degrees)

        return adjusted_angle

class Paddle:
    def __init__(self, posx, posy, width, height, speed, color, name, parry_duration, parry_timer, player, bulletRadius, bulletSpeed):
        self.posx = posx
        self.posy = posy
        self.width = width
        self.height = height
        self.speed = speed
        self.color = color
        self.radius = width / 2
        self.name = name

        #STUPID PARRY ASSIGNMENT
        self.parry_duration = parry_duration
        self.parry_timer = parry_timer
        self.player = player
        self.bulletRadius = bulletRadius
        self.bulletSpeed = bulletSpeed

        self.col = p.Rect(posx, posy, width, height)
        self.paddle = p.draw.rect(screen, self.color, self.col)

        self.parry_mode = True

    def display(self):
        self.paddle = p.draw.rect(screen, self.color, self.col)


    def update(self, yDir):
        self.posy = self.posy + self.speed * yDir

        if yDir < 0:
            yDir = -1
        elif yDir >= 0:
            yDir = 1

        if self.posy <= 25:
            self.posy = 25
        elif self.posy + self.height >= 675:
            self.posy = 675 - self.height

        self.col = (self.posx, self.posy, self.width, self.height)

    def cpuUpdate(self, yDir, yPos):
        if self.speed > 0:
            self.posy = yPos
            self.posy = self.posy + self.speed * yDir
        elif self.speed == 0:
            self.posy = yPos

        if yDir < 0:
            yDir = -1
        elif yDir >= 0:
            yDir = 1

        if self.posy <= 25:
            self.posy = 25
        elif self.posy + self.height >= 675:
            self.posy = 675 - self.height

        self.col = (self.posx, self.posy, self.width, self.height)

    def getRect(self):
        return self.paddle
    
    def cpuParry(self, CPU, parry_duration, parry_timer, player, bulletRadius, bulletSpeed):
            # Parry mechanic for CPU
            if not CPU.parry_mode:
                parry_timer += 1
                if parry_timer >= parry_duration:
                    # Enter "parry" mode and reset the timer
                    CPU.parry_mode = True
                    parry_timer = 0

            # When in "parry" mode, CPU fires bullets randomly
            if CPU.parry_mode and r.randint(0, 25) < 5:  # Adjust the probability as needed
                # Fire a bullet towards the player's position
                angle_to_player = math.atan2(player.posy - CPU.posy, player.posx - CPU.posx)
                parry_sound.play()
                bullet = Bullet(CPU.posx + 10, CPU.posy + 10, RED, bulletRadius, bulletSpeed, angle_to_player, "BULLET")
                objArray.append(bullet)

            # ...

            # When leaving "parry" mode, reset the timer and flag
            if parry_timer >= parry_duration:
                CPU.parry_mode = False
                parry_timer = 0
    
    def check_collision(self, ball):
        # Calculate the distance between the ball's center and the paddle's center
        dist_x = abs(ball.posx - (self.posx + self.width / 2))
        dist_y = abs(ball.posy - (self.posy + self.height / 2))

        # Calculate the half-width and half-height of the paddle
        half_width = self.width / 2
        half_height = self.height / 2

        # Check if the ball is within a certain distance from the paddle's center
        if dist_x <= (half_width + ball.radius) and dist_y <= (half_height + ball.radius):
            if self.name == "PLAYER":
                ball.posx = (self.posx + self.width) + ball.radius
            elif self.name == "CPU":
                ball.posx = self.posx - ball.radius
            if ball.name == "BULLET" and self.name == "CPU":
                self.cpuParry(self, self.parry_duration, self.parry_timer, self.player, self.bulletRadius, self.bulletSpeed)
            return True  # Collision occurred
        return False
    
class Ball:
    def __init__(self, posx, posy, radius, speed, color, name):
        self.posx = posx
        self.posy = posy
        self.radius = radius
        self.speed = speed
        self.color = color
        self.name = name

        self.xDir = 1
        self.yDir = -1
        self.ball = p.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
        self.firstTime = 1

    def display(self):
        self.ball = p.draw.circle(screen, self.color, (self.posx, self.posy), self.radius)
    
    def update(self):
        self.posx += self.speed * self.xDir
        self.posy += self.speed * self.yDir 

        if self.posy <= 51 or self.posy >= screenHeight - 51:
            self.yDir *= -1
        elif self.posx <= 51 or self.posx >= screenWidth - 51:
            self.xDir *= -1
        
        if self.posx <= 50 and self.firstTime:
            self.firstTime = 0
            return 1
        elif self.posx >= 650 and self.firstTime:
            self.firstTime = 0
            return -1
        else:
            return 0
        
    def reset(self):
        self.posx = (screenWidth - 50) // 2
        self.posy = (screenHeight - 50) // 2
        self.xDir *= -1
        self.yDir *= -1
        self.firstTime= 1

        self.speed = 7

        

    def hit(self):
        self.xDir *= -1

    def getRect(self):
        return self.ball

class Bullet:
    def __init__(self, posx, posy, color, radius, speed, angle, name):
        self.posx = posx
        self.posy = posy
        self.color = color
        self.radius = radius
        self.speed = speed
        self.angle = angle
        self.name = name

        bLength = 20
        self.posx, self.posy = self.calculateInitialPosition(posx, posy, angle, bLength)

        self.bullet = p.draw.circle(screen, RED, (self.posx, self.posy), self.radius)
        self.rect = p.Rect(self.posx - self.radius, self.posy - self.radius, 2 * self.radius, 2 * self.radius)

    def display(self):
        self.bullet = p.draw.circle(screen, RED, (self.posx, self.posy), self.radius)

    def getRect(self):
        return self.rect

    def update(self):
        self.posx += self.speed * math.cos(self.angle)
        self.posy += self.speed * math.sin(self.angle)

    def calculateInitialPosition(self, posx, posy, angle, distance):
        new_x = posx + distance * math.cos(angle)
        new_y = posy + distance * math.sin(angle)

        return new_x, new_y
    
    def check_collision(self, ball):
        # Calculate the distance between the bullet and the center of the ball
        distance = math.sqrt((self.posx - ball.posx) ** 2 + (self.posy - ball.posy) ** 2)

        # Check if a collision has occurred (assuming the bullet radius is small)
        if distance < self.radius + ball.radius:
            if ball.name == "CPU":
                return True
            elif ball.name == "BALL":    
                # Calculate the angle between the bullet and the ball's center
                angle = math.atan2(ball.posy - self.posy, ball.posx - self.posx)

                # Calculate the new velocity components for the ball
                ball.posx += 5 * ball.xDir
                ball.speed += 1  # Increase ball speed
                ball.xDir = math.cos(angle)  # Adjust x-direction
                ball.yDir = math.sin(angle)  # Adjust y-direction

                return True  # Collision occurred
        return False



#Display Methods
def displayScore(playerScore, cpuScore, x , y):
    font = p.font.Font("Evil Empire.otf", 75)
    text = font.render((str(playerScore) + " : " + str(cpuScore)), True, WHITE, BLACK)
    textRect = text.get_rect()
    textRect.center = (x, y)

    screen.blit(text, textRect)

def displayWinner(name,score, x, y):
    font = p.font.Font("Evil Empire.otf", 50)
    text = font.render((name + " Wins"), True, WHITE, BLACK)
    restart = font.render(("Press any key to restart"), True, WHITE, BLACK)
    restartRect = restart.get_rect()
    textRect = text.get_rect()
    restartRect.center = (x, y + 80)
    textRect.center = (x, y)
    screen.blit(text, textRect)
    screen.blit(restart, restartRect)

    
def drawTable():
    table = p.draw.rect(screen, WHITE, p.Rect(25,25, 650, 650), 2)
    return table
def getMousePos():
    coords = p.mouse.get_pos()
    return coords






def main():
    bg_sound.play(1)
    #Declare Objects
    cpuSpeed = ballSpeed
    cpu_slowdown_duration = 50
    # Timer for CPU "parry" mode
    parry_timer = 0
    parry_duration = 100  # Adjust the duration as needed (number of frames)
    cpu_freeze_flag = False
    collided = False

    bulletSpeed = 20
    bulletRadius = 5
    firing = False
    
    player = Paddle(50, 300, 50, 100, playerSpeed, GREEN, "PLAYER", None, None, None, None, None)
    CPU = Paddle(600, 300, 50, 100, cpuSpeed, GREEN, "CPU", parry_duration, parry_timer, player, bulletRadius, bulletSpeed)
    ball = Ball((screenWidth - 50) // 2, (screenHeight - 50) // 2, 20, ballSpeed, WHITE, "BALL")
    gun = Gun(player.posx, player.posy, gunPic, 0)
    

    #Declare Collision and Velocity Vars
    playerDir = 0
    colliders = [player, CPU]

    #Declare Game Loop Vars
    playerScore, cpuScore = 0, 0
    running = True

    #p.mouse.set_visible(False)
    while running:
        # Check for collisions between ball and paddles
        if player.check_collision(ball) and collided == False:
            collided = True
            ball.hit()  # Handle the bounce
        if CPU.check_collision(ball) and collided == False:
            collided = True
            ball.hit()  # Handle the bounce


        if cpu_freeze_flag == True:
            cpu_slowdown_duration -= 1

        if cpu_slowdown_duration == 0:
            cpu_freeze_flag = False

#Controls
        coords = p.mouse.get_pos()
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False
            if event.type == p.KEYDOWN:
                if event.key == p.K_w:
                    playerDir = -1
                if event.key == p.K_s:
                    playerDir = 1
            if event.type == p.KEYUP:
                if event.key == p.K_w or event.key == p.K_s:
                    playerDir = 0
            if event.type == p.MOUSEBUTTONUP and event.button == 1:
                if gun.fire():
                    firing = True
                    gun.angle = gun.getAngle(coords)
                    bullet = Bullet(player.posx + 10, player.posy + 10, RED, bulletRadius, bulletSpeed, gun.angle, "BULLET")
                    objArray.append(bullet)

        for bullet in objArray:
            bullet.check_collision(ball)
            #print("ball collision")
            if CPU.check_collision(bullet):
                cpu_freeze_flag = True


        #Remove Bullets
            # Check if the bullet is off-screen
            if bullet.posx < 0 or bullet.posx > screenWidth:
                objArray.remove(bullet)

            # Check for collisions with the ball or paddles
            if bullet.check_collision(ball) or any(paddle.check_collision(bullet) for paddle in colliders) and firing == False:
                objArray.remove(bullet)


        screen.fill(BLACK)
        drawTable()
        player.update(playerDir)

        if cpu_freeze_flag == False:
            CPU.cpuUpdate(ball.yDir, ball.posy)


        gun.update(player.posx, player.posy)
        gun.updateCooldown()
        point = ball.update()
        displayScore(playerScore, cpuScore, screenWidth // 2, 75)
        #print((-math.atan(coords[1]/325)) * (180 * math.pi))
        

#Update Scores
        # -1 --> Player gets point
        # 1  --> CPU gets point
        if point == -1:
            playerScore += 1
            point_sound.play()
        elif point == 1:
            cpuScore += 1
            point_sound.play()

        if point != 0:
            cpu_freeze_flag = False
            ball.reset()
            point = 0

        for bullet in objArray:
            bullet.update()
            bullet.display()

        if playerScore >= scoreGoal:
            state = "PAUSED"
            while state == "PAUSED":
                displayWinner("Player 1 ", playerScore, 325, 325)
                for event in p.event.get():
                    if event.type == p.QUIT:
                        running = False
                        quit()
                    if event.type == p.KEYDOWN:
                        main()

                CPU.display()
                player.display()
                gun.display(player.posx, player.posy, coords)
                p.display.update()
                clock.tick(60)

        if cpuScore >= scoreGoal:
            state = "PAUSED"
            while state == "PAUSED":
                displayWinner("CPU ", cpuScore, 350, 325)
                for event in p.event.get():
                    if event.type == p.QUIT:
                        running = False
                        quit()
                    if event.type == p.KEYDOWN:
                        main()

                CPU.display()
                player.display()
                gun.display(player.posx, player.posy, coords)
                p.display.update()
                clock.tick(60)
            


#Display Scene
        CPU.display()
        player.display()
        gun.display(player.posx, player.posy, coords)
        #bullet.display()
        ball.display()
        p.display.update()
        displayScore(playerScore, cpuScore, 500, 75)
        clock.tick(60)

        collided = False
        firing = False


main()