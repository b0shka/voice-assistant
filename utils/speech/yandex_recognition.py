import io
import wave
import pyaudio
from speechkit import Session, ShortAudioRecognition
from common.config import YANDEX_OAUTH_TOKEN, YANDEX_CATALOG_ID


session = Session.from_yandex_passport_oauth_token(YANDEX_OAUTH_TOKEN, YANDEX_CATALOG_ID)
recognizeShortAudio = ShortAudioRecognition(session)

sample_rate = 16000
chunk_size=4000

p = pyaudio.PyAudio()
stream = p.open(
	format=pyaudio.paInt16,
	channels=1,
	rate=sample_rate,
	input=True,
	frames_per_buffer=8000
)
stream.start_stream()


def record_audio(seconds, sample_rate, chunk_size=4000, num_channels=1):
	frames = []
	try:
		for i in range(0, int(sample_rate / chunk_size * seconds)):
			data = stream.read(chunk_size)
			frames.append(data)
	finally:
		stream.stop_stream()
		stream.close()
		p.terminate()
		
	container = io.BytesIO()
	wf = wave.open(container, 'wb')
	wf.setnchannels(num_channels)
	wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
	wf.setframerate(sample_rate)
	wf.writeframes(b''.join(frames))
	container.seek(0)
	return container


def listen():
	print('Start listen')

	while True:
		data = stream.read(4000, exception_on_overflow=False)
		if len(data) > 0:
			yield data

#data = record_audio(3, sample_rate)

for data in listen():
	print(data)
	text = recognizeShortAudio.recognize(data, format='lpcm', sampleRateHertz=sample_rate)
	if text != '':
		print(text)