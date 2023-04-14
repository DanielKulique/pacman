import pygame
from abc import ABCMeta, abstractmethod
import random

#iniciando code e adicionando tela

pygame.init()

screen = pygame.display.set_mode((800, 600), 0)
fonte = pygame.font.SysFont("arial", 40, True, False)

#cores
AMARELO = (255, 255, 0)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
BRANCO = (255, 255, 255)
VERMELHO = (255, 0, 0)
LARANJA = (255, 140, 0)
ROSA = (255, 150, 192)
CIANO = (0, 255, 255)

#direções
ACIMA = 1
ABAIXO = 2
DIREITA = 3
ESQUERDA = 4


class ElementoJogo(metaclass=ABCMeta):
    @abstractmethod
    def pintar(self, tela):
        pass
    
    @abstractmethod
    def calcular_regras(self):
        pass
    
    @abstractmethod
    def processar_eventos(self, eventos):
        pass


class Movivel(metaclass=ABCMeta):
    @abstractmethod
    def aceitar_movimento(self):
        pass
    
    @abstractmethod
    def recusar_movimento(self, direcoes):
        pass

    @abstractmethod
    def esquina(self, direcoes):
        pass


#movimento
VELOCIDADE = 1
PARADO = 0


class Cenario(ElementoJogo):
    def __init__(self, tamanho, pac):
        self.pac = pac
        self.moviveis = []
        self.pontos = 0
        # Estados possiveis 0-Jogando, 1-Pausado, 2-GameOver, 3-Vitória
        self.estado = 'JOGANDO'
        self.tamanho = tamanho
        self.vidas = 5
        self.matriz = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]


    def adicionar_movivel(self, obj):
        self.moviveis.append(obj)


    def pintar_score(self, tela):
        pontos_x =  30 * self.tamanho
        pontos_img = fonte.render(f'Score: {self.pontos}', True, AMARELO)
        vidas_img = fonte.render(f'Vidas {self.vidas}', True, AMARELO)
        tela.blit(pontos_img, (pontos_x, 50))
        tela.blit(vidas_img, (pontos_x, 100))


    def pintar_linha(self, tela, numero_linha, linha):
        for numero_coluna, coluna in enumerate(linha): #numero_coluna é feito pelo metod. enumerate
            x = numero_coluna * self.tamanho
            y = numero_linha * self.tamanho
            metade_tam = self.tamanho / 2
            cor = PRETO
            if coluna == 2:
                cor = AZUL
            pygame.draw.rect(tela, cor, (x, y, self.tamanho, self.tamanho), 0)
            if coluna == 1:
                pygame.draw.circle(tela, AMARELO, (x + metade_tam, y + metade_tam), self.tamanho // 10, 0)


    def pintar(self, tela):
        if self.estado == 'JOGANDO':
            self.pintar_jogando(tela)
        elif self.estado == 'PAUSADO':
            self.pintar_jogando(tela)
            self.pintar_pausado(tela)
        elif self.estado == 'GAMEOVER':
            self.pintar_jogando(tela)
            self.pintar_gameover(tela)
        elif self.estado == 'VITORIA':
            self.pintar_jogando(tela)
            self.pintar_vitoria(tela)


    def pintar_texto_centro(self, tela, texto, cor):
        texto_img = fonte.render(texto, True, cor)
        texto_x = (tela.get_width() - texto_img.get_width()) // 2
        texto_y = (tela.get_height() - texto_img.get_height()) // 2
        tela.blit(texto_img, (texto_x, texto_y))
    

    def pintar_vitoria(self, tela):
        self.pintar_texto_centro(tela, ' P A R A B É N S - V O C Ê - V E N C E U ! ! !', VERDE)


    def pintar_gameover(self, tela):
        self.pintar_texto_centro(tela, 'G A M E - O V E R', VERMELHO)
        

    def pintar_pausado(self, tela):
        self.pintar_texto_centro(tela, 'P A U S A D O', AMARELO)


    def pintar_jogando(self, tela):
        for numero_linha, linha in enumerate(self.matriz):
            self.pintar_linha(tela, numero_linha, linha)
        self.pintar_score(tela)

    
    def get_direcoes(self, linha, coluna):
        direcoes = []
        if self.matriz[int(linha - 1)][int(coluna)] != 2:
            direcoes.append(ACIMA)
        if self.matriz[int(linha + 1)][int(coluna)] != 2:
            direcoes.append(ABAIXO)
        if self.matriz[int(linha)][int(coluna - 1)] != 2:
            direcoes.append(ESQUERDA)
        if self.matriz[int(linha)][int(coluna + 1)] != 2:
            direcoes.append(DIREITA)
        return direcoes 

    def calcular_regras(self):
        if self.estado == 'JOGANDO':
            self.calcular_regras_jogando()
        elif self.estado == 'PAUSADO':
            self.calcular_regras_pausado()
        elif self.estado == 'GAMEOVER':
            self.calcular_regras_gameover()


    def calcular_regras_gameover(self):
        pass


    def calcular_regras_pausado(self):
        pass


    def calcular_regras_jogando(self):
        for movivel in self.moviveis:
            lin = int(movivel.linha)
            col = int(movivel.coluna)
            lin_intencao = int(movivel.linha_intencao)
            col_intencao = int(movivel.coluna_intencao)
            direcoes = self.get_direcoes(lin, col)
            if len(direcoes) >= 3:
                movivel.esquina(direcoes)
            if isinstance(movivel, Fantasma) and \
                movivel.linha == self.pac.linha and \
                    movivel.coluna == self.pac.coluna:
                self.vidas -= 1
                if self.vidas <= 0:
                    self.estado = 'GAMEOVER'
                else:
                    self.pac.linha = 1
                    self.pac.coluna = 1
            else:
                if 0 <= col_intencao < 28 and 0 <= lin_intencao < 29 and \
                self.matriz[lin_intencao][col_intencao] != 2:
                    movivel.aceitar_movimento()
                    if isinstance(movivel, Pacman) and self.matriz[lin][col] == 1:
                        self.pontos += 1
                        self.matriz[lin][col] = 0 
                        if self.pontos >= 306:
                            self.estado = 'VITORIA'
                else:
                    movivel.recusar_movimento(direcoes)


    def processar_eventos(self, evts):
            for e in evts:
                if e.type == pygame.QUIT:
                    exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_p:
                        if self.estado == 'JOGANDO':
                            self.estado = 'PAUSADO'
                        else:
                            self.estado = 'JOGANDO'


class Pacman(ElementoJogo, Movivel):
    def __init__(self, tamanho):
        self.coluna = 1
        self.linha = 1
        self.centro_x = 400
        self.centro_y = 300
        self.tamanho = tamanho
        self.vel_x = PARADO
        self.vel_y = PARADO
        self.raio = int(self.tamanho // 2)
        self.coluna_intencao = self.coluna
        self.linha_intencao = self.linha
        self.abertura = 0
        self.vel_abertura = 1


    def calcular_regras(self):
        self.coluna_intencao = self.coluna + self.vel_x
        self.linha_intencao = self.linha + self.vel_y
        self.centro_x = int(self.coluna * self.tamanho + self.raio)
        self.centro_y = int(self.linha * self.tamanho + self.raio)


    def pintar(self, tela):
        # desenhar o corpo do Pacman
        pygame.draw.circle(tela, AMARELO, (self.centro_x, self.centro_y), self.raio) #centro do pacman + o raio = desenho formato de circulo

        self.abertura += self.vel_abertura
        if self.abertura > self.raio:
            self.vel_abertura = -1
        if self.abertura <=0:
            self.vel_abertura = 1

        # desenho da boca
        canto_boca = (self.centro_x, self.centro_y)
        labio_superior = (self.centro_x + self.raio, self.centro_y - self.abertura)
        labio_inferior = (self.centro_x + self.raio, self.centro_y + self.abertura)
        pontos_boca = [canto_boca, labio_superior, labio_inferior]
        pygame.draw.polygon(tela, PRETO, pontos_boca, 0)

        # olhos do pacman
        olho_x = int(self.centro_x + self.raio / 3)
        olho_y = int(self.centro_y - self.raio * 0.70)
        olho_raio = int(self.raio / 7)
        pygame.draw.circle(tela, PRETO, (olho_x, olho_y), olho_raio, 0)


    def processar_eventos(self, eventos):
        #captura de eventos
        for e in eventos:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:     #DIREITA
                    self.vel_x = VELOCIDADE
                elif e.key == pygame.K_LEFT:    #ESQUERDA
                    self.vel_x = -VELOCIDADE
                elif e.key == pygame.K_UP:      #PARA CIMA
                    self.vel_y = -VELOCIDADE
                elif e.key == pygame.K_DOWN:    #PARA BAIXO
                    self.vel_y = VELOCIDADE
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.vel_x = PARADO
                elif e.key == pygame.K_LEFT:
                    self.vel_x = PARADO
                elif e.key == pygame.K_UP:
                    self.vel_y = PARADO
                elif e.key == pygame.K_DOWN:
                    self.vel_y = PARADO


    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao


    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna


    def esquina(self, direcoes):
        pass


class Fantasma(ElementoJogo):
    def __init__(self, cor, tamanho):
        self.coluna = 13
        self.linha = 15
        self.velocidade = 1
        self.direcao = ABAIXO
        self.tamanho = tamanho
        self.cor = cor
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna


    def pintar(self, tela):
        fatia = self.tamanho // 8
        px = int(self.coluna * self.tamanho)
        py = int(self.linha * self.tamanho)
        contorno = [(px, py + self.tamanho),
                    (px + fatia, py + fatia * 2),
                    (px + fatia * 2, py + fatia // 2),
                    (px + fatia * 3, py),
                    (px + fatia * 5, py),
                    (px + fatia * 6, py + fatia // 2),
                    (px + fatia * 7, py + fatia * 2),
                    (px + self.tamanho, py + self.tamanho)]
        pygame.draw.polygon(tela, self.cor, contorno)
        

        olho_raio_ext = fatia       #externo
        olho_raio_int = fatia // 2  #interno

        olho_e_x = int(px + fatia * 2.5)    #olho esquerdo
        olho_e_y = int(py + fatia * 2.5)    

        olho_d_x = int(px + fatia * 5.5)
        olho_d_y = int(py + fatia * 2.5)

        pygame.draw.circle(tela, BRANCO, (olho_e_x, olho_e_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_e_x, olho_e_y), olho_raio_int, 0)
        pygame.draw.circle(tela, BRANCO, (olho_d_x, olho_d_y), olho_raio_ext, 0)
        pygame.draw.circle(tela, PRETO, (olho_d_x, olho_d_y), olho_raio_int, 0)

                       

    def calcular_regras(self):
        if self.direcao == ACIMA:
            self.linha_intencao -= self.velocidade
        elif self.direcao == ABAIXO:
            self.linha_intencao += self.velocidade
        elif self.direcao == DIREITA:
            self.coluna_intencao += self.velocidade
        else: 
            self.coluna_intencao -= self.velocidade
    
    def mudar_direcao(self, direcoes):
        self.direcao = random.choice(direcoes)

    def esquina(self, direcoes):
        self.mudar_direcao(direcoes)

    def aceitar_movimento(self):
        self.linha = self.linha_intencao
        self.coluna = self.coluna_intencao

    def recusar_movimento(self, direcoes):
        self.linha_intencao = self.linha
        self.coluna_intencao = self.coluna
        self.mudar_direcao(direcoes)


    def processar_eventos(self, evts):
        pass
    

if __name__ == "__main__":
    tamanho_blocos = (600 // 30)
    pacman = Pacman(tamanho_blocos)
    blinky = Fantasma(VERMELHO, tamanho_blocos)
    inky = Fantasma(CIANO, tamanho_blocos)
    clyde = Fantasma(LARANJA, tamanho_blocos)
    pinky = Fantasma(ROSA, tamanho_blocos)
    cenario = Cenario(tamanho_blocos, pacman)
    cenario.adicionar_movivel(pacman)
    cenario.adicionar_movivel(blinky)
    cenario.adicionar_movivel(inky)
    cenario.adicionar_movivel(clyde)
    cenario.adicionar_movivel(pinky)



while True:
    #calcular as regras
    pacman.calcular_regras()
    blinky.calcular_regras()
    inky.calcular_regras()
    clyde.calcular_regras()
    pinky.calcular_regras()
    cenario.calcular_regras()
    


    #pintar a tela
    screen.fill(PRETO)
    cenario.pintar(screen)
    pacman.pintar(screen)
    blinky.pintar(screen)
    inky.pintar(screen)
    clyde.pintar(screen)
    pinky.pintar(screen)
    pygame.display.update()
    pygame.time.delay(100)


    #captura de eventos
    eventos = pygame.event.get()
    pacman.processar_eventos(eventos)
    cenario.processar_eventos(eventos)