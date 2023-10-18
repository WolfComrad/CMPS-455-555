import os
import pygame
import sys
import random


class GameState():
    def __init__(self):
        self.state = 'welcome'
        self.AI_counter = 0
        self.player_counter = 0
        self.ball_counter = 0
        self.shoot = 0
        # self.current_time = 0
        # self.shooting_time = 0
        # self.random_time = 0

    def welcome(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(event.pos):
                    self.state = 'game'
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        screen.fill((30, 15, 55))
        screen.blit(welcome_text1, welcome_text_rect1)
        screen.blit(welcome_text2, welcome_text_rect2)
        screen.blit(welcome_text3, welcome_text_rect3)
        screen.blit(welcome_text4, welcome_text_rect4)
        screen.blit(welcome_text5, welcome_text_rect5)
        screen.blit(welcome_text6, welcome_text_rect6)
        screen.blit(how_to_play_text1, how_to_play_text_rect1)
        screen.blit(how_to_play_text2, how_to_play_text_rect2)
        screen.blit(how_to_play_text3, how_to_play_text_rect3)
        screen.blit(how_to_play_text4, how_to_play_text_rect4)
        screen.blit(objective_text1, objective_text_rect1)
        screen.blit(objective_text2, objective_text_rect2)
        screen.blit(objective_text3, objective_text_rect3)
        screen.blit(objective_text4, objective_text_rect4)
        screen.blit(objective_text5, objective_text_rect5)
        pygame.draw.rect(screen, (80, 80, 255), start_button)
        screen.blit(start_text, (start_button.x + 10, start_button.y + 10))
        pygame.draw.rect(screen, (80, 80, 255), exit_button)
        screen.blit(exit_text, (exit_button.x + 10, exit_button.y + 10))
        pygame.display.flip()

    def game(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = 'welcome'
            self.game_reset()
        if keys[pygame.K_UP]:
            if player.rect.top > 0:  # player.rect.top
                player.rect.top -= 4  # player.rect.top
        if keys[pygame.K_DOWN]:
            if player.rect.bottom < height:  # player.rect.bottom
                player.rect.bottom += 4  # player.rect.bottom
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(player_group) is not 0:
                        player_bullet_group.add(player.create_bullet())
                        self.shooting_time = pygame.time.get_ticks()

        # Moving AI
        if len(AI_group) is not 0:
            if AI.rect.y < ball.rect.y-43:  # AI.rect.y
                AI.rect.top += 4  # AI.rect.top
            if AI.rect.bottom > ball.rect.y+73:  # AI.rect.bottom
                AI.rect.bottom -= 4  # AI.rect.bottom

        # AI shooting
        self.shoot = random.randrange(100)
        if self.shoot == 10 and len(AI_bullet_group) == 0 and len(AI_group) is not 0:
            AI_bullet_group.add(AI.create_bullet())

        # Reset after killed
        if len(AI_group) == 0:
            self.AI_counter += 1
            if self.AI_counter > 150:
                AI_group.add(AI)
                self.AI_counter = 0
        if len(player_group) == 0:
            self.player_counter += 1
            if self.player_counter > 150:
                player_group.add(player)
                self.player_counter = 0
        if len(ball_group) == 0:
            self.ball_counter += 1
            if self.ball_counter > 150:
                ball_group.add(ball)
                self.ball_counter = 0

        # End game
        if AI_points.game_end == True:
            self.state = 'AI_win'
            self.game_reset()
        if player_points.game_end == True:
            self.state = 'player_win'
            self.game_reset()

        pygame.display.flip()
        screen.blit(background, (0, 0))

        points_group.draw(screen)
        player_group.draw(screen)
        AI_group.draw(screen)
        ball_group.draw(screen)
        player_bullet_group.draw(screen)
        AI_bullet_group.draw(screen)

        player_bullet_group.update(player)
        AI_bullet_group.update(AI)
        ball_group.update()

    def AI_win(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_AI_button.collidepoint(event.pos):
                    self.state = 'game'
                if exit_AI_win_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if back_AI_win_button.collidepoint(event.pos):
                    self.state = 'welcome'

        screen.fill((30, 15, 55))
        screen.blit(AI_win_text, AI_win_text_rect)
        pygame.draw.rect(screen, (80, 80, 255), play_again_AI_button)
        screen.blit(play_again_AI_text, (play_again_AI_button.x +
                    10, play_again_AI_button.y + 10))
        pygame.draw.rect(screen, (80, 80, 255), back_AI_win_button)
        screen.blit(back_AI_win_text, (back_AI_win_button.x +
                    10, back_AI_win_button.y + 10))
        pygame.draw.rect(screen, (80, 80, 255), exit_AI_win_button)
        screen.blit(exit_AI_win_text, (exit_AI_win_button.x +
                    10, exit_AI_win_button.y + 10))
        pygame.display.flip()

    def player_win(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_player_button.collidepoint(event.pos):
                    self.state = 'game'
                if exit_player_win_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                if back_player_win_button.collidepoint(event.pos):
                    self.state = 'welcome'

        screen.fill((30, 15, 55))
        screen.blit(player_win_text, player_win_text_rect)
        pygame.draw.rect(screen, (80, 80, 255), play_again_AI_button)
        screen.blit(play_again_player_text, (play_again_player_button.x +
                    10, play_again_player_button.y + 10))
        pygame.draw.rect(screen, (80, 80, 255), back_player_win_button)
        screen.blit(back_player_win_text, (back_player_win_button.x +
                    10, back_player_win_button.y + 10))
        pygame.draw.rect(screen, (80, 80, 255), exit_player_win_button)
        screen.blit(exit_player_win_text, (exit_player_win_button.x +
                    10, exit_player_win_button.y + 10))
        pygame.display.flip()

    def state_manager(self):
        if self.state == 'welcome':
            self.welcome()
        if self.state == 'game':
            self.game()
        if self.state == 'AI_win':
            self.AI_win()
        if self.state == 'player_win':
            self.player_win()

    def game_reset(self):
        player_points.reset()
        AI_points.reset()
        player.reset()
        AI.reset()
        ball.reset()
        player_bullet_group.empty()


# need to fix bullet collisions
class Bullet(pygame.sprite.Sprite):      
    def __init__(self, pos_x, pos_y, pic):
        super().__init__()
        self.image = pygame.image.load(pic)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))

    def update(self, who):
        if who == player:
            self.rect.x -= 10
        if who == AI:
            self.rect.x += 10
        if self.rect.x >= width + 200 or self.rect.x <= -200:
            self.kill()
        if pygame.sprite.groupcollide(player_bullet_group, AI_group, False, False):
            AI.hit()
            player_points.gain_point()
            self.kill()
        if pygame.sprite.groupcollide(AI_bullet_group, player_group, False, False):
            player.hit()
            AI_points.gain_point()
            self.kill()
        if pygame.sprite.groupcollide(player_bullet_group, ball_group, False, False):
            ball.hit()
            player_points.loose_point()
            self.kill()
        if pygame.sprite.groupcollide(AI_bullet_group, ball_group, False, False):
            ball.hit()
            AI_points.loose_point()
            self.kill()
        if pygame.sprite.groupcollide(AI_bullet_group, player_bullet_group, False, False):
            AI_b_hits = pygame.sprite.groupcollide(
                AI_bullet_group, player_bullet_group, False, False)
            player_b_hits = pygame.sprite.groupcollide(
                player_bullet_group, AI_bullet_group, False, False)
            for i, j in zip(AI_b_hits, player_b_hits):
                AI_bullet_group.remove(i)
                player_bullet_group.remove(j)

    def reset(self):
        self.kill()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('shpong/ship2.png')
        self.rect = self.image.get_rect(center=(width - 80, height/2))

    def create_bullet(self):
        return Bullet(player.rect.midleft[0], player.rect.midleft[1], 'shpong/ship2Bullet.png')

    def hit(self):
        self.kill()
        self.reset()

    def reset(self):
        self.rect = self.image.get_rect(center=(width - 80, height/2))


class AI(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('shpong/ship1.png')
        self.rect = self.image.get_rect(center=(80, height/2))

    def create_bullet(self):
        return Bullet(AI.rect.midright[0], AI.rect.midright[1], 'shpong/ship1Bullet.png')

    def hit(self):
        self.kill()
        self.reset()

    def reset(self):
        self.rect = self.image.get_rect(center=(80, height/2))


class Points(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super().__init__()
        self.sprites = []
        self.next = False
        self.game_end = False
        self.sprites.append(pygame.image.load("shpong/points/0.png"))
        self.sprites.append(pygame.image.load("shpong/points/1.png"))
        self.sprites.append(pygame.image.load("shpong/points/2.png"))
        self.sprites.append(pygame.image.load("shpong/points/3.png"))
        self.sprites.append(pygame.image.load("shpong/points/4.png"))
        self.sprites.append(pygame.image.load("shpong/points/5.png"))
        self.sprites.append(pygame.image.load("shpong/points/6.png"))
        self.sprites.append(pygame.image.load("shpong/points/7.png"))
        self.sprites.append(pygame.image.load("shpong/points/8.png"))
        self.sprites.append(pygame.image.load("shpong/points/9.png"))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [x_pos, y_pos]

    def point_won(self):
        self.next = True

    def update(self):
        if self.next == True:
            # self.current_sprite += 1
            if self.current_sprite >= len(self.sprites):
                self.game_end = True
                self.next = False
            if self.current_sprite <= 9:
                self.image = self.sprites[int(self.current_sprite)]
                self.next = False
                ball.reset()

    def reset(self):
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

    def loose_point(self):
        if self.current_sprite > 0:
            self.current_sprite -= 1
            self.image = self.sprites[int(self.current_sprite)]

    def gain_point(self):
        if self.current_sprite < 9:
            self.current_sprite += 1
            self.image = self.sprites[int(self.current_sprite)]


class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(
            "shpong/planets/" + random.choice(os.listdir("shpong/planets")))
        self.rect = self.image.get_rect(center=(width//2, height//2))
        self.x_speed, self.y_speed = random.choice(
            [1, -1]), random.choice([1, -1])

    def update(self):
        if self.rect.y >= height - 30:
            self.y_speed = -1
        if self.rect.y <= 0:
            self.y_speed = 1
        if self.rect.x <= 0:
            player_points.next = True
            if player_points.current_sprite < 10:
                player_points.current_sprite += 1
            points_group.update()
            self.rect.center = (width/2, height/2)
            self.x_speed, self.y_speed = random.choice(
                [1, -1]), random.choice([1, -1])

        if self.rect.x >= width:
            AI_points.next = True
            if AI_points.current_sprite < 10:
                AI_points.current_sprite += 1
            points_group.update()
            self.rect.center = (width/2, height/2)
            self.x_speed, self.y_speed = random.choice(
                [1, -1]), random.choice([1, -1])

        if pygame.sprite.groupcollide(ball_group, player_group, False, False):
            self.x_speed = -1
        if pygame.sprite.groupcollide(ball_group, AI_group, False, False):
            self.x_speed = 1

        self.rect.x += self.x_speed * 3
        self.rect.y += self.y_speed * 3

    def hit(self):
        self.kill()
        self.reset()

    def reset(self):
        self.image = pygame.image.load(
            "shpong/planets/" + random.choice(os.listdir("shpong/planets")))
        self.rect = self.image.get_rect(center=(width//2, height//2))
        self.x_speed, self.y_speed = random.choice(
            [1, -1]), random.choice([1, -1])


# Setup
pygame.init()
width, height = 1280, 720
clock = pygame.time.Clock()
game_state = GameState()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Galactic Pong")
hit_time = 0
current_time = 0

# Welcome screen texts and fonts
big_font = pygame.font.Font('fonts/Futurewave.ttf', 42)
small_font = pygame.font.Font('fonts/Futurewave.ttf', 25)
welcome_text1 = big_font.render(
    "WELCOME TO GALACTIC PONG!!", True, (25, 255, 25))
welcome_text_rect1 = welcome_text1.get_rect()
welcome_text_rect1.center = (width//2, height//8)
welcome_text2 = small_font.render(
    "Prepare for an epic journey through the cosmos like never before.", True, (25, 255, 25))
welcome_text_rect2 = welcome_text2.get_rect()
welcome_text_rect2.topleft = (width//175, height//5)
welcome_text3 = small_font.render(
    "As you step into your high-tech spaceship, the fate of the universe", True, (25, 255, 25))
welcome_text_rect3 = welcome_text2.get_rect()
welcome_text_rect3.topleft = (width//175, height//4)
welcome_text4 = small_font.render(
    "rests in your hands. It's time to embark on a mission of galactic", True, (25, 255, 25))
welcome_text_rect4 = welcome_text2.get_rect()
welcome_text_rect4.topleft = (width//175, height//3.3)
welcome_text5 = small_font.render(
    "proportions and become the ultimate Pong Blaster!", True, (25, 255, 25))
welcome_text_rect5 = welcome_text2.get_rect()
welcome_text_rect5.topleft = (width//175, height//2.8)
welcome_text6 = big_font.render(
    "how to play", True, (25, 255, 25))
welcome_text_rect6 = welcome_text6.get_rect()
welcome_text_rect6.center = (width//1.4, height//2.2)
how_to_play_text1 = small_font.render(
    "Move up: up arrow", True, (25, 255, 25))
how_to_play_text_rect1 = how_to_play_text1.get_rect()
how_to_play_text_rect1.center = (width//1.4, height//1.9)
how_to_play_text2 = small_font.render(
    "Move down: down arrow", True, (25, 255, 25))
how_to_play_text_rect2 = how_to_play_text2.get_rect()
how_to_play_text_rect2.center = (width//1.4, height//1.75)
how_to_play_text3 = small_font.render(
    "shoot: space bar", True, (25, 255, 25))
how_to_play_text_rect3 = how_to_play_text3.get_rect()
how_to_play_text_rect3.center = (width//1.4, height//1.61)
how_to_play_text4 = small_font.render(
    "Exit: esc key", True, (25, 255, 25))
how_to_play_text_rect4 = how_to_play_text4.get_rect()
how_to_play_text_rect4.center = (width//1.4, height//1.49)
objective_text1 = big_font.render(
    "objective", True, (25, 255, 25))
objective_text_rect1 = objective_text1.get_rect()
objective_text_rect1.center = (width//3.4, height//2.2)
objective_text2 = small_font.render(
    "get 10 points", True, (25, 255, 25))
objective_text_rect2 = objective_text2.get_rect()
objective_text_rect2.center = (width//3.4, height//1.9)
objective_text3 = small_font.render(
    "+1 for scoring with ball", True, (25, 255, 25))
objective_text_rect3 = objective_text3.get_rect()
objective_text_rect3.center = (width//3.4, height//1.75)
objective_text4 = small_font.render(
    "+1 hitting enemy ship", True, (25, 255, 25))
objective_text_rect4 = objective_text4.get_rect()
objective_text_rect4.center = (width//3.4, height//1.62)
objective_text5 = small_font.render(
    "-1 for hitting the ball", True, (25, 255, 25))
objective_text_rect5 = objective_text5.get_rect()
objective_text_rect5.center = (width//3.4, height//1.49)

# Welcome screen buttons
button_font = pygame.font.Font('fonts/Futurewave.ttf', 20)
start_text = button_font.render("Start", True, (25, 255, 25))
start_button = pygame.Rect(width//4, height//1.3, 105, 35)
exit_text = button_font.render("Leave", True, (25, 255, 25))
exit_button = pygame.Rect(width//1.5, height//1.3, 110, 35)

# Player win page
player_win_text = big_font.render(
    "YOU WON!!", True, (25, 255, 25))
player_win_text_rect = player_win_text.get_rect()
player_win_text_rect.center = (width//2, height//5)
button_font = pygame.font.Font('fonts/Futurewave.ttf', 20)
play_again_player_text = button_font.render("Play again", True, (25, 255, 25))
play_again_player_button = pygame.Rect(width//7, height//2, 170, 35)
exit_player_win_text = button_font.render("Leave", True, (25, 255, 25))
exit_player_win_button = pygame.Rect(width//2.3, height//2, 110, 35)
back_player_win_text = button_font.render("Main Menu", True, (25, 255, 25))
back_player_win_button = pygame.Rect(width//1.5, height//2, 179, 35)

# AI win page
AI_win_text = big_font.render(
    "THE COMPUTER WON!!", True, (25, 255, 25))
AI_win_text_rect = AI_win_text.get_rect()
AI_win_text_rect.center = (width//2, height//5)
button_font = pygame.font.Font('fonts/Futurewave.ttf', 20)
play_again_AI_text = button_font.render("Play again", True, (25, 255, 25))
play_again_AI_button = pygame.Rect(width//7, height//2, 170, 35)
exit_AI_win_text = button_font.render("Leave", True, (25, 255, 25))
exit_AI_win_button = pygame.Rect(width//2.3, height//2, 110, 35)
back_AI_win_text = button_font.render("Main Menu", True, (25, 255, 25))
back_AI_win_button = pygame.Rect(width//1.5, height//2, 179, 35)

# Game screen stuff
background = pygame.image.load('spacebackgrounds/GreenNebula7.png')
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
AI = AI()
AI_group = pygame.sprite.Group()
AI_group.add(AI)
player_bullet_group = pygame.sprite.Group()
AI_bullet_group = pygame.sprite.Group()
ball = Ball()
ball_group = pygame.sprite.Group()
ball_group.add(ball)
player_points = Points(width - 30, 5)
AI_points = Points(7, 5)
points_group = pygame.sprite.Group()
points_group.add(player_points)
points_group.add(AI_points)

while True:
    game_state.state_manager()
    clock.tick(100)
