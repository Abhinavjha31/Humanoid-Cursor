import pyaudio
import speech_recognition as sr
import time

# create a recognizer object
r = sr.Recognizer()

# set up the audio stream
chunk_size = 1024  # number of audio samples per chunk
sample_rate = 44100  # number of audio samples per second
audio_format = pyaudio.paInt16  # audio format (16-bit integer)
num_channels = 1  # number of audio channels (mono)
stream = pyaudio.PyAudio().open(format=audio_format,
                                channels=num_channels,
                                rate=sample_rate,
                                input=True,
                                frames_per_buffer=chunk_size)

# listen for speech and convert to text
print("Speak now!")
audio_buffer = []
while True:
    # read a chunk of audio data from the stream
    data = stream.read(chunk_size, exception_on_overflow=False)
    audio_buffer.append(data)
    
    # check if speech has stopped (silence for at least 1 second)
    if len(audio_buffer) > sample_rate / chunk_size:
        audio_buffer.pop(0)  # remove oldest audio chunk
        audio_signal = b''.join(audio_buffer)
        try:
            audio_data = sr.AudioData(audio_signal, sample_rate=sample_rate, sample_width=2)
            text = r.recognize_google(audio_data)
            print("You said: " + text)
            break
        except sr.UnknownValueError:
            print("Speech was unintelligible.")
        except sr.RequestError as e:
            print("Error: {0}".format(e))
            print("Retrying in 5 seconds...")
            time.sleep(5)
            continue
        audio_buffer = []  # reset audio buffer