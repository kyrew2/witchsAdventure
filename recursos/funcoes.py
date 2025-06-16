import datetime



def lerLogs(caminhoLog="recursos/log.dat", maxLinhas=5):
    try:
        with open(caminhoLog, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            return linhas[-maxLinhas:]
    except FileNotFoundError:
        return []

def salvarLog(nomeJogador, pontos, caminhoLog="recursos/log.dat"):
    agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    with open(caminhoLog, "a", encoding="utf-8") as f:
        f.write(f"{nomeJogador} - Pontos: {pontos} - {agora}\n")

