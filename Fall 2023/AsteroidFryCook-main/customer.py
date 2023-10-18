import pygame as p
import random


class customer():

    def __init__(self, x=0, y=0, gameWidth=2000, gameHeight=2000):

        self.x = x
        self.y = y
        self.gameWidth = gameWidth
        self.gameHeight = gameHeight

        self.satiated = False

        # select sprite
        selection = random.randrange(1, 9, 2)

        file1 = "./sprites/aliens/customers_" + str(selection) + ".png"
        file2 = "./sprites/aliens/customers_" + str(selection + 1) + ".png"

        self.images = []
        self.images.append(p.image.load(file1))
        self.images.append(p.image.load(file2))
        self.images[0] = p.transform.scale(self.images[0], (self.images[0].get_width() * 2, self.images[0].get_height() * 2))
        self.images[1] = p.transform.scale(self.images[1], (self.images[1].get_width() * 2, self.images[1].get_height() * 2))

        self.rect = p.rect.Rect(self.x, self.y, self.images[0].get_width(), self.images[0].get_height())
    

    def drawMe(self, screen):

        # update rectangle
        self.rect.x = self.x
        self.rect.y = self.y

        i = 0

        if self.satiated:
            i += 1
        
        screen.blit(self.images[i], (self.rect.x, self.rect.y))

        # make sure customer doesn't leave bounds
        if (self.x < 0 - self.images[0].get_width()):
            self.x = self.gameWidth
        elif (self.x > self.gameWidth):
            self.x = 0

        if (self.y < 0 - self.images[0].get_height()):
            self.y = self.gameHeight
        elif (self.y > self.gameHeight):
            self.y = 0

        #p.draw.rect(screen, (0, 255, 0), self.rect, 2)


    def checkCollision(self, ship):

        if not self.satiated:
            collide = self.rect.colliderect(ship.collRect)

            if collide and ship.ammo > 0:
                ship.ammo -= 1
                self.satiated = True
        
        else:
            collide = False

        return collide