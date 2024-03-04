import os
import pygame
from gtts import gTTS

def Text_to_speech(text):
    speech = gTTS(text=text, lang='en', tld='com.au')
    speech.save('finalproj.mp3')
    pygame.mixer.init()
    pygame.mixer.music.load('finalproj.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.stop()
    pygame.mixer.quit()  # Release the mixer resources
    os.remove('finalproj.mp3')  # Delete the file after playback is complete

def main():
    user_input = input("Enter Text: ")
    Text_to_speech(user_input)

if __name__ == "__main__":
    main()

