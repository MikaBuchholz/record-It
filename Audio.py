import pyaudio
import wave

class AudioRecorder:
    def __init__(self, filename = 'audio.wav'):
        self.filename = filename
        self.bitRate = pyaudio.paInt16 # 16-bit resolution
        self.channels = 1 # Check $python -m sounddevice for 'in'    ex. (2 in, 0 out)
        self.sampleRate = 44100 # 44.1kHz sampling rate
        self.chunk = 4096 # 2^12 samples for buffer
        self.deviceIndex = 2 # $pip install sounddevice and then $python -m sounddevice
        self.audioModule = pyaudio.PyAudio() # create pyaudio instantiation
        self.frames = []
        self.start_stream()

    def start_stream(self):
        # create pyaudio stream
        self.stream = self.audioModule.open(format = self.bitRate, rate = self.sampleRate, 
                                       channels = self.channels, input_device_index = self.deviceIndex, 
                                       input = True, frames_per_buffer=self.chunk)

    def record(self):
        # started
        # loop through stream and append audio chunks to frame array
        data = self.stream.read(self.chunk, exception_on_overflow = False)
        self.frames.append(data)
        # finished

    def stop(self):
        # self.open = False
        # stop the stream, close it, and terminate the pyaudio instantiation
        self.stream.stop_stream()
        self.stream.close()
        self.audioModule.terminate()
        self.__save()

    def __save(self):
        # save the audio frames as .wav file
        with wave.open(self.filename, 'wb') as wavefile:
            wavefile.setnchannels(self.channels)
            wavefile.setsampwidth(self.audioModule.get_sample_size(self.bitRate))
            wavefile.setframerate(self.sampleRate)
            wavefile.writeframes(b''.join(self.frames))
            
if __name__ == '__main__':
    i = 0
    audio = AudioRecorder()
    print('started')
    for _ in range(220): # formula for seconds -> ((seconds + seconds * 0.1) * 10) (tested on: sample_rate = 44100, chunk = 4096)
        audio.record()
    audio.stop()
    print('finished')
    
    print('started again')
    audio.start_stream()
    audio.filename = 'audio2'
    for _ in range(220):
        audio.record()
    audio.stop()
    print('finished again')
    
    
