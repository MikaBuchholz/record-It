import pyaudio
import wave

class AudioRecorder():
    def __init__(self, audioLength = 10, filename = 'sound'):
        self.recordLength = audioLength # seconds to record
        self.filename = filename
        self.bitRate = pyaudio.paInt16 # 16-bit resolution
        self.channels = 1 # 1 channel
        self.sampleRate = 44100 # 44.1kHz sampling rate
        self.chunk = 4096 # 2^12 samples for buffer
        self.deviceIndex = 2 # device index found by p.get_device_info_by_index(ii)
        self.audioModule = pyaudio.PyAudio() # create pyaudio instantiation

    def recordAudio(self):
        # create pyaudio stream
        stream = self.audioModule.open(format = self.bitRate ,rate = self.sampleRate,channels = self.channels, \
                            input_device_index = self.deviceIndex,input = True, \
                            frames_per_buffer=self.chunk)
        print("recording")
        frames = []

        # loop through stream and append audio chunks to frame array
        for _ in range(0,int((self.sampleRate/self.chunk)* self.recordLength)):
            data = stream.read(self.chunk)
            frames.append(data)

        print("finished recording")

        # stop the stream, close it, and terminate the pyaudio instantiation
        stream.stop_stream()
        stream.close()
        self.audioModule.terminate()

        # save the audio frames as .wav file
        wavefile = wave.open(self.filename,'wb')
        wavefile.setnchannels(self.channels)
        wavefile.setsampwidth(self.audioModule.get_sample_size(self.bitRate))
        wavefile.setframerate(self.sampleRate)
        wavefile.writeframes(b''.join(frames))
        wavefile.close()

