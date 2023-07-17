import speech_recognition as sr
import pyautogui
import time
import subprocess
import pyttsx3

band = False
class VoiceCommands:

    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()

    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self):
        
        with sr.Microphone() as source:
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            print("Reconociendo...")
            command = self.recognizer.recognize_google(audio, language='es')
            #print("Comando reconocido:", command)
            if "abi" in command.lower():
                
                self.listen_for_action()
            else:
                self.speak("Lo lamento no te he escuchado")
        except sr.UnknownValueError:
            self.speak("¿Si.., ¿cómo puedo ayudarte?")
        except sr.RequestError as e:
            print("Error al solicitar los resultados del reconocimiento de voz: {0}".format(e))

    def listen_for_action(self):
        with sr.Microphone() as source:
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            print("Reconociendo...")
            action = self.recognizer.recognize_google(audio, language='es')
            print("Acción reconocida:", action)
            self.execute_action(action)
        except sr.UnknownValueError:
            print("No se pudo reconocer la acción.")
        except sr.RequestError as e:
            print("Error al solicitar los resultados del reconocimiento de voz: {0}".format(e))

    def execute_action(self, action):

            if "activa el modo cine" in action.lower():
                self.activate_cinema_mode()
            elif "activa el modo desarrollador" in action.lower():
                self.activate_developer_mode()
            elif "cierra el asistente de voz" in action.lower():
                self.close_voice_assistant()
            elif "minimiza todas las ventanas" in action.lower():
                self.minimize_windows()
            else:
                print("Acción no reconocida.")

    def activate_cinema_mode(self):
        mode = "cine"
        try:
            time.sleep(1)  # Esperar 1 segundo antes de preguntar por la aplicación

            # Preguntar por la aplicación a utilizar
            self.speak("¿Qué aplicación deseas utilizar? PrimeVideo, Netflix, Crunchyroll")
            app = self.listen_for_application()

            if app == "prime video":
                self.speak("Modo cine activado.")
                self.open_application("Prime")
            elif app == "netflix":
                self.speak("Modo cine activado.")
                self.open_application("Netflix")
            elif app == "crunchyroll":
                self.speak("Modo cine activado.")
                self.open_application("Crunchyroll")
            else:
                self.speak("Aplicación no reconocida.")

            
        except Exception as e:
            print("No se pudo activar el modo cine: {0}".format(e))
        return mode

    def activate_developer_mode(self):
        try:
            # Minimizar todas las ventanas de Windows
            pyautogui.hotkey("win", "d")
            time.sleep(1)  # Esperar 1 segundo antes de abrir las aplicaciones
            # Abrir o ejecutar Spotify
            spotify_path = r"C:\Program Files\WindowsApps\SpotifyAB.SpotifyMusic_1.214.1149.0_x86__zpdnekdrzrea0\Spotify.exe"  # Reemplaza con la ruta correcta
            subprocess.Popen(spotify_path)
            time.sleep(1)  # Esperar 1 segundo antes de abrir las aplicaciones
            # Abrir o ejecutar Visual Studio Code
            vscode_path = r"C:\Users\rober\AppData\Local\Programs\Microsoft VS Code\Code.exe"  # Reemplaza con la ruta correcta
            subprocess.Popen(vscode_path)

            self.speak("Modo desarrollador activado.")
        except Exception as e:
            print("No se pudo activar el modo desarrollador: {0}".format(e))

    def close_voice_assistant(self):
        self.speak("Cerrando asistente de voz.")
        exit()

    def minimize_windows(self):
        pyautogui.hotkey("win", "d")
        self.speak("Ventanas minimizadas.")

    def listen_for_application(self):
        with sr.Microphone() as source:
            print("Escuchando...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            print("Reconociendo...")
            app = self.recognizer.recognize_google(audio, language='es').lower()
            print("Aplicación seleccionada:", app)
            return app
        except sr.UnknownValueError:
            print("No se pudo reconocer la aplicación.")
        except sr.RequestError as e:
            print("Error al solicitar los resultados del reconocimiento de voz: {0}".format(e))

        return None

    def open_application(self, app_name):
        pyautogui.press("win")  # Presionar tecla de Windows
        pyautogui.typewrite(app_name)  # Escribir el nombre de la aplicación
        time.sleep(2)
        pyautogui.press("enter")  # Presionar Enter

# Uso de la clase
vc = VoiceCommands()
while band == False:
    vc.speak("Bienvenido a tu asistente personal AVI")
    vc.listen()
