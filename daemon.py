import esn
import input
import server

INPUT_COUNT = 13
NEURON_COUNT = 100
CONNECTIVITY = 0.5

class Daemon:

    def __init__(self):
        print("Generating network...")
        self.network = esn.create_network(
            inputCount=INPUT_COUNT,
            neuronCount=NEURON_COUNT,
            outputCount=1,
            connectivity=CONNECTIVITY,
            useOrthonormalMatrix=True)
        self.input_audio = input.Audio()
        self.server = server.Server(self)
        self.server.start()
        self.state = Daemon.RunningState()

    def loop(self):
        self.working = True
        while self.working:
            self.state.step(self)
        self.input_audio.close()

    def exit(self, options):
        print("Exiting...")
        self.working = False

    class State:

        def step(self, daemon):
            raise NotImplementedError()

    class RunningState(State):

        def step(self, daemon):
            daemon.network.set_inputs(daemon.input_audio.read())
