import pyaudio
from speechkit import SpeechSynthesis
from utils.speech.config import session
from common.states import states


synthesizeAudio = SpeechSynthesis(session)

num_channels = 1
sample_rate = 48000
chunk_size = 4000
lang = 'ru-RU'
voice = 'alena'
emotion = 'neutral'
speed = 1.0
format = 'lpcm'


def synthesis_audio_bytes(audio_data):
	try:
		p = pyaudio.PyAudio()
		stream = p.open(
			format=pyaudio.paInt16,
			channels=num_channels,
			rate=sample_rate,
			output=True,
			frames_per_buffer=chunk_size
		)
		for i in range(0, len(audio_data), chunk_size):
			stream.write(audio_data[i:i + chunk_size])
	finally:
		stream.stop_stream()
		stream.close()
		p.terminate()


def synthesis_text(text):
	while states.get_synthesis_work_state(): pass
	states.change_synthesis_work_state(True)

	audio_data = synthesizeAudio.synthesize_stream(
		text=text,
		lang=lang,
		voice=voice,
		emotion=emotion,
		speed=speed,
		format=format,
		sampleRateHertz=sample_rate
	)

	synthesis_audio_bytes(audio_data=audio_data)
	states.change_synthesis_work_state(False)