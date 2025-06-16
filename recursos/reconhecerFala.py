import speech_recognition as sr
import pyttsx3

engine = pyttsx3.init()
engine.setProperty('rate', 150)

def reconhecerFala():
    reconhecedor = sr.Recognizer()
    with sr.Microphone() as fonte:
        print("Diga seu nome...")
        audio = reconhecedor.listen(fonte)
    try:
        texto = reconhecedor.recognize_google(audio, language="pt-BR")
        return texto
    except Exception:
        return ""

def falarNome(nome):  # <-- Corrigido: agora recebe o nome como argumento
    engine.say(f"Olá, {nome}!")
    engine.runAndWait()
