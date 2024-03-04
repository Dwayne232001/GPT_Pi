try:
    with speech_recognition.Microphone() as source:
        recogniser.adjust_for_ambient_noise(source, duration=1)
        audio = recogniser.listen(source)
        text = recogniser.recognize_google(audio)
        text=text.lower()
        print(f"Recognised {text}")

except speech_recognition.UnknownValueError:
    recogniser = speech_recognition.Recognizer()
    continue