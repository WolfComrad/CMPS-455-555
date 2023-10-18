import pygame as p

framerate = 60

class animatedSprite(p.sprite.Sprite):

    def __init__(self, x, y, images, scale=1):
        super().__init__()

        self.images = images

        self.width = images[0].get_width()
        self.height = images[0].get_height()
        
        # scale images in for loop
        ind = 0
        for i in self.images:
            i = p.transform.scale(i, (i.get_width() * scale, i.get_height() * scale))
            self.images[ind] = i

            ind += 1

        self.rect = p.Rect(x, y, self.width, self.height)

        self.animSpeed = 0.1
        self.frames = len(images)
        self.currFrame = 0


    def play(self, screen):

        currFrame = int(self.currFrame // 1)

        screen.blit(self.images[currFrame], (self.rect.x, self.rect.y))

        if self.currFrame < self.frames - self.animSpeed:
            self.currFrame += self.animSpeed
        else:
            self.currFrame = 0


    # speed is frames
    def set_speed(self, speed):
        self.animSpeed = speed