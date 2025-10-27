import pyttsx3
#from playsound import playsound
import pygame
import speech_recognition as sr
import comtypes



class AudioRoom:
    def __init__(self):
        pass
    def listener(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            recognizer.pause_threshold = 1.2  # Increase pause detection (default is 0.8)
            #recognizer.energy_threshold = 300
            try:
                print("listening...")
                audio =recognizer.listen(source)
                speech_text = recognizer.recognize_google(audio)
                return speech_text.lower()
            except Exception as e:
                return "couldn't listen"

    def speak(self, text):
        comtypes.CoInitialize()
        engine = pyttsx3.init()
        output_file = "output.wav"
        engine.save_to_file(text, output_file)
        engine.runAndWait()
        pygame.mixer.init()
        pygame.mixer.music.load(output_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pass
        pygame.mixer.music.unload()


controlstation = AudioRoom()
