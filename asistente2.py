#
#python -m venv env    version 3.9.12
#cd env  
#cd Script
#.\activate.bat
#python.exe -m pip install --upgrade pip
#pip install wolframalpha
#pip install pyttsx3
#pip install tkinter  No instalado
#pip install wikipedia
#pip install SpeechRecognition
#pip install ecapture
#pip install pyjokes
#pip install twilio
#pip install requests
#pip install beautifulsoup4
#pip install winshell
#pip install feedparser
#pip install clint
#pip install pyaudio
#pip install pipwin
#pip install openai
#pip install pyfiglet
#pip install pygame
#pip install pillow

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


# Configura tu token de API para META-Llama

API_TOKEN = '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'  # Reemplaza con tu token de API
MODEL_ID = 'meta-llama/Meta-Llama-3-8B-Instruct'  # Reemplaza con el ID del modelo que deseas usar

# Define la URL de la API
url = f'https://api-inference.huggingface.co/models/{MODEL_ID}'

# Configura los headers para la autenticación
headers = {
    'Authorization': f'Bearer {API_TOKEN}'
}

engine = pyttsx3.init()
engine.setProperty('rate', 150)
voices = engine.getProperty('voices')
# Seleccionar la voz de hombre en español
for voice in voices:
    if 'spanish' in voice.languages and 'male' in voice.name:
        engine.setProperty('voice', voice.id)
        break
wikipedia.set_lang("es")

# Inicializa pygame
pygame.init()

# Configura la ventana
ancho, alto = 250, 250
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

def speak(texto):
    
    def on_end():
        nonlocal hilo_animacion
        hilo_animacion.join()  # Espera a que el hilo de animación termine
        print("Pronunciación terminada")
    
    engine.connect('finished-utterance', on_end)
    
    # Calcula el tiempo estimado de pronunciación
    num_palabras = len(texto.split())
    tasa_palabras_por_minuto = 150
    tiempo_estimado_minutos = num_palabras / tasa_palabras_por_minuto
    tiempo_estimado_segundos = tiempo_estimado_minutos * 60

    # Inicia el hilo de animación
    hilo_animacion = threading.Thread(target=animar_boca, args=(0.3, tiempo_estimado_segundos))
    hilo_animacion.start()

    # Reproduce el texto
    engine .say(texto)
    engine .runAndWait()

def wishMe():
    global assname
    hour = int(datetime.datetime.now().hour)
    if hour>= 0 and hour<12:
        speak("Buenos dias !")
  
    elif hour>= 12 and hour<18:
        speak("Buenas tardes !")   
  
    else: 
        speak("Buenas Noches !")  
  
    assname =("Smartina")
    speak("Soy "+assname+" su asistente en el laboratorio")
    #speak(assname)
    
 
def username():
    global uname
    speak("Cual es su nombre")
    uname = takeCommand()
    speak(uname+",Bienvenido al Centro de desarrollo tecnológico")
    speak("Si dices Smartina, estaré listo a ayudarte")
    columns = shutil.get_terminal_size().columns
     
    print("###############################################".center(columns))
    print("Bienvenido al Centro de Desarrollo Tecnológico".center(columns))
    print("Smart Region Lab".center(columns))
    print("###############################################".center(columns))

 
def takeCommand():
     
    r = sr.Recognizer()     
    with sr.Microphone() as source:
         
        print("Escuchando...")
        r.pause_threshold = 1
        audio = r.listen(source, phrase_time_limit=4)
    try:
        print("Reconociendo...")    
        query = r.recognize_google(audio, language ='es-ES')
        print(f"dijiste : {query}\n")
  
    except Exception as e:
        print(e)    
        print("No entendi.")  
        return ""
     
    return query

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
  
def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 465)
    server.ehlo()
    server.starttls()
     
    # Enable low security in gmail
    server.login('adiaz@unab.edu.co', 'Intelig321!Arti')
    server.sendmail('adiaz@unab.edu.co', to, content)
    server.close()

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


def interaccion():
    i=0
    while True:
        if i==0:
            speak("En qué te puedo ayudar")
            i=1
            print("Escuchando...")
        query = takeCommand().lower()
        if 'wikipedia' in query:
            speak('Qué quieres buscar en Wikipedia...')
            query = takeCommand()
            try:
                results = wikipedia.summary(query, sentences = 1)
                speak("De acuerdo a Wikipedia")
                speak(results)
                speak('Puedes ir a la página de Wikipedia si quieres más información')
            except Exception as e:
                print(e)
                speak("No fué posible encontrar esa información en Wikipedia")
            otra()
            break

        elif 'abra youtube' in query or 'abrir youtube' in query or 'youtube' in query:
            speak("En esta página abrí Youtube\n")
            webbrowser.open("youtube.com")
            otra()
            break
        
        elif 'centro de desarrollo' in query or "cdt" in query or "cdt unab" in query or "soluciones iot" in query or "desarrollo tecnológico" in query or "smart" in query:
            speak('Los centros de desarrollo tecnológico son organizaciones públicas o privadas, dedicadas al desarrollo de proyectos de investigación aplicada, el desarrollo de tecnología propia y actividades de transferencia que responden a necesidades y/o oportunidades de desarrollo social y económico del país, sus regiones y/o ciudades.')
            #speak("Te llevo a una página que te sirve de referencia\n")
            otra()
            break
            #webbrowser.open("https://apolo.unab.edu.co/es/organisations/centro-de-desarrollo-tecnol%C3%B3gico-smart-regions-center")

        elif 'objetivo del laboratorio' in query :
            speak("El Centro de Desarrollo Tecnológico (CDT) Smart Regions es un centro enfocado en el diseño y desarrollo de proyectos de CTeI, tecnologías propias y actividades de transferencia que responden a necesidades y/o oportunidades de desarrollo social y económico, articulando Sociedad, Estado, Empresa y Academia soportados en investigación y uso de tecnologías 4.0 para la transformación digital, creando valor sostenible y escalable para territorios inteligentes.\n")
            otra()
            break

        elif 'temas de laboratorio' in query :
            speak("Los temas que cubre el CDT son: Estructuración de proyectos de I+D+I, Entrenamiento y formación especializada, Diseño, desarrollo y validación de soluciones tecnológicas,Vigilancia Tecnológica e Inteligencia Competitiva, Consultoría especializada en innovación. El Smart Center Lan donde estas ubicado se divide en espacios de trabajo que comprende: Area de ideación, de diseño, prototipado superficial, desarrollo electrónico, Manufactura, y prueba de concepto terminal")
            otra()
            break

        elif 'sectores del laboratorio' in query:
            speak("Los sectores son: Energía,Salud,Agroindustria,Turismo,Manufactura,Biotecnología,Derecho a la Alimentación,Territorios sostenibles.\n")
            otra()
            break

        elif 'tecnologías del laboratorio' in query :
            speak("Las Tecnologías de la Industria 4.0 Priorizadas son:Internet de las Cosas,Ciencia de datos,Inteligencia Artificial.")
            speak("También tenemos capacidades para trabajar en:Simulación,Videojuegos,Ciberseguridad,Robótica,Ciudades inteligentes.")
            speak("Todo nuestro trabajo se desarrolla con herramientas de Creatividad para generar Innovaciones")
            otra()
            break

        elif ('página web' in query or "homepage" in query or "página" in query) and ('del laboratorio' in query ):
            speak("En tu navegador te estoy abriendo la página del laboratorio del CDT")
            webbrowser.open("https://smartregionscenter.com.co/laboratorio_iot")
            otra()
            break

        elif ('abre la presentación' in query or "la presentación" in query or "presentación" in query or "cavan" in query) and "del laboratorio" in query:
            speak("En tu navegador te estoy abriendo la página del laboratorio del CDT")
            webbrowser.open("https://www.canva.com/design/DAGLQbszSsk/y7QCQsVQQ1ogUHyudr4g3Q/view?utm_content=DAGLQbszSsk&utm_campaign=designshare&utm_medium=link&utm_source=editor#1")
            otra()
            break


        elif 'abra google' in query or 'ir a google' in query or 'google' in query:
            speak("Quiere ir a Google, aquí tienes google\n")
            webbrowser.open("google.com")
            otra()
            break


        elif 'escuchar música' in query or "canción" in query or "música" in query or "oir una canción" in query or "Música" in query:
            speak("Tengo pocas canciones, porque mi jefa no me deja oir musica")
            # music_dir = "G:\\Song"
            music_dir = "C:/Users/User/Desktop/CDD/songs"
            songs = os.listdir(music_dir)
            print(songs)    
            random = os.startfile(os.path.join(music_dir, songs[1]))
            otra()
            break

        elif 'fecha' in query or 'deme la hora' in query or 'deme la fecha' in query or 'dime la fecha' in query or 'hora' in query:
            strTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            # Obtener la fecha y hora actual
            speak(f"La fecha y hora son {strTime}")
            otra()
            break

        #elif 'open opera' in query:
        #    codePath = r"C:\\Users\\GAURAV\\AppData\\Local\\Programs\\Opera\\launcher.exe"
        #    os.startfile(codePath)

        elif 'email al director' in query or 'correo al director' in query:
            try:
                speak("Qué quiere decirle?")
                content = takeCommand()
                to = "adiaz@unab.edu.co"   
                sendEmail(to, content)
                speak("El email fué enviado !")
            except Exception as e:
                print(e)
                speak("No fué posible enviar el email, intenta más tarde")
            otra()
            break

        elif 'enviar email' in query or 'email' in query or 'enviar un email' in query:
            try:
                speak("Qué quiere decir?")
                content = takeCommand()
                speak("A quién desea enviale, escribe usa tu teclado")
                to = input()    
                sendEmail(to, content)
                speak("El email fué enviado !")
            except Exception as e:
                print(e)
                speak("No fué posible enviar el email, intenta más tarde")
            otra()
            break

        elif 'Cómo estás' in query or 'cómo está'in query or 'Qué tal estás'in query  or  'qué tal'in query:
            speak("Yo muy bien, gracias")
            speak("Espero que usten tabién este disfrutando este asistente?")
            otra()
            break

        elif 'yo bien' in query or "muy bien" in query or "estoy bien" in query:
            speak("Es muy bueno saber que está usted bien")
            otra()
            break

        elif "cambiar tu nombre" in query or "cambia tu nombre" in query or "otro nombre para ti" in query:
            speak("Cual sería mi nuevo nombre")
            assname = takeCommand()
            speak("Gracias, ahora mis amigos me conocerán por"+assname)
            otra()
            break


        elif "cambiar nombre" in query or "cambia mi nombre" in query or "otro nombre" in query:
            speak("Cuál es tu nombre")
            uname = takeCommand()
            speak("A partir de ahora eres"+uname)
            otra()
            break

        elif "cuál es tu nombre" in query or "qué nombre tienes" in query:
            speak("Mis amigos me llaman Smartina")
            otra()
            break

        elif 'salir' in query or 'chao' in query or 'adios' in query  :
            speak("Gracias por su tiempo")
            otra()
            break

        elif "quién te construyó" in query or "quién te creó" in query or "cómo naciste" in query or "de dónde saliste" in query or "quién te hizo" in query: 
            speak("Yo fuí adaptada y entrenada por Alfredo Diaz del Centro de Desarrollo Tecnológico, a quien le debo mi vida. Aún soy muy joven y estoy aprendiendo")
            otra()
            break                
        elif 'chiste' in query:
            speak("Mis chiste son muy técnicos  y analíticos, pero te voy a contar uno:")
            speak(pyjokes.get_joke(language='es', category= 'all'))
            speak("Analizalo y ojalá te haya gustado")
            otra()
            break
                
        elif "calcula" in query or "operación matemática" in query  :           
            app_id = "Wolframalpha api id"
            client = wolframalpha.Client("3527QJ-EYKJ9QYEQY")
            # Obtener la consulta para calcular
            if 'calcula' in query:
                indx = query.lower().split().index('calcula') 
            else:
                indx = query.lower().split().index('operación') + 1
            query = query.split()[indx + 1:] 
            
            try:
                # Consultar a Wolfram Alpha
                res = client.query(' '.join(query)) 
                answer = next(res.results).text
                print("La respuesta es:", answer) 
                speak("La respuesta es: " + answer)
            except Exception as e:
                print("Hubo un error al calcular la operación:", e)
            
            otra()
            break

        elif 'busca en internet' in query or 'encuentra en internet' in query:
                
            query = query.replace('busca en internet', "") 
            query = query.replace('encuentra en internet', "")          
            webbrowser.open(query) 
            
            otra()
            break


        elif "quién soy yo" in query or "quién soy" in query:
            speak("dado que estás hablando, eres un humano y veo que estás interesado o visitando mi casa, el CDT.")
            otra()
            break

        elif "vino" in query or "viniste" in query  or "razón de ser" in query  or "para qué nació" in query  or "por qué nació" in query:
            speak("Vine a este mundo gracias al trabajo de Alfredo, estoy entrenado para ti y apoyarte con el Smart Region Lab")
            otra()
            break

        #elif 'presentación' in query or 'presentacion' in query or 'Presentacion' in query:
        #    speak("Abriendo la presentación de Power Point")
        #    power = r"D:\Proyecto IA\asistente\presentacion\cdt.pptx"
        #    os.startfile(power)
        #   
        #    otra()
        #    break

        elif 'qué es amor' in query or 'que es amor' in query or 'Qué es amor' in query:
            speak("Es el séptimo sentido que destruye a los otros sentidos. es una broma")
            otra()
            break

        elif "quién eres" in query or 'quién eres' in query or 'Quién eres' in query:
            speak("Yo soy el asistente virtual del Smart Region Lab entrenado por Alfredo")
            
            otra()
            break

        elif 'Para qué te crearon' in query or 'Por qué te crearon' in query or 'te crearon' in query:
            speak("Fuí creado para un experimento en el laboratorio Smart Region Lab por Alfredo")
            
            otra()
            break

        #elif 'change background' in query:
        #    ctypes.windll.user32.SystemParametersInfoW(20, 
        #                                               0, 
        #                                               "Location of wallpaper",
        #                                               0)
        #    speak("Background changed successfully")
        # 
        #elif 'open bluestack' in query:
        #    appli = r"C:\\ProgramData\\BlueStacks\\Client\\Bluestacks.exe"
        #    os.startfile(appli)

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

            
        elif 'bloquea la pantalla' in query or 'bloquea windows' in query:
                speak("Bloquendo windows")
                ctypes.windll.user32.LockWorkStation()
            
                otra()
                break

        elif 'bajar el sistema' in query or 'cerrar el sistema' in query:
                speak("Espera un segundo ! Su sistema está en camino de apagarse")
                subprocess.call('shutdown / p /f')
                
                otra()
                break
                    
        elif 'borra reciclaje' in query or 'limpia el reciclaje' in query:
            winshell.recycle_bin().empty(confirm = False, show_progress = False, sound = True)
            speak("Reciclaje borrado")

        elif "no escuchar" in query or "pare de escuchar" in query:
            speak("¿Durante cuánto tiempo deseas que  deje de escuchar comandos?")
            a = int(takeCommand())
            time.sleep(a)
            print(a)

        elif "dónde estamos" in query or "dónde está el laboratorio" in query or "dónde queda" in query :
            query = query.replace("donde estamos ubicados", "")
            location = query
            speak("El laboratorio queda en el edificio de Ingenieria de la Unab. Te voy ayudar a ubiqcarte en la Unab usando google map")
            speak(location)
            webbrowser.open("https://www.google.nl/maps/search/unab/@7.1170986,-73.1060737,17z")

        elif "cámara" in query or "foto" in query:
            speak("Espera un 30 segundos mientras activo la camara, tomo una foto y cierra la imagen para continuar")
            ec.capture(0, "foto", "img.jpg")

        elif "restart" in query:
            subprocess.call(["shutdown", "/r"])
                
        elif "hibernar" in query or "sleep" in query:
            speak("Hibernando")
            subprocess.call("shutdown / h")

        elif "cerrar sesión" in query or "sign out" in query:
            speak("Asegúrese de que todas las aplicaciones estén cerradas antes de cerrar sesión.")
            time.sleep(5)
            subprocess.call(["shutdown", "/l"])

        elif "escribe una nota" in query or "escribir nota" in query or "toma una nota" in query:
            speak("Qué quisiera que yo escribiera")
            note = takeCommand()
            file = open('nota.txt', 'w')
            speak("Puedo incluir la fecha")
            snfm = takeCommand()
            if 'si' in snfm or 'seguro' in snfm:
                strTime = datetime.datetime.now().strftime("% H:% M:% S")
                file.write(strTime)
                file.write(" :- ")
                file.write(note)
            else:
                file.write(note)
            
        elif "mostrar la nota" in query or "ver la nota" in query or "ver nota" in query or "muestre la nota" in query :
            speak("mostrando la nota")
            file = open("nota.txt", "r") 
            print(file.read())
            speak(file.read(6))

        elif "actualizar el asistente" in query:
            speak("Después de descargar el archivo, reemplace este archivo con el descargado.")
            url = 'https://raw.githubusercontent.com/adiacla/asistente/main/'
            r = requests.get(url, stream = True)
                
            with open("asistente.py", "wb") as Pypdf:
                    
                total_length = int(r.headers.get('content-length'))
                    
                for ch in progress.bar(r.iter_content(chunk_size = 2391975),
                                        expected_size =(total_length / 1024) + 1):
                    if ch:
                        Pypdf.write(ch)
                        
        # NPPR9-FWDCX-D2C8J-H872K-2YT43
        elif "es Martina" in query:               
            wishMe()
            speak("Si señor ese soy yo... ")
            speak(assname + "pregunta lo que quieras")

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
                
        elif "enviar mensaje" in query:
                # You need to create an account on Twilio to use this service
                account_sid = 'Account Sid key'
                auth_token = 'Auth token'
                client = Client(account_sid, auth_token)

                message = client.messages \
                                .create(
                                    body = takeCommand(),
                                    from_='Sender No',
                                    to ='Receiver No'
                                )

                print(message.sid)

        elif "abrir wikipedia" in query:
            webbrowser.open("wikipedia.com")

        elif "hola" in query or  "que tal" in query or "buenas" in query:
            speak("" +query)
            speak("Espero te encuentre muy bien? Puedes iniciar preguntando")

        # most asked question from google Assistant
        elif "seré tu novio" in query or "seré tu novia" in query or "tu novio" in query or "tu novia" in query or "mi novia" in query:   
            speak("No puedo amar, así que mejor busque otra pareja, concentrese mejor en tu trabajo del laboratorio, me hizo poner roja, mejor continuemos")

        elif "te amo" in query:
            speak("Yo no puedo amar pero gracias por expresarlo, en qué te puedo ayudar")

        elif "busca" in query:           
            # Use the same API key 
            # that we have generated earlier
            client = wolframalpha.Client("3527QJ-EYKJ9QYEQY")
            res = client.query(query)
                
            try:
                print (next(res.results).text)
                speak (next(res.results).text)
            except StopIteration:
                print ("No tengo resultados para esa pregunta")
                speak ("No encontré una respuesta, intenta otra vez")
        
        elif "Llama" in query or 'llama' in query:
            speak("¿Qué deseas preguntar?")
            # Captura la pregunta del usuario
            message = takeCommand()
            speak("Dame un segundo.")
            
            # Ajustamos el prompt del sistema para mejorar la consistencia en español y evitar respuestas regionales
            system_prompt = """
            Eres un asistente virtual que habla en español. Responde siempre en español. 
            Evita proporcionar información específica de España a menos que el usuario lo pida explícitamente. 
            Prefiere información general o de América Latina cuando sea relevante.
            No respondas en contexto espeficio
            """
            
            # Llamada a la función de chat con los ajustes sugeridos
            resultado = chat_function(message, history="", system_prompt=system_prompt, max_new_tokens=250, temperature=0.7)
            
            print(resultado)
            print(type(resultado))
            
            speak(resultado)
            otra()
            break

        # elif "" in query:
            # Command go here
            # For adding more commands


def print_message(mensaje):
    # Crear un objeto Figlet con el estilo deseado
    font = pyfiglet.Figlet(font='slant')
    
    # Generar el texto ASCII art
    ascii_art = font.renderText(mensaje)
    
    # Imprimir el texto ASCII art
    print(ascii_art)



if __name__ == '__main__':
    query=''
    clear = lambda: os.system('cls')    
    # Esta´función limpia el comando
    # antes de la ejecución de python
    clear()
    print_message('Bienvenido')
    wishMe()
    username()

    while True:

        query = takeCommand2().lower()
        if 'smartina' in query or 'esmartina' in query  or 'Martina' in query or 'es martina' in query or 'Esmartina' in query:
            interaccion()
            speak("Para activarme di smartina")
        elif 'salir' in query or 'apagar' in query or 'quitar' in query or 'terminar' in query or'salga' in query:
            speak("Gracias por visitarnos")
            print_message('Gracias')
            break

        # All the commands said by user will be 
        # stored here in 'query' and will be
        # converted to lower case for easily 
pygame.quit()