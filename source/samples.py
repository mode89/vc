import glob
import numpy
import os
import wave

class Sample:

    def __init__(self, path):
        file = wave.open(path, "r")
        frame_count = file.getnframes()
        self.frames = numpy.fromstring(file.readframes(frame_count),
            dtype=numpy.int16) / float(2 ** 15)
        self.frame_rate = file.getframerate()
        file.close()
        self.pointer = 0

    def read_frames(self, time):
        count = int(time * self.frame_rate)
        lower = self.pointer
        upper = self.pointer + count
        if upper > len(self.frames):
            return None
        else:
            self.pointer = upper
            return self.frames[lower:upper]

    def reset(self):
        self.pointer = 0

DATA_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)), "data")
SAMPLES = list(Sample(path) for path in
    glob.glob(os.path.join(DATA_DIR, "music*")))
NOISE = Sample(os.path.join(DATA_DIR, "noise.wav"))
