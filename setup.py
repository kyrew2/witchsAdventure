import sys
from cx_Freeze import setup, Executable

# --- CONFIGURAÇÕES BÁSICAS ---
# ALtere para o nome do seu script principal do jogo (ex: 'main.py')
scriptPrincipal = "main.py"

# Informações da aplicação
nomeJogo = "Witch's Adventure"
versao = "1.0"
descricao = "Um jogo de plataforma 2D com visual e gameplay retrô"

# --- OPÇÕES DE BUILD (MAIS IMPORTANTES PARA VOCÊ) ---
buildExeOptions = {
    # 'packages': Lista de pacotes que o cx_Freeze DEVE incluir.
    # Inclua todos os pacotes que você usa diretamente ou que são importantes para suas dependências.
    "packages": ["pygame", "speech_recognition", "pyttsx3", "os", "math", "random", "datetime", "sys", "aifc", "chunk", "audioop","http", "http.client"],
    # 'includes': Módulos específicos que podem não ser detectados automaticamente.
    # Adicione aqui se o executável der "ModuleNotFoundError" para um módulo Python.
    "includes": [],
    # 'excludes': Módulos que você sabe que NÃO usa e quer EXCLUIR para reduzir o tamanho do executável.
    "excludes": [
        "tkinter", "unittest", "email", "html", "xml", "distutils",
        "pydoc", "sqlite3", "test", "PyQt5", "numpy", "IPython",
        "jupyter_client", "matplotlib", "pandas", "scipy", "setuptools"
    ],
    # 'include_files': Arquivos e pastas que DEVEM ser incluídos no executável.
    # MUITO IMPORTANTE para seus recursos e arquivos externos!
    "include_files": [
        "recursos/",  # Inclui toda a sua pasta 'recursos' (imagens, sons, etc.)
        # Se 'recursos/funcoes.py' e 'recursos/reconhecerFala.py' não forem detectados
        # como imports internos, você pode precisar adicioná-los:
        # ("recursos/funcoes.py", "funcoes.py"),
        # ("recursos/reconhecerFala.py", "reconhecerFala.py"),
        # Dependências específicas do PyAudio ou pyttsx3:
        # ATENÇÃO: Essas linhas são CUIDADOSAS. Tente SEM elas primeiro.
        # Se você tiver ModuleNotFoundError para '_portaudio' ou problemas com pyttsx3,
        # pode ser necessário adicionar DLLs ou módulos específicos.
        # Exemplo (NÃO GARANTIDO, caminho pode variar):
        # r"C:\Python39\Lib\site-packages\pyaudio\_portaudio.cp39-win_amd64.pyd",
        # r"C:\Python39\Lib\site-packages\pyttsx3" # Isso tentaria incluir a pasta pyttsx3 inteira
    ],
    "optimize": 1,  # Nível de otimização (1 ou 2)
    "silent": True, # Suprime algumas mensagens de build (opcional, pode remover para ver mais detalhes)
}

# --- CONFIGURAÇÃO DO EXECUTÁVEL ---
# 'base="Win32GUI"' esconde a janela do console no Windows, ideal para jogos.
# Se você quiser que o console apareça para ver erros/prints, remova 'base'.
base = None
if sys.platform == "win32":
    base = "Win32GUI"
elif sys.platform == "darwin": # Para macOS
    base = "MacOSX"

executables = [
    Executable(
        scriptPrincipal,
        base=base,
        target_name=f"{nomeJogo}.exe", # Nome do arquivo .exe final
        icon="recursos/iconeBruxa.ico" # Caminho para o seu arquivo de ícone
    )
]

# --- SETUP PRINCIPAL ---
setup(
    name=nomeJogo,
    version=versao,
    description=descricao,
    options={"build_exe": buildExeOptions},
    executables=executables
)