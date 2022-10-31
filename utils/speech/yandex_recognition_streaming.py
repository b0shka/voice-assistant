import pyaudio
from common.states import states
from domain.data_class.Command import Command
from domain.enum_class.CommandMode import CommandMode
from speechkit import DataStreamingRecognition
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
			if states.SYNTHESIS_WORK:
				# если в данный момент происходит синтез речи
				break
			if not states.WAITING_RESULT_RECOGNITION:
				# если больше не нужно ожидать конечного результата распознавания речи
				break
			yield stream.read(4000)
	finally:
		stream.stop_stream()
		stream.close()
		p.terminate()


def listen() -> Command:
	count_equal_data = 0
	previous_data = None

	while True:
		if not states.SYNTHESIS_WORK:
			for data in data_streaming_recognition.recognize(gen_audio_capture_function):
				text_command = data[0][0].lower()

				if not states.WAITING_RESULT_RECOGNITION:
					# если больше не нужно ожидать конечного результата распознавания речи
					yield Command(None, CommandMode.FINITE)
					break

				if text_command == previous_data:
					count_equal_data += 1
					if count_equal_data == 3:
						# Если полученный текст повроляется уже 3-ий раз, то останавливать распознавание и возвращать текущий результат
						yield Command(text_command, CommandMode.FINITE)
						count_equal_data = 0
						previous_data = None
						break
				else:
					if data[1]:
						yield Command(text_command, CommandMode.FINITE)
					else:
						yield Command(text_command, CommandMode.INTERMEDIATE)

				previous_data = text_command