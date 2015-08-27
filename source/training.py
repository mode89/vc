import random
import samples

class Inputs:

    def __init__(self):
        self.state = Inputs.PlaySample()

    def __call__(self):
        assert 0, "Not yet implemented"

    def update(self, step):
        self.state.update(step)

    class State: pass

    class PlaySample(State):

        def __init__(self):
            self.sample = random.choice(samples.SAMPLES)

        def update(self, step):
            assert 0, "Not yet implemented"

    class PlayNoise(State):

        def update(self, step):
            assert 0, "Not yet implemented"

class Trainer:

    def __init__(self, network):
        self.network = network
        self.inputs = Inputs()

    def step(self, step):
        self.inputs.update(step)
        self.network.set_inputs(self.inputs())
        self.network.step(step)
