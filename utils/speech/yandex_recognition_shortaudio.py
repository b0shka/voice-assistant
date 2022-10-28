import io
import wave
import pyaudio
from speechkit import ShortAudioRecognition
from utils.speech.config import session


recognizeShortAudio = ShortAudioRecognition(session)

sample_rate = 16000
chunk_size = 4000
num_channels = 1


def record_audio(seconds):
	p = pyaudio.PyAudio()
	stream = p.open(
		format=pyaudio.paInt16,
		channels=1,
		rate=sample_rate,
		input=True,
		frames_per_buffer=8000
	)
	frames = []

	try:
		for _ in range(0, int(sample_rate / chunk_size * seconds)):
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


data = record_audio(3)
text = recognizeShortAudio.recognize(data, format='lpcm', sampleRateHertz=sample_rate)
print(text.lower())