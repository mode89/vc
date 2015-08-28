import random
import samples

NOISE_LENGTH_RANGE = (0.5, 2.0)

class Inputs:

    def __init__(self):
        self.state = Inputs.PlaySample()

    def __call__(self):
        assert 0, "Not yet implemented"

    def update(self, step):
        self.frames = self.state.read_frames(step)
        if self.frames is None:
            self.state = self.state.next()
            self.frames = self.state.read_frames(step)
        assert self.frames is not None, "There are must be some frames"

    class State: pass

    class PlaySample(State):

        def __init__(self):
            self.sample = random.choice(samples.SAMPLES)
            self.sample.reset()

        def read_frames(self, step):
            return self.sample.read_frames(step)

        def next(self):
            return Inputs.PlayNoise()

    class PlayNoise(State):

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
            return Inputs.PlaySample()

class Trainer:

    def __init__(self, network):
        self.network = network
        self.inputs = Inputs()

    def step(self, step):
        self.inputs.update(step)
        self.network.set_inputs(self.inputs())
        self.network.step(step)
