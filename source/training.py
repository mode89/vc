class Trainer:

    def __init__(self, network):
        self.network = network

    def step(self, step):
        self.network.step(step)
