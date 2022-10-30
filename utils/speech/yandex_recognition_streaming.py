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
			if not states.get_waiting_result_recognition():
				break
			yield stream.read(4000)
	finally:
		stream.stop_stream()
		stream.close()
		p.terminate()


def listen():
	count_equal_data = 0
	previous_data = None

	while True:
		if not states.get_synthesis_work_state():
			for data in data_streaming_recognition.recognize(gen_audio_capture_function):
				text_command = data[0][0].lower()

				if not states.get_waiting_result_recognition():
					yield {
						'text': None,
						'mode': 'finite'
					}
					break

				if text_command == previous_data:
					count_equal_data += 1
					if count_equal_data == 3:
						# Если полученный текст повроляется уже 3-ий раз, то останавливать распознавание и возвращать текущий результат
						yield {
							'text': text_command,
							'mode': 'finite'
						}
						count_equal_data = 0
						previous_data = None
						break
				else:
					if data[1]:
						yield {
							'text': text_command,
							'mode': 'finite'
						}
					else:
						yield {
							'text': text_command,
							'mode': 'intermediate'
						}

				previous_data = text_command