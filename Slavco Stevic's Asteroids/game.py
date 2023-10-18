import pygame as p
from ship import spaceShip
from bullets import Bullets
from bullets import Bullet
from asteroids import Asteroids
from rocket import Rocket

class Screen:
    def __init__(self, bg):
        # Screen dimensions
        self.screenWidth = 1280
        self.screenHeight = 720
        
        # Background
        self.background = p.transform.scale(bg, (self.screenWidth, self.screenHeight))
        self.background_rect = self.background.get_rect()
        self.screen = p.display.set_mode((self.screenWidth, self.screenHeight))
        
        # Borders
        self.leftX = 0
        self.rightX = self.screenWidth
        self.topY = 0
        self.botY = self.screenHeight
    
    def apply_background(self):
        self.screen.blit(self.background, self.background_rect)

def displayScore(ship):
    text = f"Score: {ship.score}"
    font = p.font.Font(None, 25)
    text_surface = font.render(text, True, (255, 255, 255))
    text_rect = text_surface.get_rect(topleft=(50, 50))
    scr.screen.blit(text_surface, text_rect)
    
def displayShield(ship):
    font = p.font.Font(None, 25)
    if ship.power_up == True:
        text = "Shield: READY"
        text_surface = font.render(text, True, (0, 255, 0))
    else:
        text = "Shield: UNAVAILABLE"
        text_surface = font.render(text, True, (255, 0, 0))
    text_rect = text_surface.get_rect(topleft=(50, 80))
    scr.screen.blit(text_surface, text_rect)
    
def displayRocket(ship):
    font = p.font.Font(None, 25)
    if ship.power_up == True:
        text = "Rocket: READY"
        text_surface = font.render(text, True, (0, 255, 0))
    else:
        text = "Rocket: UNAVAILABLE"
        text_surface = font.render(text, True, (255, 0, 0))
    text_rect = text_surface.get_rect(topleft=(50, 110))
    scr.screen.blit(text_surface, text_rect)
    
def graphics(scr):
    p.init()
    
    ship = spaceShip(scr)
    bullets = Bullets(scr)
    last_fire_time = 0
    asteroids = Asteroids(scr)
    rocket = Rocket(ship.turret, scr)
    
    running = True
    #ship.start_sound.play()
    while running:
        scr.apply_background()
        if rocket.flying == False and (rocket.frame_index == 0 or rocket.frame_index == 5):
            rocket.followTurret(ship.turret)
        
        for event in p.event.get():
            if event.type == p.QUIT:
                running = False

            if event.type == p.MOUSEBUTTONDOWN and event.button == 3:
                ship = spaceShip(scr)
                bullets = Bullets(scr)
                last_fire_time = 0
                asteroids = Asteroids(scr)
                rocket = Rocket(ship.turret, scr)
        
        ship.didYouLose()
        # END GAME SCREEN
        font = p.font.Font(None, 100)
        if ship.win == True:
            textWin = "WIN!"
            text_surface = font.render(textWin, True, (0, 255, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (scr.screenWidth // 2, scr.screenHeight // 2)
            scr.screen.blit(text_surface, text_rect)
            ship.win_sound.play()
            asteroids.reset()
            ship.reset()
            bullets.reset()
            rocket.reset(ship.turret)
            
        if ship.defeat == True:
            textLose = "GAME OVER!"
            text_surface = font.render(textLose, True, (255, 0, 0))
            text_rect = text_surface.get_rect()
            text_rect.center = (scr.screenWidth // 2, scr.screenHeight // 2)
            scr.screen.blit(text_surface, text_rect)
            ship.lose_sound.play()
            asteroids.reset()
            ship.reset()
            bullets.reset()
            rocket.reset(ship.turret)
        
        if ship.playing == True:
            #ship.ambience_sound.play()
            """ Check for keyboard presses. """
            key = p.key.get_pressed()
                
            if (key[p.K_ESCAPE] == True): 
                running = False
            if (key[p.K_LEFT] == True): 
                inc = 'L'
                ship.turret.rotateTurret(inc)
                pass
            if (key[p.K_RIGHT] == True): 
                inc = 'R'
                ship.turret.rotateTurret(inc)
                pass
            if (key[p.K_w] == True): 
                inc = 'Up'
                ship.moveShip(inc)
                pass
            if (key[p.K_a] == True): 
                inc = 'L'
                ship.moveShip(inc)
                pass
            if (key[p.K_d] == True): 
                inc = 'R'
                ship.moveShip(inc)
                pass
            if (key[p.K_s] == True): 
                if ship.power_up == True:
                    ship.power_up = False
                    ship.shield = True
                    ship.shield_time = p.time.get_ticks()
                    ship.shield_sound.play()
                else:
                    p.mixer.Sound('sounds/error.wav').play()
                pass
            if (key[p.K_SPACE] == True):
                curr_fire_time = p.time.get_ticks()
                if curr_fire_time - last_fire_time >= 100:
                    last_fire_time = curr_fire_time
                    bullet = Bullet(ship.turret, scr)
                    bullets.fireBullet(bullet)
                pass
            if (key[p.K_r] == True): 
                if ship.power_up == True:
                    ship.power_up = False
                    rocket.flying = True
                    rocket.drawRocket(ship.turret)
                    rocket.rocket_flying_sound.play()
                else:
                    p.mixer.Sound('sounds/error.wav').play()
                pass
            if (key[p.K_t] == True):
                if ship.power_up == False and rocket.flying == True:
                    rocket.flying = False
                    rocket.explosion_playing = True
                    asteroids.didRocketHit(rocket, ship)
                    ship.didRocketHit(rocket)
                pass
            
            # Score
            displayScore(ship)
            displayShield(ship)
            displayRocket(ship)
            ship.didShieldExpire()
            # Collisions
            bullets.bulletCollision()
            asteroids.didAsteroidsCollide()
            asteroids.didBulletHit(bullets.bullets, ship, rocket)
            ship.didAsteroidHit(asteroids, rocket)
            ship.gotHit()
            # Drawing            
            ship.drawShip()
            ship.turret.rotateTurret('')
            bullets.drawBullets()
            if rocket.flying == True:
                rocket.drawRocket(ship.turret)
            rocket.drawExplosion()
            asteroids.drawAsteroids()
        
        p.display.flip()
    p.quit()
    
### MAIN ###
bg = p.image.load("graphics/space.jpg")
scr = Screen(bg)

graphics(scr)