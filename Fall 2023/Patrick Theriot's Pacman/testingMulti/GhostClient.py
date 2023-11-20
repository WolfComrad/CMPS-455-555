import pygame, math
from board import boards
from network import Network
import Pygame_Lights
from YouWon import youwon
from YouLost import youlost

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps = 60
pygame.display.set_caption("Client2")
level = boards
for i in range(len(level)):
    for j in range(len(level[i])):
        if level[i][j] == 9 or level[i][j] == 1:
            level[i][j] = 0
#*Can change the color*#
color = 'blue'
PI = math.pi
player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'sprites/Pacman/{i}.png'), (38,38)))
ghost_images = []
for i in range(1,5):
    ghost_images.append(pygame.transform.scale(pygame.image.load(f'sprites/ghost1/{i}.png'), (38,38)))
kill_images = []
for i in range(1,5):
    kill_images.append(pygame.transform.scale(pygame.image.load(f'sprites/killghost/{i}.png'), (38,38)))
light_right = Pygame_Lights.LIGHT(500, Pygame_Lights.pixel_shader(500, (255,255,255), 1, True, 0, 90))
light_left = Pygame_Lights.LIGHT(500, Pygame_Lights.pixel_shader(500, (255,255,255), 1, True, 180,90))
light_up = Pygame_Lights.LIGHT(500, Pygame_Lights.pixel_shader(500, (255,255,255), 1, True, 90,90))
light_down = Pygame_Lights.LIGHT(500, Pygame_Lights.pixel_shader(500, (255,255,255), 1, True, 270,90))


clientNumber = 0


def draw_board(lvl, flicker):
    num1 = ((HEIGHT - 50) // 32)
    num2 = ((WIDTH // 30))
    for i in range(len(lvl)):
        for j in range(len(lvl[i])):
            if lvl[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 +(0.5*num1)), 4)
            if lvl[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5*num2), i * num1 +(0.5*num1)), 10)
            if lvl[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5*num2), i * num1), (j * num2 + (0.5*num2), i * num1 + num1), 3)
            if lvl[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5*num1)), (j * num2 + num2, i * num1 + (0.5*num1)), 3)
            if lvl[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2*0.4)) - 2, (i * num1 + (0.5*num1)), num2, num1], 0, PI/2, 3)
            if lvl[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num2 + (num2*0.5)), (i * num1 + (0.5*num1)), num2, num1], PI/2, PI, 3)
            if lvl[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2*0.5)), (i * num1 - (0.4*num1)), num2, num1], PI, 3*PI/2, 3)
            if lvl[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * num2 - (num2*0.4)) - 2, (i * num1 - (0.4*num1)), num2, num1], 3*PI/2, 2*PI, 3)


class Player():
    def __init__(self, x, y, width, height, images):
        self.images = images
        self.direction = 0
        self.direction_command = 0
        self.turns_allowed = [False,False,False,False]
        self.speed = 2        
        self.score = 0
        self.x = x
        self.y = y
        self.centerx = self.x + 19
        self.centery = self.y + 19
        self.width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(x,y,width,height)
        self.vel = 3

    def draw(self):
        #* Right *#
        if self.direction == 0:
            screen.blit(self.images[0], (self.x,self.y))
        #* Left *#
        elif self.direction == 1:
            screen.blit(self.images[1], (self.x,self.y))
        #* Up *#
        elif self.direction == 2:
            screen.blit(self.images[2], (self.x,self.y))
        #* Down *#
        elif self.direction == 3:
            screen.blit(self.images[3], (self.x,self.y))

    def draw2(self, counter):
        #* Right *#
        if self.direction == 0:
            screen.blit(self.images[counter // 6], (self.x,self.y))
        #* Left *#
        elif self.direction == 1:
            screen.blit(pygame.transform.flip(self.images[counter // 6], True, False), (self.x,self.y))
        #* Up *#
        elif self.direction == 2:
            screen.blit(pygame.transform.rotate(self.images[counter // 6], 90), (self.x,self.y))
        #* Down *#
        elif self.direction == 3:
            screen.blit(pygame.transform.rotate(self.images[counter // 6], -90), (self.x,self.y))

    def move(self):
        #* R, L, U, D *#
        if self.direction == 0 and self.turns_allowed[1]:
            self.x += self.speed
        elif self.direction == 1 and self.turns_allowed[0]:
            self.x -= self.speed
        if self.direction == 2 and self.turns_allowed[2]:
            self.y -= self.speed
        elif self.direction == 3 and self.turns_allowed[3]:
            self.y += self.speed

        self.update()

    def check_position(self):
        turns = [False,False,False,False]
        num1 = ((HEIGHT-50)//32)
        num2 = (WIDTH//30)
        num3 = 15
        num4 = 18
        num5 = 10
        #* Check collisions based on centerx/y of player +/- num3 *#
        if self.centerx // 30 < 40:
            if self.direction == 0:
                if level[self.centery//num1][(self.centerx+num4)//num2] < 3:
                    turns[1] = True
            if self.direction == 1:
                if level[self.centery//num1][(self.centerx-num3)//num2] < 3:
                    turns[0] = True
            if self.direction == 2:
                if level[(self.centery+num3)//num1][self.centerx//num2] < 3:
                    turns[3] = True
            if self.direction == 3:
                if level[(self.centery-num3)//num1][self.centerx//num2] < 3:
                    turns[2] = True
            
            if self.direction == 2 or self.direction == 3:
                if 12 <= self.centerx % num2 <= 18:
                    if level[(self.centery+num5)//num1][self.centerx//num2] < 3:
                        turns[3] = True
                    if level[(self.centery-num3)//num1][self.centerx//num2] < 3:
                        turns[2] = True
                if 12 <= self.centery % num1 <= 18:
                    if level[self.centery//num1][(self.centerx-num2)//num2] < 3:
                        turns[1] = True
                    if level[self.centery//num1][(self.centerx+num2)//num2] < 3:
                        turns[0] = True
            if self.direction == 0 or self.direction == 1:
                #!Might need to change this
                if 12 <= self.centerx % num2 <= 18:
                    if level[(self.centery+num4)//num1][self.centerx//num2] < 3:
                        turns[3] = True
                    if level[(self.centery-num4)//num1][self.centerx//num2] < 3:
                        turns[2] = True
                if 12 <= self.centerx % num2 <= 18:
                    
                    if level[self.centery//num1][(self.centerx+num4)//num2] < 3:
                        turns[1] = True
                    if level[self.centery//num1][(self.centerx-num4)//num2] < 3:
                        turns[0] = True
                    
        else:
            turns[0] = True
            turns[1] = True
            
        return turns

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def eat(self):
        num1 = ((HEIGHT - 50) // 32)
        num2 = WIDTH//30
        if 0 < self.x < 1070:
            print(level[self.centery // num1][self.centerx // num2])
            if level[self.centery // num1][self.centerx // num2] == 1:
                print("yum")
                level[self.centery // num1][self.centerx // num2] = 0
            if level[self.centery // num1][self.centerx // num2] == 2:
                level[self.centery // num1][self.centerx // num2] = 0

def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1]), int(str[2]), int(str[3]), int(str[4]), int(str[5]), int(str[6])

def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1]) + "," + str(tup[2]) + "," + str(tup[3]) + "," + str(tup[4]) + "," + str(tup[5]) + "," + str(tup[6])

def redrawWindow(player, player2, flicker, counter, s):
    screen.fill('black')
    draw_board(level, flicker)
    player.draw()
    player2.draw2(counter)
    #Lighting ------

    if player.direction == 0:
        lights_display = pygame.Surface((screen.get_size()))
        
        lights_display.blit(global_light(screen.get_size(), 0), (0,0))
        light_right.main(s, lights_display, player.rect.midleft[0], player.rect.midleft[1])
        
        screen.blit(lights_display, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    elif player.direction == 1:
        lights_display = pygame.Surface((screen.get_size()))
        
        lights_display.blit(global_light(screen.get_size(), 0), (0,0))
        light_left.main(s, lights_display, player.rect.midright[0], player.rect.midright[1])
        
        screen.blit(lights_display, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    elif player.direction == 2:
        lights_display = pygame.Surface((screen.get_size()))
        
        lights_display.blit(global_light(screen.get_size(), 0), (0,0))
        light_up.main(s, lights_display, player.rect.midbottom[0], player.rect.midbottom[1])
        
        screen.blit(lights_display, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    elif player.direction == 3:
        lights_display = pygame.Surface((screen.get_size()))
        
        lights_display.blit(global_light(screen.get_size(), 0), (0,0))
        light_down.main(s, lights_display, player.rect.midtop[0], player.rect.midtop[1])
        
        screen.blit(lights_display, (0,0), special_flags=pygame.BLEND_RGBA_MULT)
    #---------------
    pygame.display.update()

def global_light(size,intensity):
    dark = pygame.Surface(size).convert_alpha()
    dark.fill((255,255,255, intensity))
    return dark

def main():
    run = True
    n = Network()
    startPos = read_pos(n.getPos())
    p = Player(startPos[0],startPos[1],38,38,ghost_images)
    p.direction = startPos[2]
    p2 = Player(0,0,38,38,player_images)
    clock = pygame.time.Clock()
    counter = 0
    counter2 = 0
    flicker = False
    shadow_objects = []

    while run:
        clock.tick(fps)
        p2Pos = read_pos(n.send(make_pos((p.x, p.y, p.direction, 0, 0, 0, 0))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.direction = p2Pos[2]
        
        if p2Pos[6] == 1:
            youlost()
        elif p2Pos[6] == 2:
            youwon()
        
        if p2Pos[4] == 1:
            p.images = kill_images
            #* Eating the ghost *#
            if p2Pos[3] == 1:
                p.x = 460
                p.y = 330
                p.images = ghost_images
        if p2Pos[4] == 0:
            p.images = ghost_images
        
        if p2Pos[5] == 1:
            p.x = 460
            p.y = 130
            p2.x = 460
            p2.y = 682
        
        p2.update()
        
        if counter < 17:
            counter += 1
        else:
            counter = 0
            flicker = True
        if counter2 < 25:
            counter2 += 1
            if counter2 > 5:
                flicker = False
        else:
            counter2 = 0
            flicker = True
            
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    p.direction_command = 0
                if event.key == pygame.K_a:
                    p.direction_command = 1
                if event.key == pygame.K_w:
                    p.direction_command = 2
                if event.key == pygame.K_s:
                    p.direction_command = 3
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d and p.direction_command == 0:
                    p.direction_command = p.direction
                if event.key == pygame.K_a and p.direction_command == 1:
                    p.direction_command = p.direction
                if event.key == pygame.K_w and p.direction_command == 2:
                    p.direction_command = p.direction
                if event.key == pygame.K_s and p.direction_command == 3:
                    p.direction_command = p.direction
                    
        if p.direction_command == 0 and p.turns_allowed[0]:
            p.direction = 0
        if p.direction_command == 1 and p.turns_allowed[1]:
            p.direction = 1
        if p.direction_command == 2 and p.turns_allowed[2]:
            p.direction = 2
        if p.direction_command == 3 and p.turns_allowed[3]:
            p.direction = 3

        if p.x > 950: #1010
            p.x = 10 #-47
        elif p.x < 10: #-10
            p.x = 950 #1000

        p.centerx = p.x + 19
        p.centery = p.y + 19
        p.turns_allowed = p.check_position()
        p.move()
        redrawWindow(p, p2, flicker, counter, shadow_objects)
main()