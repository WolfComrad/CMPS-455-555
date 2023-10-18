import pygame
import sys
import random

pygame.init()

width, height = 1280, 720
font = pygame.font.SysFont("Pong", int(width/20))
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pong!")
clock = pygame.time.Clock()

# Paddles
player = pygame.Rect(width-110, height/2-50, 10, 100)
computer = pygame.Rect(110, height/2-50, 10, 100)
player_score, computer_score = 0, 0

# Ball
ball = pygame.Rect(width/2-10, height/2-10, 20, 20)
x_speed, y_speed = 1, 1


while True:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        if player.top > 0:
            player.top -= 2
    if keys[pygame.K_DOWN]:
        if player.bottom < height:
            player.bottom += 2
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if ball.y >= height:
        y_speed = -1
    if ball.y <= 0:
        y_speed = 1
    if ball.x <= 0:
        player_score += 1
        ball.center = (width/2, height/2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])

    if ball.x >= width:
        computer_score += 1
        ball.center = (width/2, height/2)
        x_speed, y_speed = random.choice([1, -1]), random.choice([1, -1])

    if player.x - ball.width <= ball.x <= player.x and ball.y in range(player.top-ball.width, player.bottom+ball.width):
        x_speed = -1
    if computer.x - ball.width <= ball.x <= computer.x and ball.y in range(computer.top-ball.width, computer.bottom+ball.width):
        x_speed = 1
    print(computer.x - ball.width, ball.x, ball.width)
    ball.x += x_speed * 2
    ball.y += y_speed * 2

    if computer.y < ball.y:
        computer.top += 2
    if computer.bottom > ball.y:
        computer.bottom -= 2

    player_score_text = font.render(str(player_score), True, "white")
    computer_score_text = font.render(str(computer_score), True, "white")

    screen.fill("black")
    pygame.draw.rect(screen, "white", player)
    pygame.draw.rect(screen, "white", computer)
    pygame.draw.circle(screen, "white", ball.center, 10)
    screen.blit(player_score_text, (width/2+50, 50))
    screen.blit(computer_score_text, (width/2-50, 50))
    pygame.display.update()
    clock.tick(100)
