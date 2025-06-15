# Importa as bibliotecas necessárias
import pygame
import os


#inicializa o pygame
pygame.init()
 
#Cria a janela do jogo
tela = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Witch's Adventure")

#Cores
preto = (0, 0, 0)
branco = (255,  255, 255)
amarelo = (255, 255, 0)

relogio = pygame.time.Clock()
fase = 5000


#jogador
fundo = pygame.image.load("recursos/fundo.png")
fundo = pygame.transform.scale(fundo, (fase, 1000))
bruxaParada = pygame.image.load("recursos/bruxaV2.png")
bruxaParada = pygame.transform.scale(bruxaParada, (60, 80))
bruxaFrameAndando1 = pygame.image.load("recursos/bruxaAnda.png")
bruxaFrameAndando1 = pygame.transform.scale(bruxaFrameAndando1, (60, 80))
bruxaFrameAndando2 = pygame.image.load("recursos/bruxaAnda2.png")
bruxaFrameAndando2 = pygame.transform.scale(bruxaFrameAndando2, (60, 80))

tamanhoMoedaX = 30
tamanhoMoedaY = 40
framesMoeda = [
    pygame.image.load("recursos/moedaFrame1.png"),
    pygame.image.load("recursos/moedaFrame2.png"),
    pygame.image.load("recursos/moedaFrame3.png"),
    pygame.image.load("recursos/moedaFrame4.png"),
    pygame.image.load("recursos/moedaFrame5.png"),
    pygame.image.load("recursos/moedaFrame6.png"),
    pygame.image.load("recursos/moedaFrame7.png"),
]
framesMoeda = [pygame.transform.scale(frame, (tamanhoMoedaX, tamanhoMoedaY)) for frame in framesMoeda]
frameMoeda = 0
contaAnimacaoMoeda = 0
velocidadeAnimacaoMoeda = 7

tamanhoMagia = 30
framesMagia = [
    pygame.image.load(f"recursos/magiaFrame{i}.png") for i in range(1,8)

]
framesMagia = [pygame.transform.scale(frame, (tamanhoMagia, tamanhoMagia)) for frame in framesMagia]
frameMagia = 0
contaAnimacaoMagia = 0
velocidadeAnimacaoMagia = 5
bruxaVirada = False
cameraBruxa = 0



framesAndando = [bruxaParada, bruxaFrameAndando1, bruxaFrameAndando2]
frameBruxa = 0
contaAnimação = 0
velocidadeAnimação = 7

def menuJogo():
    fonte = pygame.font.SysFont(None, 72)
    textoMenu = fonte.render("APERTE ENTER PARA JOGAR", True, (255, 255, 255))
    rodandoMenu = True
    while rodandoMenu:
        tela.fill((0, 0, 0))
        tela.blit(textoMenu, (tela.get_width()//2 - textoMenu.get_width()//2, tela.get_height()//2 - textoMenu.get_height()//2))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    rodandoMenu = False
def telaMorte():
    fonte = pygame.font.SysFont(None, 72)
    textoMorte1 = fonte.render("VOCÊ MORREU", True, (255, 0, 0))
    textoMorte2 = pygame.font.SysFont(None, 36).render("Pressione ENTER para reiniciar", True, (255, 255, 255))
    while True:
        tela.fill((0, 0, 0))
        tela.blit(textoMorte1, (tela.get_width()//2 - textoMorte1.get_width()//2, tela.get_height()//2 - textoMorte1.get_height()//2 - 40))
        tela.blit(textoMorte2, (tela.get_width()//2 - textoMorte2.get_width()//2, tela.get_height()//2 + 20))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return
def pausarJogo():
    pausado = True
    fonte = pygame.font.SysFont(None, 72)
    textoPause = fonte.render("PAUSADO", True, (255, 255, 255))
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Pressione ESPAÇO para despausar
                    pausado = False
        tela.blit(textoPause, (tela.get_width()//2 - textoPause.get_width()//2, tela.get_height()//2 - textoPause.get_height()//2))
        pygame.display.flip()

def resetarJogo():
    global velocidadeAnimacaoMagia, contaAnimacaoMagia, frameMagia, velocidadeAnimacaoMoeda, contaAnimacaoMoeda, frameMoeda, posicaoBruxaX, posicaoBruxaY, movimentoBruxaX, movimentoBruxaY, pula, magias, velocidadeMagia, gravidade, chaoFase, segundoChaoFase, plataformas, inimigos, patrulhaInimigos, direcaoInimigos, moedas
    

    #Posição e movimento da bruxa
    posicaoBruxaX = 100
    posicaoBruxaY = 500
    movimentoBruxaX = 0
    movimentoBruxaY = 0


    magias = []
    velocidadeMagia = 10

    #Gravidade e pulo
    gravidade = 1
    pula = False

    #Chão e plataformas da fase

    chaoFase = pygame.Rect(0, 600, 1500, 100)
    segundoChaoFase = pygame.Rect(4000, 600, fase, 100)
    plataformas = [
        pygame.Rect(0, 600, 1500, 100),
        pygame.Rect(4000, 600, fase, 100),
        pygame.Rect(1000, 450, 200, 50),
        pygame.Rect(1300, 350, 700, 50),
        pygame.Rect(2180, 450, 200, 50),
        pygame.Rect(2500, 350, 200, 50),
        pygame.Rect(2800, 390, 200, 50),
        pygame.Rect(3200, 350, 200, 50),
        pygame.Rect(3600, 490, 200, 50),
    ]

    #inimigos
    inimigos = [
        pygame.Rect(500, 550, 50, 50),
        pygame.Rect(1100, 400, 50, 50),
        pygame.Rect(1400, 300, 50, 50),
        pygame.Rect(2250, 400, 50, 50),
        pygame.Rect(2550, 300, 50, 50),
        pygame.Rect(2850, 340, 50, 50),
        pygame.Rect(3250, 300, 50, 50),
        pygame.Rect(3650, 440, 50, 50),
    ]
    patrulhaInimigos = [
        (500, 1000),
        (1000, 1150),
        (1300, 1950),
        (2180, 2330),
        (2500, 2650),
        (2800, 2950),
        (3200, 3350),
        (3600, 3750),

    ]
    direcaoInimigos = [1] * len(inimigos)
    #moedas
    moedas = [

        pygame.Rect(1085, 350, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(1550, 400, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(1550, 500, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(1400, 200, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(1500, 200, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(1600, 200, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(1700, 200, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(1800, 200, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(1900, 200, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(2220, 350, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(2300, 350, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(2300, 130, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(2530, 250, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(2630, 250, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(2850, 130, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(2840, 300, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(2920, 300, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(3100, 130, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(3220, 300, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(3340, 300, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(3630, 400, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(3730, 400, tamanhoMoedaX, tamanhoMoedaY),
        pygame.Rect(3950, 240, tamanhoMoedaX, tamanhoMoedaY),

    ]
menuJogo()
resetarJogo()
#Loop Principal
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
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_UP and not pula:
            pula = True
            movimentoBruxaY = -20
        elif evento.type == pygame.KEYUP and evento.key == pygame.K_z:
            direcao = -1 if bruxaVirada else 1
            magiaX = posicaoBruxaX + (0 if bruxaVirada else bruxaParada.get_width())
            magiaY = posicaoBruxaY + bruxaParada.get_height() // 2
            magias.append([pygame.Rect(magiaX, magiaY, tamanhoMagia, tamanhoMagia), direcao, magiaX, 0, 0])
        elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE:
            pausarJogo()
            

        if posicaoBruxaY > 700:
            telaMorte()

    #Frames (na tela) da bruxa
    if movimentoBruxaX != 0:
        contaAnimação += 1
        if contaAnimação >= velocidadeAnimação:
            contaAnimação = 0
            frameBruxa = (frameBruxa + 1) % len(framesAndando)
        bruxa  = framesAndando[frameBruxa]
    else:
        bruxa = bruxaParada
        frameBruxa = 0
        contaAnimação = 0
    
    if movimentoBruxaX < 0:
        bruxaVirada = True
    elif movimentoBruxaX > 0:
        bruxaVirada = False

    #Atualiza a posição da bruxa
    
    movimentoBruxaY += gravidade

    posicaoBruxaX +=movimentoBruxaX
    posicaoBruxaY +=movimentoBruxaY

    if posicaoBruxaX > fase:
        posicaoBruxaX = fase
    elif posicaoBruxaX < 0:
        posicaoBruxaX = 0
        

    #Colisão da Bruxa com o chão e plataformas
    colisaoBruxa = pygame.Rect(posicaoBruxaX, posicaoBruxaY, bruxaParada.get_width(), bruxaParada.get_height())

    #configuração camera
    cameraBruxa = posicaoBruxaX - 350
    if cameraBruxa < 0:
        cameraBruxa = 0
    elif cameraBruxa > fase - 1000:
        cameraBruxa = fase - 1000
    
    #Mostra na tela
    tela.blit(fundo, (-cameraBruxa, 0))
    if colisaoBruxa.colliderect(chaoFase):
        posicaoBruxaY = chaoFase.y - bruxa.get_height()
        movimentoBruxaY = 0
        pula = False
    
    pygame.draw.rect(tela, branco, (chaoFase.x - cameraBruxa, chaoFase.y, chaoFase.width, chaoFase.height))
    pygame.draw.rect(tela, branco, (segundoChaoFase.x - cameraBruxa, segundoChaoFase.y, segundoChaoFase.width, segundoChaoFase.height))

    #Colisão da bruxa com chão e plataformas
    for plataforma in plataformas:
        pygame.draw.rect(tela, branco, (plataforma.x - cameraBruxa, plataforma.y, plataforma.width, plataforma.height))
        if (
            colisaoBruxa.colliderect(plataforma) and movimentoBruxaY >= 0 and posicaoBruxaY + bruxa.get_height() - movimentoBruxaY <= plataforma.y):
            posicaoBruxaY = plataforma.y - bruxa.get_height()
            movimentoBruxaY = 0
            pula = False
    
    #Colisão da bruxa com o inimigos
    for i,inimigo in enumerate(inimigos):
        pygame.draw.rect(tela, preto, (inimigo.x - cameraBruxa, inimigo.y, inimigo.width, inimigo.height))
        if colisaoBruxa.colliderect(inimigo):
            telaMorte()
            posicaoBruxaX = 100
            posicaoBruxaY = 500
            movimentoBruxaY = 0
            pula = False
        inimigo.x += direcaoInimigos[i] * 2
        minimoX, maximoX = patrulhaInimigos[i]
        if inimigo.x < minimoX or inimigo.x > maximoX:
            direcaoInimigos[i] *= -1
    
    #Desenha e atualiza as magias
        
    for magia in magias[:]:
        magia[4] += 1
        if magia[4] >= 5:
            magia[4] = 0
            magia[3] = (magia[3] + 1) % len(framesMagia)
        # Flip se direção for -1
        frame = framesMagia[magia[3]]
        if magia[1] == -1:
            frame = pygame.transform.flip(frame, True, False)
        tela.blit(frame, (magia[0].x - cameraBruxa, magia[0].y))
        magia[0].x += magia[1] * 10
        
        if magia[0].x < 0 or magia[0].x > fase:
            magias.remove(magia)

        magiaColisao = pygame.Rect(magia[0].x, magia[0].y, tamanhoMagia, tamanhoMagia)
        for i, inimigo in enumerate(inimigos[:]):
            if magiaColisao.colliderect(inimigo):
                inimigos.pop(i)
                patrulhaInimigos.pop(i)
                direcaoInimigos.pop(i)
                if magia in magias:
                    magias.remove(magia)
                break
            
    #Desenha e colisão das moedas  
    contaAnimacaoMoeda += 1
    if contaAnimacaoMoeda >= velocidadeAnimacaoMoeda:
        contaAnimacaoMoeda = 0
        frameMoeda = (frameMoeda + 1) % len(framesMoeda)

        

    for moeda in moedas[:]:
        moedaColisao = pygame.Rect(moeda.x, moeda.y, tamanhoMoedaX, tamanhoMoedaY)
        tela.blit(framesMoeda[frameMoeda], (moeda.x - cameraBruxa, moeda.y))
        if colisaoBruxa.colliderect(moeda):
            moedas.remove(moeda)

    if bruxaVirada:
        mostraBruxa = pygame.transform.flip(bruxa, True, False)
    else:
        mostraBruxa = bruxa
    tela.blit(mostraBruxa, (posicaoBruxaX - cameraBruxa, posicaoBruxaY))

    #Atualiza a tela e limita o FPS
    pygame.display.flip()
    relogio.tick(60)