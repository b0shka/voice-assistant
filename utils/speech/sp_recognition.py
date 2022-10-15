import io
import wave
import pyaudio
import speech_recognition as sr


r = sr.Recognizer()
m = sr.Microphone()

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


#data = record_audio(3)

with m as source:
	r.adjust_for_ambient_noise(source, 1)
	print("Say something")
	audio = r.listen(source)

try:
	print(r.recognize_google(audio, language='ru-RU'))
except sr.UnknownValueError:
	print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
	print(f"Could not request results from Google Speech Recognition service; {e}")