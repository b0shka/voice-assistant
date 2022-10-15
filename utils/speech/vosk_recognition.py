#import speech_recognition
import pyaudio
import json
from vosk import Model, KaldiRecognizer


#sr = speech_recognition.Recognizer()
#sr.pause_threshold = 0.5

#with speech_recognition.Microphone() as microphone:
#	sr.adjust_for_ambient_noise(source=microphone, duration=0.5)
#	audio = sr.listen(source=microphone)
#	query = sr.recognize_google(audio_data=audio, language='ru-RU').lower()

#print(query)


model = Model('vosk-model-small-ru')
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(
	format=pyaudio.paInt16,
	channels=1,
	rate=16000,
	input=True,
	frames_per_buffer=8000
)
stream.start_stream()

def listen():
	print('Start listen')

	while True:
		data = stream.read(4000, exception_on_overflow=False)
		if rec.AcceptWaveform(data) and len(data) > 0:
			answer = json.loads(rec.Result())
			if answer['text']:
				yield answer['text']


for text in listen():
	print(text)