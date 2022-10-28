import os
import json
import pyaudio
from vosk import Model, KaldiRecognizer
from common.states import states


sample_rate = 16000
chunk_size = 8000
model_path = 'utils/speech/models/vosk-model-small-ru'
#model_path = 'models/vosk-model-small-ru'

if not os.path.exists(model_path):
	print('Модель не найдена')
	exit(1)
	
model = Model(model_path)
rec = KaldiRecognizer(model, sample_rate)

p = pyaudio.PyAudio()
stream = p.open(
	format=pyaudio.paInt16,
	channels=1,
	rate=sample_rate,
	input=True,
	frames_per_buffer=chunk_size
)
stream.start_stream()

def listen():
	try:
		while True:
			if not states.get_synthesis_work_state():
				data = stream.read(4000, exception_on_overflow=False)

				if len(data) != 0:
					if rec.AcceptWaveform(data):
						answer = json.loads(rec.Result())
						if answer['text']:
							yield {
								'text': answer['text'].lower(),
								'mode': 'finite'
							}
					else:
						answer = json.loads(rec.PartialResult())
						if answer['partial']:
							yield {
								'text': answer['partial'].lower(),
								'mode': 'intermediate'
							}
						
	finally:
		stream.stop_stream()
		stream.close()
		p.terminate()