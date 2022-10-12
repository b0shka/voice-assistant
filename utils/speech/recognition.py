import speech_recognition
import pyaudio

sr = speech_recognition.Recognizer()
sr.pause_threshold = 0.5

with speech_recognition.Microphone() as microphone:
	sr.adjust_for_ambient_noise(microphone, duration=0.5)
	audio = sr.listen(source=microphone)
	query = sr.recognize_google(audio, language='ru-RU').lower()

	print(query)