from scikits.talkbox.features import mfcc
import numpy
import random
import samples
import signals

NOISE_LENGTH_RANGE = (0.5, 2.0)
OUTPUT_AMPLITUDE = 0.7
OUTPUT_PULSE_WIDTH = 0.1
TRAIN_THRESHOLD = 0.01

class Inputs:

    def __init__(self):
        self.state = PlaySample()
        self.end_of_sample = False

    def __call__(self):
        return self.mfcc

    def update(self, step):
        self.end_of_sample = False
        self.frames = self.state.read_frames(step)
        if self.frames is None:
            if isinstance(self.state, PlaySample):
                self.end_of_sample = True
            self.state = self.state.next()
            self.frames = self.state.read_frames(step)
        assert self.frames is not None, "There are must be some frames"
        self.mfcc = mfcc(self.frames,
            fs=len(self.frames)/step, nceps=13)[0][0]

class PlaySample():

    def __init__(self):
        self.sample = random.choice(samples.COMPUTER)
        self.sample.reset()

    def read_frames(self, step):
        return self.sample.read_frames(step)

    def next(self):
        return PlayNoise()

class PlayFalseSample():

    def __init__(self):
        self.sample = random.choice(samples.MUSIC + samples.CLAP)
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
        return random.choice([PlaySample, PlayFalseSample])()

class Outputs:

    def __init__(self, inputs):
        self.inputs = inputs
        self.pulse = self.new_pulse()
        self.pulse_time = 0

    def update(self, step):
        if self.inputs.end_of_sample:
            self.pulse = self.new_pulse()
            self.pulse_time = 0
        self.value = self.pulse(self.pulse_time)
        self.pulse_time += step

    def new_pulse(self):
        return signals.GaussianPulse(
            amplitude=OUTPUT_AMPLITUDE, width=OUTPUT_PULSE_WIDTH)

class Trainer:

    def __init__(self, network, washout_time, train_time):
        self.network = network
        self.washout_time = washout_time
        self.train_time = train_time
        self.inputs = Inputs()
        self.outputs = Outputs(self.inputs)
        self.time = 0

    def step(self, step):
        self.time += step
        self.inputs.update(step)
        self.outputs.update(step)
        self.network.set_inputs(self.inputs())
        self.network.step(step)

        network_output = self.network.capture_output(1)[0]
        if self.time > self.washout_time and self.time < self.train_time:
            if self.outputs.pulse_time <= OUTPUT_PULSE_WIDTH or \
                (self.outputs.pulse_time > OUTPUT_PULSE_WIDTH and \
                    abs(network_output) > TRAIN_THRESHOLD):
                self.network.train_online([self.outputs.value],
                    forceOutput=False)
