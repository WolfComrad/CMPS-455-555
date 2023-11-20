import pygame, sys
def youwon():
    pygame.init()
    clock = pygame.time.Clock()
    width,height = 800,800
    screen = pygame.display.set_mode((width,height))
    pygame.display.set_caption("You Won!!")
    font = pygame.font.Font('freesansbold.ttf', 130)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill((30,30,30))
        text = font.render("YOU WON!!", True, 'blue')
        text_rect = text.get_rect(center=(width//2,height//2))
        screen.blit(text, text_rect)
        pygame.display.flip()