import speech_recognition
import pyttsx3
import os
import pygame

def play_sound_pygame(sound_file_path):
    # Use 'pygame' to load and play the sound
    sound = pygame.mixer.Sound(sound_file_path)
    sound.play()


recogniser = speech_recognition.Recognizer()

try:
    pygame.init()
    with speech_recognition.Microphone() as source:
        play_sound_pygame("start.wav")
        recogniser.adjust_for_ambient_noise(source, duration=1)
        audio = recogniser.listen(source)
        play_sound_pygame("end.wav")
        text = recogniser.recognize_google(audio)
        text=text.lower()
        print(f"Recognised {text}")

except speech_recognition.UnknownValueError:
    recogniser = speech_recognition.Recognizer()