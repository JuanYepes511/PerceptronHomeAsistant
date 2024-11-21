# pip install wolframalpha 
# pip install pyttsx3 
# pip install tkinter   
# pip install wikipedia 
# pip install SpeechRecognition 
# pip install ecapture 
# pip install pyjokes 
# pip install twilio 
# pip install requests 
# pip install beautifulsoup4 
# pip install winshell 
# pip install feedparser 
# pip install clint 
# pip install pyaudio 
# pip install pipwin 
# pip install openai 
# pip install pyfiglet 
# pip install pygame 
# pip install pillow

import pyttsx3
import time
import pygame
import threading
from PIL import Image
import pyfiglet
import subprocess
import wolframalpha
import openai
import pyttsx3
import json
#import random
#import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import winshell
import pyjokes
#import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
#from bs4 import BeautifulSoup
#import win32com.client as wincl
from urllib.request import urlopen
# pip install requests gradio
import gradio as gr
from pygame import mixer
import re
from typing import Union


# Configura tu token de API para META-Llama

API_TOKEN = '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'  # Reemplaza con tu token de API
MODEL_ID = 'meta-llama/Meta-Llama-3-8B-Instruct'  # Reemplaza con el ID del modelo que deseas usar

# Define la URL de la API
url = f'https://api-inference.huggingface.co/models/{MODEL_ID}'

# Configura los headers para la autenticación
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

# Configuración del motor de voz
def setup_voice_engine():
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)
    voices = engine.getProperty('voices')
    # Seleccionar voz en español
    for voice in voices:
        if 'spanish' in voice.languages and 'male' in voice.name:
            engine.setProperty('voice', voice.id)
            break
    return engine
pygame.init()
def speak(texto):
    def on_end():
        nonlocal hilo_animacion
        hilo_animacion.join()  
        print("Pronunciación terminada") 

    num_palabras = len(texto.split())
    tasa_palabras_por_minuto = 150
    tiempo_estimado_minutos = num_palabras / tasa_palabras_por_minuto
    tiempo_estimado_segundos = tiempo_estimado_minutos * 60

    hilo_animacion = threading.Thread(target=animar_boca, args=(0.3, tiempo_estimado_segundos))
    hilo_animacion.start()   
    engine= setup_voice_engine()
    print(f"Perceptron: {texto}")
    engine.say(texto)
    engine.runAndWait()
    
ancho, alto = 600, 600
ventana = pygame.display.set_mode((ancho, alto))
pygame.display.set_caption('Sincronización de Voz')

# Carga las imágenes de boca abierta y cerrada
boca_abierta = pygame.image.load('images/asistente.png')
boca_cerrada = pygame.image.load('images/asistente.png')


def mostrar_boca(abierta):

    ventana.fill((255, 255, 255))  # Fondo blanco
    if abierta:
        ventana.blit(boca_abierta, (ancho // 2 - boca_abierta.get_width() // 2, alto // 2 - boca_abierta.get_height() // 2))
    else:
        ventana.blit(boca_cerrada, (ancho // 2 - boca_cerrada.get_width() // 2, alto // 2 - boca_cerrada.get_height() // 2))
    pygame.display.flip()


def animar_boca(intervalo, duracion):
    tiempo_inicio = time.time()
    while time.time() - tiempo_inicio < duracion:
        tiempo_actual = time.time() - tiempo_inicio
        if int(tiempo_actual / intervalo) % 2 == 0:
            mostrar_boca(True)
        else:
            mostrar_boca(False)
        pygame.time.wait(50)  # Espera un poco antes de actualizar la pantalla
    mostrar_boca(False)  # Asegúrate de mostrar la boca cerrada después

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Escuchando...")
        speak("Te escucho")  # Agregado para confirmar que está escuchando
        # Ajustar el umbral de energía dinámicamente
        r.adjust_for_ambient_noise(source, duration=1)
        r.pause_threshold = 1
        r.energy_threshold = 300  # Reducido para mayor sensibilidad
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=5)
            print("Procesando tu solicitud...")
            query = r.recognize_google(audio, language='es-ES')
            print(f"Has dicho: {query}")
            return query.lower()
        except sr.WaitTimeoutError:
            print("No se detectó ningún audio")
            return ""
        except sr.UnknownValueError:
            print("No pude entender el audio")
            speak("No pude entender, ¿podrías repetirlo?")
            return ""
        except sr.RequestError as e:
            print(f"Error en el servicio de reconocimiento: {e}")
            speak("Hay un problema con el servicio de reconocimiento")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

# Nuevas funciones para el hogar inteligente
def control_luces(comando, ubicacion="todas"):
    if "encender" in comando:
        speak(f"Encendiendo las luces de {ubicacion}")
    elif "apagar" in comando:
        speak(f"Apagando las luces de {ubicacion}")
    elif "atenuar" in comando:
        speak(f"Atenuando las luces de {ubicacion}")

def control_temperatura(comando):
    if "subir" in comando:
        speak("Aumentando la temperatura a 24 grados")
    elif "bajar" in comando:
        speak("Bajando la temperatura a 20 grados")
    elif "consultar" in comando:
        speak("La temperatura actual es de 22 grados")

def control_seguridad(comando):
    if "activar" in comando:
        speak("Activando sistema de seguridad")
    elif "desactivar" in comando:
        speak("Desactivando sistema de seguridad")
    elif "estado" in comando:
        speak("El sistema de seguridad está activo")

def rutina_automatica(tipo):
    if tipo == "mañana":
        speak("Ejecutando rutina de buenos días")
        control_luces("encender", "dormitorio")
        control_temperatura("subir")
        # Más acciones...
    elif tipo == "noche":
        speak("Ejecutando rutina nocturna")
        control_luces("apagar", "todas")
        control_temperatura("bajar")
        control_seguridad("activar")

def wishMe():
    global assname
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Buenos días, bienvenido a casa!")
    elif hour>= 12 and hour<18:
        speak("Buenas tardes, bienvenido a casa!")   
    else: 
        speak("Buenas noches, bienvenido a casa!")  
  
    assname =("Perceptrona")
    speak("Soy "+assname+" tu asistente personal para el hogar")

def username():
    global uname
    speak("¿Cómo te gustaría que te llame?")
    uname = takeCommand()
    speak(f"Bienvenido a tu hogar inteligente, {uname}")
    speak("Si necesitas ayuda, solo di 'Perceptrona' y estaré listo para ayudarte")
    
    
 
def otra():
    time.sleep(2)

    
    speak("puedes continuar usando el asistente")

# Realiza la solicitud POST a la API
def chat_function(message, history, system_prompt, max_new_tokens, temperature):
    # Asegúrate de que la temperatura sea estrictamente positiva
    if temperature <= 0:
        return "La temperatura debe ser mayor que 0."

    data = {
        'inputs': message,
        'parameters': {
            'max_new_tokens': max_new_tokens,
            'temperature': temperature,
            'return_full_text': False
        }
    }

    # Añadir system_prompt si no es vacío
    if system_prompt:
        data['system_prompt'] = system_prompt

    response = requests.post(url, headers=headers, json=data)

    # Verifica el estado de la respuesta
    if response.status_code == 200:
        # Procesa la respuesta
        result = response.json()
        # Verifica si la respuesta contiene el texto generado
        if 'generated_text' in result:
            return result['generated_text']
        elif isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        else:
            return "No se pudo generar una respuesta adecuada."
    else:
        return f'Error: {response.status_code}, {response.text}'

# Configuración de APIs
WOLFRAM_APP_ID = "TETJ9H-98TRL5UQEV"  # Necesitas registrarte en Wolfram Alpha
wikipedia.set_lang('es')
def calcular_wolfram(query: str):
    """Función específica para cálculos complejos con Wolfram Alpha"""
    try:
        client = wolframalpha.Client(WOLFRAM_APP_ID)
        res = client.query(query)
        respuesta = next(res.results).text
        return respuesta
    except Exception as e:
        return f"Error al consultar Wolfram Alpha: {str(e)}"
# Función para reproducir música
def reproducir_musica(cancion=None):
    try:
        mixer.init()
        if cancion:
            # Aquí podrías implementar una búsqueda en una carpeta de música
            speak(f"Reproduciendo {cancion}")
            # mixer.music.load(ruta_cancion)
        else:
            # Reproducir música por defecto
            speak("Reproduciendo música")
            # mixer.music.load("ruta_por_defecto.mp3")
        mixer.music.play()
    except Exception as e:
        speak("Lo siento, no pude reproducir la música")

# Función para búsquedas en internet
def buscar_wikipedia(consulta):
    try:
        speak("Buscando en Wikipedia...")
        resultado = wikipedia.summary(consulta, sentences=2)
        speak(resultado)
    except:
        speak("No pude encontrar información sobre eso en Wikipedia")

def extraer_numeros(texto: str) -> list:
    """Extrae números del texto, incluyendo decimales"""
    return [float(num) for num in re.findall(r'-?\d*\.?\d+', texto)]

def calcular_local(query: str) -> Union[float, str]:
    """Realiza cálculos básicos sin necesidad de API externa"""
    try:
        numeros = extraer_numeros(query)
        if len(numeros) < 2:
            return "No detecté suficientes números para realizar el cálculo"
        
        if "suma" in query or "más" in query or "+" in query:
            return sum(numeros)
        elif "resta" in query or "menos" in query or "-" in query:
            return numeros[0] - sum(numeros[1:])
        elif "multiplica" in query or "por" in query or "x" in query:
            resultado = 1
            for num in numeros:
                resultado *= num
            return resultado
        elif "divide" in query or "entre" in query or "/" in query:
            if 0 in numeros[1:]:
                return "No puedo dividir entre cero"
            resultado = numeros[0]
            for num in numeros[1:]:
                resultado /= num
            return resultado
        else:
            return "No reconocí la operación a realizar"
    except Exception as e:
        return f"Error al realizar el cálculo: {str(e)}"

def calcular(query: str):
    """Función principal para manejar cálculos"""
    # Limpieza básica del query
    query = query.lower().replace("cuánto es", "").replace("calcula", "").strip()
    
    # Intentar cálculo local primero
    resultado = calcular_local(query)
    
    if isinstance(resultado, (int, float)):
        speak(f"El resultado es {resultado}")
    elif "wolfram" in query:  # Solo usar Wolfram para consultas específicas o complejas
        try:
            client = wolframalpha.Client(WOLFRAM_APP_ID)
            res = client.query(query)
            respuesta = next(res.results).text
            speak(f"Según Wolfram Alpha, el resultado es {respuesta}")
        except Exception as e:
            speak("Lo siento, no pude realizar ese cálculo con Wolfram Alpha")
    else:
        speak(resultado)

# Función para contar chistes
def contar_chiste():
    try:
        chiste = pyjokes.get_joke(language='es')
        speak(chiste)
    except:
        speak("Lo siento, no pude recordar ningún chiste en este momento")

# Función para búsquedas web
def buscar_google(query):
    speak(f"Buscando {query} en Google")
    webbrowser.open(f"https://www.google.com/search?q={query}")

# Configuración de OpenWeatherMap
OPENWEATHER_API_KEY = "TU-API-KEY-AQUI"
# Ciudad por defecto (puedes modificarla)
CIUDAD_DEFAULT = "Bucaramanga,CO"



# Modificar la función de interacción principal
def interaccion():
    speak("¿En qué puedo ayudarte?")
    while True:
        query = takeCommand()
        
        if not query:  # Si no hay comando, continuar escuchando
            continue
            
        print(f"Procesando comando: {query}")  # Debug
        
        # Hora actual
        if any(palabra in query for palabra in ["hora", "qué hora", "dime la hora"]):
            strTime = datetime.datetime.now().strftime("%H:%M")
            speak(f"Son las {strTime}")

        # Música
        elif any(palabra in query for palabra in ["reproduce", "música", "canción", "pon"]):
            if "reproduce" in query:
                cancion = query.replace("reproduce", "").strip()
                reproducir_musica(cancion)
            else:
                reproducir_musica()
     #noticias
        elif 'noticia' in query:
                
            try: 
                api_news='a3a77c24281644b5a598d70a6f1e887c'
                jsonObj = urlopen('''https://newsapi.org/v2/everything?q=colombia&from=2024-03-18&sortBy=publishedAt&apiKey=a3a77c24281644b5a598d70a6f1e887c''')
                data = json.load(jsonObj)
                i = 1
                    
                speak('Aquí hay algunas noticias de colombia.')
                print('''=============== NOTICIAS ============'''+ '\n')
                    
                for item in data['articles']:
                        
                    print(str(i) + '. ' + item['title'] + '\n')
                    print(item['description'] + '\n')
                    speak(str(i) + '. ' + item['title'] + '\n')
                    i += 1
            except Exception as e:
                    
                print(str(e))
            
            otra()
            break

        # Wikipedia
        elif any(palabra in query for palabra in ["busca", "qué es", "quién es", "información"]):
            buscar_wikipedia(query)
        #notas
        elif "escribe una nota" in query or "escribir nota" in query or "toma una nota" in query:
            speak("Qué quisiera que yo escribiera")
            note = takeCommand()
            file = open('nota.txt', 'w')
            file.write(note)
        #mostrar notas
        elif "mostrar la nota" in query or "ver la nota" in query or "ver nota" in query or "muestre la nota" in query :
            speak("mostrando la nota")
            file = open("nota.txt", "r") 
            print(file.read())
            speak(file.read(6))   
        # Cálculos matemáticos
        elif any(palabra in query for palabra in ["calcula", "cuánto es", "suma", "resta", "multiplica", "divide", "más", "menos", "por", "entre"]):
            print(f"Procesando cálculo: {query}")  # Debug
            calcular(query)

        # Chistes
        elif "chiste" in query:
            contar_chiste()

        # Búsqueda en Google
        elif "google" in query or "busca en internet" in query:
            buscar_google(query.replace("google", "").replace("busca en internet", "").strip())

        # Control de luces (simulado)
        elif "luces" in query:
            if "encender" in query or "prender" in query:
                speak("Simulando encender las luces")
            elif "apagar" in query:
                speak("Simulando apagar las luces")

        # Control de temperatura (simulado)
        elif "temperatura" in query:
            if "subir" in query:
                speak("Simulando subir la temperatura")
            elif "bajar" in query:
                speak("Simulando bajar la temperatura")
            else:
                speak("La temperatura simulada es de 22 grados")
        #camara
        elif "cámara" in query or "foto" in query:
            speak("Espera un 30 segundos mientras activo la camara, tomo una foto y cierra la imagen para continuar")
            ec.capture(0, "foto", "img.jpg")
        # Clima
        elif "clima" in query:
                
            # Google Open weather website
            # to get API of Open weather 
            api_key = "b175155b402c44d69e3a12377008afca"
            base_url = "http://api.openweathermap.org/data/2.5/weather?"
            speak(" Dime la ciudad ")
            print("El clima de : ")
            city_name = takeCommand()
            complete_url = base_url + "appid=" + api_key + "&q=" + city_name
            response = requests.get(complete_url) 
            x = response.json() 
            print(response.text)

            if x["cod"] != "404" and x["cod"] != "400": 
                y = x["main"] 
                current_temperature = str(round(float(y["temp"] - 273.15 ),0))
                current_pressure = y["pressure"] 
                current_humidity = y["humidity"] 
                z = x["weather"] 
                weather_description = z[0]["description"] 
                speak(" Temperatura es= " +str(current_temperature)+"grados centigrados"+"\n presión atmosférica="+str(current_pressure) +"hpa"+"\n la humedad es= " +str(current_humidity)+"porciento") 
            else:
                speak(" la ciudad no fué encontrada o no la entendí ")
            otra()
            break

        # Gestión de alarmas
        elif "alarma" in query:
            if "crear" in query or "pon" in query or "establece" in query:
                crear_alarma(query)
            elif "listar" in query or "mostrar" in query:
                listar_alarmas()
            elif "eliminar" in query or "borrar" in query:
                eliminar_alarma(query)
            else:
                speak("¿Qué deseas hacer con las alarmas? Puedo crear, listar o eliminar alarmas")

        # Salir
        elif any(palabra in query for palabra in ["salir", "adiós", "terminar", "finalizar"]):
            speak("Hasta luego, que tengas un buen día")
            break

        # Respuesta por defecto
        else:
            speak("No entendí tu solicitud. ¿Podrías repetirla?")

def print_message(mensaje):
    # Crear un objeto Figlet con el estilo deseado
    font = pyfiglet.Figlet(font='slant')
    
    # Generar el texto ASCII art
    ascii_art = font.renderText(mensaje)
    
    # Imprimir el texto ASCII art
    print(ascii_art)

def takeCommand2():
     
    r = sr.Recognizer()     
    with sr.Microphone() as source:
         
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=2)
    try:
        print("Reconociendo...")    
        activa = r.recognize_google(audio, language ='es-ES')
        print(f"dijiste : {activa}\n")
    except Exception as e:
        print(e)    
        print("No entendi.")  
        return ""
     
    return activa

# Lista para almacenar las alarmas activas
alarmas = []

class Alarma(threading.Thread):
    def __init__(self, hora, minutos, descripcion=""):
        super().__init__()
        self.hora = hora
        self.minutos = minutos
        self.descripcion = descripcion
        self.activa = True
        self.daemon = True  # El hilo se cerrará cuando el programa principal termine

    def run(self):
        while self.activa:
            ahora = datetime.now()
            if ahora.hour == self.hora and ahora.minute == self.minutos:
                self.sonar_alarma()
                break
            time.sleep(30)  # Revisar cada 30 segundos

    def sonar_alarma(self):
        try:
            mixer.init()
            # Puedes cambiar el sonido por defecto
            mixer.music.load("ruta/a/tu/sonido/alarma.mp3")  
            mixer.music.play()
            mensaje = f"¡Alarma! Son las {self.hora:02d}:{self.minutos:02d}"
            if self.descripcion:
                mensaje += f". Recordatorio: {self.descripcion}"
            speak(mensaje)
            time.sleep(30)  # Sonar por 30 segundos
            mixer.music.stop()
        except Exception as e:
            speak("¡Alarma activada!")
            print(f"Error al reproducir sonido: {e}")

def extraer_tiempo(query):
    """Extrae la hora y minutos de la consulta del usuario"""
    # Buscar patrones como "7:30", "07:30", "7 y 30"
    patrones = [
        r'(\d{1,2}):(\d{2})',  # 7:30, 07:30
        r'(\d{1,2})\s*y\s*(\d{2})',  # 7 y 30
        r'(\d{1,2})\s*horas?\s*(?:con)?\s*(\d{2})',  # 7 horas 30, 7 horas con 30
    ]
    
    for patron in patrones:
        match = re.search(patron, query)
        if match:
            hora = int(match.group(1))
            minutos = int(match.group(2))
            return hora, minutos
    return None, None

def crear_alarma(query):
    """Crea una nueva alarma basada en la consulta del usuario"""
    hora, minutos = extraer_tiempo(query)
    
    if hora is None or minutos is None:
        speak("No pude entender la hora. Por favor, especifica la hora en formato hora:minutos")
        return

    # Validar hora y minutos
    if not (0 <= hora <= 23 and 0 <= minutos <= 59):
        speak("La hora especificada no es válida")
        return

    # Extraer descripción si existe
    descripcion = ""
    if "para" in query:
        descripcion = query.split("para")[-1].strip()

    # Crear y iniciar la alarma
    alarma = Alarma(hora, minutos, descripcion)
    alarmas.append(alarma)
    alarma.start()

    speak(f"Alarma establecida para las {hora:02d}:{minutos:02d}")
    if descripcion:
        speak(f"Recordatorio: {descripcion}")

def listar_alarmas():
    """Lista todas las alarmas activas"""
    if not alarmas:
        speak("No hay alarmas activas")
        return

    speak("Alarmas activas:")
    for i, alarma in enumerate(alarmas, 1):
        mensaje = f"Alarma {i}: {alarma.hora:02d}:{alarma.minutos:02d}"
        if alarma.descripcion:
            mensaje += f" - {alarma.descripcion}"
        speak(mensaje)

def eliminar_alarma(query):
    """Elimina una alarma específica o todas las alarmas"""
    if "todas" in query:
        for alarma in alarmas:
            alarma.activa = False
        alarmas.clear()
        speak("Todas las alarmas han sido eliminadas")
    else:
        listar_alarmas()
        speak("Di el número de la alarma que deseas eliminar")
        numero = takeCommand()
        try:
            indice = int(numero) - 1
            if 0 <= indice < len(alarmas):
                alarma = alarmas.pop(indice)
                alarma.activa = False
                speak(f"Alarma de las {alarma.hora:02d}:{alarma.minutos:02d} eliminada")
            else:
                speak("Número de alarma no válido")
        except ValueError:
            speak("No pude entender el número de alarma")

if __name__ == '__main__':
    clear = lambda: os.system('cls')    
    clear()
    print_message('Bienvenido')
    wishMe()
    username()
    
    print("Sistema iniciado y listo para escuchar")
    speak("Sistema iniciado y listo para escuchar")

    while True:
        print("Di 'perceptrona' para activarme...")
        query = takeCommand().lower()
        
        if query:  # Solo procesar si hay un comando
            print(f"Comando detectado: {query}")  # Debug
            
            if any(nombre in query for nombre in ['perceptron', 'perceptrona', 'perceptro','percep','periodo']):
                
                interaccion()
            elif any(palabra in query for palabra in ['salir', 'apagar', 'terminar']):
                speak("Gracias por visitarnos")
                print_message('Gracias')
                break

   
pygame.quit()
