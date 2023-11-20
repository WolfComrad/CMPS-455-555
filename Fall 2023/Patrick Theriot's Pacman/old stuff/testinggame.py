import pygame, math
from board import boards

pygame.init()

WIDTH = 1000
HEIGHT = 800
screen = pygame.display.set_mode([WIDTH,HEIGHT])
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = boards
#*Can change the color*#
color = 'blue'
PI = math.pi
player_images = []
for i in range(1,5):
    player_images.append(pygame.transform.scale(pygame.image.load(f'sprites/Pacman/{i}.png'), (38,38)))
player_x = 460
player_y = 682
direction = 0
counter = 0
counter2 = 0
flicker = False
turns_allowed = [False,False,False,False]
direction_command = 0
player_speed = 2
score = 0

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10,765))

def eat(score):
    num1 = ((HEIGHT - 50) // 32)
    num2 = WIDTH//30
    if 0 < player_x < 1070:
        if level[center_y // num1][center_x // num2] == 1:
            level[center_y // num1][center_x // num2] = 0
            score += 10
        if level[center_y // num1][center_x // num2] == 2:
            level[center_y // num1][center_x // num2] = 0
            score += 50
            
    return score

def draw_board(lvl):
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
            if lvl[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5*num1)), (j * num2 + num2, i * num1 + (0.5*num1)), 3)

def draw_player():
    #* Right *#
    if direction == 0:
        screen.blit(player_images[counter // 6], (player_x,player_y))
    #* Left *#
    elif direction == 1:
        screen.blit(pygame.transform.flip(player_images[counter // 6], True, False), (player_x,player_y))
    #* Up *#
    elif direction == 2:
        screen.blit(pygame.transform.rotate(player_images[counter // 6], 90), (player_x,player_y))
    #* Down *#
    elif direction == 3:
        screen.blit(pygame.transform.rotate(player_images[counter // 6], -90), (player_x,player_y))

def check_position(centerx, centery):
    turns = [False, False, False, False]
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    pygame.draw.circle(screen, 'red', [centerx, centery], 2)
    num3 = 15
    num4 = 18
    num5 = 10

    grid_row = centery // num1
    grid_col = centerx // num2

    if grid_row >= 0 and grid_row < len(level) and grid_col >= 0 and grid_col < len(level[0]):
        if centerx // 30 < 40:
            if direction == 0:
                if level[grid_row][grid_col] < 3:
                    turns[1] = True
                if level[grid_row][grid_col - 1] < 3 and 12 <= centery % num1 <= 18:
                    turns[3] = True
                if level[grid_row][grid_col + 1] < 3 and 12 <= centery % num1 <= 18:
                    turns[2] = True

            if direction == 1:
                if level[grid_row][grid_col] < 3:
                    turns[0] = True
                if level[grid_row][grid_col - 1] < 3 and 12 <= centery % num1 <= 18:
                    turns[3] = True
                if level[grid_row][grid_col + 1] < 3 and 12 <= centery % num1 <= 18:
                    turns[2] = True

            if direction == 2:
                if level[grid_row][grid_col] < 3:
                    turns[3] = True
                if level[grid_row - 1][grid_col] < 3 and 12 <= centerx % num2 <= 18:
                    turns[1] = True
                if level[grid_row + 1][grid_col] < 3 and 12 <= centerx % num2 <= 18:
                    turns[0] = True

            if direction == 3:
                if level[grid_row][grid_col] < 3:
                    turns[2] = True
                if level[grid_row - 1][grid_col] < 3 and 12 <= centerx % num2 <= 18:
                    turns[1] = True
                if level[grid_row + 1][grid_col] < 3 and 12 <= centerx % num2 <= 18:
                    turns[0] = True

        else:
            turns[0] = True
            turns[1] = True

    return turns




    
def move_player(playx,playy):
        #* R, L, U, D *#
        if direction == 0 and turns_allowed[1]:
            playx += player_speed
        elif direction == 1 and turns_allowed[0]:
            playx -= player_speed
        if direction == 2 and turns_allowed[2]:
            playy -= player_speed
        elif direction == 3 and turns_allowed[3]:
            playy += player_speed
        return playx, playy
    
run = True
while run:
    timer.tick(fps)
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
        
    screen.fill('black')
    draw_board(level)
    draw_player()
    draw_misc()
    center_x = player_x + 19
    center_y = player_y + 19
    turns_allowed = check_position(center_x,center_y)
    player_x, player_y = move_player(player_x,player_y)
    score = eat(score)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                direction_command = 0
            if event.key == pygame.K_a:
                direction_command = 1
            if event.key == pygame.K_w:
                direction_command = 2
            if event.key == pygame.K_s:
                direction_command = 3
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_d and direction_command == 0:
                direction_command = direction
            if event.key == pygame.K_a and direction_command == 1:
                direction_command = direction
            if event.key == pygame.K_w and direction_command == 2:
                direction_command = direction
            if event.key == pygame.K_s and direction_command == 3:
                direction_command = direction
                
    # for i in range(4):
    #     if direction_command == i and turns_allowed[i]:
    #         direction = i
    
    if direction_command == 0 and turns_allowed[0]:
        direction = 0
    if direction_command == 1 and turns_allowed[1]:
        direction = 1
    if direction_command == 2 and turns_allowed[2]:
        direction = 2
    if direction_command == 3 and turns_allowed[3]:
        direction = 3
                
    if player_x > 1010:
        player_x = -47
    elif player_x < -10:
        player_x = 1000
        
    pygame.display.flip()
pygame.quit()