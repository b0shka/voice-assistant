import pyaudio
from speechkit import DataStreamingRecognition
from common.states import states
from utils.speech.config import session


sample_rate = 16000
chunk_size = 8000
num_channels = 1

data_streaming_recognition = DataStreamingRecognition(
	session,
	language_code='ru-RU',
	audio_encoding='LINEAR16_PCM',
	sample_rate_hertz=sample_rate,
	profanity_filter=False,
	partial_results=True,
	single_utterance=True,
	raw_results=False
)


def gen_audio_capture_function():
	p = pyaudio.PyAudio()
	stream = p.open(
		format=pyaudio.paInt16,
		channels=num_channels,
		rate=sample_rate,
		input=True,
		frames_per_buffer=chunk_size
	)
	try:
		while True:
			if states.get_synthesis_work_state():
				break
			yield stream.read(4000)
	finally:
		stream.stop_stream()
		stream.close()
		p.terminate()


def listen():
	while True:
		if not states.get_synthesis_work_state():
			for data in data_streaming_recognition.recognize(gen_audio_capture_function):
				if data[1]:
					yield {
						'text': data[0][0].lower(),
						'mode': 'finite'
					}
				else:
					yield {
						'text': data[0][0].lower(),
						'mode': 'intermediate'
					}