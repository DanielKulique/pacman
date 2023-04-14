import pygame
from time import sleep

pygame.init()
#constantes
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
VELOCIDADE = 0.1
RAIO = 30

tela = pygame.display.set_mode((640, 480), 0)
x = 10 #bola horizontal
y = 10 #bola vertical
vel_x = VELOCIDADE #velocidade de x
vel_y = VELOCIDADE #velocidade de y
while True:
    # calcula as regras
    x += vel_x
    y += vel_y
    if (x + RAIO) > 640:
        vel_x -= VELOCIDADE
    if (x - RAIO) < 0:
        vel_x = VELOCIDADE
    if (y + RAIO) > 480:
        vel_y -= VELOCIDADE
    if (y - RAIO) < 0:
        vel_y = VELOCIDADE

    # pinta
    tela.fill(PRETO)
    pygame.draw.circle(tela, (AMARELO), (int(x), int(y)), 30, 0)
    pygame.display.update()

    # eventos
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            exit()


