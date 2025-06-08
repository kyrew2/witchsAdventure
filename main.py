# Importa as bibliotecas necessárias
import pygame
import os
import recursos


#inicializa o pygame
pygame.init()
 
#Cria a janela do jogo
tela = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Jogo de plataforma")

fase = 5000

#Cores
preto = (0, 0, 0)
branco = (255,  255, 255)
amarelo = (255, 255, 0)

relogio = pygame.time.Clock()



#jogador
fundo = pygame.image.load("recursos/fundo.png")
fundo = pygame.transform.scale(fundo, (fase, 1000))
bruxaParada = pygame.image.load("recursos/bruxaV2.png")
bruxaParada = pygame.transform.scale(bruxaParada, (60, 80))
bruxaFrameAndando1 = pygame.image.load("recursos/bruxaAnda.png")
bruxaFrameAndando1 = pygame.transform.scale(bruxaFrameAndando1, (60, 80))
bruxaFrameAndando2 = pygame.image.load("recursos/bruxaAnda2.png")
bruxaFrameAndando2 = pygame.transform.scale(bruxaFrameAndando2, (60, 80))
bruxaVirada = False
cameraBruxa = 0


framesAndando = [bruxaParada, bruxaFrameAndando1, bruxaFrameAndando2]
frame = 0
contaAnimação = 0
velocidadeAnimação = 7

#Posição e movimento da bruxa
posicaoBruxaX = 100
posicaoBruxaY = 500
movimentoBruxaX = 0
movimentoBruxaY = 0


#Gravidade e pulo
gravidade = 1
pula = False

#Chão da fase

chaoFase = pygame.Rect(0, 600, fase, 100)
plataformas = [
    pygame.Rect(1000, 450, 200, 50),#plataforma 1
    pygame.Rect(1300, 350, 700, 50),#plataforma 2
    pygame.Rect(2200, 450, 200, 50),#plataforma 3
 ]

moedas = [
    pygame.Rect(1100, 400, 40, 40),
    pygame.Rect(1500, 200, 40, 40),
    pygame.Rect(1600, 200, 40, 40),
    pygame.Rect(1700, 200, 40, 40),
    pygame.Rect(1800, 200, 40, 40),
    pygame.Rect(1900, 200, 40, 40),  
]

#Loop Principal do Jogo 
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
            movimentoBruxaX = 5
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
            movimentoBruxaX = -5
        elif evento.type == pygame.KEYUP and (evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT):
            movimentoBruxaX = 0  
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:     
            movimentoBruxaX = 0
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP and not pula:
            pula = True
            movimentoBruxaY = -20
            


    #Frames (na tela) da bruxa
    
    if movimentoBruxaX != 0:
        contaAnimação += 1
        if contaAnimação >= velocidadeAnimação:
            contaAnimação = 0
            frame = (frame + 1) % len(framesAndando)
        bruxa  = framesAndando[frame]
    else:
        bruxa = bruxaParada
        frame = 0
        contaAnimação = 0
    
    if movimentoBruxaX < 0:
        bruxaVirada = True
    elif movimentoBruxaX > 0:
        bruxaVirada = False

    #Atualiza a posição da bruxa
    colisaoBruxa = pygame.Rect(posicaoBruxaX, posicaoBruxaY, bruxaParada.get_width(), bruxaParada.get_height())
    movimentoBruxaY += gravidade
    posicaoBruxaX +=movimentoBruxaX
    posicaoBruxaY +=movimentoBruxaY
    if posicaoBruxaX > fase:
        posicaoBruxaX = fase
    elif posicaoBruxaX < 0:
        posicaoBruxaX = 0
        

    #Colisão da Bruxa com o chão e plataformas

    cameraBruxa = posicaoBruxaX - 350
    if cameraBruxa < 0:
        cameraBruxa = 0
    elif cameraBruxa > fase - 1000:
        cameraBruxa = fase - 1000

    #Mostra na tela
    tela.blit(fundo, (-cameraBruxa, 0))
    if colisaoBruxa.colliderect(chaoFase):
        posicaoBruxaY = 600 - bruxa.get_height()
        movimentoBruxaY = 0
        pula = False
    
    pygame.draw.rect(tela, branco, (chaoFase.x - cameraBruxa, chaoFase.y, chaoFase.width, chaoFase.height))
    for plataforma in plataformas:
        pygame.draw.rect(tela, branco, (plataforma.x - cameraBruxa, plataforma.y, plataforma.width, plataforma.height))
        if colisaoBruxa.colliderect(plataforma) and movimentoBruxaY >= 0:
            posicaoBruxaY = plataforma.y - bruxa.get_height()
            movimentoBruxaY = 0
            pula = False
        

    for moeda in moedas:
        pygame.draw.rect(tela, amarelo, (moeda.x - cameraBruxa, moeda.y, moeda.width, moeda.height))




      # Desenha o chão
    if bruxaVirada:
        mostraBruxa = pygame.transform.flip(bruxa, True, False)
    else:
        mostraBruxa = bruxa
    tela.blit(mostraBruxa, (posicaoBruxaX - cameraBruxa, posicaoBruxaY))

    #Atualiza a tela e limita o FPS
    pygame.display.flip()
    relogio.tick(60)