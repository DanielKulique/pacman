import pygame

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)

fonte = pygame.Sysfont("arial", 48, True, False)

texto = 'ola mundo pygame'

fonte = pygame.font.SysFont('arial', 48, True, False)
img_texto = fonte.render(texto, True, (255, 255, 0), 0)

while True:
    screen.blit(img_texto, (100, 100))
    pygame.display.update()
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()
