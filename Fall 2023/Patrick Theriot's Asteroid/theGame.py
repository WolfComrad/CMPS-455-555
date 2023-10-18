import pygame, sys, math, random, numpy

class GameState():
    def __init__(self):
        self.state = 'level_three' #welcome
        self.count = 0
        self.level = 2 #0
        self.base_start = True
        self.shoot = False
        
    def welcome(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(event.pos):
                    self.state = 'level_one'
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
         
        pygame.display.flip()
        screen.blit(background, (0,0)) 
        screen.blit(welcome_text1,welcome_text1_rect1)
        screen.blit(welcome_text2,welcome_text2_rect2)
        screen.blit(welcome_text3,welcome_text3_rect3)
        screen.blit(welcome_text4,welcome_text4_rect4)
        screen.blit(welcome_text5,welcome_text5_rect5)
        screen.blit(welcome_text6,welcome_text6_rect6)
        screen.blit(welcome_text7,welcome_text7_rect7)
        screen.blit(welcome_text8,welcome_text8_rect8)
        screen.blit(welcome_text9,welcome_text9_rect9)
        screen.blit(welcome_text10,welcome_text10_rect10)
        screen.blit(start_button_image,start_button)
        screen.blit(exit_button_image,exit_button)
        
    #TODO: Fix explosions
    #* Normal Asteroids
    def level_one(self):
        self.count += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = 'welcome'
            self.game_reset()
        if keys[pygame.K_w]:
            player.moveForword()
        if keys[pygame.K_a]:
            player.turnLeft()
        if keys[pygame.K_d]:
            player.turnRight()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(player_group) is not 0:
                        player_bullet_group.add(player.create_bullet())
        if self.count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            asteroids_group.add(Asteroids(ran))
        
        if player.lives <= 0:
            self.level = 0
            self.state = "loose"
            self.game_reset()
        if player.points >= 15:
            self.level += 1
            self.state = "win"
            self.game_reset()
        
        pygame.display.flip()
        screen.blit(background, (0,0))
        screen.blit(player.rotatedImage,player.rotatedRect)
        player_bullet_group.draw(screen)
        asteroids_group.draw(screen)
        #! Uncomment this for explosions
        #explosions_group.draw(screen)
        
        player_bullet_group.update(player)
        player.offScreen()
        asteroids_group.update()
        #! Uncomment this for explosions
        #explosions_group.update(1)
        
        self.show_score()
    
    #* Space Pirates
    def level_two(self):
        self.count += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = 'welcome'
            self.game_reset()
        if keys[pygame.K_w]:
            player.moveForword()
        if keys[pygame.K_a]:
            player.turnLeft()
        if keys[pygame.K_d]:
            player.turnRight()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(player_group) is not 0:
                        player_bullet_group.add(player.create_bullet())
                        
        if player.lives <= 0:
            self.level -= 1
            self.game_reset()
            self.state = "loose"
        if not space_pirates_group:
            self.game_reset()
            self.level += 1
            self.state = "win2"
            
        if self.count % 30 == 0:
            if enemy1.dead == False:
                space_pirates_bullet_group.add(enemy1.create_bullet())
        if self.count % 40 == 0:
            if enemy2.dead == False:
                space_pirates_bullet_group.add(enemy2.create_bullet())
        if self.count % 50 == 0:
            if enemy3.dead == False:
                space_pirates_bullet_group.add(enemy3.create_bullet())
        if self.count % 20 == 0:
            if enemy4.dead == False:
                space_pirates_bullet_group.add(enemy4.create_bullet())
        if self.count % 60 == 0:
            if enemy5.dead == False:
                space_pirates_bullet_group.add(enemy5.create_bullet())
        
        pygame.display.flip()
        screen.blit(background, (0,0))
        screen.blit(player.rotatedImage,player.rotatedRect)
        player_bullet_group.draw(screen)
        space_pirates_group.draw(screen)
        space_pirates_bullet_group.draw(screen)
        #! Uncomment this for explosions
        #explosions_group.draw(screen)
        
        player_bullet_group.update(player)
        player.offScreen()
        space_pirates_group.update()
        space_pirates_bullet_group.update()
        #! Uncomment this for explosions
        #explosions_group.update(1)
        
    #* Black Hole/Gravity
    def level_three(self):
        self.count += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = 'welcome'
            self.game_reset()
        if keys[pygame.K_w]:
            player.moveForword()
        if keys[pygame.K_a]:
            player.turnLeft()
        if keys[pygame.K_d]:
            player.turnRight()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(player_group) is not 0:
                        player_bullet_group.add(player.create_bullet())
        if self.count % 50 == 0:
            ran = random.choice([1,1,1,2,2,3])
            gravity_asteroid_group.add(Gravity_Asteroids(ran))
        
        if player.lives <= 0:
            self.level -= 1
            self.state = "loose"
            self.game_reset()
        if player.points >= 15:
            self.level += 1
            self.state = "win3"
            self.game_reset()
    
        pygame.display.flip()
        screen.blit(background, (0,0))
        screen.blit(player.rotatedImage,player.rotatedRect)
        player_bullet_group.draw(screen)
        gravity_asteroid_group.draw(screen)
        #! Uncomment this for explosions
        explosions_group.draw(screen)
        
        player_bullet_group.update(player)
        player.offScreen()
        gravity_asteroid_group.update()
        #! Uncomment this for explosions
        explosions_group.update(1)
        
        self.show_score()
        
    #* Asteroid Bases
    def level_four(self):
        self.count += 1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            self.state = 'welcome'
            self.game_reset()
        if keys[pygame.K_w]:
            player.moveForword()
        if keys[pygame.K_a]:
            player.turnLeft()
        if keys[pygame.K_d]:
            player.turnRight()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if len(player_group) is not 0:
                        player_bullet_group.add(player.create_bullet())
        
        if player.lives <= 0:
            self.level -= 1
            self.state = "loose"
            self.game_reset()
        if player.base_points >= 10:
            self.level += 1
            self.state = "win4"
            self.game_reset()
        
        if self.base_start:
            Base_Asteroids.create()
            self.base_start = False
        
        for i in base_asteroid_group:
            Base_Asteroids.angle(i)        
        
        pygame.display.flip()
        screen.blit(background, (0,0))
        screen.blit(player.rotatedImage,player.rotatedRect)
        player_bullet_group.draw(screen)
        base_asteroid_group.draw(screen)
        base_asteroid_bullet_group.draw(screen)
        #! Uncomment this for explosions
        #explosions_group.draw(screen)
        
        player_bullet_group.update(player)
        player.offScreen()
        base_asteroid_group.update()
        base_asteroid_bullet_group.update()
        #! Uncomment this for explosions
        #explosions_group.update(1)
    
    def win(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(event.pos):
                    if self.level == 0:
                        self.state = 'level_one'
                    elif self.level == 1:
                        asteroids_group.empty()
                        self.state = 'level_two'
                    elif self.level == 2:
                        space_pirates_group.empty()
                        space_pirates_bullet_group.empty()
                        self.state = 'level_three'
                    elif self.level == 3:
                        gravity_asteroid_group.empty()
                        self.state = 'level_four'
                if menu_button.collidepoint(event.pos):
                    self.state = 'welcome'
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()
        screen.blit(win_background, (0,0))
        screen.blit(win_text1,win_text1_rect1)
        screen.blit(win_text2,win_text2_rect2)
        screen.blit(start_button_image,start_button)
        screen.blit(exit_button_image,exit_button)
        screen.blit(menu_button_image,menu_button)
    
    def win2(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(event.pos):
                    if self.level == 0:
                        self.state = 'level_one'
                    elif self.level == 1:
                        asteroids_group.empty()
                        self.state = 'level_two'
                    elif self.level == 2:
                        space_pirates_group.empty()
                        space_pirates_bullet_group.empty()
                        self.state = 'level_three'
                    elif self.level == 3:
                        gravity_asteroid_group.empty()
                        self.state = 'level_four'
                if menu_button.collidepoint(event.pos):
                    self.state = 'welcome'
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()
        screen.blit(win_background, (0,0))
        screen.blit(win2_text1,win2_text1_rect1)
        screen.blit(win2_text2,win2_text2_rect2)
        screen.blit(win2_text3,win2_text3_rect3)
        screen.blit(win2_text4,win2_text4_rect4)
        screen.blit(start_button_image,start_button)
        screen.blit(exit_button_image,exit_button)
        screen.blit(menu_button_image,menu_button)
        
    def win3(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(event.pos):
                    if self.level == 0:
                        self.state = 'level_one'
                    elif self.level == 1:
                        asteroids_group.empty()
                        self.state = 'level_two'
                    elif self.level == 2:
                        space_pirates_group.empty()
                        space_pirates_bullet_group.empty()
                        self.state = 'level_three'
                    elif self.level == 3:
                        gravity_asteroid_group.empty()
                        self.state = 'level_four'
                if menu_button.collidepoint(event.pos):
                    self.state = 'welcome'
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()
        screen.blit(win_background, (0,0))
        screen.blit(win3_text1,win3_text1_rect1)
        screen.blit(win3_text2,win3_text2_rect2)
        screen.blit(start_button_image,start_button)
        screen.blit(exit_button_image,exit_button)
        screen.blit(menu_button_image,menu_button)
        
    def win4(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if win4_menu_button.collidepoint(event.pos):
                    self.state = 'welcome'
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()
        screen.blit(win_background, (0,0))
        screen.blit(win4_text1,win4_text1_rect1)
        screen.blit(win4_text2,win4_text2_rect2)
        screen.blit(exit_button_image,exit_button)
        screen.blit(menu_button_image,win4_menu_button)        
    
    def loose(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                if start_button.collidepoint(event.pos):
                    if self.level == 0:
                        self.state = 'level_one'
                    elif self.level == 1:
                        self.state = 'level_two'
                    elif self.level == 2:
                        self.state = 'level_three'
                    elif self.level == 3:
                        self.state = 'level_four'
                if menu_button.collidepoint(event.pos):
                    self.state = 'welcome'
                if exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                    
        pygame.display.flip()
        screen.blit(loose_background, (0,0))
        screen.blit(loose_text1,loose_text1_rect1)
        screen.blit(loose_text2,loose_text2_rect2)
        screen.blit(start_button_image,start_button)
        screen.blit(exit_button_image,exit_button)
        screen.blit(menu_button_image,menu_button)
    
    def state_manager(self):
        if self.state == 'welcome':
            self.welcome()
        if self.state == 'level_one':
            self.level_one()
        if self.state == 'level_two':
            self.level_two()
        if self.state == 'level_three':
            self.level_three()
        if self.state == 'level_four':
            self.level_four()
        if self.state == 'win':
            self.win()
        if self.state == 'win2':
            self.win2()
        if self.state == 'win3':
            self.win3()
        if self.state == 'win4':
            self.win4()
        if self.state == 'loose':
            self.loose()

    def game_reset(self):
        if self.level == 0:
            player.lives = 4
            player.points = 0
            player.reset()
            asteroids_group.empty()
            player_bullet_group.empty()
            Starting_Asteroids.reset()
        elif self.level == 1:
            player.lives = 4
            player.reset()
            player.points = 0
            player_bullet_group.empty()
            space_pirates_group.empty()
            space_pirates_bullet_group.empty()
            Space_Pirates.reset()
        elif self.level == 2:
            player.lives = 4
            player.points = 0
            player.reset()
            player_bullet_group.empty()
            gravity_asteroid_group.empty()
        elif self.level == 3:
            player.lives = 4
            player.points = 0
            player.reset()
            player_bullet_group.empty()
            base_asteroid_group.empty()
            base_asteroid_bullet_group.empty()
            Base_Asteroids.create()
    
    # Score
    def show_score(test):
        font = pygame.font.Font('fonts/scifi/OpenType-TT/The-Resto.ttf', 42)
        score = font.render("Score: " + str(player.points), True, (25,255,25))
        screen.blit(score, (10,10))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.lives = 4
        self.points = 0
        self.base_points = 0
        self.image = pygame.image.load('Example_ships/1B.png')
        self.rect = self.image.get_rect(center=(WIDTH//2,HEIGHT//2))
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.angle = 0
        self.rotatedImage = pygame.transform.rotate(self.image, self.angle)
        self.rotatedRect = self.rotatedImage.get_rect()
        self.rotatedRect.center = self.rect.center
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.rect.centerx + self.cosine * self.w//2, self.rect.centery - self.sine * self.h//2)
        self.shoot = pygame.mixer.Sound("Digital_SFX_Set/laser4.mp3")
        
    def turnLeft(self):
        self.angle += 10
        self.rotatedImage = pygame.transform.rotate(self.image,self.angle)
        self.rotatedRect = self.rotatedImage.get_rect()
        self.rotatedRect.center = self.rect.center
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.rect.centerx + self.cosine * self.w//2, self.rect.centery - self.sine * self.h//2)
    
    def turnRight(self):
        self.angle -= 10
        self.rotatedImage = pygame.transform.rotate(self.image,self.angle)
        self.rotatedRect = self.rotatedImage.get_rect()
        self.rotatedRect.center = self.rect.center
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.rect.centerx + self.cosine * self.w//2, self.rect.centery - self.sine * self.h//2)   
        
    def moveForword(self):
        self.rect.centerx += self.cosine * 8
        self.rect.centery -= self.sine * 8
        self.rotatedImage = pygame.transform.rotate(self.image,self.angle)
        self.rotatedRect = self.rotatedImage.get_rect()
        self.rotatedRect.center = self.rect.center
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.head = (self.rect.centerx + self.cosine * self.w//2, self.rect.centery - self.sine * self.h//2) 
        
    def offScreen(self):
        if self.rect.x > WIDTH:
            self.rect.x = 0
        elif self.rect.x < 0 - self.w:
            self.rect.x = WIDTH
        elif self.rect.y < 0 - self.h:
            self.rect.y = HEIGHT
        elif self.rect.y > HEIGHT:
            self.rect.y = 0
        
    def create_bullet(self):
        self.shoot.play()
        return Bullets(self.head, self.cosine, self.sine, 'spaceshooter/items/bullets/15.png')
    
    def hit(self):
        self.lives -= 1
        self.reset()
        
    def reset(self):
        self.rect = self.image.get_rect(center=(WIDTH//2,HEIGHT//2))
        
class Bullets(pygame.sprite.Sprite):
    def __init__(self, head, cos, sin, pic):
        super().__init__()
        self.image = pygame.image.load(pic)
        self.x, self.y = head
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.cos = cos
        self.sin = sin
        self.xSpeed = self.cos * 15
        self.ySpeed = self.sin * 15

    def update(self, who):
        if who == player:
            self.rect.x += self.xSpeed
            self.rect.y -= self.ySpeed
                
        if self.rect.x >= WIDTH + 200 or self.rect.x <= -200 or self.rect.y >= HEIGHT + 200 or self.rect.y <= -200:
            self.kill()
        if pygame.sprite.spritecollide(enemy1,player_bullet_group,False):
            explode = Explosion(self.rect.x,self.rect.y)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            enemy1.hit()
            self.kill()
            player.points += 1
        if pygame.sprite.spritecollide(enemy2,player_bullet_group,False):
            explode = Explosion(self.rect.x,self.rect.y)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            enemy2.hit()
            self.kill()
            player.points += 1
        if pygame.sprite.spritecollide(enemy3,player_bullet_group,False):
            explode = Explosion(self.rect.x,self.rect.y)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            enemy3.hit()
            self.kill()
            player.points += 1
        if pygame.sprite.spritecollide(enemy4,player_bullet_group,False):
            explode = Explosion(self.rect.x,self.rect.y)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            enemy4.hit()
            self.kill()
            player.points += 1
        if pygame.sprite.spritecollide(enemy5,player_bullet_group,False):
            explode = Explosion(self.rect.x,self.rect.y)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            enemy5.hit()
            self.kill()
            player.points += 1

    def hit(self):
        self.kill()

    def reset(self):
        self.kill()
            
class Asteroids(pygame.sprite.Sprite):
    def __init__(self, rank):
        super().__init__()
        self.rank = rank
        if self.rank == 1:
            self.image = random.choice(small_asteroids)
        elif self.rank == 2:
            self.image = random.choice(medium_asteroids)
        else:
            self.image = random.choice(big_asteroids)
        self.rect = self.image.get_rect()
        self.ranpoint = random.choice([(random.randrange(0,WIDTH-self.rect.w), random.choice([-1*self.rect.h - 5, HEIGHT + 5])), (random.choice([-1*self.rect.w - 5, WIDTH + 5]), random.randrange(0,HEIGHT - self.rect.h))])
        self.rect.x, self.rect.y = self.ranpoint
        if self.rect.x < WIDTH//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.rect.y < HEIGHT//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xSpeed = self.xdir * random.randrange(2,5)
        self.ySpeed = self.ydir * random.randrange(2,5)
        
    def update(self):
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        
        # Collision
        if pygame.sprite.groupcollide(asteroids_group, player_bullet_group, False, False):
            bullets_hits = pygame.sprite.groupcollide(player_bullet_group, asteroids_group, False, False)
            asteroids_hits = pygame.sprite.groupcollide(asteroids_group, player_bullet_group, False, False)
            if self.rank == 3:
                asteroid1 = Asteroids(2)
                asteroid2 = Asteroids(2)
                asteroid1.rect.x = self.rect.x
                asteroid2.rect.x = self.rect.x
                asteroid1.rect.y = self.rect.y
                asteroid2.rect.y = self.rect.y
                asteroids_group.add(asteroid1)
                asteroids_group.add(asteroid2)
            elif self.rank == 2:
                asteroid1 = Asteroids(1)
                asteroid2 = Asteroids(1)
                asteroid1.rect.x = self.rect.x
                asteroid2.rect.x = self.rect.x
                asteroid1.rect.y = self.rect.y
                asteroid2.rect.y = self.rect.y
                asteroids_group.add(asteroid1)
                asteroids_group.add(asteroid2)
            for i in bullets_hits:
                for j in asteroids_hits:
                    #! Uncomment thi for explosions
                    # explode = Explosion(self.rect.x,self.rect.y)
                    # explosions_group.add(explode)
                    # explode.animate()
                    # if explode.is_animating == False:
                    #     explode.kill()
                    player_bullet_group.remove(i)
                    asteroids_group.remove(j)
            player.points += 1
        if pygame.sprite.groupcollide(asteroids_group, player_group, False, False):
            explode = Explosion(self.rect.x,self.rect.y)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            player.hit()
            self.kill()
        self.offscreen()
        
        # Fix the bouncing issue
        
        # if pygame.sprite.spritecollide(self,asteroids_group,False):
        #     Asteroids.bounce(self)
            
    def offscreen(self):
        if self.rect.x > WIDTH:
            self.rect.x = 0
        elif self.rect.x < 0 - self.rect.w:
            self.rect.x = WIDTH
        elif self.rect.y < 0 - self.rect.h:
            self.rect.y = HEIGHT
        elif self.rect.y > HEIGHT:
            self.rect.y = 0
            
    def bounce(self):
        self.xSpeed *= -1
        self.ySpeed *= -1

class Gravity_Asteroids(pygame.sprite.Sprite):
    def __init__(self, rank):
        super().__init__()
        self.rank = rank
        if self.rank == 1:
            self.image = random.choice(small_asteroids)
        elif self.rank == 2:
            self.image = random.choice(medium_asteroids)
        else:
            self.image = random.choice(big_asteroids)
        self.rect = self.image.get_rect()
        self.ranpoint = random.choice([(random.randrange(0,WIDTH-self.rect.w), random.choice([-1*self.rect.h - 5, HEIGHT + 5])), (random.choice([-1*self.rect.w - 5, WIDTH + 5]), random.randrange(0,HEIGHT - self.rect.h))])
        self.rect.x, self.rect.y = self.ranpoint
        self.dx, self.dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        self.dist = math.hypot(self.dx,self.dy)
        self.dx, self.dy = self.dx/self.dist, self.dy/self.dist
        self.xSpeed = self.dx * random.randrange(9,13)
        self.ySpeed = self.dy * random.randrange(9,13)
        
    def update(self):
        self.dx, self.dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        self.dist = math.hypot(self.dx,self.dy)
        self.dx, self.dy = self.dx/self.dist, self.dy/self.dist
        self.xSpeed = self.dx * random.randrange(9,13)
        self.ySpeed = self.dy * random.randrange(9,13)
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        
        # Collision
        if pygame.sprite.groupcollide(gravity_asteroid_group, player_bullet_group, False, False):
            bullets_hits = pygame.sprite.groupcollide(player_bullet_group, gravity_asteroid_group, False, False)
            asteroids_hits = pygame.sprite.groupcollide(gravity_asteroid_group, player_bullet_group, False, False)
            for i in bullets_hits:
                for j in asteroids_hits:
                    explode = Explosion(self.rect.x,self.rect.y)
                    explosions_group.add(explode)
                    explode.animate()
                    if explode.is_animating == False:
                        explode.kill()
                    player_bullet_group.remove(i) 
                    gravity_asteroid_group.remove(j)
            player.points += 1
        if pygame.sprite.groupcollide(gravity_asteroid_group, player_group, False, False):
            explode = Explosion(self.rect.x,self.rect.y)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            player.hit()
            self.kill()
            
#TODO: Fix explosion problem
class Base_Asteroids(pygame.sprite.Sprite):
    def __init__(self, rank, pos_x, pos_y):
        super().__init__()
        self.rank = rank
        if self.rank == 1:
            self.image = pygame.image.load('space_base/a21.png')
        elif self.rank == 2:
            self.image = pygame.image.load('space_base/a8.png')
        else:
            self.image = pygame.image.load('space_base/a1.png')
        self.rect = self.image.get_rect()
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.rect.x, self.rect.y = pos_x,pos_y
        if self.rect.x < WIDTH//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.rect.y < HEIGHT//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xSpeed = self.xdir * random.randrange(2,5)
        self.ySpeed = self.ydir * random.randrange(2,5)
        self.head = random.choice([self.rect.midtop,self.rect.midleft,self.rect.midbottom,self.rect.midright])       
        
    def update(self):        
        # Collision
        if pygame.sprite.groupcollide(base_asteroid_group, player_bullet_group, False, False):
            bullets_hits = pygame.sprite.groupcollide(player_bullet_group, base_asteroid_group, False, False)
            asteroids_hits = pygame.sprite.groupcollide(base_asteroid_group, player_bullet_group, False, False)
            for i in bullets_hits:
                for j in asteroids_hits:
                    explode = Explosion(self.rect.centerx,self.rect.centery)
                    explosions_group.add(explode)
                    explode.animate()
                    if explode.is_animating == False:
                        explode.kill()
                    player_bullet_group.remove(i)
                    base_asteroid_group.remove(j)
            player.base_points += 1
        if pygame.sprite.groupcollide(base_asteroid_group, player_group, False, False):
            explode = Explosion(self.rect.centerx,self.rect.centery)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            player.hit()
            self.kill()
    
    def angle(self):
        if self.head == self.rect.midtop:
            if player.rotatedRect.centerx > self.head[0] - (self.w//2 + 100) and player.rotatedRect.centerx < self.head[0] + (self.w//2 + 100) and player.rotatedRect.centery < self.head[1] and player.rotatedRect.centery > self.head[1] - 400:
                dx, dy = player.rotatedRect.centerx - self.head[0], player.rotatedRect.centery - self.head[1]
                rads = math.atan2(-dy,dx)
                rads %= 2*math.pi
                degs = math.degrees(rads)
                if numpy.clip(degs, -45, 45):
                    if game_state.count % 20 == 0:
                        base_asteroid_bullet_group.add(Base_Asteroid_Bullets(self.head, 'spaceshooter/items/bullets/15.png'))
            
        if self.head == self.rect.midleft:
            if player.rotatedRect.centerx > self.head[0] - 400 and player.rotatedRect.centerx < self.head[0] and player.rotatedRect.centery < self.head[1] + (self.h//2 + 100) and player.rotatedRect.centery > self.head[1] - (self.h//2 + 100):
                dx, dy = player.rotatedRect.centerx - self.head[0], player.rotatedRect.centery - self.head[1]
                rads = math.atan2(-dy,dx)
                rads %= 2*math.pi
                degs = math.degrees(rads)
                if numpy.clip(degs, -45, 45):
                    if game_state.count % 20 == 0:
                        base_asteroid_bullet_group.add(Base_Asteroid_Bullets(self.head, 'spaceshooter/items/bullets/15.png'))
            
        if self.head == self.rect.midbottom:
            if player.rotatedRect.centerx > self.head[0] - (self.w//2 + 100) and player.rotatedRect.centerx < self.head[0] + (self.w//2 + 100) and player.rotatedRect.centery < self.head[1] + 400 and player.rotatedRect.centery > self.head[1]:
                dx, dy = player.rotatedRect.centerx - self.head[0], player.rotatedRect.centery - self.head[1]
                rads = math.atan2(-dy,dx)
                rads %= 2*math.pi
                degs = math.degrees(rads)
                if numpy.clip(degs, -45, 45):
                    if game_state.count % 20 == 0:
                        base_asteroid_bullet_group.add(Base_Asteroid_Bullets(self.head, 'spaceshooter/items/bullets/15.png'))
            
        if self.head == self.rect.midright:
            if player.rotatedRect.centerx > self.head[0] and player.rotatedRect.centerx < self.head[0] + 400 and player.rotatedRect.centery < self.head[1] + (self.h//2 + 100) and player.rotatedRect.centery > self.head[1] - (self.h//2 + 100):
                dx, dy = player.rotatedRect.centerx - self.head[0], player.rotatedRect.centery - self.head[1]
                rads = math.atan2(-dy,dx)
                rads %= 2*math.pi
                degs = math.degrees(rads)
                if numpy.clip(degs, -45, 45):
                    if game_state.count % 20 == 0:
                        base_asteroid_bullet_group.add(Base_Asteroid_Bullets(self.head, 'spaceshooter/items/bullets/15.png'))
            
    def create():
        for q in range(0,10):
            xpos = random.randrange(100, 1600)
            ypos = random.randrange(100, 850)
            rank = random.randrange(1,3)
            asteroid = Base_Asteroids(rank,xpos,ypos)
            base_asteroid_group.add(asteroid)

class Starting_Asteroids(pygame.sprite.Sprite):
    def __init__(self, rank, pos_x, pos_y):
        super().__init__()
        self.rank = rank
        if self.rank == 1:
            self.image = pygame.image.load('asteroids/small/a10000.png')
        elif self.rank == 2:
            self.image = pygame.image.load('asteroids/medium/a10000.png')
        else:
            self.image = pygame.image.load('asteroids/large/a10000.png')
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_x,pos_y
        if self.rect.x < WIDTH//2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.rect.y < HEIGHT//2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xSpeed = self.xdir * random.randrange(2,5)
        self.ySpeed = self.ydir * random.randrange(2,5)
        
    def update(self):
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        
        # Collision
        if pygame.sprite.groupcollide(asteroids_group, player_bullet_group, False, False):
            bullets_hits = pygame.sprite.groupcollide(player_bullet_group, asteroids_group, False, False)
            asteroids_hits = pygame.sprite.groupcollide(asteroids_group, player_bullet_group, False, False)
            if self.rank == 3:
                asteroid1 = Asteroids(2)
                asteroid2 = Asteroids(2)
                asteroid1.rect.x = self.rect.x
                asteroid2.rect.x = self.rect.x
                asteroid1.rect.y = self.rect.y
                asteroid2.rect.y = self.rect.y
                asteroids_group.add(asteroid1)
                asteroids_group.add(asteroid2)
            elif self.rank == 2:
                asteroid1 = Asteroids(1)
                asteroid2 = Asteroids(1)
                asteroid1.rect.x = self.rect.x
                asteroid2.rect.x = self.rect.x
                asteroid1.rect.y = self.rect.y
                asteroid2.rect.y = self.rect.y
                asteroids_group.add(asteroid1)
                asteroids_group.add(asteroid2)
            for i in bullets_hits:
                for j in asteroids_hits:
                    #! Ucomment this for explosions
                    # explode = Explosion(self.rect.x,self.rect.y)
                    # explosions_group.add(explode)
                    # explode.animate()
                    # if explode.is_animating == False:
                    #     explode.kill()
                    player_bullet_group.remove(i)
                    asteroids_group.remove(j)
            player.points += 1
        if pygame.sprite.groupcollide(asteroids_group, player_group, False, False):
            explode = Explosion(self.rect.x,self.rect.y)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            player.hit()
            self.kill()
        self.offscreen()
            
    def reset():
        for i in range(0,10):
            xpos = random.randrange(100, 2400)
            ypos = random.randrange(100, 1200)
            rank = random.randrange(1,3)
            asteroid = Starting_Asteroids(rank,xpos,ypos)
            asteroids_group.add(asteroid)

    def offscreen(self):
        if self.rect.x > WIDTH:
            self.rect.x = 0
        elif self.rect.x < 0 - self.rect.w:
            self.rect.x = WIDTH
        elif self.rect.y < 0 - self.rect.h:
            self.rect.y = HEIGHT
        elif self.rect.y > HEIGHT:
            self.rect.y = 0 

class Base_Asteroid_Bullets(pygame.sprite.Sprite):
    def __init__(self, head, pic):
        super().__init__()
        self.image = pygame.image.load(pic)
        self.x, self.y = head
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.dx, self.dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        self.dist = math.hypot(self.dx,self.dy)
        self.dx, self.dy = self.dx/self.dist, self.dy/self.dist
        self.xSpeed = self.dx * 10
        self.ySpeed = self.dy * 10
        
    def update(self):
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        
        if pygame.sprite.groupcollide(base_asteroid_bullet_group,player_group,False,False):
            bullet = pygame.sprite.groupcollide(base_asteroid_bullet_group,player_group,False,False)
            explode = Explosion(self.rect.centerx,self.rect.centery)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()
            player.hit()
            for i in bullet:
                base_asteroid_bullet_group.remove(i)

#TODO: Fix the explosion error
class Space_Pirates(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = random.choice(ships)
        self.rect = self.image.get_rect()
        self.w = self.image.get_width()
        self.h = self.image.get_height()
        self.dx, self.dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        self.dist = math.hypot(self.dx,self.dy)
        self.dx, self.dy = self.dx/self.dist, self.dy/self.dist
        self.xSpeed = self.dx * 2
        self.ySpeed = self.dy * 2
        self.moveTo = True
        self.dead = False
        self.shoot = pygame.mixer.Sound("Digital_SFX_Set/laser9.mp3")
    
    def offScreen(self):
        if self.rect.x > WIDTH:
            self.rect.x = 0
        elif self.rect.x < 0 - self.w:
            self.rect.x = WIDTH
        elif self.rect.y < 0 - self.h:
            self.rect.y = HEIGHT
        elif self.rect.y > HEIGHT:
            self.rect.y = 0
    
    def create_bullet(self):
        self.shoot.play()
        return Pirate_Bullet(self.rect.centerx, self.rect.centery, 'spaceshooter/items/bullets/15.png')
    
    def hit(self):
        self.dead = True
        player.points += 1
        self.kill()
        
    def reset():
        enemy1.rect.x = random.randrange(10, WIDTH-10)
        enemy1.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy1)
        enemy1.dead = False
        enemy2.rect.x = random.randrange(10, WIDTH-10)
        enemy2.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy2)
        enemy2.dead = False
        enemy3.rect.x = random.randrange(10, WIDTH-10)
        enemy3.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy3)
        enemy3.dead = False
        enemy4.rect.x = random.randrange(10, WIDTH-10)
        enemy4.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy4)
        enemy4.dead = False
        enemy5.rect.x = random.randrange(10, WIDTH-10)
        enemy5.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy5)  
        enemy5.dead = False
        ship1_check = []
        ship2_check = []
        ship3_check = []
        ship4_check = []
        ship5_check = []
        ship1_check.append(enemy2)
        ship1_check.append(enemy3)
        ship1_check.append(enemy4)
        ship1_check.append(enemy5)
        ship2_check.append(enemy1)
        ship2_check.append(enemy3)
        ship2_check.append(enemy4)
        ship2_check.append(enemy5)
        ship3_check.append(enemy2)
        ship3_check.append(enemy1)
        ship3_check.append(enemy4)
        ship3_check.append(enemy5)
        ship4_check.append(enemy2)
        ship4_check.append(enemy3)
        ship4_check.append(enemy1)
        ship4_check.append(enemy5)
        ship5_check.append(enemy2)
        ship5_check.append(enemy3)
        ship5_check.append(enemy4)
        ship5_check.append(enemy1)
        
    def update(self):
        self.dx, self.dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        self.dist = math.hypot(self.dx,self.dy)
        self.dx, self.dy = self.dx/self.dist, self.dy/self.dist
        if self.moveTo is True:
            self.xSpeed = self.dx * 5
            self.ySpeed = self.dy * 5
            self.rect.x += self.xSpeed
            self.rect.y += self.ySpeed
            if self.dist <= 200:
                self.moveTo = False
        if self.moveTo is False:
            self.xSpeed = self.dx * -5
            self.ySpeed = self.dy * -5
            self.rect.x += self.xSpeed
            self.rect.y += self.ySpeed
            if self.dist >= 700:
                self.moveTo = True
        if pygame.sprite.spritecollideany(enemy1,ship1_check):
            space_pirates_group.remove(enemy1)
            # explode = Explosion(self.rect.x,self.rect.y)
            # explosions_group.add(explode)
            # explode.animate()
            # if explode.is_animating == False:
            #     explode.kill()
            enemy1.hit()
        elif pygame.sprite.spritecollideany(enemy2,ship2_check):
            space_pirates_group.remove(enemy2)
            enemy2.hit()
            player.points += 1
        elif pygame.sprite.spritecollideany(enemy3,ship3_check):
            space_pirates_group.remove(enemy3)
            enemy3.hit()
            player.points += 1
        elif pygame.sprite.spritecollideany(enemy4,ship4_check):
            space_pirates_group.remove(enemy4)
            enemy4.hit()
            player.points += 1
        elif pygame.sprite.spritecollideany(enemy5,ship5_check):
            space_pirates_group.remove(enemy5)
            enemy5.hit()
            player.points += 1
        elif pygame.sprite.groupcollide(space_pirates_group,player_group,False,False):
            # explode = Explosion(self.rect.x,self.rect.y)
            # explosions_group.add(explode)
            # explode.animate()
            # if explode.is_animating == False:
            #     explode.kill()
            self.hit()
            player.hit()
          
    def create():
        enemy1.rect.x = random.randrange(10, WIDTH-10)
        enemy1.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy1)
        enemy2.rect.x = random.randrange(10, WIDTH-10)
        enemy2.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy2)
        enemy3.rect.x = random.randrange(10, WIDTH-10)
        enemy3.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy3)
        enemy4.rect.x = random.randrange(10, WIDTH-10)
        enemy4.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy4)
        enemy5.rect.x = random.randrange(10, WIDTH-10)
        enemy5.rect.y = random.randrange(10, HEIGHT-10)
        space_pirates_group.add(enemy5)  

        ship1_check.append(enemy2)
        ship1_check.append(enemy3)
        ship1_check.append(enemy4)
        ship1_check.append(enemy5)
        ship2_check.append(enemy1)
        ship2_check.append(enemy3)
        ship2_check.append(enemy4)
        ship2_check.append(enemy5)
        ship3_check.append(enemy2)
        ship3_check.append(enemy1)
        ship3_check.append(enemy4)
        ship3_check.append(enemy5)
        ship4_check.append(enemy2)
        ship4_check.append(enemy3)
        ship4_check.append(enemy1)
        ship4_check.append(enemy5)
        ship5_check.append(enemy2)
        ship5_check.append(enemy3)
        ship5_check.append(enemy4)
        ship5_check.append(enemy1)
      
class Pirate_Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y,pic):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load(pic)
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.dx, self.dy = player.rect.x - self.rect.x, player.rect.y - self.rect.y
        self.dist = math.hypot(self.dx,self.dy)
        self.dx, self.dy = self.dx/self.dist, self.dy/self.dist
        self.xSpeed = self.dx * 10
        self.ySpeed = self.dy * 10
        
    def update(self):
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        if pygame.sprite.groupcollide(space_pirates_bullet_group,player_group,False,False):
            bullet = pygame.sprite.groupcollide(space_pirates_bullet_group,player_group,False,False)
            explode = Explosion(self.rect.x,self.rect.y)
            explosions_group.add(explode)
            explode.animate()
            if explode.is_animating == False:
                explode.kill()            
            player.hit()
            for i in bullet:
                space_pirates_bullet_group.remove(i)

class Explosion(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.is_animating = False
        self.current_sprite = 0
        self.image = sprites[self.current_sprite]
        
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x,pos_y]
        self.boom = pygame.mixer.Sound("Digital_SFX_Set/explosion.wav")
        
    def animate(self):
        self.boom.play()
        self.is_animating = True
        
    def update(self, speed):
        if self.is_animating == True:
            self.current_sprite += speed
            
            if self.current_sprite >= len(sprites):
                self.current_sprite = 0
                self.is_animating = False
            
            self.image = sprites[int(self.current_sprite)]


global sprites
sprites = []
sprites.append(pygame.image.load("animation/explosion1.png"))
sprites.append(pygame.image.load("animation/explosion2.png"))
sprites.append(pygame.image.load("animation/explosion3.png"))
sprites.append(pygame.image.load("animation/explosion4.png"))
sprites.append(pygame.image.load("animation/explosion5.png"))
sprites.append(pygame.image.load("animation/explosion6.png"))
sprites.append(pygame.image.load("animation/explosion7.png"))
sprites.append(pygame.image.load("animation/explosion8.png"))
sprites.append(pygame.image.load("animation/explosion9.png"))
sprites.append(pygame.image.load("animation/explosion10.png"))

# Pygame set up
pygame.init()
WIDTH, HEIGHT = 1700,950  #1250,750
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Galactic Asteroids")
game_state = GameState()
player = Player()
player_group = pygame.sprite.Group()
player_group.add(player)
player_bullet_group = pygame.sprite.Group()
asteroids_group = pygame.sprite.Group()
for i in range(0,10):
    xpos = random.randrange(100, 1600)
    ypos = random.randrange(100, 850)
    rank = random.randrange(1,3)
    asteroid = Starting_Asteroids(rank,xpos,ypos)
    asteroids_group.add(asteroid)
space_pirates_group = pygame.sprite.Group()
space_pirates_bullet_group = pygame.sprite.Group()
ship = []
gravity_asteroid_group = pygame.sprite.Group()
base_asteroid_group = pygame.sprite.Group()
base_start_asteroid_group = pygame.sprite.Group()
base_asteroid_bullet_group = pygame.sprite.Group()
explosions_group = pygame.sprite.Group()
clock = pygame.time.Clock()
background = pygame.image.load('backgrounds/Blue-Nebula.png')
win_background = pygame.image.load('backgrounds/Starfield-8.png')
loose_background = pygame.image.load('backgrounds/Starfield-7.png')

# Welcome screen texts and fonts
big_font = pygame.font.Font('fonts/scifi/OpenType-TT/The-Resto.ttf', 52)
medium_font = pygame.font.Font('fonts/scifi/OpenType-TT/The-Resto.ttf', 42)
small_font = pygame.font.Font('fonts/scifi/OpenType-TT/The-Resto.ttf', 25)
welcome_text1 = big_font.render("Welcome to Galactic Asteroids!!", True, (25,255,25))
welcome_text1_rect1 = welcome_text1.get_rect()
welcome_text1_rect1.center = (WIDTH//2, HEIGHT//9)
welcome_text2 = medium_font.render("Objective:", True, (25,255,25))
welcome_text2_rect2 = welcome_text2.get_rect()
welcome_text2_rect2.center = (WIDTH//2, HEIGHT//5)
welcome_text3 = small_font.render("Stay alive and rack up points!", True, (25,255,25))
welcome_text3_rect3 = welcome_text3.get_rect()
welcome_text3_rect3.center = (WIDTH//2, HEIGHT//3.9)
welcome_text4 = medium_font.render("How to play:", True, (25,255,25))
welcome_text4_rect4 = welcome_text4.get_rect()
welcome_text4_rect4.center = (WIDTH//2, HEIGHT//3)
welcome_text5 = small_font.render("Shoot asteroids to earn points. If you get hit by an asteroid, you will die...", True, (25,255,25))
welcome_text5_rect5 = welcome_text5.get_rect()
welcome_text5_rect5.center = (WIDTH//2, HEIGHT//2.6)
welcome_text6 = medium_font.render("Controls:", True, (25,255,25))
welcome_text6_rect6 = welcome_text6.get_rect()
welcome_text6_rect6.center = (WIDTH//2, HEIGHT//2.2)
welcome_text7 = small_font.render("Move forword: 'w' key", True, (25,255,25))
welcome_text7_rect7 = welcome_text7.get_rect()
welcome_text7_rect7.center = (WIDTH//2, HEIGHT//2)
welcome_text8 = small_font.render("Turn left: 'a' key", True, (25,255,25))
welcome_text8_rect8 = welcome_text8.get_rect()
welcome_text8_rect8.center = (WIDTH//2, HEIGHT//1.85)
welcome_text9 = small_font.render("Turn right: 'd' key", True, (25,255,25))
welcome_text9_rect9 = welcome_text9.get_rect()
welcome_text9_rect9.center = (WIDTH//2, HEIGHT//1.73)
welcome_text10 = small_font.render("Move shoot: 'space' key", True, (25,255,25))
welcome_text10_rect10 = welcome_text10.get_rect()
welcome_text10_rect10.center = (WIDTH//2, HEIGHT//1.63)

# Level_1 Win screen text
win_text1 = big_font.render("YOU WON!!", True, (25,255,25))
win_text1_rect1 = win_text1.get_rect()
win_text1_rect1.center = (WIDTH//2, HEIGHT//9)
win_text2 = medium_font.render("To pass level 2 you must destroy all the space pirates!", True, (25,255,25))
win_text2_rect2 = win_text2.get_rect()
win_text2_rect2.center = (WIDTH//2, HEIGHT//3.5)

# Level_2 Win screen text
win2_text1 = big_font.render("YOU WON!!", True, (25,255,25))
win2_text1_rect1 = win2_text1.get_rect()
win2_text1_rect1.center = (WIDTH//2, HEIGHT//9)
win2_text2 = medium_font.render("To pass level 3 you must get 15 points", True, (25,255,25))
win2_text2_rect2 = win2_text2.get_rect()
win2_text2_rect2.center = (WIDTH//2, HEIGHT//3.5)
win2_text3 = medium_font.render("Also, from here on out, watch out for the voids in space.", True, (25,255,25))
win2_text3_rect3 = win2_text3.get_rect()
win2_text3_rect3.center = (WIDTH//2, HEIGHT//2.9)
win2_text4 = medium_font.render("The voids will destroy your bullets.", True, (25,255,25))
win2_text4_rect4 = win2_text4.get_rect()
win2_text4_rect4.center = (WIDTH//2, HEIGHT//2.5)

# Level_3 Win screen text
win3_text1 = big_font.render("YOU WON!!", True, (25,255,25))
win3_text1_rect1 = win3_text1.get_rect()
win3_text1_rect1.center = (WIDTH//2, HEIGHT//9)
win3_text2 = medium_font.render("To pass level 4 you must destroy all the bases!", True, (25,255,25))
win3_text2_rect2 = win3_text2.get_rect()
win3_text2_rect2.center = (WIDTH//2, HEIGHT//3.5)

# Level_4 Win screen text
win4_text1 = big_font.render("YOU WON!!", True, (25,255,25))
win4_text1_rect1 = win4_text1.get_rect()
win4_text1_rect1.center = (WIDTH//2, HEIGHT//9)
win4_text2 = medium_font.render("You are now the best pilot in the universe... Probably Bc you killed everyone else", True, (25,255,25))
win4_text2_rect2 = win4_text2.get_rect()
win4_text2_rect2.center = (WIDTH//2, HEIGHT//3.5)

# Loose screen text
loose_text1 = big_font.render("You lost..", True, (25,255,25))
loose_text1_rect1 = loose_text1.get_rect()
loose_text1_rect1.center = (WIDTH//2, HEIGHT//9)
loose_text2 = medium_font.render("Going back a level... hehe", True, (25,255,25))
loose_text2_rect2 = loose_text2.get_rect()
loose_text2_rect2.center = (WIDTH//2, HEIGHT//3.5)

# Buttons
start_button_image = pygame.image.load('buttons-2/start-2.png')
start_button = start_button_image.get_rect(center=(WIDTH//4,HEIGHT//1.2))
exit_button_image = pygame.image.load('buttons-2/exit-2.png')
exit_button = exit_button_image.get_rect(center=(WIDTH//1.3,HEIGHT//1.2))
menu_button_image = pygame.image.load('buttons-2/about-2.png')
menu_button = menu_button_image.get_rect(center=(WIDTH//1.91,HEIGHT//1.2))
win4_menu_button = menu_button_image.get_rect(center=(WIDTH//4,HEIGHT//1.2))

# Asteroids
big_asteroids = []
big_asteroids.append(pygame.image.load('asteroids/large/a10000.png'))
big_asteroids.append(pygame.image.load('asteroids/large/a10001.png'))
big_asteroids.append(pygame.image.load('asteroids/large/a10002.png'))
big_asteroids.append(pygame.image.load('asteroids/large/a10003.png'))
big_asteroids.append(pygame.image.load('asteroids/large/a30000.png'))
big_asteroids.append(pygame.image.load('asteroids/large/a30001.png'))
big_asteroids.append(pygame.image.load('asteroids/large/a30002.png'))
big_asteroids.append(pygame.image.load('asteroids/large/a30003.png'))
big_asteroids.append(pygame.image.load('asteroids/large/b10000.png'))
big_asteroids.append(pygame.image.load('asteroids/large/b30000.png'))
big_asteroids.append(pygame.image.load('asteroids/large/c10000.png'))
big_asteroids.append(pygame.image.load('asteroids/large/c30000.png'))
big_asteroids.append(pygame.image.load('asteroids/large/c40000.png'))
big_asteroids.append(pygame.image.load('asteroids/large/c40001.png'))
big_asteroids.append(pygame.image.load('asteroids/large/c40002.png'))
medium_asteroids = []
medium_asteroids.append(pygame.image.load('asteroids/medium/a10000.png'))
medium_asteroids.append(pygame.image.load('asteroids/medium/a30000.png'))
medium_asteroids.append(pygame.image.load('asteroids/medium/a40000.png'))
medium_asteroids.append(pygame.image.load('asteroids/medium/b40000.png'))
medium_asteroids.append(pygame.image.load('asteroids/medium/c10000.png'))
medium_asteroids.append(pygame.image.load('asteroids/medium/c30000.png'))
small_asteroids = []
small_asteroids.append(pygame.image.load('asteroids/small/a10000.png'))
small_asteroids.append(pygame.image.load('asteroids/small/a30000.png'))
small_asteroids.append(pygame.image.load('asteroids/small/a40000.png'))
small_asteroids.append(pygame.image.load('asteroids/small/b10000.png'))
small_asteroids.append(pygame.image.load('asteroids/small/b30000.png'))
small_asteroids.append(pygame.image.load('asteroids/small/b40000.png'))

ships = []
ships.append(pygame.image.load('Example_ships/2B.png'))
ships.append(pygame.image.load('Example_ships/4B.png'))
ships.append(pygame.image.load('Example_ships/6B.png'))
ships.append(pygame.image.load('Example_ships/8B.png'))
ships.append(pygame.image.load('Example_ships/10B.png'))
ships.append(pygame.image.load('Example_ships/11B.png'))
ships.append(pygame.image.load('Example_ships/12B.png'))
ships.append(pygame.image.load('Example_ships/13B.png'))

enemy1 = Space_Pirates()
enemy2 = Space_Pirates()
enemy3 = Space_Pirates()
enemy4 = Space_Pirates()
enemy5 = Space_Pirates()

ship1_check = []
ship2_check = []
ship3_check = []
ship4_check = []
ship5_check = []
Space_Pirates.create()

def music():
    music = pygame.mixer.Sound("Hero Immortal.mp3")
    music.play(1)

play = True

# Main loop
while True:
    if play == True:
        music()
        play = False
    game_state.state_manager()
    clock.tick(100)