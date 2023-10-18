import pygame as p
import random
import helperFunctions as hF
import ship
import constants as c
import asteroid
import bullet

def asteroids():
    p.init()

    size = (c.screenWidth, c.screenHeight)
    screen = p.display.set_mode(size)

    p.display.set_caption("asteroids")

    random.seed()

    gameState = 'running'

    clock = p.time.Clock()

    initialHeading = 270
    scaleFactor = 3
    spaceShip = ship.spaceShip(c.gameMidX, c.gameMidY, initialHeading,
                     scaleFactor, ship.basicShip)
    shipSpeed = 3

    # Bullet stuff
    bullets = []
    bulletSize = int(0.8 * scaleFactor)
    bulletSpeed = 3 * shipSpeed
    shotCount = 0

    maxSpeed = 15
    spaceShip.setGunSpot([14, 0])
    score = 0

    my_font = p.font.SysFont('Comic Sans MS', 15)
    healthText = my_font.render('Health', False, c.GREEN)
    
    bulletTime = False

    myAsteroids = []
    for j in range(c.nAsteroids):
        myAsteroids.append(asteroid.spaceRock())

    while True:
        for event in p.event.get():
            if event.type == p.QUIT:
                p.quit()

        key = p.key.get_pressed()
        
        # Handle keypresses.
        if (key[p.K_ESCAPE] == True): 
            p.quit()
        if (key[p.K_w] == True):
            if(spaceShip.gas > 1):
                spaceShip.thrustUp(1.005, maxSpeed, bulletTime)
                spaceShip.myDrawThrust = True
                spaceShip.drawThrust(screen, c.RED)
                spaceShip.gasDown(bulletTime)
        else:
            spaceShip.thrustDown()
            spaceShip.myDrawThrust = False
            if(spaceShip.gas <= 100):
                spaceShip.gasUp(bulletTime)
        if (key[p.K_a] == True):
            spaceShip.turn(-3)
        if (key[p.K_d] == True):
            spaceShip.turn(3)
        if (key[p.K_SPACE] == True):
            if (shotCount == 0):
                gunX, gunY = spaceShip.getGunSpot()
                myBullet = bullet.bullet(gunX, gunY, spaceShip.heading,
                                  bulletSize, bulletSpeed)
                bullets.append(myBullet)
                shotCount = c.maxShootingDelay
        if (key[p.K_RETURN] == True): 
            gameState = 'pause'
        if (key[p.K_p] == True): 
            p.mixer.music.unpause()
            gameState = 'running'
        if (key[p.K_TAB] == True):
            gameState = 'restart'
        if (key[p.K_f] == True):
            spaceShip.flashLightOn = True
        if (key[p.K_LSHIFT] == True):
            bulletTime = True

        if gameState == 'gameOver':
            text_surface = my_font.render('Game Over', False, c.GREEN)
            screen.blit(text_surface, (c.gameMidX, c.gameMidY))
            p.display.flip()

        if gameState == 'running':
            spaceShip.moveMe(bulletTime)

            for b in bullets:
                b.moveMe(bulletTime)

            for a in myAsteroids:
                a.moveMe(bulletTime)
                a.bouncing = False

            # Check to see if a bullet hit an asteroid.
            for a in myAsteroids:
                for b in bullets:
                    if (a.isActive and b.isActive):
                        smacked = a.checkCollision(b.x, b.y, False)
                        if (smacked == True):
                            b.setExplosion()
                            score += 1

            for a in myAsteroids:
                if (a.isActive):
                    smacked = a.checkCollision(spaceShip.x, spaceShip.y, False)
                    if(smacked):
                        spaceShip.health -= 1

            for a in myAsteroids:
                for A in myAsteroids:
                    if (a != A):
                        if (a.isActive and A.isActive):
                            if (a.bouncing == False) and (A.bouncing == False):
                                smacked = a.checkCollision(A.x, A.y, True)
                                #whacked = a.didAstroidsCollide(A.x, A.y, A.bounceRadius)
                                if (smacked == True):
                                    a.bounce()
                                    A.bounce()
                                    a.bouncing = True
                                    A.bouncing = True     
            
            if bulletTime:
                if spaceShip.flashLightOn:
                    spaceShip.battery -= 2 * c.bulletTimeSlowFactor
                if spaceShip.battery < 0:
                    spaceShip.flashLightOn = False
                    bulletTime = False
                if not spaceShip.flashLightOn:
                    if spaceShip.battery < 360:
                        spaceShip.battery += 1 * c.bulletTimeSlowFactor
            else:
                if spaceShip.flashLightOn:
                    spaceShip.battery -= 2
                if spaceShip.battery < 0:
                    spaceShip.flashLightOn = False
                    bulletTime = False
                if not spaceShip.flashLightOn:
                    if spaceShip.battery < 360:
                        spaceShip.battery += 1


            if (spaceShip.health == 0):
                gameState = 'gameOver'

            #Rendering stuff    
            #BackGround Stuff
            screen.fill(c.BLACK)

            #Conditional render for bullets
            for b in bullets:
                if (hF.getDist(b.x, b.y, spaceShip.x, spaceShip.y) <= 100):
                    b.isVisible = True
                else:
                    b.isVisible = False

                if spaceShip.flashLightOn:
                    b.isVisible = True
                if b.isVisible:
                    b.drawMe(screen, c.GREEN)

            #Conditional render for asteroids
            for a in myAsteroids:
                if(hF.getDist(a.x, a.y, spaceShip.x, spaceShip.y) <= 100):
                    a.isVisible = True
                else:
                    a.isVisible = False
                if spaceShip.flashLightOn:
                    a.isVisible = True
                if a.isVisible:
                    a.drawMe(screen)

            #Draw flashlight
            if spaceShip.flashLightOn:
                spaceShip.drawFlashlight(screen)

            spaceShip.drawMe(screen, c.BLUE, ship.basicShip)

            #Draw lens
            spaceShip.updateLens()
            spaceShip.drawLens(screen)

            if spaceShip.myDrawThrust:
                spaceShip.drawThrust(screen, c.RED)

            scoreToRender = 'Score: {}'.format(score.__str__())
            scoreText = my_font.render(scoreToRender, True, c.WHITE, c.BLACK)
            scoreTextRect = scoreText.get_rect()
            scoreTextRect.center = (c.screenWidth // 2, 100)
            screen.blit(scoreText, scoreTextRect)

            winningTextToRender = 'You win!'
            winningText = my_font.render(winningTextToRender, True, c.WHITE, c.BLACK)
            winningTextRect = winningText.get_rect()
            winningTextRect.center = (c.gameMidX, c.gameMidY)
            if (score >= 10):
                screen.blit(winningText, winningTextRect)
                spaceShip.health = 100

            #Draw health
            for x in range(spaceShip.health):
                p.draw.circle(screen, c.GREEN, [x * 20 + 20, c.screenHeight - 20], 5, 1)
            screen.blit(healthText, (20, c.screenHeight - 50))

            #Draw gas
            for x in range(int(spaceShip.gas)):
                p.draw.circle(screen, c.RED, [x * 2 + 20, c.screenHeight - 50], 3, 1)
            
            #Draw battery
            for x in range(int(spaceShip.battery/36)):
                p.draw.circle(screen, c.WHITE, [x * 2 + 20, c.screenHeight - 75], 5)

            #ForeGround stuff
            p.display.flip()

            clock.tick(60)

            # Implement shooting delay to keep bullet count lower.
            if (shotCount > 0):
                shotCount = shotCount - 1
                
            # Do some book keeping on arrays.
            # Remove inactive elements of bullets array.
            for b in bullets:
                if (b.isActive == False):
                    bullets.remove(b)
            # Remove inactive elements of asteroids array.
            for a in myAsteroids:
                if (a.isActive == False):
                    myAsteroids.remove(a)

asteroids()