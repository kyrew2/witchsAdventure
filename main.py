# Importa as bibliotecas necessárias
import pygame
from recursos.funcoes import lerLogs, salvarLog
import math
import random


#inicializa o pygame
pygame.init()
 
#Cria a janela do jogo
tela = pygame.display.set_mode((1000, 700))
pygame.display.set_caption("Witch's Adventure")

#Cores
preto = (0, 0, 0)
branco = (255,  255, 255)
amarelo = (255, 255, 0)
roxo = (123,104,238)
roxo2 = (128, 0, 128)

pontos = 0

relogio = pygame.time.Clock()
fase = 5000


fundo = pygame.image.load("recursos/fundo.png")
fundo = pygame.transform.scale(fundo, (fase, 1000))
bruxaParada = pygame.image.load("recursos/bruxaV2.png")
bruxaParada = pygame.transform.scale(bruxaParada, (60, 80))
bruxaFrameAndando1 = pygame.image.load("recursos/bruxaAnda.png")
bruxaFrameAndando1 = pygame.transform.scale(bruxaFrameAndando1, (60, 80))
bruxaFrameAndando2 = pygame.image.load("recursos/bruxaAnda2.png")
bruxaFrameAndando2 = pygame.transform.scale(bruxaFrameAndando2, (60, 80))
iconeStart = pygame.image.load("recursos/iconeStart.png")
iconeStartSelecionado = pygame.image.load("recursos/iconeStartSelecionado.png")
iconeStart = pygame.transform.scale(iconeStart, (200, 180))
iconeStartSelecionado = pygame.transform.scale(iconeStartSelecionado, (200, 180))
iconeMorte = pygame.image.load("recursos/iconeMorte.png")
iconeMorte = pygame.transform.scale(iconeMorte, (200, 180))
telaPause = pygame.image.load("recursos/telaPause.png")

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
contaAnimacao = 0
velocidadeAnimacao= 7

# Configuração dos vagalumes
numVagalumes = 22
vagalumes = []
for _ in range(numVagalumes):
    x = random.randint(800, 4000)  # posição X no cenário
    y = random.randint(80, 300)    # posição Y no cenário
    raio = random.randint(4, 8)    # tamanho base do vagalume
    offset = random.uniform(0, 2 * math.pi)  # para pulsar em tempos diferentes
    cor = (255, 255, random.randint(120, 200))  # tom amarelado
    vagalumes.append({'x': x, 'y': y, 'raio': raio, 'offset': offset, 'cor': cor})

def desenharVagalumes(tela, tempo, cameraBruxa, vagalumes):
    for v in vagalumes:
        raio = int(v['raio'] + 2 * math.sin(tempo * 2 + v['offset']))
        xTela = v['x'] - cameraBruxa + math.sin(tempo + v['offset']) * 10
        yTela = v['y'] + math.cos(tempo + v['offset']) * 8
        haloSurface = pygame.Surface((raio * 4, raio * 4), pygame.SRCALPHA)
        pygame.draw.circle(haloSurface, (*v['cor'], 60), (raio * 2, raio * 2), int(raio * 1.7))
        tela.blit(haloSurface, (xTela - raio * 2, yTela - raio * 2))
        pygame.draw.circle(tela, v['cor'], (int(xTela), int(yTela)), raio)


def menuJogo():
    fonteTitulo = pygame.font.SysFont(None, 78)
    fonteTutorial = pygame.font.SysFont(None, 48)
    fonteInput = pygame.font.SysFont(None, 48)
    rodandoMenu = True
    nomeJogador = ""
    inputAtivo = False

    while rodandoMenu:
        tela.fill((roxo))
        mousePosicao = pygame.mouse.get_pos()
        mouseClick = pygame.mouse.get_pressed()[0]

        textoTitulo = fonteTitulo.render("Witch's Adventure", True, (roxo2))
        tela.blit(textoTitulo, (260, 250))

        # Caixa de input para nome
        inputColisao = pygame.Rect(tela.get_width() // 2 - 150, 150, 300, 50)
        corInput = (200, 200, 255) if inputAtivo else (180, 180, 180)
        pygame.draw.rect(tela, corInput, inputColisao, 0, border_radius=8)
        textoNome = fonteInput.render(nomeJogador, True, (preto))
        tela.blit(textoNome, (inputColisao.x + 10, inputColisao.y + 10))

        # Botão Start (ícone)
        iconeColisao = iconeStart.get_rect(center=(465, 500))
        mouseSobreBotao = iconeColisao.collidepoint(mousePosicao)
        if mouseSobreBotao:
            tela.blit(iconeStartSelecionado, iconeColisao)
            if mouseClick and nomeJogador.strip():
                rodandoMenu = False
        else:
            tela.blit(iconeStart, iconeColisao)

        textoStart = fonteTutorial.render("Use as setas para controlar a bruxa e Z para atirar", True, (branco))
        tela.blit(textoStart, (tela.get_width() // 2 - textoStart.get_width() // 2, iconeColisao.bottom + 20))

        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if inputAtivo:
                    if evento.key == pygame.K_RETURN:
                        inputAtivo = False
                    elif evento.key == pygame.K_BACKSPACE:
                        nomeJogador = nomeJogador[:-1]
                    else:
                        if len(nomeJogador) < 16 and evento.unicode.isprintable():
                            nomeJogador += evento.unicode
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Primeiro, verifica se clicou no botão Start
                if iconeColisao.collidepoint(evento.pos) and nomeJogador.strip():
                    rodandoMenu = False
                # Depois, verifica se clicou na caixa de texto
                elif inputColisao.collidepoint(evento.pos):
                    inputAtivo = True
                else:
                    inputAtivo = False

    return nomeJogador

def telaMorte(nomeJogador, pontos):
    salvarLog(nomeJogador, pontos)
    fonteTitulo = pygame.font.SysFont(None, 72)
    fonteLog = pygame.font.SysFont(None, 15)
    logs = lerLogs()
    rodando = True

    while rodando:
        tela.fill((roxo))
        textoMorte = fonteTitulo.render("Você Morreu!", True, (roxo2))
        tela.blit(iconeMorte, (370, 300))
        tela.blit(textoMorte, (tela.get_width() // 2 - textoMorte.get_width() // 2, 100))
        tela.blit(fonteLog.render("Últimas 5 partidas:", True, (255, 255, 0)), (30, 30))
        for i, linha in enumerate(logs):
            tela.blit(fonteLog.render(linha.strip(), True, (branco)), (30, 60 + i * 30))
        textoContinuar = fonteLog.render("Clique para jogar novamente", True, (branco))
        tela.blit(textoContinuar, (tela.get_width() // 2 - textoContinuar.get_width() // 2, 600))
        pygame.display.flip()
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                rodando = False  
def pausarJogo():
    pausado = True
    fonte = pygame.font.SysFont(None, 28)
    while pausado:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:  # Pressione ESPAÇO para despausar
                    pausado = False
        overlay = pygame.Surface((1000, 700))
        overlay.set_alpha(5)  # 0 = totalmente transparente, 255 = opaco
        overlay.fill((roxo))  # Cor preta
        tela.blit(overlay, (0, 0))
        tela.blit(telaPause, (300, 250))
        textoPause = fonte.render("Pressione ESPAÇO para continuar!", True, branco)
        tela.blit(textoPause, (350, 500))
        pygame.display.flip()
def resetarJogo():
    global velocidadeAnimacaoMagia, contaAnimacaoMagia, frameMagia, velocidadeAnimacaoMoeda, contaAnimacaoMoeda, frameMoeda, posicaoBruxaX, posicaoBruxaY, movimentoBruxaX
    global movimentoBruxaY, pula, magias, velocidadeMagia, gravidade, chaoFase, segundoChaoFase, plataformas, inimigos, patrulhaInimigos, direcaoInimigos, moedas, pontos
    
    pontos = 0
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
while True:
    nomeJogador = menuJogo()
    resetarJogo()

    rodando = True
    while rodando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                exit()
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
                telaMorte(nomeJogador, pontos)
                rodando = False

        #Frames (na tela) da bruxa
        if movimentoBruxaX != 0:
            contaAnimacao += 1
            if contaAnimacao >= velocidadeAnimacao:
                contaAnimacao = 0
                frameBruxa = (frameBruxa + 1) % len(framesAndando)
            bruxa  = framesAndando[frameBruxa]
        else:
            bruxa = bruxaParada
            frameBruxa = 0
            contaAnimacao = 0
        
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
        parallax = 0.3
        offsetFundo = int(cameraBruxa * parallax)
        tela.blit(fundo, (-offsetFundo, 0))
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
                telaMorte(nomeJogador, pontos)
                rodando = False
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
                    pontos += 1
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
                pontos += 1

        if bruxaVirada:
            mostraBruxa = pygame.transform.flip(bruxa, True, False)
        else:
            mostraBruxa = bruxa
        tela.blit(mostraBruxa, (posicaoBruxaX - cameraBruxa, posicaoBruxaY))

        fontePontos = pygame.font.SysFont(None, 36)
        textoPontos = fontePontos.render(f"Pontos: {pontos}", True, branco)
        tela.blit(textoPontos, (20,20))
        fontePause = pygame.font.SysFont(None, 24)
        textoPause = fontePause.render("Press SPACE to Pause Game", True, (200, 200, 200))
        tela.blit(textoPause, (textoPontos.get_width() + 35, 26))
        #Atualiza a tela e limita o FPS
        tempo = pygame.time.get_ticks() / 1000
        desenharVagalumes(tela, tempo, cameraBruxa, vagalumes)
        pygame.display.flip()
        relogio.tick(60)