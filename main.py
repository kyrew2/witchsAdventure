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

relogio = pygame.time.Clock()



#jogador
bruxa = pygame.image.load("recursos/bruxa.png")
posicaoBruxaX = 100
posicaoBruxaY = 500
movimentoBruxaX = 0
movimentoBruxaY = 0
gravidade = 1
pula = False


#Loop Principal do Jogo
rodando = True
while rodando:
    #Verifica os eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
            movimentoBruxaX = 15
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
            movimentoBruxaX = -15
        elif evento.type == pygame.KEYUP and (evento.key == pygame.K_RIGHT or evento.key == pygame.K_LEFT):
            movimentoBruxaX = 0  
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:     
            movimentoBruxaX = 0
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP and not pula:
            pula = True
            movimentoBruxaY -=20
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_UP:
            pula = False
            movimentoBruxaY += 20


    posicaoBruxaX +=movimentoBruxaX
    posicaoBruxaY +=movimentoBruxaY
    
    pygame.draw.rect(tela, branco, (5000, 550, 1000, 150)) #desenha o chão
    if pula:
        movimentoBruxaY += gravidade
    else:
        movimentoBruxaY = 0
    tela.fill(preto)
    tela.blit(bruxa, (posicaoBruxaX, posicaoBruxaY))

    pygame.display.flip()
    relogio.tick(60) #Limita a 60 FPS