import numpy
import pyaudio
import struct

INPUT_FORMAT = pyaudio.paInt16
FRAME_RATE = 44100
SAMPLE_RATE = 100
FRAMES_PER_BUFFER = FRAME_RATE / SAMPLE_RATE
SAMPLE_STEP = 1.0 / SAMPLE_RATE

class Audio:

    def __init__(self):
        pa = pyaudio.PyAudio()
        self.stream = pa.open(
            input=True,
            format=INPUT_FORMAT,
            channels=1,
            rate=FRAME_RATE,
            frames_per_buffer=FRAMES_PER_BUFFER)
        self.stream.start_stream()

    def read(self):
        try:
            frames = struct.unpack(
                "%ih" % FRAMES_PER_BUFFER,
                self.stream.read(FRAMES_PER_BUFFER))
            return [float(val) / 2 ** 15 for val in frames]
        except IOError as e:
            print(e)
            return [0.0] * FRAMES_PER_BUFFER

    def read_array(self):
        try:
            frames = numpy.fromstring(
                self.stream.read(FRAMES_PER_BUFFER), numpy.int16)
            return frames;
        except IOError as e:
            print(e)
            return numpy.zeros(FRAMES_PER_BUFFER)

    def close(self):
        self.stream.stop_stream()
        self.stream.close()
