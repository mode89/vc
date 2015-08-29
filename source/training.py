from scikits.talkbox.features import mfcc
import random
import samples

NOISE_LENGTH_RANGE = (0.5, 2.0)

class Inputs:

    def __init__(self):
        self.state = PlaySample()

    def __call__(self):
        return self.mfcc

    def update(self, step):
        self.frames = self.state.read_frames(step)
        if self.frames is None:
            self.state = self.state.next()
            self.frames = self.state.read_frames(step)
        assert self.frames is not None, "There are must be some frames"
        self.mfcc = mfcc(self.frames,
            fs=len(self.frames)/step, nceps=13)[0][0]

class PlaySample():

    def __init__(self):
        self.sample = random.choice(samples.SAMPLES)
        self.sample.reset()

    def read_frames(self, step):
        return self.sample.read_frames(step)

    def next(self):
        return PlayNoise()

class PlayNoise():

    def __init__(self):
        self.sample = samples.NOISE
        self.length = random.uniform(*NOISE_LENGTH_RANGE)

    def read_frames(self, step):
        self.length -= step
        if self.length < 0:
            return None
        frames = self.sample.read_frames(step)
        if frames is None:
            self.sample.reset()
            frames = self.sample.read_frames(step)
            assert frames is not None, "There are must be some frames"
        return frames

    def next(self):
        return PlaySample()

class Trainer:

    def __init__(self, network):
        self.network = network
        self.inputs = Inputs()

    def step(self, step):
        self.inputs.update(step)
        self.network.set_inputs(self.inputs())
        self.network.step(step)
